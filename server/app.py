"""Single-shop ordering service. Run one worker (SQLite + local rate limiter)."""
import os, json, sqlite3, secrets, hashlib, hmac, time, threading
from pathlib import Path
from contextlib import contextmanager
from contextvars import ContextVar
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
ACTIVE_DB = ContextVar('vju_active_db', default=None)
TRIAL_ID = ContextVar('vju_trial_id', default=None)
TRIAL_ENABLED = os.environ.get('VJU_TRIAL_ENABLED', '1') == '1'
SHOP_TRIAL_PASSWORD = 'QuanTest2026!'
TRIAL_PASSWORD = 'VjuTest2026!'  # Public demo credential; never a production admin.
app = FastAPI(title='VJU Food Hola', docs_url=None, redoc_url=None, openapi_url=None)

def fail(code, message): raise HTTPException(code, message)
def digest(value): return hashlib.sha256(value.encode()).hexdigest()
def password_hash(password, salt): return hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1).hex()

@contextmanager
def db():
    c = sqlite3.connect(ACTIVE_DB.get() or DB, timeout=15)
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
    target = ACTIVE_DB.get() or DB
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with db() as c:
        c.executescript('''
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS app_migrations(name TEXT PRIMARY KEY);
        CREATE TABLE IF NOT EXISTS trial_sessions(token_hash TEXT PRIMARY KEY, filename TEXT NOT NULL, expires REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS order_events(id INTEGER PRIMARY KEY, code TEXT NOT NULL, actor TEXT NOT NULL, action TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS settings(id INTEGER PRIMARY KEY CHECK(id=1), data TEXT NOT NULL, secret TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS dishes(id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS admins(username TEXT PRIMARY KEY, salt TEXT NOT NULL, hash TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS customers(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone TEXT UNIQUE NOT NULL, salt TEXT NOT NULL, hash TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS customer_sessions(token_hash TEXT PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE, csrf TEXT NOT NULL, expires REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, username TEXT NOT NULL REFERENCES admins(username), csrf TEXT NOT NULL, expires REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS orders(code TEXT PRIMARY KEY, lookup_hash TEXT NOT NULL, idem TEXT UNIQUE NOT NULL, fingerprint TEXT NOT NULL, data TEXT NOT NULL, status TEXT NOT NULL, paid INTEGER NOT NULL DEFAULT 0, cancel_reason TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL);
        ''')
        columns = {r['name'] for r in c.execute('PRAGMA table_info(orders)')}
        for column in ('updated_at', 'paid_at', 'customer_id'):
            if column not in columns:
                c.execute(f'ALTER TABLE orders ADD COLUMN {column} {"INTEGER REFERENCES customers(id)" if column == "customer_id" else "TEXT"}')
        if not c.execute('SELECT 1 FROM settings').fetchone():
            c.execute('INSERT INTO settings VALUES(1,?,?)', (json.dumps({'name':'Quán mẫu gần VJU','accepting':True,'opens':'10:00','closes':'22:00'}), secrets.token_hex(32)))
            for item in json.loads((HERE/'seed.json').read_text(encoding='utf-8')):
                item['active'] = True
                c.execute('INSERT INTO dishes(id,data) VALUES(?,?)', (item['id'],json.dumps(item,ensure_ascii=False)))
        if not c.execute("SELECT 1 FROM app_migrations WHERE name='v5-hours'").fetchone():
            shop=json.loads(c.execute('SELECT data FROM settings WHERE id=1').fetchone()[0])
            shop.update(opens='10:00',closes='22:00')
            c.execute('UPDATE settings SET data=? WHERE id=1',(json.dumps(shop,ensure_ascii=False),))
            c.execute('UPDATE trial_sessions SET expires=0')
            c.execute("INSERT INTO app_migrations VALUES('v5-hours')")
        # V7 one-time catalog reset: restore availability of the eight sample dishes.
        # Keep subsequent manager edits intact on future restarts.
        if not c.execute("SELECT 1 FROM app_migrations WHERE name='v7-demo-menu' ").fetchone():
            defaults={d['id']:d['name'] for d in json.loads((HERE/'seed.json').read_text(encoding='utf-8'))}
            for row in c.execute('SELECT id,data FROM dishes').fetchall():
                dish=json.loads(row['data'])
                if defaults.get(row['id'])==dish['name'] and not dish.get('available',True):
                    dish['available']=True
                    if dish.get('tag')=='Tạm hết': dish['tag']='Cà phê Việt'
                    c.execute('UPDATE dishes SET data=? WHERE id=?',(json.dumps(dish,ensure_ascii=False),row['id']))
            c.execute("INSERT INTO app_migrations VALUES('v7-demo-menu')")
        # Add new dishes once, using fresh IDs: existing custom IDs and edits stay intact.
        if not c.execute("SELECT 1 FROM app_migrations WHERE name='v73-extra-menu'").fetchone():
            names={json.loads(r['data'])['name'].casefold() for r in c.execute('SELECT data FROM dishes')}
            for item in json.loads((HERE/'seed.json').read_text(encoding='utf-8')):
                if item['id'] <= 8 or item['name'].casefold() in names: continue
                ident=c.execute('INSERT INTO dishes(data) VALUES(?)', ('{}',)).lastrowid
                item.update(id=ident,active=True)
                c.execute('UPDATE dishes SET data=? WHERE id=?',(json.dumps(item,ensure_ascii=False),ident))
                names.add(item['name'].casefold())
            c.execute("INSERT INTO app_migrations VALUES('v73-extra-menu')")
        # Match by dish name, so renamed or custom dishes never get a wrong picture.
        images={x['name']:x.get('image','') for x in json.loads((HERE/'seed.json').read_text(encoding='utf-8'))}
        for row in c.execute('SELECT id,data FROM dishes').fetchall():
            dish=json.loads(row['data'])
            if 'image' not in dish:
                dish['image']=images.get(dish['name'],'')
                c.execute('UPDATE dishes SET data=? WHERE id=?',(json.dumps(dish,ensure_ascii=False),row['id']))
    try: os.chmod(target, 0o600)
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
    pickup: str = Field(min_length=3, max_length=200)
    slot: str = Field(max_length=40)
    note: str = Field(default='', max_length=250)
    key: str = Field(min_length=16, max_length=100, pattern=r'^[a-zA-Z0-9_-]+$')
    items: list[Item] = Field(min_length=1, max_length=30)
