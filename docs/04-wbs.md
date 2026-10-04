# WBS — Cấu trúc phân rã công việc

## 1. Thông tin chung
- Dự án: Website đặt đồ ăn cho sinh viên VJU.
- Người thực hiện: Lâm Hải Sơn.
- Phạm vi: bản đầu phục vụ một quán, chưa tích hợp AI.
- WBS được tổ chức theo sản phẩm bàn giao.
- Lịch, thời lượng và quan hệ phụ thuộc được lập trong tài liệu riêng.

## 2. Cấu trúc WBS

### 1.0. Website đặt đồ ăn cho sinh viên VJU

#### 1.1. Hồ sơ và quản lý dự án
- 1.1.1. Bản mô tả dự án và phạm vi.
- 1.1.2. Danh sách yêu cầu, User Story và mức ưu tiên.
- 1.1.3. Bản thiết kế kiến trúc, API và cơ sở dữ liệu.
- 1.1.4. WBS, bảng ước lượng, sơ đồ Gantt và đường găng.
- 1.1.5. Quy trình phát triển, backlog và nhật ký tiến độ.
- 1.1.6. Hồ sơ xác nhận thực đơn, giá và quy trình phối hợp với quán.

#### 1.2. Nền tảng kỹ thuật và dữ liệu
- 1.2.1. Repo, cấu trúc mã nguồn và cấu hình môi trường mẫu.
- 1.2.2. Cấu trúc cơ sở dữ liệu và quy trình khởi tạo.
- 1.2.3. Dữ liệu mẫu: món, điểm nhận, khung giờ và tài khoản quản trị.
- 1.2.4. Kết nối backend với cơ sở dữ liệu.

#### 1.3. Backend và API
- 1.3.1. API thực đơn và lựa chọn nhận món.
- 1.3.2. Xác thực quản trị, phiên đăng nhập và kiểm tra quyền.
- 1.3.3. API thêm, sửa, ẩn món và cập nhật tình trạng món.
- 1.3.4. Xử lý kiểm tra giỏ hàng, giá và tính tổng tiền.
- 1.3.5. API tạo đơn, lưu chi tiết và chống tạo đơn trùng.
- 1.3.6. API tra cứu đơn bằng thông tin tra cứu hợp lệ.
- 1.3.7. API danh sách và chi tiết đơn cho quản trị.
- 1.3.8. API chuyển trạng thái đơn và ghi nhận thanh toán.

#### 1.4. Giao diện khách hàng
- 1.4.1. Bố cục chung và trang thực đơn.
- 1.4.2. Tìm kiếm và lọc món.
- 1.4.3. Giỏ hàng và điều chỉnh số lượng.
- 1.4.4. Biểu mẫu đặt hàng, chọn giờ/điểm nhận và ghi chú.
- 1.4.5. Trang xác nhận thành công và thông tin tra cứu.
- 1.4.6. Trang theo dõi đơn.
- 1.4.7. Kết nối API và xử lý trạng thái tải, rỗng, lỗi.
- 1.4.8. Giao diện thích ứng với điện thoại.

#### 1.5. Giao diện quản trị
- 1.5.1. Trang đăng nhập và chức năng đăng xuất.
- 1.5.2. Trang quản lý thực đơn.
- 1.5.3. Trang danh sách và chi tiết đơn hàng.
- 1.5.4. Điều khiển trạng thái đơn và xác nhận thu tiền.
- 1.5.5. Kết nối API và hiển thị lỗi, thông báo kết quả.

#### 1.6. Kiểm thử và chất lượng
- 1.6.1. Danh sách tình huống và dữ liệu kiểm thử.
- 1.6.2. Kiểm thử tính tiền, dữ liệu đầu vào và chuyển trạng thái.
- 1.6.3. Kiểm thử API, quyền truy cập và chống tạo đơn trùng.
- 1.6.4. Kiểm thử toàn bộ luồng đặt, xử lý và nhận món.
- 1.6.5. Kiểm thử giao diện điện thoại và xử lý lỗi.
- 1.6.6. Kết quả kiểm tra tốc độ, tải dự kiến và độ bền dữ liệu.
- 1.6.7. Danh sách lỗi và kết quả kiểm thử lại.

#### 1.7. Triển khai và vận hành thử
- 1.7.1. Bản triển khai trên VPS với HTTPS và cấu hình riêng.
- 1.7.2. Quy trình cập nhật phiên bản và quay lại bản trước.
- 1.7.3. Quy trình sao lưu và kết quả thử khôi phục dữ liệu.
- 1.7.4. Thực đơn, tài khoản và cấu hình nhận món thực tế.
- 1.7.5. Hướng dẫn sử dụng cho khách và quản trị viên.
- 1.7.6. Biên bản chạy thử với quán và khách, kèm phản hồi.

