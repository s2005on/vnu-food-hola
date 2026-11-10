# B5 — Risk register

## 1. Thông tin
- Dự án: Website đặt đồ ăn cho sinh viên VJU.
- Người thực hiện: Lâm Hải Sơn — MSSV 23110216.
- Phạm vi: một quán, thanh toán tiền mặt, không tích hợp AI.
- Ngày lập: 22/10/2026.
- Đây là đánh giá dự kiến cho sản phẩm sẽ xây dựng.
- Các hành động bên dưới là kế hoạch, chưa được coi là đã kiểm chứng.

## 2. Thang đánh giá trước kiểm soát

Đánh giá khả năng xảy ra trong thời gian thực hiện đồ án:
- Xác suất P: 1 = thấp, 2 = trung bình, 3 = cao.
- Tác động I:
  - 1 = nhỏ: sửa trong một buổi, không chặn luồng chính.
  - 2 = vừa: cần 2–3 buổi sửa hoặc làm gián đoạn một chức năng.
  - 3 = lớn: sai tiền, lộ/mất dữ liệu hoặc chặn nghiệm thu.
- Điểm ưu tiên = P × I.
- 1–2: thấp; 3–4: trung bình; 6–9: cao.

P và I dưới đây được chấm TRƯỚC khi áp dụng biện pháp kiểm soát.
Đây là ước lượng ban đầu, không phải số liệu thống kê.

## 3. Danh sách rủi ro

| Mã | Nhóm | Nguyên nhân → Sự kiện có thể xảy ra → Hậu quả | P | I | Điểm / Ưu tiên |
|---|---|---|---:|---:|---|
| R1 | Kỹ thuật / sản phẩm | Tin giá do trình duyệt gửi hoặc không lưu giá tại lúc đặt → Đơn bị tính sai hoặc đổi tổng tiền sau khi sửa giá món → Khách và quán tranh chấp số tiền | 2 | 3 | 6 / Cao |
| R2 | Kỹ thuật / sản phẩm | Mạng chậm, khách bấm nhiều lần và backend chưa chống trùng → Một yêu cầu tạo nhiều đơn → Quán chuẩn bị thừa và khách bị ghi nhận nhiều đơn | 3 | 2 | 6 / Cao |
| R3 | Kỹ thuật / sản phẩm | Thiếu kiểm tra quyền ở backend hoặc tra cứu chỉ bằng mã dễ đoán → Người không có quyền xem/sửa đơn → Lộ thông tin khách và sai trạng thái đơn | 2 | 3 | 6 / Cao |
| R4 | Kỹ thuật / vận hành | Chưa có bản sao lưu đã thử khôi phục, dữ liệu chỉ nằm trên VPS → Khi lỗi triển khai hoặc VPS bị đặt lại, dữ liệu không khôi phục được → Mất đơn và gián đoạn chạy thử | 2 | 3 | 6 / Cao |
| R5 | Con người | Một người kiêm nhiều việc và chưa quen công nghệ → Ước lượng thiếu, công việc bị dồn → Chậm tiến độ và thiếu thời gian kiểm thử | 3 | 2 | 6 / Cao |
| R6 | Phạm vi / phối hợp | Chưa thống nhất quy trình với quán và tiếp nhận thêm yêu cầu không đánh giá → Phạm vi mở rộng hoặc phải sửa luồng nhận món → Làm lại chức năng và trễ kế hoạch | 3 | 2 | 6 / Cao |

## 4. Kế hoạch ứng phó

### R1 — Sai tiền
- Chiến lược: giảm thiểu.
- Hành động: tính tổng tại backend từ giá trong CSDL; lưu giá
  từng món tại thời điểm đặt; kiểm tra số lượng nguyên dương.
- Thời điểm: trước khi hoàn thành API tạo đơn.
- Dấu hiệu kích hoạt: tổng tiền khác kết quả tính tay hoặc đơn cũ
  thay đổi khi cập nhật giá thực đơn.
- Khi xảy ra: tạm dừng nhận đơn qua chức năng bị lỗi,
  đối chiếu các đơn ảnh hưởng, sửa và kiểm thử lại.
- Phụ trách: Lâm Hải Sơn.
- Trạng thái: mở — đã lập kế hoạch, chưa kiểm chứng trên backend.

### R2 — Đơn trùng
- Chiến lược: giảm thiểu.
- Hành động: dùng khóa chống trùng và ràng buộc duy nhất trong
  CSDL; kiểm thử gửi lại cùng yêu cầu, kể cả gửi đồng thời.
  Nút đặt hàng bị khóa khi đang gửi chỉ là hỗ trợ giao diện.
