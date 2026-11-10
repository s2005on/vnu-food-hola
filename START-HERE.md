# VJU Food Hola — bản chạy thử có backend (v3)

Giữ phong cách giao diện V2. Phần mới nằm trong `server/`; bản demo cũ không bị thay thế.
Đây là bản chạy thử có cơ sở dữ liệu thật, chưa phải xác nhận quán đã dùng vận hành thực tế.

## Chạy nhanh trên Windows

1. Giải nén **toàn bộ** ZIP vào một thư mục (không mở từ bên trong ZIP).
2. Cài Python 3.11 hoặc 3.12 nếu máy chưa có. Cần Internet trong lần cài thư viện.
3. Nhấp đúp `RUN-WINDOWS.bat`.
4. Lần đầu tạo tài khoản quản trị `son`, nhập mật khẩu tự chọn 12–128 ký tự hai lần.
   Mật khẩu không hiện khi gõ. Không gửi mật khẩu lên chat/GitHub.
5. Giữ cửa sổ chạy mở và mở `http://127.0.0.1:8016/`.
6. Trang quản trị: `http://127.0.0.1:8016/admin.html`.

Không mở `server/web/index.html` bằng file://: bản này phải chạy qua Python để gọi API.
Dừng bằng Ctrl+C. Lần chạy sau dữ liệu vẫn ở `server/data/food.sqlite3`.
Nếu cổng 8016 đang bận, dừng phiên VJU cũ hoặc đổi cổng trong lệnh chạy; không tắt tiến trình lạ.

## Chức năng đã có

- Giữ bố cục, màu sắc V2; thực đơn lấy từ máy chủ, tìm kiếm không dấu, lọc, yêu thích, giỏ hàng.
- Đặt đơn với tên, số điện thoại, giờ nhận và ghi chú; lưu SQLite.
- Backend kiểm tra món còn bán, số lượng, giá hiện tại; tính tổng tiền phía máy chủ.
- Giá/tên món và điểm nhận được chụp lại tại thời điểm đặt, không đổi theo thực đơn mới.
- Khóa chống trùng: gửi lại cùng yêu cầu trả lại cùng đơn và mã tra cứu, kể cả phản hồi đầu bị mất.
- Tra cứu đơn trên thiết bị khác bằng mã đơn + mã tra cứu bí mật.
- Đặt lại món từ đơn cũ theo giá/tình trạng hiện tại, không tự tạo đơn mới.
- Quản trị đăng nhập/đăng xuất; thêm/sửa/ẩn món và đánh dấu hết món.
- Quản trị nhận đơn, cập nhật trạng thái, hủy kèm lý do, ghi nhận tiền mặt.
- Đơn chỉ hoàn thành sau khi đã thu tiền. Đơn đã thu tiền không hủy tự động.
- Cài giờ mở/đóng, bật/tắt nhận đơn; tạo các khung 30 phút trong hôm nay, đặt trước ít nhất 15 phút.
- Thống kê các đơn tạo hôm nay: tổng đơn, số hoàn thành/hủy và số tiền đã thu cho những đơn đó.
- Công cụ sao lưu SQLite, kiểm thử API và workflow GitHub Actions.

## Thử từ đầu đến cuối

1. Đăng nhập quản trị, mở mục Cài đặt quán. Đảm bảo hiện tại đang trong giờ mở và còn khung nhận.
   Quán mẫu mặc định 08:00–20:00 theo giờ Việt Nam. Nếu thử ban đêm, chỉnh giờ cho phù hợp.
2. Mở trang khách: chọn 1 cơm gà và 1 bún thịt nướng, tổng 65.000đ.
3. Dùng tên/số điện thoại thử nghiệm, chọn giờ và đặt.
4. Lưu mã đơn và mã tra cứu bí mật ở phần chi tiết đơn. Không đưa mã bí mật vào ảnh nộp bài.
5. Trang quản trị → Đơn hàng: đơn mới xuất hiện; nhận đơn → đang chuẩn bị → sẵn sàng nhận.
6. Ghi nhận thu tiền chỉ khi mô phỏng đã nhận đủ tiền, sau đó hoàn thành.
7. Trang khách → Đơn của tôi: mở lại để cập nhật; trạng thái phải khớp với quản trị.
8. Tắt/chạy lại máy chủ, kiểm tra đơn vẫn còn. Thử tra cứu ở cửa sổ riêng tư bằng hai mã.

