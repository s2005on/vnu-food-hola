# B5 — Kế hoạch chất lượng

## 1. Thông tin
- Dự án: Website đặt đồ ăn cho sinh viên VJU.
- Người phụ trách: Lâm Hải Sơn — MSSV 23110216.
- Ngày lập: 22/10/2026.
- Phạm vi: một quán, thanh toán tiền mặt, không tích hợp AI.
- Trạng thái: kế hoạch kiểm tra cho sản phẩm sẽ xây dựng.
- B5 chưa yêu cầu triển khai API hoặc CSDL thật.

QA là các hoạt động phòng ngừa lỗi trong quá trình làm.
QC là kiểm tra sản phẩm và đối chiếu kết quả với ngưỡng đạt.

## 2. Q1 — Tính đúng tiền và kiểm tra đầu vào
- Rủi ro liên quan: R1.
- Người phụ trách: Lâm Hải Sơn.
- Ngưỡng đạt:
  - Đạt cả 8 ca QC bên dưới.
  - Tổng tiền lệch 0 VND so với kết quả tính tay.
  - Yêu cầu không hợp lệ không tạo bản ghi đơn.
- QA:
  - Tiền dùng số nguyên VND.
  - Backend lấy giá từ CSDL và lưu giá tại thời điểm đặt.
  - Viết test cho dữ liệu hợp lệ, biên và không hợp lệ.
- QC:
  1. Món 30.000 VND × 2: tổng 60.000 VND.
  2. Món 30.000 × 2 và 15.000 × 1: tổng 75.000 VND.
  3. Giỏ rỗng: từ chối tạo đơn.
  4. Số lượng 0: từ chối tạo đơn.
  5. Số lượng -1: từ chối tạo đơn.
  6. Số lượng 1,5: từ chối tạo đơn.
  7. Sửa giá gửi từ trình duyệt xuống 1 VND: không tạo đơn
     với giá bị sửa; nếu lệch giá hiện tại, yêu cầu xác nhận lại.
  8. Đổi giá thực đơn sau khi đặt: giá và tổng đơn cũ giữ nguyên.
- Thời điểm: khi hoàn thành API tạo đơn và sau mỗi lần sửa logic tiền.
- Bằng chứng dự kiến: báo cáo pytest, dữ liệu mẫu và kết quả
  API/CSDL của 8 ca; ghi commit được kiểm tra.
- Trạng thái: chưa kiểm tra trên backend đồ án.
- Ghi chú: bài HW3 tính tổng tiền là bài tập độc lập,
  không thay thế kiểm thử API và CSDL của đồ án.

## 3. Q2 — Quyền quản trị và bảo mật thông tin đơn
- Rủi ro liên quan: R3.
- Người phụ trách: Lâm Hải Sơn.
- Ngưỡng đạt:
  - Đạt cả 6 ca QC bên dưới.
  - Không ca truy cập trái phép nào trả thông tin khách
    hoặc làm thay đổi dữ liệu.
- QA:
  - Kiểm tra quyền tại backend, không chỉ ẩn nút trên giao diện.
  - Mã đơn đi kèm mã tra cứu bí mật.
  - Không đưa bí mật vào URL, repo hoặc log.
  - Mật khẩu quản trị được lưu bằng hàm băm mật khẩu phù hợp.
- QC:
  1. Chưa đăng nhập gọi API danh sách đơn quản trị: bị từ chối.
  2. Chưa đăng nhập gọi API đổi trạng thái: bị từ chối,
     trạng thái trong CSDL không đổi.
  3. Dùng phiên đã đăng xuất: bị từ chối.
  4. Tra cứu bằng mã đơn nhưng thiếu mã bí mật: không thấy dữ liệu đơn.
  5. Dùng mã bí mật của đơn A để tra cứu đơn B: không thấy dữ liệu đơn B.
  6. Mã đơn và mã bí mật hợp lệ: chỉ nhận thông tin đơn tương ứng.
- Thời điểm: trước khi dùng dữ liệu thật và sau khi sửa xác thực.
- Bằng chứng dự kiến: báo cáo test API, mã trạng thái HTTP,
  đối chiếu CSDL trước/sau; dùng khách giả và che bí mật.
- Trạng thái: chưa kiểm tra.

## 4. Q3 — Chống tạo đơn trùng
- Rủi ro liên quan: R2.
- Người phụ trách: Lâm Hải Sơn.
- Ngưỡng đạt:
  - Gửi tuần tự 10 lần cùng khóa và nội dung: chỉ có 1 đơn.
  - Gửi đồng thời 10 lần cùng khóa và nội dung: chỉ có 1 đơn.
  - Cùng khóa nhưng nội dung khác: bị từ chối, đơn cũ không đổi.
  - Gửi lại hợp lệ sau khi mất phản hồi: nhận lại mã đơn cũ
    và tiếp tục tra cứu được.
