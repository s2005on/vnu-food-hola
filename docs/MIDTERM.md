# Hồ sơ nghiệm thu giữa kỳ

**Dự án:** VNU Food Hola · **Học phần:** CSE3045  
**Ngày cập nhật:** 15/11/2026

## Trạng thái hiện tại

| Hạng mục | Kết quả |
|---|---|
| MVP V7.3 | Đã merge qua [PR #10](https://github.com/s2005on/vnu-food-hola/pull/10) |
| Tài khoản khách | Đã merge qua [PR #14](https://github.com/s2005on/vnu-food-hola/pull/14), commit ứng dụng `0eba90e` |
| Hồ sơ và CI | [PR #15](https://github.com/s2005on/vnu-food-hola/pull/15) đã merge; CI Ubuntu và Windows đạt |
| Hosting | Đã quan sát website trên [SV27](https://sv27.bcse-vju.com/) qua HTTPS ngày 15/11/2026; phụ thuộc block VPS |
| Luồng khách–quán | Đã quan sát ảnh: khách xem đơn → quản trị xử lý → khách thấy Hoàn thành/Đã thanh toán |
| Release | Chưa tạo tag `v0.2.0` |

## Bảng kiểm nghiệm thu

| ID | Kiểm tra | Kết quả |
|---|---|---|
| M01 | Mở website HTTPS, tải thực đơn | **Đạt theo ảnh**: trang 16 món hiển thị trên SV27. Chưa kiểm tra độc lập từ mạng ngoài |
| M02 | Khách đặt đơn hợp lệ, tổng tiền đúng, quản trị nhìn thấy | **Đạt theo ảnh**: đơn thử 2 món, tổng 65.000đ; mã đơn đã che |
| M03 | Quản trị cập nhật trạng thái và khách nhận kết quả | **Đạt theo ảnh**: `pending → confirmed → preparing → ready → paid → completed`; thao tác thanh toán chỉ là mô phỏng |
| M04 | Tải lại trang/khởi động lại và xác nhận đơn còn nguyên | Chưa kiểm thử thủ công trên VPS |
| M05 | Sai số điện thoại hoặc thiếu địa điểm nhận | Chưa kiểm thử thủ công trên hosting |
| M06 | Món hết/ẩn hoặc giá thay đổi | Chưa kiểm thử thủ công trên hosting |
| M07 | Gửi lại cùng yêu cầu, không tạo đơn trùng | Có kiểm thử tự động; chưa kiểm thử thủ công trên hosting |
| M08 | Chọn giờ nhận không hợp lệ | Có kiểm thử tự động; chưa kiểm thử thủ công trên hosting |
| M09 | Gọi API quản trị khi chưa đăng nhập | Có kiểm thử tự động; chưa kiểm thử thủ công trên hosting |
| M10 | Phiên demo tách khỏi dữ liệu quán | Có kiểm thử tự động; chưa kiểm thử thủ công trên hosting |
| M11 | Kiểm tra giao diện trên điện thoại | Chưa thực hiện |
| M12 | Sao lưu SQLite và kiểm tra tính toàn vẹn | **Đạt integrity check**: SQLite trả `ok`; chưa thử khôi phục backup |

## Kiểm tra tài khoản khách

| ID | Kiểm tra | Kết quả |
|---|---|---|
| A01 | Đăng nhập khách và hiển thị khu vực tài khoản | Đã quan sát trên SV27 |
| A02 | Xem lịch sử và nhận trạng thái đơn từ quản trị | Đạt theo ảnh: Chờ xác nhận, Sẵn sàng nhận và Hoàn thành |
| A03 | Đăng nhập lại trên trình duyệt/thiết bị khác | Chưa kiểm thử thủ công |
| A04 | Tài khoản B không xem được đơn của tài khoản A | Có kiểm thử tự động; chưa kiểm thử thủ công trên hosting |
| A05 | Số điện thoại trùng, mật khẩu sai, đăng xuất và cookie HTTPS | Chưa kiểm thử đủ trên hosting |

## Bộ minh chứng SV27

Ảnh được lưu trong [`docs/evidence/sv27-2026-11-15/`](evidence/sv27-2026-11-15/README.md). Thông tin nhận dạng khách, mã đơn và tên đăng nhập quản trị đã được che.

- [01 — Trang thực đơn](evidence/sv27-2026-11-15/01-sv27-homepage.jpg)
- [02 — Lịch sử đơn Chờ xác nhận](evidence/sv27-2026-11-15/02-customer-order-pending.jpg)
- [03 — Quản trị: Sẵn sàng nhận](evidence/sv27-2026-11-15/03-admin-order-ready.jpg)
- [04 — Nhật ký chuyển trạng thái](evidence/sv27-2026-11-15/04-order-audit-log.jpg)
- [05 — Khách thấy Hoàn thành/Đã thanh toán](evidence/sv27-2026-11-15/05-customer-order-completed.jpg)
- [06 — 46 kiểm thử, service và health](evidence/sv27-2026-11-15/06-vps-tests-health.jpg)
- [07 — Backup SQLite integrity check](evidence/sv27-2026-11-15/07-sqlite-backup-integrity.jpg)

## Thông tin triển khai

- URL: `https://sv27.bcse-vju.com/`
- Commit ứng dụng trên VPS: `0eba90e451312ddfc5b57dff268322e4ddb8cf7e`.
- Service systemd: `active`, `enabled`; API health trả HTTP 200.
- Terminal ghi nhận 46 Python tests đạt.
- Backup SQLite có `integrity_check=ok`; chưa kiểm tra restore.

## Việc còn lại trước khi bàn giao

1. Thử tài khoản khách thứ hai và xác nhận cách ly dữ liệu giữa hai tài khoản.
2. Thử trên thiết bị và mạng khác; kiểm tra giao diện điện thoại.
3. Thử khôi phục backup SQLite trên môi trường riêng.
4. Quay video liên tục 2–3 phút: khách đặt đơn, quản trị xử lý, khách xem trạng thái.
5. Hoàn thành các mục M04–M11 và xin giảng viên nghiệm thu.

**Giới hạn:** đây là bản chạy thử học phần với dữ liệu mẫu. Ghi nhận thanh toán trên website không phải chứng từ nhận tiền thực tế. VPS theo block không bảo đảm hoạt động 24/7. Không đưa dữ liệu khách, mật khẩu hoặc mã tra cứu bí mật lên GitHub.
