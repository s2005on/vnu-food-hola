# VJU Food Hola — giao diện demo v2

Bản nâng cấp độc lập từ demo B4; giữ nguyên demo/index.html và trang B1.

## Chạy trên Windows
Giải nén gói nâng cấp vào thư mục repo vnu-food-hola, giữ cấu trúc demo/v2.
Mở PowerShell trong repo và chạy:

    Start-Process .\demo\v2\index.html

Không cần Node, npm, backend hay cài thư viện để mở giao diện.
Font Google là tùy chọn; khi không có mạng, giao diện dùng Arial.
Minh họa món dùng emoji hệ thống và CSS, không phải ảnh món thực tế.

## Chức năng
- 8 món mẫu, thẻ món, thông báo hết món.
- Tìm kiếm không dấu, lọc loại món, sắp xếp giá.
- Thêm/bỏ món yêu thích.
- Giỏ hàng tăng/giảm/xóa; giới hạn 20 phần mỗi món.
- Tổng tiền theo giá trong danh sách demo; không nhận giá từ dữ liệu giỏ đã lưu.
- Lưu giỏ và yêu thích vào localStorage khi trình duyệt cho phép.
- Biểu mẫu tên dùng thử, giờ và điểm nhận minh họa, ghi chú.
- Tạo mã đơn demo, lưu tối đa 20 đơn, xem chi tiết, xóa lịch sử có xác nhận.
- Từ chối tên chỉ có khoảng trắng; escape nội dung người nhập khi hiển thị.
- Bố cục thích ứng điện thoại; nhãn cho nút và hộp thoại đóng bằng Escape.

## Giới hạn quan trọng
Chỉ là frontend demo. Không có backend, xác thực, gửi đơn đến quán,
thanh toán, kiểm tra khung giờ theo thời gian thực hoặc quản trị thật.
Dữ liệu lưu trên trình duyệt này, có thể bị người dùng sửa hoặc xóa;
không dùng làm căn cứ bán hàng. Không nhập dữ liệu khách hàng thật.
Mở file trực tiếp có thể bị một số trình duyệt giới hạn localStorage;
khi đó trang vẫn hoạt động nhưng không đảm bảo lưu sau khi đóng.
Dữ liệu không tự đồng bộ giữa máy, domain hoặc tab; thông báo tải lại
xuất hiện khi có thay đổi localStorage từ tab khác.

## Kiểm tra đã thực hiện
- node --check app.js thành công.
- 9 kiểm tra logic bằng Node: tổng 65.000đ, loại dữ liệu giỏ sai,
  giới hạn số lượng, xóa khi giảm về 0, chặn món hết hàng,
  tìm không dấu, lọc yêu thích, tìm không có kết quả, sắp xếp giá.
- Chưa kiểm thử tương tác trực tiếp trong trình duyệt hoặc trên VPS.

## Kiểm tra thủ công trước khi deploy
1. Thêm cơm gà và bún thịt nướng: tổng 65.000đ.
2. Tăng, giảm, xóa món; tải lại và kiểm tra giỏ nếu lưu trữ được phép.
3. Tìm "com ga", lọc Đồ uống, lưu yêu thích, đổi thứ tự giá.
4. Tạo đơn bằng tên giả, xem chi tiết và lịch sử sau tải lại.
5. Xóa lịch sử bằng hai lần bấm xác nhận; kiểm tra trên màn hình điện thoại.

## Đưa vào Git
Tạo nhánh từ bản tích hợp B7 hiện có, không reset mã đang làm.
Chỉ thêm thư mục demo/v2 và commit sau khi chạy thử.
Triển khai v2 sang đường dẫn riêng trên VPS sau khi kiểm tra cấu hình
hiện tại; không thay cấu hình Nginx hoặc ứng dụng của nhóm khác.

## Ghi nhận hỗ trợ AI
ChatGPT hỗ trợ xây dựng HTML/CSS/JavaScript, kiểm tra logic và hướng dẫn.
Người thực hiện cần đọc hiểu, kiểm tra trên máy và ghi lại kết quả thực tế.
