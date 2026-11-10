"""Single-shop ordering service. Run one worker (SQLite + local rate limiter)."""
import os, json, sqlite3, secrets, hashlib, hmac, time, threading
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Annotated, Literal
from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, ConfigDict, StringConstraints

HERE = Path(__file__).parent
DB = Path(os.environ.get('VJU_DB', str(HERE / 'data' / 'food.sqlite3')))
SECURE = os.environ.get('VJU_COOKIE_SECURE', '1') == '1'
COOKIE_PATH = os.environ.get('VJU_BASE_PATH', '/').rstrip('/') + '/'
TZ = ZoneInfo('Asia/Ho_Chi_Minh')
app = FastAPI(title='VJU Food Hola', docs_url=None, redoc_url=None, openapi_url=None)

def fail(code, message): raise HTTPException(code, message)
def digest(value): return hashlib.sha256(value.encode()).hexdigest()
def password_hash(password, salt): return hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1).hex()

@contextmanager
def db():
    c = sqlite3.connect(DB, timeout=15)
    c.row_factory = sqlite3.Row
    c.execute('PRAGMA foreign_keys=ON')
    try:
        yield c
        c.commit()
    except Exception:
        c.rollback()
        raise
    finally: c.close()

def init_db():
    DB.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with db() as c:
        c.executescript('''
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS settings(id INTEGER PRIMARY KEY CHECK(id=1), data TEXT NOT NULL, secret TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS dishes(id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS admins(username TEXT PRIMARY KEY, salt TEXT NOT NULL, hash TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, username TEXT NOT NULL REFERENCES admins(username), csrf TEXT NOT NULL, expires REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS orders(code TEXT PRIMARY KEY, lookup_hash TEXT NOT NULL, idem TEXT UNIQUE NOT NULL, fingerprint TEXT NOT NULL, data TEXT NOT NULL, status TEXT NOT NULL, paid INTEGER NOT NULL DEFAULT 0, cancel_reason TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL);
        ''')
        if not c.execute('SELECT 1 FROM settings').fetchone():
            c.execute('INSERT INTO settings VALUES(1,?,?)', (json.dumps({'name':'Quán mẫu gần VJU','accepting':True,'opens':'08:00','closes':'20:00'}), secrets.token_hex(32)))
            for item in json.loads((HERE/'seed.json').read_text(encoding='utf-8')):
                item['active'] = True
                c.execute('INSERT INTO dishes(id,data) VALUES(?,?)', (item['id'],json.dumps(item,ensure_ascii=False)))
    try: os.chmod(DB, 0o600)
    except OSError: pass

init_db()

class Model(BaseModel):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)
Text = Annotated[str, StringConstraints(min_length=1, max_length=100)]
class Item(Model):
    id: int = Field(gt=0, strict=True)
    qty: int = Field(ge=1, le=20, strict=True)
    price: int = Field(ge=0, strict=True)
class NewOrder(Model):
    name: Text
    phone: str = Field(pattern=r'^0[0-9]{9}$')
    slot: str = Field(max_length=40)
    note: str = Field(default='', max_length=250)
    key: str = Field(min_length=16, max_length=100, pattern=r'^[a-zA-Z0-9_-]+$')
    items: list[Item] = Field(min_length=1, max_length=30)
class Login(Model):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=False)
    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
    password: str = Field(min_length=1, max_length=128)
class Dish(Model):
    name: Text
    desc: str = Field(default='', max_length=300)
    price: int = Field(ge=0, le=10000000, strict=True)
    category: Literal['Cơm','Bún & mì','Ăn nhẹ','Đồ uống']
    emoji: str = Field(default='🍽️', max_length=12)
    bg: str = Field(default='#f6e8d5', pattern=r'^#[0-9a-fA-F]{6}$')
    tag: str = Field(default='', max_length=40)
    available: bool = True
    active: bool = True
