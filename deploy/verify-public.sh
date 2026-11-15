#!/usr/bin/env bash
# Read-only smoke test: never creates orders or logs into admin.
set -euo pipefail
BASE="${1:-https://sv21.bcse-vju.com/b1-23110216/v3/}"
BASE="${BASE%/}/"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
curl --fail --silent --show-error --location --max-time 25 "${BASE}api/health" > "$TMP/health.json"
python3 - "$TMP/health.json" <<'CHECK'
import json,sys
assert json.load(open(sys.argv[1])) == {'ok':True}, 'Unexpected health response'
CHECK
curl --fail --silent --show-error --location --max-time 25 "${BASE}api/menu" > "$TMP/menu.json"
python3 - "$TMP/menu.json" <<'CHECK'
import json,sys
x=json.load(open(sys.argv[1]))
assert isinstance(x.get('dishes'),list), 'Menu response missing dishes'
print('Menu API OK; dishes:',len(x['dishes']))
CHECK
curl --fail --silent --show-error --location --max-time 25 "$BASE" > "$TMP/index.html"
python3 - "$TMP/index.html" <<'CHECK'
import sys
s=open(sys.argv[1]).read().lower()
assert '<html' in s and 'app.js' in s and 'vju' in s, 'Unexpected application page'
CHECK
printf 'Public smoke checks passed: %s\nStill verify customer/admin flow in a browser.\n' "$BASE"
