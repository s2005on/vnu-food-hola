# Verification — 10/11/2026

## Executed

- `python -m unittest discover -s tests -p test_server.py -v`: 17 tests passed.
- `node --check server/web/app.js` and `node --check server/web/admin.js`: passed.
- Browser, customer flow against FastAPI preview:
  - Menu loaded from API, 8 seed dishes.
  - Added chicken rice + grilled pork noodles, total 65,000 VND.
  - Submitted test name/phone and available pickup slot.
  - Order created in SQLite and displayed with pending/unpaid state, correct item details/total.
  - Navigated away to admin login and back; order was fetched from the server again successfully.
  - Admin login screen rendered; authenticated admin UI was not exercised in browser.
- API tests cover auth, CSRF, server pricing, input rejection, sold-out/hidden dishes, duplicate item rejection,
  retry keys including concurrent retry, lookup authorization, snapshot preservation, status transitions,
  payment gate, cancellation, session logout, login throttling, shop hours, creation of dishes, backup restore.

## Environment

Python 3.12, FastAPI 0.141.1, Pydantic 2.13.4, Uvicorn 0.52.1, HTTPX 0.28.1.
The test runner reports a Starlette deprecation warning for HTTPX; it did not fail tests.
Requirements use bounded compatible major versions; future dependency changes must rerun tests.

## Not yet verified

- Windows batch launcher on the user's Windows machine.
- VPS systemd, HTTPS cookie, and Nginx path integration on SV21.
- Authenticated admin browser interactions, mobile browser layout, real shop workflow and load testing.
- CI file has been prepared, not pushed/run on GitHub by this session.

No claim that this version is deployed on the user's VPS or ready for real customer data.

## AI assistance

Backend, frontend wiring, administration pages, tests and instructions were generated with AI assistance.
The student should read and understand the create-order transaction, server-side totals, lookup authorization,
admin session/CSRF checks and order-status rules before presentation or real use.