class Shop(Model):
    name: Text
    accepting: bool
    opens: str = Field(pattern=r'^([01][0-9]|2[0-3]):[0-5][0-9]$')
    closes: str = Field(pattern=r'^([01][0-9]|2[0-3]):[0-5][0-9]$')
class Transition(Model):
    status: Literal['pending','confirmed','preparing','ready','completed','cancelled']
    reason: str = Field(default='', max_length=250)
class Paid(Model):
    paid: Literal[True]

limits = {}
lock = threading.Lock()
def throttle(request, action, maximum):
    key = (request.client.host if request.client else 'unknown', action)
    now = time.monotonic()
    with lock:
        for old in list(limits):
            limits[old] = [t for t in limits[old] if now-t<60]
            if not limits[old]: del limits[old]
        attempts = limits.setdefault(key, [])
        if len(attempts) >= maximum: fail(429, 'Thao tác quá nhanh. Vui lòng thử lại sau một phút.')
        attempts.append(now)

@app.middleware('http')
async def headers(request, call_next):
    if request.method not in ('GET','HEAD','OPTIONS') and request.headers.get('x-vju-request') != '1':
        return Response('Missing request header',status_code=403)
    response = await call_next(request)
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='no-referrer'
    response.headers['X-Frame-Options']='DENY'
    if request.url.path.startswith('/api/'):
        response.headers['Cache-Control']='no-store'
    return response

def settings(c): return json.loads(c.execute('SELECT data FROM settings WHERE id=1').fetchone()[0])
def options(s, now=None):
    now = now or datetime.now(TZ)
    start = datetime.combine(now.date(), datetime.strptime(s['opens'],'%H:%M').time(), TZ)
    end = datetime.combine(now.date(), datetime.strptime(s['closes'],'%H:%M').time(), TZ)
    slots=[]
    while start + timedelta(minutes=30) <= end:
        if start >= now+timedelta(minutes=15):
            slots.append({'id':start.isoformat(),'label':start.strftime('%d/%m %H:%M')+' – '+(start+timedelta(minutes=30)).strftime('%H:%M')})
        start += timedelta(minutes=30)
    return slots if s['accepting'] and s['opens'] <= now.strftime('%H:%M') < s['closes'] else []

@app.get('/api/health')
def health(): return {'ok':True}
@app.get('/api/menu')
def menu():
    with db() as c:
        s=settings(c)
        return {'dishes':[d for row in c.execute('SELECT data FROM dishes') if (d:=json.loads(row[0]))['active']], 'shop':s, 'slots':options(s)}

def lookup_token(c, code, key):
    secret=c.execute('SELECT secret FROM settings WHERE id=1').fetchone()[0]
    return hmac.new(secret.encode(), (code+':'+key).encode(), hashlib.sha256).hexdigest()
def order_view(row):
    return {**json.loads(row['data']), 'code':row['code'], 'status':row['status'], 'paid':bool(row['paid']), 'cancel_reason':row['cancel_reason'], 'date':row['created_at']}

@app.post('/api/orders', status_code=201)
def create_order(order: NewOrder, request: Request):
    throttle(request,'order',15)
    payload=order.model_dump()
    fingerprint=digest(json.dumps(payload,sort_keys=True,ensure_ascii=False))
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        old=c.execute('SELECT * FROM orders WHERE idem=?',(order.key,)).fetchone()
        if old:
            if old['fingerprint']!=fingerprint: fail(409,'Khóa đặt đơn đã dùng cho nội dung khác.')
            return {**order_view(old),'token':lookup_token(c,old['code'],order.key)}
        s=settings(c)
        slot=next((x for x in options(s) if x['id']==order.slot),None)
        if not slot: fail(409,'Quán đang nghỉ hoặc khung giờ đã hết hạn. Hãy tải lại thực đơn.')
        if len({i.id for i in order.items}) != len(order.items): fail(422,'Mỗi món chỉ được xuất hiện một lần.')
        items=[]
        for item in order.items:
            row=c.execute('SELECT data FROM dishes WHERE id=?',(item.id,)).fetchone()
            d=json.loads(row[0]) if row else None
            if not d or not d['active'] or not d['available']: fail(409,'Có món đã hết hoặc ngừng bán. Hãy tải lại thực đơn.')
            if item.price!=d['price']: fail(409,'Giá món đã thay đổi. Hãy tải lại, kiểm tra giá và đặt lại.')
            items.append({'id':item.id,'name':d['name'],'price':d['price'],'qty':item.qty})
        data={'name':order.name,'phone':order.phone,'note':order.note,'pickup':s['name'],'time':slot['label'],'items':items,'total':sum(i['price']*i['qty'] for i in items)}
        code='VJU-'+secrets.token_hex(6).upper()
        token=lookup_token(c,code,order.key)
        c.execute('INSERT INTO orders(code,lookup_hash,idem,fingerprint,data,status,created_at) VALUES(?,?,?,?,?,?,?)',(code,digest(token),order.key,fingerprint,json.dumps(data,ensure_ascii=False),'pending',datetime.now(TZ).isoformat()))
        row=c.execute('SELECT * FROM orders WHERE code=?',(code,)).fetchone()
        return {**order_view(row),'token':token}