class Login(Model):
    model_config = ConfigDict(extra='forbid', str_strip_whitespace=False)
    username: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
    password: str = Field(min_length=1, max_length=128)
class CustomerRegistration(Model):
    name: Annotated[str, StringConstraints(min_length=2, max_length=60)]
    phone: str = Field(pattern=r'^0[0-9]{9}$')
    password: str = Field(min_length=10, max_length=128)

class CustomerCredentials(Model):
    phone: str = Field(pattern=r'^0[0-9]{9}$')
    password: str = Field(min_length=1, max_length=128)

class ClaimOrder(Model):
    code: str = Field(pattern=r'^VJU-[0-9A-F]{12}$')
    token: str = Field(min_length=16, max_length=128)

class Dish(Model):
    name: Text
    desc: str = Field(default='', max_length=300)
    price: int = Field(ge=0, le=10000000, strict=True)
    category: Literal['Cơm','Bún & mì','Ăn nhẹ','Đồ uống']
    image: str = Field(default='', pattern=r'^(|assets/food-(?:[1-9]|1[0-6])\.png)$')
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
    trial_cookie = request.cookies.get('vju_trial', '')
    trial_path, trial_id = None, None
    # Browsers can retain a cookie after the 2-hour demo session expires.
    # Read-only public pages should still render the menu, without allowing an
    # expired demo to silently submit an order to the main database.
    expired_trial = False
    if trial_cookie and request.url.path not in ('/api/trial/login', '/api/trial/logout'):
        with db() as c:
            row = c.execute('SELECT * FROM trial_sessions WHERE token_hash=? AND expires>?', (digest(trial_cookie), time.time())).fetchone()
        if row and TRIAL_ENABLED:
            candidate = DB.parent / 'trials' / row['filename']
            if candidate.is_file():
                trial_path, trial_id = candidate, row['filename'].removesuffix('.sqlite3')
        expired_trial = trial_path is None
        public_read = request.method == 'GET' and request.url.path in ('/api/session', '/api/menu')
        if expired_trial and request.url.path.startswith('/api/') and not public_read:
            return Response(json.dumps({'detail':'Phiên demo đã hết hạn. Hãy đăng nhập lại.'}), status_code=401, media_type='application/json', headers={'Cache-Control':'no-store'})
    expected_trial = request.headers.get('x-vju-trial')
    if expected_trial and expected_trial != trial_id:
        return Response(json.dumps({'detail':'Phiên demo đã thay đổi hoặc hết hạn. Vui lòng tải lại trang.'}),status_code=401,media_type='application/json',headers={'Cache-Control':'no-store'})
    if request.headers.get('x-vju-mode') == 'guest' and trial_id:
        return Response(json.dumps({'detail':'Chế độ đã thay đổi ở tab khác. Hãy tải lại trang trước khi đặt đơn.'}), status_code=409, media_type='application/json')
    request.state.trial_expired = expired_trial
    db_context = ACTIVE_DB.set(trial_path)
    id_context = TRIAL_ID.set(trial_id)
    try:
        response = await dispatch_headers(request, call_next)
        # Keep expired demo context until the customer explicitly exits it.
        # Public menu reads must never silently turn demo checkout into a main order.
        return response
    finally:
        ACTIVE_DB.reset(db_context)
        TRIAL_ID.reset(id_context)

