# Kết quả kiểm chứng

**Ngày kiểm tra:** 15/11/2026  
**Môi trường:** VPS học phần SV27 · Ubuntu 24.04  
**Repository:** `s2005on/vnu-food-hola`

## Rà soát mã nguồn — 16/11/2026

Phạm vi: backend/API, quản lý dữ liệu và backup, giao diện khách/quản trị, kiểm thử, cấu hình triển khai và tài liệu phiên bản.

- Đã bổ sung 2 kiểm thử Python về phiên checkout và 1 kiểm thử JavaScript về header gửi đơn; xem kết quả CI của PR #17 để xác nhận lượt kiểm thử mới.
- Bản sửa thanh điều hướng và kiểm tra phiên checkout không thay đổi schema SQLite hay dependencies.
- `v0.2.0` đã phát hành tại `f0359f6`; các tài liệu còn ghi “chưa tạo tag” được cập nhật.
- Kiểm tra trực quan bản sửa header chưa hoàn tất do Chromium không khởi động được trong môi trường kiểm thử.

### Lỗi còn mở: trạng thái tài khoản giữa các tab

Tái hiện bằng TestClient: đăng ký tài khoản → đăng xuất → gửi yêu cầu đặt món với dữ liệu còn giữ ở tab cũ → API trả 201 → đăng nhập lại → lịch sử tài khoản không có đơn đó. Đơn được tạo dưới dạng khách vãng lai vì backend dựa vào cookie hiện tại; frontend chưa ràng buộc danh tính đã dùng khi mở checkout.

Hướng xử lý: xác thực lại danh tính phiên khi gửi đơn và từ chối khi phiên thay đổi. Lỗi này chưa được sửa trong bản cập nhật giao diện. Trong lúc chờ sửa, tải lại trang đặt món sau khi đăng nhập/đăng xuất ở tab khác.

## Bản triển khai đã ghi nhận — 15/11/2026

- **URL:** [https://sv27.bcse-vju.com/](https://sv27.bcse-vju.com/)
- **Commit ứng dụng:** `0eba90e451312ddfc5b57dff268322e4ddb8cf7e` (PR #14).
- **Dịch vụ:** `vju-food-23110216.service` ở trạng thái `active` và `enabled`.
- **Backend:** Uvicorn lắng nghe trên `127.0.0.1:8016`; `/api/health` trả HTTP 200 và `{"ok":true}`.
- **Kiểm thử VPS:** Terminal ghi nhận 46 Python tests, kết quả `OK`.
- **SQLite:** đã tạo bản sao lưu trước nâng cấp; `PRAGMA integrity_check` trả `ok`. Chưa thử khôi phục bản sao.

## Luồng giao diện đã quan sát

1. Trang khách truy cập được trên SV27 và hiển thị thực đơn 16 món.
2. Tài khoản khách xem lịch sử với đơn thử tổng cộng 65.000đ ở trạng thái chờ xác nhận.
3. Quản trị chuyển đơn qua `confirmed → preparing → ready`.
4. Nhật ký ghi nhận `paid` và `ready → completed`.
5. Tài khoản khách hiển thị đơn `Hoàn thành` và `Đã thanh toán`.

Ghi nhận `paid` là thao tác thử trên hệ thống, **không chứng minh đã nhận tiền mặt ngoài thực tế**.

## Minh chứng

Ảnh được lưu tại [docs/evidence/sv27-2026-11-15/](docs/evidence/sv27-2026-11-15/README.md). Các ảnh đã che tên, số điện thoại, mã đơn và tên đăng nhập quản trị.

- [Trang thực đơn](docs/evidence/sv27-2026-11-15/01-sv27-homepage.jpg)
- [Lịch sử đơn phía khách](docs/evidence/sv27-2026-11-15/02-customer-order-pending.jpg)
- [Đơn phía quản trị](docs/evidence/sv27-2026-11-15/03-admin-order-ready.jpg)
- [Nhật ký xử lý](docs/evidence/sv27-2026-11-15/04-order-audit-log.jpg)
- [Đơn hoàn thành phía khách](docs/evidence/sv27-2026-11-15/05-customer-order-completed.jpg)
- [Kiểm thử và health trên VPS](docs/evidence/sv27-2026-11-15/06-vps-tests-health.jpg)
- [Kiểm tra backup SQLite](docs/evidence/sv27-2026-11-15/07-sqlite-backup-integrity.jpg)

## CI và log kiểm thử

- GitHub Actions của [PR #15](https://github.com/s2005on/vnu-food-hola/pull/15) đạt trên Ubuntu/Python 3.12 và Windows/Python 3.14.
- `docs/evidence/midterm-backend.txt` và `midterm-javascript.txt` lưu kết quả của một lượt kiểm thử cục bộ trước đó (40 Python tests và 11 JavaScript tests); không gộp các số liệu này với lượt 46 tests trên VPS.
- CI xanh không thay thế kiểm tra trình duyệt hoặc xác minh VPS.

## Chưa xác minh

- Truy cập độc lập từ mạng ngoài và khả năng hoạt động sau khi hết block SV27.
- Kiểm thử thủ công bằng tài khoản khách thứ hai và trên thiết bị/trình duyệt thứ hai.
- Các trường hợp nhập sai, món hết, giờ không hợp lệ và phân quyền API trực tiếp trên hosting.
- Khôi phục SQLite từ bản backup.
- Giao diện trên điện thoại và video demo liền mạch.
- Nghiệm thu cuối cùng của giảng viên.

VPS được cấp theo block; không cam kết uptime 24/7. Không đưa database, backup, mật khẩu hoặc mã tra cứu bí mật vào repository.
