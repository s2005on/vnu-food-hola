# Ghi chú nâng cấp MVP giữa kỳ — mốc nội bộ V7.3

`V7.3` là tên mốc phát triển, không phải Git release tag. Xem [quy ước phiên bản](docs/VERSIONING.md).

## Chạy

1. Dừng bản cũ bằng Ctrl+C.
2. Giải nén toàn bộ bản mới.
3. Chạy `RUN-WINDOWS.bat` và mở http://127.0.0.1:8016/.
4. Khi chưa có tài khoản quản trị, tạo mật khẩu mới theo lời nhắc của chương trình. Không có mật khẩu quản trị mặc định.
5. Trang quản trị: http://127.0.0.1:8016/admin.html.

Chế độ demo dùng database riêng và không có quyền truy cập database quán chính. Thông tin đăng nhập demo là công khai theo thiết kế; không sử dụng làm tài khoản quản trị thật.

## Giữ dữ liệu cũ

- Sao lưu thư mục dữ liệu trước khi nâng cấp.
- Dừng toàn bộ tiến trình cũ/mới trước khi sao chép database.
- Giữ nguyên đường dẫn `VJU_DB` trên VPS nếu database nằm ngoài thư mục mã nguồn.
- Không ghi đè database mới nếu đã có đơn cần giữ.
- Không commit database, backup hoặc thông tin đăng nhập.

## Dữ liệu và giao diện

Thực đơn khởi tạo gồm 16 món với giá mẫu. Quản trị có thể chỉnh sửa giá và trạng thái món. Ảnh món là ảnh minh họa, không phải ảnh xác nhận từ một quán hợp tác thực tế.

## Xác minh

Kết quả kiểm tra VPS SV27, mã triển khai, ảnh minh chứng và các giới hạn hiện tại nằm trong [VERIFICATION.md](VERIFICATION.md) và [hồ sơ giữa kỳ](docs/MIDTERM.md).
