# B4 — Backlog Sprint 0

## 1. Mục tiêu
Chuẩn bị cách làm việc, rà soát phạm vi và có bản mẫu
để trình bày ý tưởng website đặt đồ ăn cho sinh viên VJU.

- Người phụ trách toàn bộ công việc: Lâm Hải Sơn — 23110216.
- Quỹ thời gian dự kiến: 6 buổi, mỗi buổi 2 giờ.
- Tổng: 10 giờ công việc và 2 giờ dự phòng.
- Đây là kế hoạch; trạng thái được cập nhật theo kết quả thực tế.
- Bản mẫu dùng dữ liệu giả, chưa nhận đơn thật.

## 2. Danh sách công việc

| Mã | Công việc | Ưu tiên | Giờ | Phụ thuộc | Tiêu chí hoàn thành | Trạng thái |
|---|---|---|---:|---|---|---|
| S0-01 | Ghi phân vai và cách làm việc | Must | 1 | Không | Có bảng phân vai, cách theo dõi và điều kiện Done | Doing |
| S0-02 | Rà soát Charter và yêu cầu MVP đã có | Must | 1 | S0-01 | Thống nhất một quán, không AI; ghi rõ các điểm còn cần xác nhận | To do |
| S0-03 | Chuẩn bị câu hỏi trao đổi với quán | Must | 1 | S0-02 | Có câu hỏi về món, giá, giờ nhận, hủy đơn và thanh toán | To do |
| S0-04 | Rà soát môi trường phát triển | Must | 1 | S0-02 | Ghi phiên bản công cụ và cách chạy bản demo trên máy | To do |
| S0-05 | Dựng bản mẫu luồng đặt món | Must | 3 | S0-02 | Minh họa thực đơn, giỏ hàng và xác nhận đơn bằng dữ liệu giả | To do |
| S0-06 | Kiểm tra bản mẫu và lưu ảnh | Must | 1 | S0-04, S0-05 | Mở được demo, kiểm tra luồng chính và có ảnh minh chứng | To do |
| S0-07 | Demo ý tưởng và ghi nhận phản hồi | Must | 1 | S0-06 | Có kịch bản demo; ghi phản hồi thực tế hoặc ghi rõ chưa nhận phản hồi | To do |
| S0-08 | Chọn việc cho sprint tiếp theo | Must | 1 | S0-07 | Có danh sách ưu tiên tiếp theo, điều chỉnh theo phản hồi nếu có | To do |

## 3. Câu hỏi cần trao đổi với quán
- Những món nào sẽ bán, giá và ảnh thực tế là gì?
- Ai cập nhật món còn/hết và tiếp nhận đơn?
- Khung giờ đặt và nhận món như thế nào?
- Điểm nhận món ở đâu?
- Khi nào được hủy đơn? Xử lý khách không đến nhận ra sao?
- Ai xác nhận đã thu tiền khi khách nhận món?

Việc chuẩn bị câu hỏi không đồng nghĩa đã có thỏa thuận với quán.
Nếu chưa nhận được phản hồi, demo tiếp tục dùng dữ liệu giả
và các giả định phải được ghi rõ.

## 4. Kết quả cần có cuối Sprint 0
- Bảng phân vai và cách làm việc.
- Backlog có ưu tiên, ước lượng và tiêu chí hoàn thành.
- Bản mẫu ý tưởng kèm hướng dẫn mở và ảnh minh chứng.
- Ghi nhận phản hồi hoặc các câu hỏi còn đang chờ.
- Danh sách công việc đề xuất cho sprint tiếp theo.

## 5. Hướng dự kiến cho sprint tiếp theo
Ưu tiên làm luồng xem thực đơn:
- Khởi tạo backend FastAPI và cơ sở dữ liệu SQLite.
- Tạo dữ liệu món mẫu.
- Xây dựng API đọc thực đơn.
- Kết nối giao diện thực đơn với API.
- Viết kiểm thử và demo luồng xem món.

Chỉ chọn khối lượng phù hợp quỹ thời gian một người.
Các phần đặt đơn và quản trị được phân bổ ở những sprint sau.

## 6. Cập nhật tiến độ
Chuyển To do → Doing khi bắt đầu.
Chỉ chuyển Done khi đạt tiêu chí, đã kiểm tra và có commit/link bằng chứng.
Ghi riêng trạng thái chờ review và các trở ngại.