#### 1.8. Báo cáo và nghiệm thu
- 1.8.1. Báo cáo cuối kỳ và tài liệu thiết kế đã cập nhật.
- 1.8.2. Slide và kịch bản trình diễn.
- 1.8.3. Hồ sơ nghiệm thu đối chiếu các tiêu chí đã đặt ra.

## 3. Tiêu chí hoàn thành các nhóm bàn giao

| Mã | Nhóm bàn giao | Điều kiện hoàn thành |
|---|---|---|
| 1.1 | Hồ sơ và quản lý | Tài liệu nhất quán, có phạm vi, thứ tự ưu tiên và các điểm cần xác nhận |
| 1.2 | Nền tảng và dữ liệu | Khởi tạo được dự án, cơ sở dữ liệu và dữ liệu mẫu theo hướng dẫn |
| 1.3 | Backend | API đáp ứng yêu cầu, lưu dữ liệu đúng và kiểm tra quyền tại backend |
| 1.4 | Giao diện khách | Khách thực hiện được luồng đặt và tra cứu đơn trên máy tính, điện thoại |
| 1.5 | Giao diện quản trị | Quản trị viên đăng nhập, cập nhật món và xử lý đơn được |
| 1.6 | Kiểm thử | Có bằng chứng kiểm thử; các lỗi chặn luồng chính và lỗi truy cập trái phép đã được xử lý |
| 1.7 | Triển khai | Web chạy trên VPS, có sao lưu và hoàn thành thử nghiệm vận hành |
| 1.8 | Nghiệm thu | Báo cáo, slide và minh chứng đáp ứng phạm vi đã được duyệt |

## 4. Quy tắc 100% và ranh giới công việc
- Các nhánh bao quát toàn bộ phạm vi bản đầu: quản lý, thiết kế,
  xây dựng, kiểm thử, triển khai và nghiệm thu.
- Mỗi sản phẩm bàn giao có một vị trí chính trong WBS.
- Nhánh dữ liệu chịu trách nhiệm cấu trúc và khởi tạo dữ liệu.
- Nhánh backend chịu trách nhiệm xử lý nghiệp vụ và cung cấp API.
- Nhánh giao diện chịu trách nhiệm hiển thị và gọi API.
- Nhánh kiểm thử chịu trách nhiệm tình huống kiểm thử, bằng chứng
  và theo dõi lỗi; sửa mã nguồn vẫn thuộc phần chức năng tương ứng.
- Những chức năng ngoài phạm vi không được đưa vào lịch bản đầu.

## 5. Ánh xạ yêu cầu sang WBS

| Yêu cầu | Gói công việc liên quan |
|---|---|
| US01 — Xem thực đơn | 1.3.1, 1.4.1 |
| US02 — Tìm kiếm, lọc món | 1.3.1, 1.4.2 |
| US03 — Giỏ hàng | 1.4.3 |
| US04 — Đặt món | 1.3.4, 1.3.5, 1.4.4, 1.4.5 |
| US05 — Tra cứu đơn | 1.3.6, 1.4.6 |
| US06 — Đăng nhập quản trị | 1.3.2, 1.5.1 |
| US07 — Quản lý món | 1.3.3, 1.5.2 |
| US08 — Xem đơn quản trị | 1.3.7, 1.5.3 |
| US09 — Cập nhật trạng thái | 1.3.8, 1.5.4 |
| US10 — Ghi nhận thanh toán | 1.3.8, 1.5.4 |
| US11 — Ghi chú đơn | 1.3.5, 1.4.4 |

Các chức năng lịch sử đơn trong tài khoản, AI và thanh toán
trực tuyến tự động chưa được phân bổ công việc trong bản đầu.

## 6. Cách sử dụng WBS
- Mỗi gói công việc sẽ được chuyển thành một hoặc nhiều việc
  có thời lượng, quan hệ phụ thuộc và tiêu chí hoàn thành.
- Khi ước lượng, gói nào vượt hai ngày làm việc sẽ được tách nhỏ hơn.
- Lịch phải phù hợp với số giờ làm thực tế mỗi ngày của một người.
- Không mặc định frontend và backend được làm song song.
- Khi thay đổi phạm vi, cập nhật yêu cầu, WBS và lịch tương ứng.
