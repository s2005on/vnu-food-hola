# Bản mô tả dự án

## 1. Thông tin chung
- Tên đề tài: Website đặt đồ ăn cho sinh viên VJU.
- Người thực hiện: Lâm Hải Sơn.
- Học phần: CSE3045 – Học theo dự án Khoa học và Kỹ thuật.
- Trạng thái: Đề xuất phạm vi ban đầu, chờ giảng viên duyệt.

## 2. Vấn đề cần giải quyết
Sinh viên có thời gian nghỉ ngắn, mất thời gian chọn món và chờ mua đồ ăn.
Các quán cần nhận đơn rõ ràng, biết món và số lượng khách đặt để chuẩn bị.

## 3. Mục tiêu
Xây dựng website cho phép sinh viên xem thực đơn, đặt món và theo dõi đơn.
Quản trị viên có thể quản lý thực đơn, tiếp nhận và cập nhật trạng thái đơn.
Sản phẩm hướng đến sử dụng thực tế với một quán gần trường.

## 4. Các bên liên quan
- Sinh viên: người đặt và nhận món.
- Quán hợp tác: cung cấp món, xác nhận và chuẩn bị đơn.
- Người thực hiện: phát triển, kiểm thử và hỗ trợ vận hành.
- Giảng viên: góp ý, duyệt phạm vi và đánh giá sản phẩm.

## 5. Phạm vi bản đầu
Dự kiến phục vụ một quán gần trường với khoảng 10–20 món.

### Chức năng dành cho khách hàng
- Xem danh sách món, hình ảnh, mô tả và giá.
- Tìm kiếm và lọc món theo loại.
- Thêm, xóa và thay đổi số lượng trong giỏ hàng.
- Nhập thông tin liên hệ và nhận món.
- Chọn khung giờ, điểm nhận và nhập ghi chú.
- Đặt hàng và nhận mã đơn.
- Tra cứu trạng thái đơn của mình.

### Chức năng dành cho quản trị viên
- Đăng nhập quản trị.
- Thêm, sửa và ẩn món.
- Cập nhật giá và tình trạng còn/hết món.
- Xem thông tin và chi tiết đơn hàng.
- Xác nhận hoặc hủy đơn, ghi nhận lý do hủy.
- Cập nhật trạng thái xử lý đơn.
- Ghi nhận trạng thái thanh toán riêng với trạng thái xử lý đơn.

### Quy trình xử lý đơn
Chờ xác nhận → Đã xác nhận → Đang chuẩn bị → Sẵn sàng nhận → Hoàn thành.

Đơn có thể chuyển sang trạng thái Đã hủy theo quy định thống nhất với quán.

### Thanh toán và nhận món
- Thanh toán ban đầu: tiền mặt khi nhận món.
- Cách nhận món, điểm nhận và người phụ trách giao/nhận sẽ được thống nhất với quán.
- Giao diện sử dụng được trên máy tính và điện thoại.

## 6. Ngoài phạm vi bản đầu
- AI gợi ý món: xem xét bổ sung ở phiên bản sau.
- Theo dõi vị trí shipper theo thời gian thực.
- Thanh toán trực tuyến tự động.
- Nhiều quán tự đăng ký và quản lý gian hàng.
- Ví tiền, tích điểm và chương trình khuyến mãi phức tạp.

## 7. Tiêu chí nghiệm thu dự kiến
- Khách thực hiện được luồng xem món → giỏ hàng → đặt đơn → nhận mã đơn.
- Đơn được lưu trong cơ sở dữ liệu và vẫn tồn tại sau khi tải lại trang.
- Backend kiểm tra thông tin bắt buộc, món còn bán và số lượng hợp lệ.
- Backend tính tổng tiền từ giá trong cơ sở dữ liệu.
- Đơn lưu giá tại thời điểm đặt, không đổi khi giá thực đơn thay đổi.
- Quản trị viên xem được đơn mới và cập nhật trạng thái.
- Trạng thái thanh toán được lưu riêng với trạng thái xử lý đơn.
- Khách tra cứu được đơn của mình; thông tin đơn không công khai cho người khác.
- Chức năng quản trị yêu cầu đăng nhập và kiểm tra quyền.
- Mật khẩu và thông tin cấu hình bí mật không xuất hiện trong repo công khai.
- Các thao tác chính sử dụng được trên điện thoại và máy tính.
- Chạy thử trọn vẹn quy trình với quán và khách thật trước khi nghiệm thu.

## 8. Ràng buộc và rủi ro
- Dự án do một người thực hiện, đang học nền tảng web.
- Thời gian hoàn thành theo lịch học phần.
- Cần kiểm tra và hiểu code do công cụ AI hỗ trợ tạo.
- Việc nhận và giao món phụ thuộc thỏa thuận với quán.
- Thực đơn, giá và tình trạng còn/hết món cần được cập nhật kịp thời.
- Cần thống nhất cách xử lý đơn hủy và khách không đến nhận.

## 9. Những việc cần xác nhận
- Giảng viên duyệt đề tài và phạm vi.
- Giảng viên có chấp nhận chuyển tính năng AI sang giai đoạn sau không?
- Quán hợp tác, thực đơn và giá thực tế.
- Khung giờ, điểm nhận món và người phụ trách giao/nhận.
- Quy định xác nhận, hủy đơn và xử lý khách không đến nhận.
- Hạn nộp và thông tin VPS được cấp.
