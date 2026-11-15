# VNU Food Hola

**Website đặt món ăn cho sinh viên Trường Đại học Việt Nhật (VJU).**

Dự án học phần **CSE3045** — Lâm Hải Sơn (MSSV: 23110216).  
**Mã nguồn:** MVP giữa kỳ V7.3 và các tính năng mở rộng (tài khoản khách) · **FastAPI + SQLite + HTML/CSS/JavaScript**. Git tag phát hành gần nhất: `v0.1.0` (demo tĩnh); chưa gắn tag cho MVP.

> Đây là ứng dụng **chạy thử phục vụ học tập**: một quán, thực đơn và giá mẫu. Chưa xác nhận triển khai công khai MVP hoặc vận hành thương mại với quán thật.

## Chức năng chính

- **Khách hàng:** xem thực đơn 16 món, tìm kiếm/lọc món, thêm vào giỏ và đặt món; nhập địa điểm, chọn giờ nhận.
- **Theo dõi đơn:** lưu đơn trong SQLite; tra cứu bằng mã đơn và mã bí mật; hạn chế tạo đơn trùng khi gửi lại.
- **Quản trị quán:** đăng nhập, quản lý món, xác nhận/chuẩn bị/hoàn thành hoặc hủy đơn; ghi nhận thanh toán tiền mặt.
- **An toàn nghiệp vụ:** giá được tính ở máy chủ; trạng thái thanh toán và xử lý đơn được quản lý tách biệt.
- **Tài khoản khách:** đăng ký bằng họ tên, số điện thoại, mật khẩu; đăng nhập và xem lịch sử đơn được lưu trên máy chủ, kể cả khi đổi thiết bị.
- **Khách không đăng nhập:** vẫn đặt món và tra cứu bằng mã đơn + mã bí mật; có thể liên kết một đơn cũ vào tài khoản bằng cả hai mã.
- **Chế độ demo:** có dữ liệu thử riêng; không thay thế luồng khách và quán trên cơ sở dữ liệu chính.

**Giới hạn:** chưa có thanh toán online, giao hàng qua shipper, nhiều quán hoặc xác minh số điện thoại bằng OTP. Không dùng dữ liệu thật trước khi hoàn tất kiểm thử triển khai và chính sách bảo vệ dữ liệu.

## Chạy nhanh trên Windows

1. Tải hoặc clone **toàn bộ** repository, cài Python và chạy `RUN-WINDOWS.bat`.
2. Ở lần chạy đầu, tạo mật khẩu cho tài khoản quản trị `son` (6–128 ký tự, **không có mật khẩu mặc định**).
3. Mở các địa chỉ dưới đây khi cửa sổ máy chủ vẫn đang chạy:

| Giao diện | Địa chỉ cục bộ |
|---|---|
| Khách hàng | http://127.0.0.1:8016/ |
| Quản trị | http://127.0.0.1:8016/admin.html |

Xem [hướng dẫn chạy và demo](START-HERE.md). **Nếu nâng cấp bản cũ**, đọc [hướng dẫn giữ dữ liệu của mốc V7.3](START-V7.3.md) trước; không xóa `server/data/` tùy tiện. Không mở trực tiếp file HTML bằng `file://`.

## Kiểm thử

```bash
python -m pip install -r server/requirements-test.txt
python -m unittest discover -s tests -p test_server.py -v
node --test tests/customer-refresh.test.cjs tests/cart-drawer.test.cjs tests/menu-cards.test.cjs
```

Cần cài Node.js để chạy kiểm thử JavaScript. Xem [kết quả kiểm tra, môi trường và giới hạn xác minh](VERIFICATION.md). CI không đồng nghĩa ứng dụng đã được triển khai thành công lên VPS.

## Cấu trúc dự án

| Thư mục / tệp | Mục đích |
|---|---|
| `server/` | Backend FastAPI, giao diện hiện hành và dữ liệu mẫu |
| `tests/` | Kiểm thử backend và JavaScript |
| `deploy/` | Cấu hình, script và hướng dẫn VPS/Nginx |
| `docs/` | Yêu cầu, thiết kế, hồ sơ môn học và minh chứng |
| `demo/` | Bản demo giao diện cũ, lưu làm lịch sử |
| `RUN-WINDOWS.bat` | Khởi chạy ứng dụng cục bộ trên Windows |

## Tài liệu và trạng thái bàn giao

- [Lịch sử thay đổi](CHANGELOG.md) · [Quy ước đặt tên phiên bản](docs/VERSIONING.md) · [Bảng kiểm trước phát hành v0.2.0 (dự kiến)](docs/RELEASE-v0.2.0.md)
- [Mục lục tài liệu dự án và hồ sơ B2–B7](docs/README.md)
- [Hồ sơ B2 và minh chứng VPS trước V3](docs/B2-REPORT.md)
- [Bảng kiểm bàn giao giữa kỳ](docs/MIDTERM.md) · [Rà soát PR cũ](docs/PR-REVIEW.md)
- [Hướng dẫn triển khai VPS](deploy/README.md) · [Quy trình Git](docs/GIT.md)

**Trạng thái:** Mốc MVP giữa kỳ (tên nội bộ V7.3) đã được gộp vào `main` tại [PR #10](https://github.com/s2005on/vnu-food-hola/pull/10). Các bổ sung tài liệu/CI đã merge qua [PR #11](https://github.com/s2005on/vnu-food-hola/pull/11) ngày 15/11/2026; **chưa coi là đã triển khai công khai** nếu chưa có kiểm chứng thực tế. URL cục bộ chỉ hoạt động trên máy chạy ứng dụng.

Dự án được thực hiện cá nhân và có AI hỗ trợ. Việc tự kiểm thử/AI hỗ trợ không thay thế review độc lập. Không commit mật khẩu, database chứa dữ liệu khách hoặc mã tra cứu bí mật.
