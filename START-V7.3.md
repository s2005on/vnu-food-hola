# Ghi chú nâng cấp MVP giữa kỳ — mốc nội bộ V7.3

`V7.3` là tên mốc phát triển trước khi chuẩn hóa phiên bản, **không phải** một Git release tag. Giữ tên file này để tương thích với đường dẫn cũ. Xem [lịch sử phát hành và quy ước phiên bản](docs/VERSIONING.md).

## Chạy
Dừng bản cũ bằng Ctrl+C. Giải nén toàn bộ ZIP, chạy RUN-WINDOWS.bat, mở http://127.0.0.1:8016/.
Mật khẩu quản trị son: tối thiểu 6 ký tự, nhập lại để xác nhận. Không có mật khẩu quản trị mặc định.
Khách đặt đơn không cần tài khoản. Trang quản trị: /admin.html, đăng nhập son để xử lý đơn khách.
Demo có dữ liệu riêng: demo / VjuTest2026!, quản trị demo shoptest / QuanTest2026! trên cùng trình duyệt. Nút “Tiếp tục với vai trò khách” thoát demo về dữ liệu chung.

## Giữ dữ liệu cũ
Giữ bản cũ làm bản sao. Khi tất cả tiến trình cũ/mới đã dừng, sao lưu rồi chép nguyên thư mục server/data của bản đang dùng vào server/data của bản mới TRƯỚC lần chạy đầu. Không ghi đè nếu bản mới đã có đơn cần giữ. Với VPS, giữ nguyên VJU_DB trỏ tới database ngoài mã nguồn.
8 món mới được thêm một lần, không ghi đè ID, giá hay trạng thái của món tùy chỉnh cũ. Món cùng tên đã tồn tại sẽ được giữ lại. Tài khoản và đơn cũ giữ nguyên khi dùng đúng database.

## Giao diện
Bỏ cả hai đoạn hướng dẫn ba bước bị lặp. Bỏ thanh demo trên trang khách, vẫn hiển thị thông báo khi đang ở demo. Thu gọn giờ nhận thành một dòng, vẫn hiển thị lỗi khi quán đóng hoặc mất kết nối. Chân trang gọn với thương hiệu, ba liên kết và chú thích dữ liệu mẫu. Giữ viền thẻ món, nhãn giá và giỏ hàng góc phải của V7.2.

## 8 món mới / giá mẫu do dự án đề xuất
- Cơm sườn nướng: 35.000 đ
- Cơm rang dưa bò: 35.000 đ
- Phở bò: 35.000 đ
- Bún chả: 35.000 đ
- Xôi trứng chả: 25.000 đ
- Khoai tây chiên: 20.000 đ
- Trà đào cam sả: 18.000 đ
- Sữa đậu nành: 12.000 đ
Đây là giá mẫu cho giao diện sinh viên, chưa phải báo giá của một quán thực tế. Quản trị có thể sửa giá. Ảnh minh họa AI đi kèm, lưu cục bộ nên không phụ thuộc đường dẫn ảnh ngoài.

## Sửa lỗi và xác minh
Gộp sửa lỗi Guest vào V7.2: ngăn đơn demo hết phiên lọt sang dữ liệu chung, bảo vệ tab khách khi tab khác đổi sang demo, giữ giờ đã chọn khi tải lại thực đơn, cập nhật giờ mỗi phút, tránh cache JS/CSS cũ, bổ sung cách tạo khóa chống đơn trùng trên HTTP LAN. Sửa thẻ đóng thừa ở tiêu đề lịch sử đơn.
40 kiểm thử backend và 11 kiểm thử JavaScript đạt. Kiểm tra đường dẫn ảnh/CSS/JS và ID HTML đạt. Có kiểm thử nâng cấp database chứa món tùy chỉnh, thêm món một lần và đặt món mới đúng giá.
Chưa xác minh trực quan trên trình duyệt ở lần cập nhật này. Chưa triển khai lên VPS; localhost chỉ truy cập trên máy chạy. Cần triển khai và kiểm thử liên kết công khai để có bằng chứng nộp thầy. Luồng thanh toán vẫn là tiền mặt khi nhận, trạng thái do quản trị cập nhật.
