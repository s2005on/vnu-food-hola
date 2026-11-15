# Thiết kế hiện thực V7.3 - cập nhật giữa kỳ 15/11/2026

HTML/CSS/JavaScript gọi FastAPI cùng tên miền; FastAPI lưu SQLite. Nginx chuyển tiếp
đường dẫn /b1-23110216/v3/ về Uvicorn loopback 8016. systemd quản lý tiến trình.

## Dữ liệu và phiên
Khách thường đặt vào database chính VJU_DB, không cần tài khoản. Cookie demo chọn database
thử riêng, có hạn sử dụng; hết phiên không được âm thầm ghi đơn demo sang dữ liệu chính.
Quản trị dùng cookie HttpOnly và CSRF cho thay đổi dữ liệu. Trên VPS bật Secure cookie/HTTPS.
Tên và giá món được chụp tại thời điểm tạo đơn. Mã tra cứu riêng bảo vệ việc xem đơn.
Địa điểm là chuỗi khách tự nhập; quán cần xác nhận, không có định vị hay tính phí vận chuyển tự động.

## API hiện có

| Phương thức | Đường dẫn | Chức năng |
|---|---|---|
| GET | /api/health | Sức khỏe tiến trình |
| GET | /api/menu | Thực đơn, cài đặt và khung giờ |
| GET | /api/session | Trạng thái phiên demo/khách |
| POST | /api/orders | Tạo đơn, kiểm tra giá/giờ và khóa chống trùng |
| GET | /api/orders/{code} | Xem đơn với mã tra cứu trong Authorization |
| POST | /api/trial/login, /api/trial/logout | Vào/thoát demo |
| POST | /api/admin/login, /api/admin/logout | Phiên quản trị |
| GET | /api/admin/me | Danh tính và CSRF |
| GET, POST | /api/admin/dishes | Danh sách, thêm món |
| PUT | /api/admin/dishes/{ident} | Sửa món |
| GET | /api/admin/orders | Danh sách đơn phân trang |
| PATCH | /api/admin/orders/{code}/status | Trạng thái xử lý |
| PATCH | /api/admin/orders/{code}/payment | Trạng thái thu tiền |
| GET | /api/admin/orders/{code}/events | Lịch sử xử lý |
| GET, PUT | /api/admin/shop | Cài đặt quán |
| GET | /api/admin/stats | Thống kê |

## Quy tắc cốt lõi
- pending -> confirmed -> preparing -> ready -> completed; hủy có lý do theo trạng thái cho phép.
- unpaid/paid tách riêng; đơn hoàn thành phải đã thu tiền, không tự hủy đơn đã thu tiền.
- Backend kiểm tra số lượng, giá, tình trạng món và giờ; tạo đơn trong giao dịch SQLite.
- Gửi lại cùng khóa/nội dung trả đơn cũ; không tự tạo trùng.
- Khung giờ Asia/Ho_Chi_Minh, hôm nay/ngày mai, bước 15 phút, cách hiện tại ít nhất 15 phút.
- Database riêng ngoài checkout trên VPS; sao lưu bằng SQLite backup API.

Không có thanh toán online, shipper, nhiều quán hoặc tài khoản khách tự đăng ký.
Ảnh AI chỉ là tài nguyên minh họa, không phải chức năng AI của ứng dụng.
Xem VERIFICATION.md để biết phần đã kiểm thử và phần chưa xác minh trên VPS.
