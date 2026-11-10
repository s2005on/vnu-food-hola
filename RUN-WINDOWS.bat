@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Can cai Python 3.11 hoac 3.12 tu python.org, sau do mo lai tep nay.
  pause
  exit /b 1
)
if not exist ".venv-vju\Scripts\python.exe" (
  py -3 -m venv .venv-vju
  if errorlevel 1 goto error
)
.venv-vju\Scripts\python.exe -m pip install -r server\requirements.txt
if errorlevel 1 goto error
set VJU_COOKIE_SECURE=0
set VJU_BASE_PATH=/
set VJU_DB=%~dp0server\data\food.sqlite3
.venv-vju\Scripts\python.exe -c "from server.app import db; c=db(); x=c.__enter__(); found=x.execute('SELECT 1 FROM admins LIMIT 1').fetchone(); c.__exit__(None,None,None); raise SystemExit(0 if found else 2)"
if errorlevel 1 (
  echo Tao tai khoan quan tri son. Khi go mat khau se khong hien ky tu.
  .venv-vju\Scripts\python.exe -m server.manage admin --username son
  if errorlevel 1 goto error
)
echo.
echo Trang khach: http://127.0.0.1:8016/
echo Quan tri:    http://127.0.0.1:8016/admin.html
echo Giu cua so nay mo khi dung web. Ctrl+C de dung.
.venv-vju\Scripts\python.exe -m uvicorn server.app:app --host 127.0.0.1 --port 8016 --workers 1
if errorlevel 1 goto error
exit /b 0
:error
echo.
echo Chua khoi dong duoc. Chup thong bao loi o tren de kiem tra.
pause
exit /b 1
