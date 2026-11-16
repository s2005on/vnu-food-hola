# Changelog

## v0.2.1

- Giữ thanh điều hướng khách hàng khi cuộn; tự điều chỉnh khoảng cuộn theo chiều cao header.
- Rút gọn tài liệu và cập nhật thông tin v0.2.0 đã phát hành.
- Bổ sung kiểm tra phiên khi đặt món, ngăn đơn bị tạo sai tài khoản sau khi đăng xuất/đổi phiên ở tab khác (HTTP 409).
- Thêm kiểm thử hồi quy checkout, tổng hợp giới hạn tại [VERIFICATION.md](VERIFICATION.md).
- Không thay đổi schema SQLite hoặc dependencies.

[Ghi chú phiên bản](docs/RELEASE-v0.2.1.md).

## v0.2.0 — 16/11/2026

- Backend FastAPI, SQLite; đặt món, tra cứu đơn và quản trị quán.
- Tài khoản khách và lịch sử đơn trên nhiều thiết bị.
- Thực đơn 16 món mẫu, giỏ hàng, quản lý trạng thái và thanh toán tiền mặt.
- Bổ sung hồ sơ bàn giao và ảnh minh chứng SV27 ngày 15/11/2026.

[GitHub Release](https://github.com/s2005on/vnu-food-hola/releases/tag/v0.2.0).

## v0.1.0 — 31/10/2026

- Tài liệu Sprint 1 và demo tĩnh; chưa có backend hoặc database.

[Git tag](https://github.com/s2005on/vnu-food-hola/tree/v0.1.0).

B2–B7 và V2–V7.3 là mốc học phần/phát triển nội bộ; xem [quy ước phiên bản](docs/VERSIONING.md).