async def dispatch_headers(request, call_next):
    if request.method not in ('GET','HEAD','OPTIONS') and request.headers.get('x-vju-request') != '1':
        return Response('Missing request header',status_code=403)
    response = await call_next(request)
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='no-referrer'
    response.headers['X-Frame-Options']='DENY'
    if request.url.path.startswith('/api/') or request.url.path.endswith(('.html', '.js', '.css')) or request.url.path == '/':
        response.headers['Cache-Control']='no-store'
    return response

def settings(c): return json.loads(c.execute('SELECT data FROM settings WHERE id=1').fetchone()[0])
def options(s, now=None):
    now = now or datetime.now(TZ)
    if not s['accepting']: return []
    slots=[]
    for day in range(2):
        date=(now+timedelta(days=day)).date()
        start=datetime.combine(date,datetime.strptime(s['opens'],'%H:%M').time(),TZ)
        end=datetime.combine(date,datetime.strptime(s['closes'],'%H:%M').time(),TZ)
        while start<=end:
            if start>=now+timedelta(minutes=15):
                slots.append({'id':start.isoformat(),'label':start.strftime('%d/%m · %H:%M')})
            start+=timedelta(minutes=15)
    return slots

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
    return {**json.loads(row['data']), 'updated_at':row['updated_at'], 'paid_at':row['paid_at'], 'code':row['code'], 'status':row['status'], 'paid':bool(row['paid']), 'cancel_reason':row['cancel_reason'], 'date':row['created_at']}

CUSTOMER_SESSION_AGE = 7 * 24 * 60 * 60

def customer_identity(request: Request):
    """Resolve a customer using a hashed, unexpired HttpOnly session cookie."""
    token = request.cookies.get('vju_customer', '')
    if not token:
        return None
    with db() as c:
        row = c.execute('''
            SELECT customers.id, customers.name, customers.phone, customer_sessions.csrf
            FROM customer_sessions JOIN customers ON customers.id = customer_sessions.customer_id
            WHERE customer_sessions.token_hash=? AND customer_sessions.expires>?
        ''', (digest(token), time.time())).fetchone()
    return dict(row) if row else None

def require_customer(request: Request):
    if TRIAL_ID.get():
        fail(409, 'Hãy thoát chế độ demo trước khi sử dụng tài khoản khách.')
    result = customer_identity(request)
    if not result:
        fail(401, 'Vui lòng đăng nhập tài khoản khách.')
    return result

