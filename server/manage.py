"""Create an administrator or make a private, consistent SQLite backup."""
import argparse
from contextlib import closing
import getpass
import os
from pathlib import Path
import secrets
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('command', choices=['admin', 'backup'])
parser.add_argument('--username', default='son')
parser.add_argument('--output')
a = parser.parse_args()

if a.command == 'backup':
    # app startup seeds missing DBs; never import it for a backup operation.
    source = Path(os.environ.get('VJU_DB', str(Path(__file__).parent / 'data' / 'food.sqlite3')))
    if not source.is_file():
        raise SystemExit('Khong tim thay CSDL. Kiem tra VJU_DB; khong tao du lieu moi.')
    if not a.output:
        raise SystemExit('Can --output duong-dan-sao-luu.sqlite3')
    target = Path(a.output)
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        fd = os.open(target, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise SystemExit('File dich da ton tai; chon ten moi.')
    os.close(fd)
    try:
        with closing(sqlite3.connect(source.resolve().as_uri() + '?mode=ro', uri=True)) as src:
            with closing(sqlite3.connect(target)) as dest:
                src.backup(dest)
                if dest.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                    raise RuntimeError('Ban sao khong vuot qua kiem tra SQLite.')
    except Exception:
        target.unlink(missing_ok=True)
        raise
    print('Da sao luu:', target)
else:
    from server.app import db, password_hash
    username = a.username.strip()
    if not username or len(username) > 100:
        raise SystemExit('Ten dang nhap can 1-100 ky tu.')
    password = getpass.getpass('Mat khau moi (toi thieu 6 ky tu): ')
    if len(password) < 6 or len(password) > 128:
        raise SystemExit('Can 6-128 ky tu.')
    if password != getpass.getpass('Nhap lai: '):
        raise SystemExit('Khong khop.')
    salt = secrets.token_hex(16)
    with db() as c:
        c.execute('INSERT INTO admins VALUES(?,?,?) ON CONFLICT(username) DO UPDATE SET salt=excluded.salt, hash=excluded.hash',
                  (username, salt, password_hash(password, salt)))
        c.execute('DELETE FROM sessions WHERE username=?', (username,))
    print('Da tao/cap nhat tai khoan:', username)