- QA:
  - Ràng buộc duy nhất cho khóa chống trùng trong CSDL.
  - Lưu đơn và chi tiết trong cùng giao dịch.
  - Kiểm tra quyền và nội dung trước khi trả đơn đã có.
  - Khóa nút trong lúc gửi chỉ là biện pháp hỗ trợ giao diện.
- QC:
  1. Gửi lặp tuần tự rồi đếm đơn và dòng chi tiết trong CSDL.
  2. Gửi lặp đồng thời rồi kiểm tra không có bản ghi dư.
  3. Thay số lượng nhưng giữ khóa cũ; kiểm tra lỗi và dữ liệu không đổi.
  4. Mô phỏng mất phản hồi sau khi server đã lưu, gửi lại
     và thử tra cứu đơn bằng thông tin hợp lệ.
- Thời điểm: trước khi chạy thử luồng đặt đơn với quán.
- Bằng chứng dự kiến: script gửi yêu cầu, báo cáo kết quả,
  số bản ghi trước/sau và commit được kiểm tra.
- Trạng thái: chưa kiểm tra.

## 5. Q4 — Sao lưu và khôi phục dữ liệu
- Rủi ro liên quan: R4.
- Người phụ trách: Lâm Hải Sơn.
- Ngưỡng đạt:
  - Khôi phục được bộ dữ liệu mẫu gồm 10 đơn và toàn bộ
    dòng chi tiết tương ứng trong tối đa 30 phút.
  - Mã đơn, tổng tiền và trạng thái của cả 10 đơn khớp bản sao lưu.
  - Khi vận hành thử: bản sao lưu gần nhất không quá 24 giờ,
    đồng thời có bản sao trước mỗi lần cập nhật.
- QA:
  - Viết hướng dẫn sao lưu và khôi phục.
  - Dùng cách sao lưu nhất quán với CSDL đang hoạt động.
  - Giữ bản sao ngoài VPS, hạn chế người có quyền truy cập.
  - Thử khôi phục trên môi trường riêng.
- QC:
  1. Tạo 10 đơn mẫu và lưu số liệu đối chiếu.
  2. Tạo bản sao lưu, ghi thời điểm.
  3. Khôi phục vào CSDL thử nghiệm riêng và đo thời gian.
  4. Đối chiếu 10 đơn, chi tiết, tổng tiền và trạng thái.
- Thời điểm: trước khi có dữ liệu thật và sau khi đổi cách lưu dữ liệu.
- Bằng chứng dự kiến: biên bản thời gian, bảng đối chiếu,
  log đã che thông tin nhạy cảm; không đưa CSDL thật lên GitHub.
- Trạng thái: chưa kiểm tra.
- Giới hạn: dữ liệu phát sinh sau lần sao lưu gần nhất có thể
  phải đối chiếu lại; không cam kết khôi phục các đơn chưa được sao lưu.

## 6. Q5 — Khả năng sử dụng trên điện thoại và máy tính
- Người phụ trách: Lâm Hải Sơn.
- Ngưỡng đạt:
  - Hoàn thành luồng xem món → giỏ hàng → đặt đơn → tra cứu
    ở cả hai kích thước 375 × 812 và 1366 × 768.
  - Không cuộn ngang toàn trang, không có nút chính bị che.
  - Giỏ rỗng và thiếu thông tin bắt buộc đều có xử lý rõ ràng.
- QA:
  - Thiết kế responsive, nhãn trường dễ hiểu và thông báo lỗi cụ thể.
  - Kiểm tra giao diện sau mỗi thay đổi luồng chính.
- QC:
  1. Thực hiện toàn bộ luồng ở kích thước điện thoại.
  2. Lặp lại ở kích thước máy tính.
  3. Thử đặt khi giỏ rỗng và khi thiếu trường bắt buộc.
  4. Kiểm tra thông báo khi API lỗi hoặc mất mạng.
- Thời điểm: khi tích hợp frontend với backend và trước demo nghiệm thu.
- Bằng chứng dự kiến: ảnh/video, kích thước màn hình,
  phiên bản trình duyệt, danh sách ca kiểm tra và commit.
- Trạng thái: chưa kiểm tra trên sản phẩm tích hợp.
- Ghi chú: ảnh demo B4 chỉ chứng minh thao tác trên bản mẫu,
  không chứng minh luồng backend hay tra cứu đơn thật.

## 7. Ghi nhận kết quả và xử lý lỗi
Mỗi lần kiểm tra ghi:
- Ngày, người kiểm tra và commit.
- Môi trường, dữ liệu và mã ca kiểm tra.
- Kết quả mong đợi và thực tế.
- Đạt hoặc không đạt; link bằng chứng.
- Lỗi phát hiện, cách sửa và kết quả chạy lại.

Nếu sai tiền, lộ dữ liệu, mất dữ liệu hoặc tạo đơn trùng:
chưa cho phép vận hành thật cho tới khi sửa và kiểm tra lại đạt.

Rà soát kế hoạch cuối mỗi sprint.
Chỉ đổi trạng thái sang đã đạt khi có kết quả thực tế.
Không dùng việc tự kiểm tra để tuyên bố đã có review độc lập.