def customer_csrf(request: Request, customer):
    if not hmac.compare_digest(customer['csrf'], request.headers.get('x-csrf-token', '')):
        fail(403, 'Phiên không hợp lệ. Vui lòng tải lại trang.')

def customer_login_response(response: Response, record):
    token, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
    with db() as c:
        c.execute('DELETE FROM customer_sessions WHERE expires<?', (time.time(),))
        c.execute('INSERT INTO customer_sessions VALUES(?,?,?,?)',
                  (digest(token), record['id'], csrf, time.time()+CUSTOMER_SESSION_AGE))
    response.set_cookie('vju_customer', token, max_age=CUSTOMER_SESSION_AGE,
                        httponly=True, secure=SECURE, samesite='strict', path=COOKIE_PATH)
    return {'id': record['id'], 'name': record['name'], 'phone': record['phone'], 'csrf': csrf}

@app.post('/api/customer/register', status_code=201)
def customer_register(data: CustomerRegistration, request: Request, response: Response):
    if TRIAL_ID.get():
        fail(409, 'Hãy thoát chế độ demo trước khi đăng ký.')
    throttle(request, 'customer-register', 5)
    salt = secrets.token_hex(16)
    hashed = password_hash(data.password, salt)
    try:
        with db() as c:
            cur = c.execute('INSERT INTO customers(name,phone,salt,hash,created_at) VALUES(?,?,?,?,?)',
                            (data.name, data.phone, salt, hashed, datetime.now(TZ).isoformat()))
            record = {'id': cur.lastrowid, 'name': data.name, 'phone': data.phone}
    except sqlite3.IntegrityError:
        fail(409, 'Số điện thoại này đã có tài khoản. Hãy đăng nhập.')
    return customer_login_response(response, record)

@app.post('/api/customer/login')
def customer_login(data: CustomerCredentials, request: Request, response: Response):
    if TRIAL_ID.get():
        fail(409, 'Hãy thoát chế độ demo trước khi đăng nhập.')
    throttle(request, 'customer-login', 8)
    with db() as c:
        row = c.execute('SELECT * FROM customers WHERE phone=?', (data.phone,)).fetchone()
    salt = row['salt'] if row else '00'*16
    verified = hmac.compare_digest(password_hash(data.password, salt), row['hash'] if row else '0'*128)
    if not row or not verified:
        fail(401, 'Số điện thoại hoặc mật khẩu không chính xác.')
    return customer_login_response(response, dict(row))

@app.get('/api/customer/me')
def customer_me(request: Request):
    customer = require_customer(request)
    return {k: customer[k] for k in ('id', 'name', 'phone', 'csrf')}

@app.post('/api/customer/logout')
def customer_logout(request: Request, response: Response):
    customer = require_customer(request)
    customer_csrf(request, customer)
    with db() as c:
        c.execute('DELETE FROM customer_sessions WHERE token_hash=?',
                  (digest(request.cookies.get('vju_customer', '')),))
    response.delete_cookie('vju_customer', path=COOKIE_PATH)
    return {'ok': True}

@app.get('/api/customer/orders')
def customer_orders(request: Request):
    customer = require_customer(request)
    with db() as c:
        rows = c.execute('SELECT * FROM orders WHERE customer_id=? ORDER BY created_at DESC LIMIT 100',
                         (customer['id'],)).fetchall()
    return [order_view(row) for row in rows]

@app.post('/api/customer/orders/claim')
def claim_customer_order(data: ClaimOrder, request: Request):
    customer = require_customer(request)
    customer_csrf(request, customer)
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        row = c.execute('SELECT * FROM orders WHERE code=?', (data.code,)).fetchone()
        if not row or not hmac.compare_digest(row['lookup_hash'], digest(data.token)):
            fail(404, 'Mã đơn hoặc mã tra cứu không đúng.')
        if row['customer_id'] is not None and row['customer_id'] != customer['id']:
            fail(409, 'Đơn này đã thuộc tài khoản khác.')
        if row['customer_id'] is None:
            c.execute('UPDATE orders SET customer_id=? WHERE code=?', (customer['id'], data.code))
        return order_view(c.execute('SELECT * FROM orders WHERE code=?', (data.code,)).fetchone())

