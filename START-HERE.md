# Chạy và demo MVP (mốc nội bộ V7.3)

Tên V7.3 là nhãn của quá trình phát triển, không phải Git tag phát hành. Xem [quy ước phiên bản](docs/VERSIONING.md) và [báo cáo tổng kết, bàn giao](docs/FINAL-HANDOVER.md).

## Windows
1. Giải nén toàn bộ ZIP, dừng bản cũ bằng Ctrl+C. Không mở HTML trực tiếp bằng file://.
2. Cài Python; CI dùng Python 3.12 trên Ubuntu và 3.14 trên Windows.
3. Chạy RUN-WINDOWS.bat. Tạo mật khẩu quản trị theo lời nhắc khi khởi chạy; mật khẩu không hiện khi gõ và không có mật khẩu mặc định.
4. Giữ cửa sổ chạy mở. Khách: http://127.0.0.1:8016/ ; quản trị: http://127.0.0.1:8016/admin.html .
5. Dữ liệu ở server/data/food.sqlite3. Đọc START-V7.3.md trước khi đổi bản để giữ dữ liệu.

## Luồng demo (hai trình duyệt)
1. Trình duyệt A vào trang khách thường; nếu đang demo, chọn tiếp tục với vai trò khách.
2. Chọn cơm gà và bún thịt nướng (dữ liệu mẫu tổng 65.000 đồng; nếu quán đã sửa giá thì theo giá hiện tại).
3. Nhập thông tin giả để thử, địa điểm tự nhập và giờ hợp lệ. Mặc định 10:00-22:00, hôm nay/ngày mai, mỗi 15 phút, đặt trước ít nhất 15 phút.
4. Đặt đơn, lưu mã đơn và mã tra cứu riêng tư; không đưa mã bí mật vào ảnh công khai.
5. Trình duyệt B đăng nhập bằng tài khoản quản trị đã cấu hình trên máy. Xác nhận → chuẩn bị → sẵn sàng → ghi nhận thu tiền thử → hoàn thành.
6. Quay lại A và tải lại: trạng thái khớp. Khởi động lại backend trên máy thử: đơn vẫn còn.
7. Thử món hết hàng, thông tin thiếu, giờ hết hạn và gửi lại yêu cầu; đối chiếu [bảng kiểm giữa kỳ](docs/MIDTERM.md).

## Chế độ demo riêng
Chế độ demo dùng tài khoản thử và database tách biệt với dữ liệu quán chính. Thông tin đăng nhập demo không được ghi trong tài liệu công khai; không sử dụng tài khoản demo làm tài khoản quản trị thật.

## Nếu không hoạt động
- Cổng 8016 bận: kiểm tra tiến trình cũ; không tắt tiến trình của người khác.
- Không có giờ: kiểm tra cài đặt mở quán và đồng hồ; giờ ngày mai tự cập nhật.
- Trang cũ: tải lại Ctrl+F5, kiểm tra đã chạy đúng thư mục mới.
- Mất phản hồi đặt món: dùng kiểm tra lần đặt trước; tránh tạo yêu cầu mới khi chưa biết kết quả cũ.
- VPS: xem deploy/README.md; localhost chạy tốt chưa chứng minh link Internet chạy tốt.
