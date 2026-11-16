import os, tempfile, unittest, json, secrets, subprocess, sys
from contextlib import closing
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
    def payload(self): return {'name':'Khách thử','phone':'0900000000','pickup':'Sảnh KTX VJU','slot':SLOT,'note':'Ít cay','key':secrets.token_hex(16),'items':[{'id':1,'qty':1,'price':30000},{'id':2,'qty':1,'price':35000}]}
    def order(self,payload=None):
        r=self.client.post('/api/orders',json=payload or self.payload());self.assertEqual(r.status_code,201,r.text);return r.json()
    def test_extra_menu_migration_preserves_custom_ids_and_runs_once(self):
        with mod.db() as c:
            c.execute("DELETE FROM app_migrations WHERE name='v73-extra-menu'")
            c.execute('DELETE FROM dishes WHERE id>8')
            custom={'id':9,'name':'Món riêng của quán','price':19000,'active':True,'available':False}
            c.execute('INSERT INTO dishes(id,data) VALUES(9,?)',(json.dumps(custom),))
        mod.init_db();mod.init_db()
        with mod.db() as c:
            rows=[json.loads(r['data']) for r in c.execute('SELECT data FROM dishes')]
        self.assertEqual(len(rows),17)
        self.assertEqual(next(d for d in rows if d['id']==9)['name'],'Món riêng của quán')
        self.assertFalse(next(d for d in rows if d['id']==9)['available'])
        self.assertEqual(len({d['name'] for d in rows}),17)

    def test_new_dishes_images_and_order_prices(self):
        from pathlib import Path
        menu=self.client.get('/api/menu').json()['dishes']
        self.assertEqual(len(menu),16)
        for dish in menu:
            self.assertTrue((mod.HERE/'web'/dish['image']).is_file())
        item=next(d for d in menu if d['name']=='Sữa đậu nành')
        p=self.payload();p['items']=[{'id':item['id'],'qty':2,'price':item['price']}]
        self.assertEqual(self.order(p)['total'],24000)

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
        # V7 starts with all sample dishes available; an admin can still sell out a dish.
        import json
        with mod.db() as c:
            row=c.execute('SELECT data FROM dishes WHERE id=8').fetchone()
            dish=json.loads(row['data']);dish['available']=False
            c.execute('UPDATE dishes SET data=? WHERE id=8',(json.dumps(dish,ensure_ascii=False),))
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
        self.assertEqual(slots[0]['id'],'2026-11-08T11:45:00+07:00')
        self.assertTrue(all(x['id'].startswith('2026-11-09') for x in mod.options(shop,datetime(2026,11,8,20,0,tzinfo=mod.TZ))))
    def test_backup_restore_preserves_order(self):
        import sqlite3
        o=self.order();backup=Path(self.tmp.name)/'backup.sqlite3'
        with closing(sqlite3.connect(mod.DB)) as src,closing(sqlite3.connect(backup)) as dest:src.backup(dest)
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

    def test_proxy_rate_limits_and_spoofed_headers(self):
        from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
        proxy = ProxyHeadersMiddleware(mod.app, trusted_hosts=['127.0.0.1'])
        payload = {'username':'son','password':'wrong'}
        def send(client, ip):
            return client.post('/api/admin/login', json=payload, headers={'X-VJU-Request':'1', 'X-Forwarded-For':ip})
        with TestClient(proxy, client=('127.0.0.1', 1234)) as client:
            for _ in range(8): self.assertEqual(send(client, '198.51.100.10').status_code, 401)
            self.assertEqual(send(client, '198.51.100.10').status_code, 429)
            self.assertEqual(send(client, '198.51.100.11').status_code, 401)
        with TestClient(proxy, client=('198.51.100.10', 1234)) as client:
            self.assertEqual(send(client, '198.51.100.12').status_code, 429)

    def test_backup_command_preserves_data_and_refuses_overwrite(self):
        import sqlite3
        order = self.order()
        target = Path(self.tmp.name) / 'backup.sqlite3'
        command = [sys.executable, '-m', 'server.manage', 'backup', '--output', str(target)]
        env = {**os.environ, 'VJU_DB':str(mod.DB)}
        result = subprocess.run(command, env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        with closing(sqlite3.connect(target)) as c:
            self.assertEqual(c.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
            self.assertEqual(c.execute('SELECT code FROM orders').fetchone()[0], order['code'])
        before = target.read_bytes()
        self.assertNotEqual(subprocess.run(command, env=env, capture_output=True).returncode, 0)
        self.assertEqual(target.read_bytes(), before)

    def test_backup_missing_database_does_not_seed(self):
        source = Path(self.tmp.name) / 'missing.sqlite3'
        target = Path(self.tmp.name) / 'backup.sqlite3'
        result = subprocess.run([sys.executable, '-m', 'server.manage', 'backup', '--output', str(target)], env={**os.environ, 'VJU_DB':str(source)}, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(source.exists())
        self.assertFalse(target.exists())

    def test_seed_reads_utf8_with_legacy_encoding(self):
        source = Path(self.tmp.name) / 'seed-check.sqlite3'
        result = subprocess.run([sys.executable, '-c', 'import locale; locale.getencoding=lambda: "cp1252"; from server import app; assert app.menu()["dishes"][0]["name"]'], env={**os.environ, 'VJU_DB':str(source), 'PYTHONUTF8':'0'}, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def trial(self, client=None):
        client=client or self.client
        r=client.post('/api/trial/login',json={'username':'tester','password':mod.TRIAL_PASSWORD},headers={'X-VJU-Request':'1'})
        self.assertEqual(r.status_code,200,r.text)
        self.assertEqual(client.get('/api/admin/me').status_code,401)
        self.assertEqual(client.post('/api/admin/login',json={'username':'shoptest','password':mod.SHOP_TRIAL_PASSWORD},headers={'X-VJU-Request':'1'}).status_code,200)
        me=client.get('/api/admin/me').json()
        client.headers['X-CSRF-Token']=me['csrf']
        return client.get('/api/session').json()

    def test_demo_login_and_all_sample_dishes_available(self):
        response=self.client.post('/api/trial/login',json={'username':'demo','password':mod.TRIAL_PASSWORD},headers={'X-VJU-Request':'1'})
        self.assertEqual(response.status_code,200,response.text)
        info=self.client.get('/api/session').json()
        self.assertEqual(info['customer'],'demo')
        menu=self.client.get('/api/menu').json()
        self.assertEqual(len(menu['dishes']),16)
        self.assertTrue(all(d['available'] for d in menu['dishes']))

    def test_trial_isolated_from_main_and_other_visitors(self):
        real=self.order();info=self.trial();trial=self.order()
        self.assertTrue(info['trial'])
        self.assertEqual(self.client.get('/api/admin/orders').json()[0]['code'],trial['code'])
        self.assertEqual(self.client.get('/api/orders/'+real['code'],headers={'Authorization':'Bearer '+real['token']}).status_code,404)
        with mod.db() as c:
            self.assertEqual(c.execute('SELECT COUNT(*) FROM orders').fetchone()[0],1)
            self.assertIsNone(c.execute("SELECT 1 FROM admins WHERE username='tester'").fetchone())
        with TestClient(mod.app) as other:
            second=self.trial(other)
            self.assertNotEqual(info['trial_id'],second['trial_id'])
            self.assertEqual(other.get('/api/admin/orders').json(),[])
            self.assertEqual(other.get('/api/orders/'+trial['code'],headers={'Authorization':'Bearer '+trial['token']}).status_code,404)

    def test_public_trial_password_never_opens_real_admin(self):
        self.assertEqual(self.client.post('/api/admin/login',json={'username':'tester','password':mod.TRIAL_PASSWORD}).status_code,401)
        self.assertEqual(self.client.post('/api/trial/login',json={'username':'tester','password':'wrong'}).status_code,401)
        with patch.object(mod,'TRIAL_ENABLED',False):
            self.assertEqual(self.client.post('/api/trial/login',json={'username':'tester','password':mod.TRIAL_PASSWORD}).status_code,404)

    def test_expired_trial_cannot_create_main_order(self):
        info=self.trial()
        with mod.db() as c:c.execute('UPDATE trial_sessions SET expires=0')
        self.assertEqual(self.client.post('/api/orders',json=self.payload()).status_code,401)
        self.client.cookies.clear()
        self.assertEqual(self.client.post('/api/orders',json=self.payload(),headers={'X-VJU-Trial':info['trial_id']}).status_code,401)
        with mod.db() as c:self.assertEqual(c.execute('SELECT COUNT(*) FROM orders').fetchone()[0],0)

    def test_trial_logout_revokes_token_and_recovers_guest(self):
        self.trial();token=self.client.cookies.get('vju_trial')
        self.assertEqual(self.client.post('/api/trial/logout',json={}).status_code,200)
        self.assertFalse(self.client.get('/api/session').json()['trial'])
        self.client.cookies.set('vju_trial',token,domain='testserver.local',path='/')
        restored=self.client.get('/api/session')
        self.assertEqual(restored.status_code,200)
        self.assertTrue(restored.json()['expired'])
        self.assertFalse(restored.json()['trial'])
        self.assertIsNotNone(self.client.cookies.get('vju_trial'))
        self.assertEqual(self.client.get('/api/menu').status_code,200)

    def test_expired_demo_menu_still_visible_but_no_unsafe_fallback(self):
        self.trial()
        with mod.db() as c: c.execute('UPDATE trial_sessions SET expires=0')
        # A stale demo cookie cannot create an order in the main shop.
        self.assertEqual(self.client.post('/api/orders',json=self.payload()).status_code,401)
        self.assertEqual(self.client.cookies.get('vju_trial') is not None,True)
        # Reading the menu and session recovers without clearing saved order refs.
        response=self.client.get('/api/session')
        self.assertEqual(response.status_code,200)
        self.assertTrue(response.json()['expired'])
        self.assertFalse(response.json()['trial'])
        self.assertNotIn('vju_trial=',response.headers.get('set-cookie',''))
        self.assertIsNotNone(self.client.cookies.get('vju_trial'))
        self.assertEqual(len(self.client.get('/api/menu').json()['dishes']),16)

    def test_expired_demo_menu_request_directly_recovers(self):
        self.trial()
        with mod.db() as c: c.execute('UPDATE trial_sessions SET expires=0')
        menu=self.client.get('/api/menu')
        self.assertEqual(menu.status_code,200)
        self.assertEqual(len(menu.json()['dishes']),16)
        self.assertIsNotNone(self.client.cookies.get('vju_trial'))

    def test_expired_menu_read_does_not_enable_main_checkout(self):
        self.trial()
        with mod.db() as c: c.execute('UPDATE trial_sessions SET expires=0')
        self.client.get('/api/session'); self.client.get('/api/menu')
        self.assertEqual(self.client.post('/api/orders',json=self.payload()).status_code,401)
        self.client.post('/api/trial/logout',json={})
        self.assertEqual(self.client.post('/api/orders',json=self.payload(),headers={'X-VJU-Mode':'guest'}).status_code,201)

    def test_guest_tab_cannot_submit_into_another_trial(self):
        self.trial()
        self.assertEqual(self.client.post('/api/orders',json=self.payload(),headers={'X-VJU-Mode':'guest'}).status_code,409)

    def test_guest_and_shop_separate_browsers_persist_and_track(self):
        guest=TestClient(mod.app)
        guest.headers.update({'X-VJU-Request':'1','X-VJU-Mode':'guest'})
        o=guest.post('/api/orders',json=self.payload()).json()
        self.login()
        self.assertIn(o['code'],[x['code'] for x in self.client.get('/api/admin/orders').json()])
        self.client.patch('/api/admin/orders/'+o['code']+'/status',json={'status':'confirmed'})
        mod.init_db()
        result=guest.get('/api/orders/'+o['code'],headers={'Authorization':'Bearer '+o['token']})
        self.assertEqual(result.json()['status'],'confirmed')
        self.assertEqual(guest.get('/api/admin/orders').status_code,401)
        guest.close()

    def test_trial_full_order_flow_and_audit(self):
        self.trial();o=self.order();path='/api/admin/orders/'+o['code']
        for status in ['confirmed','preparing','ready']:
            self.assertEqual(self.client.patch(path+'/status',json={'status':status}).status_code,200)
        self.assertEqual(self.client.patch(path+'/payment',json={'paid':True}).status_code,200)
        self.assertEqual(self.client.patch(path+'/status',json={'status':'completed'}).status_code,200)
        events=self.client.get(path+'/events').json()
        self.assertEqual([e['action'] for e in events],['created','pending → confirmed','confirmed → preparing','preparing → ready','paid','ready → completed'])
        self.assertEqual(events[-1]['actor'],'shoptest')
        self.assertEqual(self.client.get('/api/admin/stats').json()['collected_today'],65000)

    def test_cash_statistics_use_payment_date_and_idempotent_audit(self):
        o=self.order();self.login();path='/api/admin/orders/'+o['code']
        with mod.db() as c:c.execute("UPDATE orders SET created_at='2020-01-01T12:00:00+07:00'")
        self.client.patch(path+'/status',json={'status':'confirmed'})
        self.client.patch(path+'/payment',json={'paid':True})
        before=self.client.get('/api/admin/orders').json()[0]['paid_at']
        self.client.patch(path+'/payment',json={'paid':True})
        self.assertEqual(self.client.get('/api/admin/orders').json()[0]['paid_at'],before)
        stats=self.client.get('/api/admin/stats').json()
        self.assertEqual(stats['orders'],0);self.assertEqual(stats['collected_today'],65000)
        events=self.client.get(path+'/events').json()
        self.assertEqual(sum(e['action']=='paid' for e in events),1)

    def test_upgrade_existing_database_preserves_rows(self):
        o=self.order()
        with mod.db() as c:
            c.execute('ALTER TABLE orders DROP COLUMN updated_at')
            c.execute('ALTER TABLE orders DROP COLUMN paid_at')
            c.execute('DROP TABLE order_events');c.execute('DROP TABLE trial_sessions')
        mod.init_db();mod.init_db()
        got=self.client.get('/api/orders/'+o['code'],headers={'Authorization':'Bearer '+o['token']}).json()
        self.assertEqual(got['total'],65000);self.assertIsNone(got['paid_at'])

    def test_trial_has_future_slots_even_at_night_but_respects_pause(self):
        from datetime import datetime
        self.slots.stop()
        token=mod.TRIAL_ID.set('test')
        try:
            shop={'opens':'08:00','closes':'20:00','accepting':True}
            slots=mod.options(shop,datetime(2026,11,8,23,50,tzinfo=mod.TZ))
            self.assertEqual(slots[0]['id'],'2026-11-09T08:00:00+07:00')
            shop['accepting']=False
            self.assertEqual(mod.options(shop),[])
        finally:mod.TRIAL_ID.reset(token)

    def test_pickup_required_and_stored(self):
        p=self.payload();p.pop('pickup')
        self.assertEqual(self.client.post('/api/orders',json=p).status_code,422)
        p=self.payload();p['pickup']='  '
        self.assertEqual(self.client.post('/api/orders',json=p).status_code,422)
        p=self.payload();p['pickup']='Cổng trường VJU, bàn bảo vệ'
        self.assertEqual(self.order(p)['pickup'],p['pickup'])

    def test_customer_trial_has_no_admin_privileges(self):
        r=self.client.post('/api/trial/login',json={'username':'tester','password':mod.TRIAL_PASSWORD})
        self.assertEqual(r.status_code,200)
        self.assertEqual(self.client.get('/api/admin/orders').status_code,401)
        self.assertEqual(self.client.get('/api/admin/me').status_code,401)
        self.order()
        self.assertEqual(self.client.post('/api/admin/login',json={'username':'tester','password':mod.TRIAL_PASSWORD}).status_code,401)
        self.client.post('/api/trial/logout',json={})
        self.assertEqual(self.client.post('/api/admin/login',json={'username':'shoptest','password':mod.SHOP_TRIAL_PASSWORD}).status_code,401)

    def test_student_hours_and_every_quarter_hour(self):
        from datetime import datetime
        self.slots.stop()
        shop={'opens':'10:00','closes':'22:00','accepting':True}
        slots=mod.options(shop,datetime(2026,11,8,9,0,tzinfo=mod.TZ))
        self.assertEqual(len(slots),98)
        self.assertEqual(slots[0]['id'],'2026-11-08T10:00:00+07:00')
        self.assertEqual(slots[1]['id'],'2026-11-08T10:15:00+07:00')
        self.assertEqual(slots[48]['id'],'2026-11-08T22:00:00+07:00')
        late=mod.options(shop,datetime(2026,11,8,21,50,tzinfo=mod.TZ))
        self.assertEqual(len(late),49)
        self.assertTrue(all(x['id'].startswith('2026-11-09') for x in late))

    def test_customer_registration_login_and_order_history(self):
        r=self.client.post('/api/customer/register',json={'name':'Nguyễn Minh Anh','phone':'0900000000','password':'SecurePass2026!'})
        self.assertEqual(r.status_code,201,r.text)
        self.assertNotIn('password',r.json())
        self.assertIn('HttpOnly',r.headers['set-cookie'])
        self.assertIn('SameSite=strict',r.headers['set-cookie'])
        self.assertEqual(r.json()['phone'],'0900000000')
        session=self.client.get('/api/session').json()
        self.assertEqual(session['customer_name'],'Nguyễn Minh Anh')
        order=self.order()
        owned=self.client.get('/api/customer/orders')
        self.assertEqual(owned.status_code,200)
        self.assertEqual([x['code'] for x in owned.json()],[order['code']])
        self.assertNotIn('token',owned.text)
        self.assertEqual(self.client.get('/api/customer/me').json()['name'],'Nguyễn Minh Anh')
        self.assertEqual(self.client.post('/api/customer/logout',json={}).status_code,403)
        self.client.headers['X-CSRF-Token']=r.json()['csrf']
        self.assertEqual(self.client.post('/api/customer/logout',json={}).status_code,200)
        self.assertEqual(self.client.get('/api/customer/orders').status_code,401)
        self.assertIsNone(self.client.get('/api/session').json()['customer_id'])
        again=self.client.post('/api/customer/login',json={'phone':'0900000000','password':'SecurePass2026!'})
        self.assertEqual(again.status_code,200,again.text)
        self.assertEqual(self.client.get('/api/customer/orders').json()[0]['code'],order['code'])

    def test_customer_registration_validation_and_duplicate_phone(self):
        url='/api/customer/register'
        self.assertEqual(self.client.post(url,json={'name':'A','phone':'0900000000','password':'SecurePass2026!'}).status_code,422)
        self.assertEqual(self.client.post(url,json={'name':'Minh Anh','phone':'bad','password':'SecurePass2026!'}).status_code,422)
        self.assertEqual(self.client.post(url,json={'name':'Minh Anh','phone':'0900000000','password':'short'}).status_code,422)
        body={'name':'Minh Anh','phone':'0900000000','password':'SecurePass2026!'}
        self.assertEqual(self.client.post(url,json=body).status_code,201)
        self.assertEqual(self.client.post(url,json=body).status_code,409)
        with mod.db() as c:
            row=c.execute('SELECT salt,hash FROM customers WHERE phone=?',(body['phone'],)).fetchone()
            self.assertNotEqual(row['hash'],body['password'])
            self.assertGreaterEqual(len(row['hash']),64)
        self.assertEqual(self.client.post('/api/customer/login',json={'phone':'0900000000','password':'incorrect'}).status_code,401)
        self.assertEqual(self.client.post('/api/customer/login',json={'phone':'0999999999','password':'incorrect'}).status_code,401)

    def test_customer_account_isolation_and_phone_binding(self):
        first=self.client.post('/api/customer/register',json={'name':'Khách Một','phone':'0900000000','password':'FirstSecure2026!'})
        self.assertEqual(first.status_code,201)
        own_order=self.order()
        self.client.headers['X-CSRF-Token']=first.json()['csrf']
        self.assertEqual(self.client.post('/api/customer/logout',json={}).status_code,200)
        second=self.client.post('/api/customer/register',json={'name':'Khách Hai','phone':'0911111111','password':'SecondSecure2026!'})
        self.assertEqual(second.status_code,201)
        self.assertEqual(self.client.get('/api/customer/orders').json(),[])
        self.assertEqual(self.client.post('/api/orders',json=self.payload()).status_code,422)
        self.client.headers['X-CSRF-Token']=second.json()['csrf']
        self.assertEqual(self.client.post('/api/customer/orders/claim',json={'code':own_order['code'],'token':own_order['token']}).status_code,409)
        data=self.payload();data['phone']='0911111111'
        order2=self.order(data)
        self.assertEqual([x['code'] for x in self.client.get('/api/customer/orders').json()],[order2['code']])
        self.assertNotEqual(order2['code'],own_order['code'])

    def test_guest_order_claim_requires_secret_and_csrf(self):
        guest=self.order()
        r=self.client.post('/api/customer/register',json={'name':'Hà My','phone':'0900000000','password':'SecurePass2026!'})
        self.assertEqual(r.status_code,201)
        self.assertEqual(self.client.get('/api/customer/orders').json(),[])
        path='/api/customer/orders/claim'
        self.assertEqual(self.client.post(path,json={'code':guest['code'],'token':'bad-token-0123456789'}).status_code,403)
        self.client.headers['X-CSRF-Token']=r.json()['csrf']
        self.assertEqual(self.client.post(path,json={'code':guest['code'],'token':'wrong-token-0123456789'}).status_code,404)
        self.assertEqual(self.client.post(path,json={'code':guest['code'],'token':guest['token']}).status_code,200)
        self.assertEqual(self.client.post(path,json={'code':guest['code'],'token':guest['token']}).status_code,200)
        self.assertEqual([x['code'] for x in self.client.get('/api/customer/orders').json()],[guest['code']])

    def test_customer_history_from_another_browser(self):
        body={'name':'Minh Anh','phone':'0900000000','password':'SecurePass2026!'}
        self.assertEqual(self.client.post('/api/customer/register',json=body).status_code,201)
        code=self.order()['code']
        with TestClient(mod.app) as other:
            other.headers['X-VJU-Request']='1'
            self.assertEqual(other.get('/api/customer/orders').status_code,401)
            login=other.post('/api/customer/login',json={'phone':body['phone'],'password':body['password']})
            self.assertEqual(login.status_code,200,login.text)
            history=other.get('/api/customer/orders')
            self.assertEqual(history.status_code,200)
            self.assertEqual([x['code'] for x in history.json()],[code])
            self.assertNotIn('lookup_hash',history.text)
            self.assertNotIn('token',history.text)

    def test_checkout_session_guard_rejects_stale_tabs(self):
        # A page loaded while signed out must not silently order under a new account.
        p = self.payload()
        signed_in = self.client.post('/api/customer/register', json={
            'name': 'Minh Anh', 'phone': '0900000000', 'password': 'SecurePass2026!'
        })
        self.assertEqual(signed_in.status_code, 201)
        csrf = signed_in.json()['csrf']
        self.assertEqual(self.client.post('/api/orders', json=p,
                         headers={'X-VJU-Checkout-Session': 'guest'}).status_code, 409)
        self.assertEqual(self.client.post('/api/orders', json=p,
                         headers={'X-VJU-Checkout-Session': 'customer:' + csrf}).status_code, 201)
        self.client.headers['X-CSRF-Token'] = csrf
        self.assertEqual(self.client.post('/api/customer/logout', json={}).status_code, 200)
        stale = self.payload()
        r = self.client.post('/api/orders', json=stale,
                             headers={'X-VJU-Checkout-Session': 'customer:' + csrf})
        self.assertEqual(r.status_code, 409)
        self.assertIn('Phiên đăng nhập', r.json()['detail'])
        with mod.db() as c:
            self.assertEqual(c.execute('SELECT COUNT(*) FROM orders').fetchone()[0], 1)
        self.assertEqual(self.client.post('/api/orders', json=stale,
                         headers={'X-VJU-Checkout-Session': 'guest'}).status_code, 201)

    def test_checkout_guard_detects_account_switch_and_login_refresh(self):
        first = self.client.post('/api/customer/register', json={
            'name': 'Khách Một', 'phone': '0900000000', 'password': 'FirstSecure2026!'
        }).json()
        self.client.headers['X-CSRF-Token'] = first['csrf']
        self.assertEqual(self.client.post('/api/customer/logout', json={}).status_code, 200)
        second = self.client.post('/api/customer/register', json={
            'name': 'Khách Hai', 'phone': '0911111111', 'password': 'SecondSecure2026!'
        }).json()
        p = self.payload()
        p['phone'] = '0911111111'
        self.assertEqual(self.client.post('/api/orders', json=p, headers={
            'X-VJU-Checkout-Session': 'customer:' + first['csrf']
        }).status_code, 409)
        self.assertEqual(self.client.post('/api/orders', json=p, headers={
            'X-VJU-Checkout-Session': 'customer:' + second['csrf']
        }).status_code, 201)

    def test_customer_demo_isolation_and_expired_sessions(self):
        self.assertEqual(self.client.get('/api/customer/orders').status_code,401)
        login=self.client.post('/api/trial/login',json={'username':'demo','password':mod.TRIAL_PASSWORD})
        self.assertEqual(login.status_code,200)
        data={'name':'Minh Anh','phone':'0900000000','password':'SecurePass2026!'}
        self.assertEqual(self.client.post('/api/customer/register',json=data).status_code,409)
        self.assertEqual(self.client.post('/api/customer/login',json={'phone':data['phone'],'password':data['password']}).status_code,409)
        self.assertEqual(self.client.get('/api/customer/orders').status_code,409)
        self.client.post('/api/trial/logout',json={})
        self.assertEqual(self.client.post('/api/customer/register',json=data).status_code,201)
        with mod.db() as c: c.execute('UPDATE customer_sessions SET expires=0')
        self.assertEqual(self.client.get('/api/customer/me').status_code,401)
        self.assertEqual(self.client.get('/api/customer/orders').status_code,401)

if __name__=='__main__':unittest.main()
