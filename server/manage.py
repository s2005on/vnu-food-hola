import argparse, getpass, secrets, sqlite3
from pathlib import Path
from server.app import db, password_hash, DB
parser=argparse.ArgumentParser()
parser.add_argument('command',choices=['admin','backup'])
parser.add_argument('--username',default='son')
parser.add_argument('--output')
a=parser.parse_args()
if a.command=='admin':
    password=getpass.getpass('Mat khau moi (toi thieu 12 ky tu): ')
    if len(password)<12 or len(password)>128: raise SystemExit('Can 12-128 ky tu.')
    if password!=getpass.getpass('Nhap lai: '): raise SystemExit('Khong khop.')
    salt=secrets.token_hex(16)
    with db() as c:
        c.execute('INSERT INTO admins VALUES(?,?,?) ON CONFLICT(username) DO UPDATE SET salt=excluded.salt, hash=excluded.hash',(a.username,salt,password_hash(password,salt)))
        c.execute('DELETE FROM sessions WHERE username=?',(a.username,))
    print('Da tao/cap nhat tai khoan:',a.username)
else:
    if not a.output: raise SystemExit('Can --output duong-dan-sao-luu.sqlite3')
    target=Path(a.output)
    if target.exists(): raise SystemExit('File dich da ton tai; chon ten moi.')
    target.parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(DB) as src, sqlite3.connect(target) as dest: src.backup(dest)
    try: target.chmod(0o600)
    except OSError: pass
    print('Da sao luu:',target)
