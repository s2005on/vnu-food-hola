# VNU Food Hola v0.2.1

Bản cập nhật giao diện và tài liệu cho Academic MVP v0.2.0.

## Thay đổi

- Giữ thanh Thực đơn, Đơn của tôi và Giỏ hàng ở đầu màn hình khi cuộn.
- Điều chỉnh khoảng cuộn theo chiều cao thanh điều hướng, kể cả khi tên tài khoản hoặc kích thước màn hình thay đổi.
- Ngăn giao diện mới tạo đơn sai tài khoản khi phiên đăng nhập thay đổi ở tab khác (API trả HTTP 409).
- Rút gọn README, quy ước Git và tài liệu phiên bản; sửa thông tin lỗi thời về v0.2.0.
- Tập trung kết quả kiểm thử và các vấn đề còn mở tại [VERIFICATION.md](../VERIFICATION.md).

## Kiểm thử và nâng cấp

Đã bổ sung kiểm thử hồi quy Python và JavaScript cho checkout. Xem GitHub Actions trên PR #17 để biết kết quả lượt kiểm tra cuối. Kiểm thử trực quan trên điện thoại chưa hoàn tất.

Không thay đổi schema SQLite hay dependencies. Thay đổi API tương thích ngược: client mới gửi `X-VJU-Checkout-Session` để server từ chối gửi đơn khi phiên thay đổi (HTTP 409); client cũ không gửi header vẫn hoạt động. Các file thay đổi gồm `server/app.py`, `server/web/app.js`, `server/web/index.html`, `server/web/customer.css`, `server/web/customer-header.js` và các bài kiểm thử.

## Giới hạn còn lại

Chưa xác nhận giao diện mobile, đa tab trong trình duyệt thực, backup restore hoặc VPS đã triển khai bản này. Xem [VERIFICATION.md](../VERIFICATION.md).

Trạng thái tag và công bố được thể hiện tại [GitHub Releases](https://github.com/s2005on/vnu-food-hola/releases); tài liệu này không xác nhận phiên bản đang chạy trên VPS.
