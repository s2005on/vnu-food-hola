import os, tempfile, unittest, json, secrets
from pathlib import Path
os.environ['VJU_COOKIE_SECURE']='0'
_tmp=tempfile.TemporaryDirectory()
os.environ['VJU_DB']=str(Path(_tmp.name)/'initial.sqlite3')
from fastapi.testclient import TestClient
from unittest.mock import patch
from server import app as mod

SLOT='2026-11-08T12:00:00+07:00'
class ServerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        mod.DB=Path(self.tmp.name)/'food.sqlite3';mod.init_db();mod.limits.clear()
        self.client=TestClient(mod.app)
        self.client.headers['X-VJU-Request']='1'
        self.slots=patch.object(mod,'options',return_value=[{'id':SLOT,'label':'08/11 12:00 – 12:30'}]);self.slots.start()
        salt=secrets.token_hex(16)
        with mod.db() as c: c.execute('INSERT INTO admins VALUES(?,?,?)',('son',salt,mod.password_hash('test-password-123',salt)))
    def tearDown(self): self.slots.stop();self.client.close();self.tmp.cleanup()
    def login(self):
        r=self.client.post('/api/admin/login',json={'username':'son','password':'test-password-123'})
        self.assertEqual(r.status_code,200)
        self.client.headers['X-CSRF-Token']=r.json()['csrf']
        return r
    def payload(self): return {'name':'Khách thử','phone':'0900000000','slot':SLOT,'note':'Ít cay','key':secrets.token_hex(16),'items':[{'id':1,'qty':1,'price':30000},{'id':2,'qty':1,'price':35000}]}
    def order(self,payload=None):
        r=self.client.post('/api/orders',json=payload or self.payload());self.assertEqual(r.status_code,201,r.text);return r.json()
    def test_price_and_lookup_secret(self):
        o=self.order();self.assertEqual(o['total'],65000)
        self.assertEqual(self.client.get('/api/orders/'+o['code']).status_code,404)
        self.assertEqual(self.client.get('/api/orders/'+o['code'],headers={'Authorization':'Bearer '+o['token']}).json()['total'],65000)
    def test_replay_returns_same_secret_after_restart(self):
        p=self.payload();a=self.order(p);mod.init_db();b=self.order(p)
        self.assertEqual(a,b)
        with mod.db() as c: self.assertEqual(c.execute('SELECT COUNT(*) FROM orders').fetchone()[0],1)
    def test_key_cannot_be_reused_with_changed_payload(self):
        p=self.payload();self.order(p);p['note']='Khác'
        self.assertEqual(self.client.post('/api/orders',json=p).status_code,409)
    def test_reject_changed_price(self):
        p=self.payload();p['items'][0]['price']=1
        self.assertEqual(self.client.post('/api/orders',json=p).status_code,409)
    def test_reject_quantity_phone_extra_fields(self):
        for update in [{'phone':'abc'},{'total':1},{'items':[{'id':1,'qty':0,'price':30000}]},{'items':[{'id':1,'qty':True,'price':30000}]}]:
            p=self.payload();p.update(update);self.assertEqual(self.client.post('/api/orders',json=p).status_code,422)
    def test_reject_soldout_and_duplicate_items(self):
        p=self.payload();p['items']=[{'id':8,'qty':1,'price':18000}]
        self.assertEqual(self.client.post('/api/orders',json=p).status_code,409)
        p=self.payload();p['items'].append(p['items'][0]);self.assertEqual(self.client.post('/api/orders',json=p).status_code,422)
    def test_closed_shop(self):
        self.slots.stop();self.slots=patch.object(mod,'options',return_value=[]);self.slots.start()
        self.assertEqual(self.client.post('/api/orders',json=self.payload()).status_code,409)
    def test_admin_auth_and_csrf(self):
        self.assertEqual(self.client.get('/api/admin/orders').status_code,401)
        self.login();del self.client.headers['X-CSRF-Token']
        self.assertEqual(self.client.post('/api/admin/logout',json={}).status_code,403)
    def test_complete_flow_and_payment_gate(self):
        o=self.order();self.login();path='/api/admin/orders/'+o['code']
        self.assertEqual(self.client.patch(path+'/status',json={'status':'completed'}).status_code,409)
        for status in ['confirmed','preparing','ready']:
            self.assertEqual(self.client.patch(path+'/status',json={'status':status}).status_code,200)
        self.assertEqual(self.client.patch(path+'/status',json={'status':'completed'}).status_code,409)
        self.assertEqual(self.client.patch(path+'/payment',json={'paid':True}).status_code,200)
        self.assertEqual(self.client.patch(path+'/status',json={'status':'completed'}).status_code,200)
        self.assertEqual(self.client.patch(path+'/status',json={'status':'pending'}).status_code,409)
    def test_cancel_reason_and_terminal_state(self):
        o=self.order();self.login();path='/api/admin/orders/'+o['code']
        self.assertEqual(self.client.patch(path+'/status',json={'status':'cancelled'}).status_code,409)
        self.assertEqual(self.client.patch(path+'/status',json={'status':'cancelled','reason':'Hết món'}).status_code,200)
        self.assertEqual(self.client.patch(path+'/payment',json={'paid':True}).status_code,409)
    def test_price_snapshot_and_hide_dish(self):
        o=self.order();self.login();d=self.client.get('/api/admin/dishes').json()[0];d.pop('id');d.update(price=40000,active=False)
        self.assertEqual(self.client.put('/api/admin/dishes/1',json=d).status_code,200)
        self.assertNotIn(1,[x['id'] for x in self.client.get('/api/menu').json()['dishes']])
        got=self.client.get('/api/orders/'+o['code'],headers={'Authorization':'Bearer '+o['token']}).json()
        self.assertEqual(got['total'],65000);self.assertEqual(got['items'][0]['price'],30000)
    def test_no_public_database_and_session_logout(self):
        self.assertEqual(self.client.get('/data/food.sqlite3').status_code,404)
        r=self.login();self.assertIn('HttpOnly',r.headers['set-cookie']);self.assertIn('SameSite=strict',r.headers['set-cookie'])
        self.assertEqual(self.client.post('/api/admin/logout',json={}).status_code,200)
        self.assertEqual(self.client.get('/api/admin/me').status_code,401)
    def test_login_rate_limit(self):
        for _ in range(8): self.client.post('/api/admin/login',json={'username':'son','password':'wrong'})
        self.assertEqual(self.client.post('/api/admin/login',json={'username':'son','password':'wrong'}).status_code,429)
    def test_settings_and_creation(self):
        self.login()
        self.assertEqual(self.client.put('/api/admin/shop',json={'name':'Quán','accepting':True,'opens':'20:00','closes':'08:00'}).status_code,422)
        self.assertEqual(self.client.post('/api/admin/dishes',json={'name':'Món mới','price':25000,'category':'Cơm'}).status_code,201)
    def test_slots_time_boundaries(self):
        from datetime import datetime
        self.slots.stop()
        shop={'opens':'08:00','closes':'20:00','accepting':True}
        slots=mod.options(shop,datetime(2026,11,8,11,16,tzinfo=mod.TZ))
        self.assertEqual(slots[0]['id'],'2026-11-08T12:00:00+07:00')
        self.assertEqual(mod.options(shop,datetime(2026,11,8,20,0,tzinfo=mod.TZ)),[])
    def test_backup_restore_preserves_order(self):
        import sqlite3
        o=self.order();backup=Path(self.tmp.name)/'backup.sqlite3'
        with sqlite3.connect(mod.DB) as src,sqlite3.connect(backup) as dest:src.backup(dest)
        mod.DB=backup
        self.assertEqual(self.client.get('/api/orders/'+o['code'],headers={'Authorization':'Bearer '+o['token']}).json()['code'],o['code'])
    def test_concurrent_retries_single_order(self):
        from concurrent.futures import ThreadPoolExecutor
        p=self.payload()
        def send(_):
            with TestClient(mod.app) as client:return client.post('/api/orders',json=p,headers={'X-VJU-Request':'1'})
        with ThreadPoolExecutor(max_workers=3) as pool: responses=list(pool.map(send,range(3)))
        self.assertTrue(all(r.status_code==201 for r in responses))
        self.assertEqual(len({r.json()['code'] for r in responses}),1)

if __name__=='__main__':unittest.main()
