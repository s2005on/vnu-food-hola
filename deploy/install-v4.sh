#!/usr/bin/env bash
# Update the existing student VPS service; preserve its DB and Nginx routes.
set -euo pipefail
cd "$(dirname "$0")/.."
SOURCE="$PWD"
SERVICE=vju-food-23110216.service
DB_PATH=/home/student/vju-food-data/food.sqlite3
[[ "$(id -un)" == student ]] || { echo 'Run as student, not sudo/root.'; exit 1; }
[[ -f "$DB_PATH" ]] || { echo 'Existing database not found. Stopped without creating another database.'; exit 1; }
ENVIRONMENT=$(systemctl show "$SERVICE" -p Environment --value)
[[ "$ENVIRONMENT" == *"VJU_DB=$DB_PATH"* ]] || { echo 'Service uses a different database. Stopped for review.'; exit 1; }
[[ "$ENVIRONMENT" == *'VJU_BASE_PATH=/b1-23110216/v3/'* ]] || { echo 'Unexpected URL prefix. Stopped for review.'; exit 1; }
STAMP=$(date -u +%Y%m%dT%H%M%S)-$$
RELEASE="/home/student/projects/vju-food-releases/$STAMP"
BACKUP_DIR="/home/student/vju-food-data/backups/$STAMP"
DROPIN=/etc/systemd/system/vju-food-23110216.service.d/90-v4-release.conf
umask 077
mkdir -p "$RELEASE" "$BACKUP_DIR"
cp -a "$SOURCE/server" "$RELEASE/server"
# Source packages should never contain runtime data; leave the main DB untouched.
if [[ -d "$RELEASE/server/data" ]]; then
  echo 'Source contains runtime data. Remove it from the source package before deploying.'
  exit 1
fi
cp -a "$SOURCE/tests" "$RELEASE/tests"
python3 -m venv "$RELEASE/.venv-vju"
"$RELEASE/.venv-vju/bin/python" -m pip install -r "$RELEASE/server/requirements-test.txt"
(cd "$RELEASE" && "$RELEASE/.venv-vju/bin/python" -m unittest discover -s tests -p test_server.py -q)
VJU_DB="$DB_PATH" "$RELEASE/.venv-vju/bin/python" -m server.manage backup --output "$BACKUP_DIR/food.sqlite3"
# Only replace this release's own drop-in. Other service settings remain intact.
HAD_OVERRIDE=0
if sudo test -f "$DROPIN"; then
  sudo cp "$DROPIN" "$BACKUP_DIR/previous-release.conf"
  HAD_OVERRIDE=1
fi
systemctl cat "$SERVICE" > "$BACKUP_DIR/service-before.txt"
sudo mkdir -p "$(dirname "$DROPIN")"
sudo tee "$DROPIN" >/dev/null <<EOF
[Service]
WorkingDirectory=$RELEASE
ExecStart=
ExecStart=$RELEASE/.venv-vju/bin/python -m uvicorn server.app:app --host 127.0.0.1 --port 8016 --workers 1 --proxy-headers --forwarded-allow-ips=127.0.0.1
EOF
rollback() {
  echo 'Restart/health failed. Restoring previous service configuration.'
  if [[ "$HAD_OVERRIDE" == 1 ]]; then sudo cp "$BACKUP_DIR/previous-release.conf" "$DROPIN"; else sudo rm -f "$DROPIN"; fi
  sudo systemctl daemon-reload
  sudo systemctl restart "$SERVICE" || true
  echo "Database backup: $BACKUP_DIR/food.sqlite3 (not automatically restored; additive schema only)."
}
sudo systemctl daemon-reload
if ! sudo systemctl restart "$SERVICE"; then rollback; exit 1; fi
OK=0
for attempt in {1..15}; do
  if curl -fsS http://127.0.0.1:8016/api/session | "$RELEASE/.venv-vju/bin/python" -c 'import sys,json; x=json.load(sys.stdin); assert x["trial_enabled"] and not x["trial"]' 2>/dev/null; then OK=1; break; fi
  sleep 1
done
if [[ "$OK" != 1 ]]; then rollback; exit 1; fi
printf '\nV5 backend is running. Release: %s\nBackup: %s\n' "$RELEASE" "$BACKUP_DIR/food.sqlite3"
printf 'Open HTTPS /b1-23110216/v3/login.html and complete the trial flow. Nginx was not changed.\n'