Nếu mất mạng khi đặt, dùng “Kiểm tra lần đặt trước”. Không bỏ yêu cầu đang chờ chỉ vì chưa thấy phản hồi;
chỉ bỏ khi xác nhận đơn chưa được tạo hoặc máy chủ đã từ chối.

## Cài thủ công (PowerShell, tại thư mục có server)

```powershell
py -3 -m venv .venv-vju
.\.venv-vju\Scripts\python.exe -m pip install -r server\requirements.txt
$env:VJU_COOKIE_SECURE="0"
.\.venv-vju\Scripts\python.exe -m server.manage admin --username son
.\.venv-vju\Scripts\python.exe -m uvicorn server.app:app --host 127.0.0.1 --port 8016 --workers 1
```

Không có mật khẩu mặc định. Chạy lại lệnh `manage admin` để đổi mật khẩu; các phiên cũ sẽ bị thu hồi.
Chỉ đặt COOKIE_SECURE=0 khi thử trên localhost HTTP. Trên VPS HTTPS dùng 1.

## Kiểm thử tự động

```powershell
.\.venv-vju\Scripts\python.exe -m pip install -r server\requirements-test.txt
.\.venv-vju\Scripts\python.exe -m unittest discover -s tests -p test_server.py -v
```

Xem `VERIFICATION.md` để biết phần đã kiểm tra và phần chưa xác minh.

## Đưa vào repo của Sơn

Chép `server/`, `tests/test_server.py`, `deploy/`, `.github/workflows/backend-ci.yml`,
`RUN-WINDOWS.bat`, `START-HERE.md`, `VERIFICATION.md` vào repo `vnu-food-hola`.
Không chép dữ liệu SQLite hoặc môi trường ảo. Thêm các dòng trong `.gitignore-backend-notes.txt`
vào `.gitignore` của repo trước khi git add. Tạo nhánh từ `feature/ui-v2`, ví dụ `feature/backend-v3`.

Không cần sửa `demo/v2`: bản đó giữ làm minh chứng giao diện. Bản có backend nằm trong `server/web`.
VPS cần tiến trình Python chạy thường trực và Nginx reverse proxy, không chỉ chép HTML vào /var/www.
Hướng dẫn cụ thể ở `deploy/README.md`.

## Giới hạn còn lại

- Một quán, một điểm nhận; nhận tại quán, trả tiền mặt; chưa có tài xế, thanh toán online, AI.
- Quản lý món dùng biểu tượng có sẵn; chưa có tải ảnh, topping/size, voucher hoặc đánh giá.
- Thực đơn và thông tin quán là mẫu. Chưa thử với khách/quán thật.
- Không có tài khoản khách; ai có cả hai mã có thể xem đơn. Giữ mã tra cứu riêng.
- Mã tra cứu lưu trên trình duyệt để tiện dùng; quên danh sách chỉ xóa tham chiếu trên máy, không xóa đơn trên server.
- Chạy một worker. Giới hạn tần suất nằm trong RAM; khi qua reverse proxy hiện tính chung theo IP proxy.
  Chưa cấu hình giới hạn phân tán hay đo tải thực tế.
- Phân trang quản trị 50 đơn/trang. Khách mở lịch sử để cập nhật; chưa tự đẩy trạng thái theo thời gian thực.
- Cookie bảo vệ phiên, mật khẩu scrypt, kiểm tra CSRF, query SQL có tham số; không phải chứng nhận kiểm toán bảo mật.
- Dữ liệu/mật khẩu không chia sẻ với các nhóm khác. VPS dùng chung tài khoản Linux không cách ly được các nhóm;
  xin tài khoản riêng hoặc môi trường riêng trước khi chứa thông tin khách thật.
