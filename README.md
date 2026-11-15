# VJU Food Hola - bàn giao giữa kỳ V7.3

Website đặt món cho sinh viên VJU. **Lâm Hải Sơn - MSSV 23110216 - CSE3045.**
Phạm vi: một quán, thực đơn mẫu 16 món, nhận món theo địa điểm khách nhập,
thanh toán tiền mặt và quản trị xử lý đơn. Chưa tiếp nhận đơn thương mại thực tế.

## Mở và kiểm tra nhanh

1. Giải nén toàn bộ mã nguồn; chạy `RUN-WINDOWS.bat` trên Windows có Python.
2. Tạo tài khoản quản trị `son`, mật khẩu tự chọn **6-128 ký tự**; không có mật khẩu mặc định.
3. Khách: http://127.0.0.1:8016/ ; quản trị: http://127.0.0.1:8016/admin.html .
4. Khách không cần đăng nhập. Đơn được lưu SQLite và quản trị quán nhìn thấy.
5. Đọc [hướng dẫn chạy](START-HERE.md) và [giữ dữ liệu khi nâng cấp](START-V7.3.md).

`localhost` chỉ truy cập trên máy chạy, chưa phải bằng chứng hosting.

## Khách, quản trị và demo

| Vai trò | Cách sử dụng | Dữ liệu |
|---|---|---|
| Khách | Tiếp tục với vai trò khách, không cần tài khoản | Database chính của quán |
| Quản trị quán | `son` và mật khẩu tự đặt | Quản lý đơn khách, món và cài đặt quán |
| Khách demo | `demo` / `VjuTest2026!` | Database thử riêng theo phiên trình duyệt |
| Quản trị demo | `shoptest` / `QuanTest2026!` sau khi vào demo | Dữ liệu demo của cùng phiên |

Để thầy xem luồng khách-quán trên hai trình duyệt, dùng **khách thường + quản trị son**.
Không dùng hai phiên demo khác nhau để kiểm tra chia sẻ đơn. Không công khai mật khẩu son.

## Chức năng giữa kỳ

- Thực đơn 16 món có ảnh minh họa AI, tìm kiếm, lọc, yêu thích, giỏ hàng gọn.
- Nhập tên, điện thoại, địa điểm, ghi chú; chọn giờ hôm nay/ngày mai, bước 15 phút.
- Giờ mẫu 10:00-22:00 theo Việt Nam; giờ nhận cách hiện tại ít nhất 15 phút.
- Máy chủ kiểm tra giá, món còn bán, giờ nhận; chống tạo trùng khi gửi lại yêu cầu.
- Theo dõi bằng mã đơn và mã tra cứu bí mật; lưu đơn sau khởi động lại.
- Quản trị xác nhận, chuẩn bị, sẵn sàng, thu tiền, hoàn thành hoặc hủy có lý do.
- Trạng thái xử lý và thanh toán tách riêng; hoàn thành yêu cầu đã thu tiền.
- SQLite, sao lưu riêng, systemd và cấu hình Nginx theo đường dẫn của sinh viên.

Chưa có thanh toán online, tài khoản khách tự đăng ký, shipper hay nhiều quán.
Giá là dữ liệu mẫu, không phải báo giá của quán đối tác đã xác nhận.

## Kiểm thử

```sh
python -m pip install -r server/requirements-test.txt
python -m unittest discover -s tests -p test_server.py -v
node --test tests/customer-refresh.test.cjs tests/cart-drawer.test.cjs tests/menu-cards.test.cjs
```

CI kiểm tra backend, cả ba bộ kiểm thử JavaScript và cú pháp JavaScript/Bash.
Xem [kết quả và giới hạn xác minh](VERIFICATION.md).

## Triển khai và minh chứng nộp thầy

- [PR #10](https://github.com/s2005on/vnu-food-hola/pull/10) đã merge vào main ngày 14/11/2026.
- Bản sửa giữa kỳ này được chuẩn bị từ commit `b2fce97027dc61bd73a4ce6fab71488ffbe3f738`.
- Link VPS dự kiến: https://sv21.bcse-vju.com/b1-23110216/v3/ .
- **Chưa xác nhận V7.3 chạy công khai**: lần kiểm tra 15/11/2026 nhận HTTP 403 từ môi trường kiểm tra; cần đối chiếu trên trình duyệt/mạng ngoài. Đây chưa phải kết luận nguyên nhân lỗi VPS.
- [Triển khai](deploy/README.md) - [bảng kiểm và minh chứng giữa kỳ](docs/MIDTERM.md).
- [Rà soát các PR cũ](docs/PR-REVIEW.md). Không merge hàng loạt những nhánh cũ.

CI thành công không tự triển khai VPS. systemd giữ tiến trình khi đóng SSH, không kéo dài block VPS 6 giờ.

## Cấu trúc và đóng góp

`server/`: FastAPI và giao diện; `tests/`: kiểm thử; `deploy/`: triển khai;
`docs/`: hồ sơ học phần; `demo/`: mẫu cũ, không phải bản ứng dụng hiện tại.
Database và backup phải giữ ngoài Git, không đưa mật khẩu hoặc mã tra cứu vào minh chứng.

Sơn thực hiện dự án cá nhân, có AI hỗ trợ mã nguồn/tài liệu. Cần tự giải thích được tính tiền
phía server, phiên khách/demo, bảo vệ quản trị, lưu SQLite và quy tắc trạng thái.
Các hồ sơ B2-B7 trong docs là lịch sử quá trình; thiết kế thực tế xem [tại đây](docs/03-system-design.md).
