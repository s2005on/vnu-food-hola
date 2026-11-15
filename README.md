# VNU Food Hola

[![Backend checks](https://github.com/s2005on/vnu-food-hola/actions/workflows/backend-ci.yml/badge.svg?branch=main)](https://github.com/s2005on/vnu-food-hola/actions/workflows/backend-ci.yml)

Website đặt món dành cho sinh viên Trường Đại học Việt Nhật (VJU), thuộc học phần CSE3045. Ứng dụng thử nghiệm phục vụ một quán, dùng thực đơn và ảnh minh họa.

[Demo SV27](https://sv27.bcse-vju.com/) · [Releases](https://github.com/s2005on/vnu-food-hola/releases) · [Tài liệu](docs/README.md)

## Chức năng

- Thực đơn 16 món mẫu, tìm kiếm, lọc và giỏ hàng.
- Đặt món theo địa điểm và giờ nhận; tra cứu bằng mã đơn và mã bí mật.
- Đăng ký, đăng nhập và lịch sử đơn theo tài khoản.
- Quản trị thực đơn, xử lý đơn, ghi nhận tiền mặt và nhật ký trạng thái.
- Backend tính giá, kiểm tra dữ liệu, hạn chế tạo đơn trùng và tách dữ liệu demo.
- Thanh điều hướng giữ ở đầu màn hình khi cuộn trang.

![Trang thực đơn trên SV27](docs/evidence/sv27-2026-11-15/01-sv27-homepage.jpg)

## Chạy nhanh

Cài Python 3.12, tải mã nguồn rồi chạy `RUN-WINDOWS.bat` trên Windows. Lần đầu chương trình yêu cầu tạo mật khẩu quản trị.

| Giao diện | Địa chỉ cục bộ |
|---|---|
| Khách hàng | http://127.0.0.1:8016/ |
| Quản trị | http://127.0.0.1:8016/admin.html |

Hướng dẫn chi tiết: [chạy ứng dụng](START-HERE.md), [giữ dữ liệu khi nâng cấp](START-V7.3.md), [triển khai VPS](deploy/README.md).

## Kiểm thử

```bash
python -m pip install -r server/requirements-test.txt
python -m unittest discover -s tests -p test_server.py -v
node --test tests/*.test.cjs
```

CI kiểm tra Ubuntu/Python 3.12 và Windows/Python 3.14. Kết quả và vấn đề còn mở: [VERIFICATION.md](VERIFICATION.md).

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `server/` | FastAPI, SQLite, giao diện HTML/CSS/JavaScript và dữ liệu mẫu |
| `tests/` | Kiểm thử backend và frontend |
| `deploy/` | systemd, Nginx và hướng dẫn vận hành |
| `docs/` | Thiết kế, hồ sơ học phần và minh chứng |
| `demo/` | Giao diện tĩnh lưu từ các giai đoạn trước |

## Phiên bản và phạm vi

[v0.2.0](https://github.com/s2005on/vnu-food-hola/releases/tag/v0.2.0) là bản Academic MVP. [v0.2.1](docs/RELEASE-v0.2.1.md) bổ sung bản sửa thanh điều hướng và chuẩn hóa tài liệu; xem [CHANGELOG](CHANGELOG.md).

Chưa có thanh toán trực tuyến, OTP/SMS, khôi phục mật khẩu, shipper hoặc nhiều quán. VPS SV27 được cấp theo thời hạn của trường. Các giới hạn kiểm thử được tập trung tại [VERIFICATION.md](VERIFICATION.md).