@app.post('/api/orders', status_code=201)
def create_order(order: NewOrder, request: Request):
    throttle(request,'order',15)
    customer = customer_identity(request) if not TRIAL_ID.get() else None
    # Bind a checkout to the session that loaded its page. Older clients without
    # this header remain compatible; the current web client always supplies it.
    expected = request.headers.get('x-vju-checkout-session')
    actual = ('trial:' + TRIAL_ID.get()) if TRIAL_ID.get() else ('customer:' + customer['csrf'] if customer else 'guest')
    if expected is not None and not hmac.compare_digest(expected, actual):
        fail(409, 'Phiên đăng nhập đã thay đổi. Hãy tải lại trang trước khi đặt món.')
    if customer and order.phone != customer['phone']:
        fail(422, 'Số điện thoại đặt hàng phải trùng số đã đăng ký.')
    payload=order.model_dump()
    fingerprint=digest(json.dumps(payload,sort_keys=True,ensure_ascii=False))
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        old=c.execute('SELECT * FROM orders WHERE idem=?',(order.key,)).fetchone()
        if old:
            if (old['customer_id'] is not None and (not customer or old['customer_id'] != customer['id'])) or (customer and old['customer_id'] is None):
                fail(409, 'Đơn cũ thuộc phiên khách khác. Hãy kiểm tra trước khi đặt lại.')
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
        data={'name':order.name,'phone':order.phone,'note':order.note,'pickup':order.pickup,'time':slot['label'],'items':items,'total':sum(i['price']*i['qty'] for i in items)}
        code='VJU-'+secrets.token_hex(6).upper()
        token=lookup_token(c,code,order.key)
        c.execute('INSERT INTO orders(code,lookup_hash,idem,fingerprint,data,status,created_at,customer_id) VALUES(?,?,?,?,?,?,?,?)',(code,digest(token),order.key,fingerprint,json.dumps(data,ensure_ascii=False),'pending',datetime.now(TZ).isoformat(),customer['id'] if customer else None))
        c.execute('INSERT INTO order_events(code,actor,action,created_at) VALUES(?,?,?,?)', (code,'customer','created',datetime.now(TZ).isoformat()))
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
def me(user=Depends(admin)): return {'username':user['username'],'csrf':user['csrf'],'trial':bool(TRIAL_ID.get())}
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
        now = datetime.now(TZ).isoformat()
        c.execute('UPDATE orders SET status=?,cancel_reason=?,updated_at=? WHERE code=?',(data.status,data.reason if data.status=='cancelled' else '',now,code))
        c.execute('INSERT INTO order_events(code,actor,action,created_at) VALUES(?,?,?,?)',(code,user['username'],row['status']+' → '+data.status,now))
        return order_view(c.execute('SELECT * FROM orders WHERE code=?',(code,)).fetchone())
@app.patch('/api/admin/orders/{code}/payment')
def payment(code:str,data:Paid,user=Depends(admin)):
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        row=c.execute('SELECT * FROM orders WHERE code=?',(code,)).fetchone()
        if not row: fail(404,'Không tìm thấy đơn.')
        if row['status'] in ('pending','cancelled'): fail(409,'Chỉ thu tiền cho đơn đã xác nhận và chưa hủy.')
        if not row['paid']:
            now = datetime.now(TZ).isoformat()
            c.execute('UPDATE orders SET paid=1,paid_at=?,updated_at=? WHERE code=?',(now,now,code))
            c.execute('INSERT INTO order_events(code,actor,action,created_at) VALUES(?,?,?,?)',(code,user['username'],'paid',now))
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
        received = c.execute('SELECT data FROM orders WHERE paid=1 AND substr(paid_at,1,10)=?',(today,)).fetchall()
        return {'collected_today':sum(json.loads(r['data'])['total'] for r in received),'date':today,'orders':len(rows),'completed':sum(r['status']=='completed' for r in rows),'cancelled':sum(r['status']=='cancelled' for r in rows),'collected':sum(json.loads(r['data'])['total'] for r in rows if r['paid'])}