@app.get('/api/orders/{code}')
def get_order(code: str, request: Request):
    throttle(request,'lookup',60)
    token=request.headers.get('authorization','').removeprefix('Bearer ')
    with db() as c:
        row=c.execute('SELECT * FROM orders WHERE code=?',(code,)).fetchone()
        if not row or not hmac.compare_digest(row['lookup_hash'],digest(token)): fail(404,'Mã đơn hoặc mã tra cứu không đúng.')
        return order_view(row)

def admin(request: Request):
    token=request.cookies.get('vju_admin','')
    with db() as c:
        row=c.execute('SELECT * FROM sessions WHERE token=? AND expires>?',(digest(token),time.time())).fetchone()
        if not row: fail(401,'Vui lòng đăng nhập quản trị.')
        if request.method not in ('GET','HEAD') and not hmac.compare_digest(row['csrf'],request.headers.get('x-csrf-token','')): fail(403,'Phiên không hợp lệ. Hãy tải lại trang.')
        return dict(row)

@app.post('/api/admin/login')
def login(data: Login, request: Request, response: Response):
    throttle(request,'login',8)
    with db() as c:
        row=c.execute('SELECT * FROM admins WHERE username=?',(data.username,)).fetchone()
        # Always perform the expensive hash, even for unknown users.
        salt=row['salt'] if row else '00'*16
        check=password_hash(data.password,salt)
        if not row or not hmac.compare_digest(row['hash'],check): fail(401,'Tên đăng nhập hoặc mật khẩu không đúng.')
        token=secrets.token_urlsafe(32); csrf=secrets.token_urlsafe(32)
        c.execute('DELETE FROM sessions WHERE expires<? OR token=?',(time.time(),digest(request.cookies.get('vju_admin',''))))
        c.execute('INSERT INTO sessions VALUES(?,?,?,?)',(digest(token),data.username,csrf,time.time()+28800))
        response.set_cookie('vju_admin',token,max_age=28800,httponly=True,secure=SECURE,samesite='strict',path=COOKIE_PATH)
        return {'csrf':csrf,'username':data.username}
@app.get('/api/admin/me')
def me(user=Depends(admin)): return {'username':user['username'],'csrf':user['csrf']}
@app.post('/api/admin/logout')
def logout(response: Response,user=Depends(admin)):
    with db() as c: c.execute('DELETE FROM sessions WHERE token=?',(user['token'],))
    response.delete_cookie('vju_admin',path=COOKIE_PATH)
    return {'ok':True}
@app.get('/api/admin/dishes')
def admin_dishes(user=Depends(admin)):
    with db() as c: return [json.loads(r[0]) for r in c.execute('SELECT data FROM dishes')]
