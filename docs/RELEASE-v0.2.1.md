# VNU Food Hola v0.2.1

Bản cập nhật giao diện và tài liệu cho Academic MVP v0.2.0.

## Thay đổi

- Giữ thanh Thực đơn, Đơn của tôi và Giỏ hàng ở đầu màn hình khi cuộn.
- Điều chỉnh khoảng cuộn theo chiều cao thanh điều hướng, kể cả khi tên tài khoản hoặc kích thước màn hình thay đổi.
- Ngăn giao diện mới tạo đơn sai tài khoản khi phiên đăng nhập thay đổi ở tab khác (API trả HTTP 409).
- Rút gọn README, quy ước Git và tài liệu phiên bản; sửa thông tin lỗi thời về v0.2.0.
- Tập trung kết quả kiểm thử và các vấn đề còn mở tại [VERIFICATION.md](../VERIFICATION.md).

## Kiểm thử và nâng cấp

46 kiểm thử Python và 15 kiểm thử JavaScript đạt trong lượt rà soát ngày 16/11/2026. JavaScript vượt kiểm tra cú pháp; script triển khai vượt kiểm tra cú pháp Bash. Kiểm thử trực quan trên điện thoại chưa hoàn tất.

Không thay đổi API, schema SQLite hay dependencies. Các file giao diện thay đổi: `server/web/index.html`, `server/web/customer.css`, `server/web/customer-header.js`. Cập nhật đủ ba file và tải lại trình duyệt để nhận giao diện mới.

## Vấn đề còn mở

Nếu đăng xuất ở tab khác, tab đặt món cũ có thể gửi đơn dưới dạng khách vãng lai. Đơn đó không tự xuất hiện trong lịch sử tài khoản. Chi tiết tái hiện và các giới hạn vận hành nằm tại [VERIFICATION.md](../VERIFICATION.md).

Trạng thái tag và công bố được thể hiện tại [GitHub Releases](https://github.com/s2005on/vnu-food-hola/releases); tài liệu này không xác nhận phiên bản đang chạy trên VPS.