@app.get('/api/session')
def session_info(request: Request):
    customer = customer_identity(request) if not TRIAL_ID.get() else None
    return {'trial':bool(TRIAL_ID.get()), 'trial_id':TRIAL_ID.get(),
            'trial_enabled':TRIAL_ENABLED, 'customer': 'demo' if TRIAL_ID.get() else None,
            'customer_id': customer['id'] if customer else None,
            'customer_name': customer['name'] if customer else None,
            'customer_phone': customer['phone'] if customer else None,
            'customer_csrf': customer['csrf'] if customer else None,
            'expired': bool(getattr(request.state, 'trial_expired', False))}

@app.get('/api/admin/orders/{code}/events')
def order_events(code: str, user=Depends(admin)):
    with db() as c:
        if not c.execute('SELECT 1 FROM orders WHERE code=?',(code,)).fetchone(): fail(404,'Không tìm thấy đơn.')
        return [dict(r) for r in c.execute('SELECT actor,action,created_at FROM order_events WHERE code=? ORDER BY id',(code,))]

@app.post('/api/trial/login')
def trial_login(data: Login, request: Request, response: Response):
    if not TRIAL_ENABLED: fail(404,'Chế độ thử đã tắt.')
    throttle(request,'trial-login',5)
    if data.username not in ('demo','tester') or not hmac.compare_digest(data.password,TRIAL_PASSWORD):
        fail(401,'Tài khoản demo: demo / VjuTest2026!')
    # Always starts from seeded sample data; never copies production customers.
    token = secrets.token_urlsafe(32)
    filename = secrets.token_hex(16)+'.sqlite3'
    trial_path = DB.parent/'trials'/filename
    with db() as c:
        c.execute('BEGIN IMMEDIATE')
        expired = c.execute('SELECT * FROM trial_sessions WHERE expires<?',(time.time()-600,)).fetchall()
        for row in expired:
            for suffix in ('','-wal','-shm'):
                (DB.parent/'trials'/(row['filename']+suffix)).unlink(missing_ok=True)
            c.execute('DELETE FROM trial_sessions WHERE token_hash=?',(row['token_hash'],))
        if c.execute('SELECT COUNT(*) FROM trial_sessions').fetchone()[0]>=50:
            fail(429,'Đang có nhiều phiên thử. Vui lòng quay lại sau.')
        c.execute('INSERT INTO trial_sessions VALUES(?,?,?)',(digest(token),filename,time.time()+7200))
    context = ACTIVE_DB.set(trial_path)
    try:
        init_db()
        admin_token, csrf = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
        salt = secrets.token_hex(16)
        with db() as c:
            c.execute('INSERT INTO admins VALUES(?,?,?)',('shoptest',salt,password_hash(SHOP_TRIAL_PASSWORD,salt)))
            shop=settings(c);shop['name']='Quán thử của bạn';shop['accepting']=True
            c.execute('UPDATE settings SET data=? WHERE id=1',(json.dumps(shop,ensure_ascii=False),))
    finally:
        ACTIVE_DB.reset(context)
    response.delete_cookie('vju_admin',path=COOKIE_PATH)
    for name,value in [('vju_trial',token)]:
        response.set_cookie(name,value,max_age=7200,httponly=True,secure=SECURE,samesite='strict',path=COOKIE_PATH)
    return {'ok':True,'trial':True,'expires_in':7200}

@app.post('/api/trial/logout')
def trial_logout(request: Request, response: Response):
    # Revoke the token as well as the browser cookie. Keep files briefly for in-flight requests.
    with db() as c:
        c.execute('UPDATE trial_sessions SET expires=? WHERE token_hash=?',(time.time(),digest(request.cookies.get('vju_trial',''))))
    response.delete_cookie('vju_trial',path=COOKIE_PATH)
    response.delete_cookie('vju_admin',path=COOKIE_PATH)
    return {'ok':True}

app.mount('/',StaticFiles(directory=HERE/'web',html=True),name='web')