- Thời điểm: trước khi chạy thử luồng đặt đơn.
- Dấu hiệu kích hoạt: cùng khóa yêu cầu xuất hiện nhiều đơn.
- Khi xảy ra: đối chiếu với quán, xử lý đơn dư có ghi nhận,
  sửa cơ chế chống trùng trước khi mở lại luồng.
- Phụ trách: Lâm Hải Sơn.
- Trạng thái: mở — chưa triển khai và kiểm chứng.

### R3 — Truy cập trái phép
- Chiến lược: giảm thiểu.
- Hành động: kiểm tra phiên trên API quản trị; yêu cầu mã tra cứu
  bí mật cho khách; không ghi bí mật vào URL hoặc log;
  kiểm thử yêu cầu không đăng nhập và mã tra cứu sai.
- Thời điểm: trước khi đưa dữ liệu khách thật vào hệ thống.
- Dấu hiệu kích hoạt: yêu cầu không có quyền vẫn đọc hoặc sửa được đơn.
- Khi xảy ra: khóa chức năng bị ảnh hưởng, thu hồi phiên/mã bị lộ,
  xác định dữ liệu ảnh hưởng và báo người liên quan.
- Phụ trách: Lâm Hải Sơn.
- Trạng thái: mở — chưa kiểm chứng quyền truy cập.

### R4 — Mất dữ liệu
- Chiến lược: giảm thiểu.
- Hành động: sao lưu CSDL trước mỗi lần cập nhật và hằng ngày
  khi vận hành thử; giữ bản sao ngoài VPS trong nơi hạn chế truy cập;
  thử khôi phục trên môi trường riêng.
- Thời điểm: trước lần vận hành có dữ liệu thật.
- Dấu hiệu kích hoạt: không đọc được CSDL hoặc thiếu đơn sau cập nhật.
- Khi xảy ra: ngừng ghi dữ liệu, khôi phục bản sao đã kiểm tra,
  đối chiếu các đơn phát sinh sau thời điểm sao lưu.
- Phụ trách: Lâm Hải Sơn.
- Trạng thái: mở — chưa có bằng chứng thử khôi phục.

### R5 — Quá tải cá nhân
- Chiến lược: giảm thiểu.
- Hành động: chia việc thành 1–2 buổi; chỉ làm một việc chính
  tại một thời điểm; ghi giờ thực tế; rà soát tiến độ mỗi tuần.
- Thời điểm: từ đầu mỗi sprint.
- Dấu hiệu kích hoạt: một việc vượt ước lượng hơn hai buổi
  hoặc công việc chưa xong bị chuyển sang tuần tiếp theo.
- Khi xảy ra: ước lượng lại, dùng quỹ dự phòng, hoãn chức năng
  Should và trao đổi giảng viên nếu mốc hoàn thành bị ảnh hưởng.
- Phụ trách: Lâm Hải Sơn.
- Trạng thái: mở — cần theo dõi qua nhật ký tiến độ.

### R6 — Thay đổi phạm vi
- Chiến lược: né tránh mở rộng ngoài MVP và giảm thiểu hiểu sai.
- Hành động: ghi rõ một quán, tiền mặt, không AI; xác nhận
  giờ nhận, điểm nhận và quy định hủy với quán; mọi yêu cầu mới
  phải đánh giá ảnh hưởng tới WBS và lịch trước khi nhận làm.
- Thời điểm: trước khi triển khai luồng nghiệp vụ liên quan.
- Dấu hiệu kích hoạt: xuất hiện yêu cầu ngoài phạm vi hoặc
  quy trình quán khác với giả định trong tài liệu.
- Khi xảy ra: đưa yêu cầu mới vào backlog, thống nhất ưu tiên,
  cập nhật tài liệu và lịch; chưa tự động đưa vào sprint đang làm.
- Phụ trách: Lâm Hải Sơn.
- Trạng thái: mở — đang chờ xác nhận quy trình với quán.

## 5. Theo dõi
- Rà soát cuối mỗi tuần và trước khi demo hoặc triển khai.
- Ưu tiên xử lý R1, R3, R4 trước khi dùng dữ liệu thật;
  R2 trước khi thử đặt đơn; R5 và R6 theo dõi xuyên suốt.
- Sau khi có bằng chứng kiểm soát, đánh giá lại P và I còn lại.
- Chưa có bằng chứng thì không tự hạ điểm rủi ro.
- Mỗi lần cập nhật ghi ngày, thay đổi, người phụ trách và link bằng chứng.
- Không đưa mật khẩu, mã phiên hoặc thông tin khách thật vào tài liệu.
