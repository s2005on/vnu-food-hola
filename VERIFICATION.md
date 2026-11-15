# Xác minh bản sửa giữa kỳ - 15/11/2026

Nguồn: main tại b2fce97027dc61bd73a4ce6fab71488ffbe3f738 (PR #10 đã merge).
Kết quả dưới đây chạy trên bản sửa cục bộ; không thay thế kết quả CI của commit mới hoặc nghiệm thu VPS.

## Đã chạy trong lần sửa này

- Python 3.12.14/Linux; FastAPI 0.163.1, Pydantic 2.14.3, Uvicorn 0.54.0, HTTPX 0.28.1.
- `python -m unittest discover -s tests -p test_server.py -v`: **40/40 đạt**.
- `node --test tests/customer-refresh.test.cjs tests/cart-drawer.test.cjs tests/menu-cards.test.cjs`: **11/11 đạt**, Node 24.22.1.
- `node --check` cho app.js, admin.js, account.js, cart-drawer.js: đạt.
- `bash -n deploy/install-v4.sh deploy/verify-public.sh`: đạt.
- Smoke test HTTP cục bộ với database tạm và VJU_TRIAL_ENABLED=0: health, API menu 16 món và trang ứng dụng đạt.
- `git diff --check`: đạt.

Log backend và JavaScript: docs/evidence/midterm-backend.txt và midterm-javascript.txt.
Kiểm thử backend bao gồm giá, quyền tra cứu, admin/CSRF, chống trùng, chuyển trạng thái,
thu tiền, sao lưu, phiên demo/khách và nâng cấp database giữ dữ liệu tùy chỉnh.

## Cập nhật trạng thái GitHub sau merge — 15/11/2026

- [PR #11](https://github.com/s2005on/vnu-food-hola/pull/11) đã merge vào `main` (commit `d3b1f0a`).
- CI trên HEAD của PR #11 đã đạt ở cả Ubuntu/Python 3.12 và Windows/Python 3.14. Đây là kết quả CI, **không phải** bằng chứng deploy VPS hay kiểm tra giao diện Windows tương tác.
- Các phát biểu “chưa push/chưa CI” ở những đoạn bên dưới ghi lại tình trạng **khi soạn bản sửa ban đầu**, không phản ánh trạng thái GitHub sau merge.

## Thay đổi CI

CI trước chỉ chạy customer-refresh.test.cjs. Bản sửa chạy thêm cart-drawer.test.cjs,
menu-cards.test.cjs và kiểm tra Bash/cú pháp cart-drawer.js; cho phép chạy thủ công.
Chưa đẩy bản sửa nên chưa có lượt CI mới. CI xanh trong ảnh trước thuộc bản V7.3 cũ.

## Chưa xác minh hoặc chưa thực hiện

- Windows và trình duyệt tương tác trong lần sửa này; không có kết quả QA trực quan mới.
- Chưa áp dụng installer/systemd/Nginx trên VPS thật.
- URL VPS công khai trả 403 từ môi trường kiểm tra; chưa xác định nguyên nhân hay kết luận website ngừng hoạt động với mọi người.
- Chưa quay demo khách-quán trên HTTPS, điện thoại hoặc thử với quán thật.
- Chưa merge/đóng PR #2-#8 và chưa push bản sửa giữa kỳ.

Thực hiện bảng kiểm docs/MIDTERM.md, ghi ngày/commit/bằng chứng thực tế trước khi đánh dấu hoàn tất.
Mã và tài liệu có AI hỗ trợ; người thực hiện cần hiểu và tự trình bày các luồng chính.