@app.post('/api/admin/dishes',status_code=201)
def add_dish(data: Dish,user=Depends(admin)):
    with db() as c:
        ident=c.execute('INSERT INTO dishes(data) VALUES(?)',('{}',)).lastrowid
        result={**data.model_dump(),'id':ident}
        c.execute('UPDATE dishes SET data=? WHERE id=?',(json.dumps(result,ensure_ascii=False),ident))
        return result
@app.put('/api/admin/dishes/{ident}')
def edit_dish(ident:int,data:Dish,user=Depends(admin)):
    with db() as c:
        if not c.execute('SELECT 1 FROM dishes WHERE id=?',(ident,)).fetchone(): fail(404,'Không tìm thấy món.')
        result={**data.model_dump(),'id':ident}
        c.execute('UPDATE dishes SET data=? WHERE id=?',(json.dumps(result,ensure_ascii=False),ident))
        return result
@app.get('/api/admin/orders')
def admin_orders(status:str='',offset:int=0,user=Depends(admin)):
    if offset<0: fail(422,'Trang không hợp lệ.')
    with db() as c:
        rows=c.execute('SELECT * FROM orders WHERE (?=\'\' OR status=?) ORDER BY created_at DESC LIMIT 50 OFFSET ?',(status,status,offset)).fetchall()
        return [order_view(row) for row in rows]
@app.patch('/api/admin/orders/{code}/status')
def transition(code:str,data:Transition,user=Depends(admin)):
    allowed={'pending':['confirmed','cancelled'],'confirmed':['preparing','cancelled'],'preparing':['ready','cancelled'],'ready':['completed','cancelled'],'completed':[],'cancelled':[]}
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        row=c.execute('SELECT * FROM orders WHERE code=?',(code,)).fetchone()
        if not row: fail(404,'Không tìm thấy đơn.')
        if data.status not in allowed[row['status']]: fail(409,'Chuyển trạng thái không hợp lệ. Hãy tải lại đơn.')
        if data.status=='completed' and not row['paid']: fail(409,'Cần ghi nhận thu tiền trước khi hoàn thành.')
        if data.status=='cancelled' and (not data.reason or row['paid']): fail(409,'Hủy đơn cần lý do và đơn chưa thu tiền. Đơn đã thu tiền cần xử lý riêng với quán.')
        c.execute('UPDATE orders SET status=?,cancel_reason=? WHERE code=?',(data.status,data.reason if data.status=='cancelled' else '',code))
        return order_view(c.execute('SELECT * FROM orders WHERE code=?',(code,)).fetchone())
@app.patch('/api/admin/orders/{code}/payment')
def payment(code:str,data:Paid,user=Depends(admin)):
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        row=c.execute('SELECT * FROM orders WHERE code=?',(code,)).fetchone()
        if not row: fail(404,'Không tìm thấy đơn.')
        if row['status'] in ('pending','cancelled'): fail(409,'Chỉ thu tiền cho đơn đã xác nhận và chưa hủy.')
        c.execute('UPDATE orders SET paid=1 WHERE code=?',(code,))
        return {'ok':True}
@app.get('/api/admin/shop')
def get_shop(user=Depends(admin)):
    with db() as c: return settings(c)
@app.put('/api/admin/shop')
def set_shop(data:Shop,user=Depends(admin)):
    if data.opens>=data.closes: fail(422,'Giờ đóng phải sau giờ mở; chưa hỗ trợ qua đêm.')
    with db() as c: c.execute('UPDATE settings SET data=? WHERE id=1',(json.dumps(data.model_dump(),ensure_ascii=False),))
    return data
@app.get('/api/admin/stats')
def stats(user=Depends(admin)):
    today=datetime.now(TZ).date().isoformat()
    with db() as c:
        rows=c.execute('SELECT * FROM orders WHERE substr(created_at,1,10)=?',(today,)).fetchall()
        return {'date':today,'orders':len(rows),'completed':sum(r['status']=='completed' for r in rows),'cancelled':sum(r['status']=='cancelled' for r in rows),'collected':sum(json.loads(r['data'])['total'] for r in rows if r['paid'])}

app.mount('/',StaticFiles(directory=HERE/'web',html=True),name='web')
