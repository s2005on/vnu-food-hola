# Yêu cầu hệ thống và phạm vi MVP

## 1. Người sử dụng
- Khách hàng: sinh viên xem món, đặt hàng và nhận món.
- Quản trị viên: người được phân công quản lý thực đơn và xử lý đơn.

## 2. Quy ước mức ưu tiên
- Must: bắt buộc có trong bản đầu.
- Should: nên có, thực hiện sau các chức năng Must.
- Could: bổ sung nếu còn thời gian.
- Won't: không thực hiện trong bản đầu.

## 3. User Story

User Story mô tả nhu cầu theo mẫu:
“Là [vai trò], tôi muốn [chức năng], để [mục đích].”

| Mã | User Story | Ưu tiên |
|---|---|---|
| US01 | Là khách hàng, tôi muốn xem thực đơn kèm ảnh, giá và tình trạng còn món để lựa chọn. | Must |
| US02 | Là khách hàng, tôi muốn tìm kiếm và lọc món theo loại để tìm món nhanh hơn. | Should |
| US03 | Là khách hàng, tôi muốn thêm, xóa và đổi số lượng món trong giỏ để điều chỉnh đơn. | Must |
| US04 | Là khách hàng, tôi muốn nhập thông tin liên hệ, chọn giờ và điểm nhận để đặt món. | Must |
| US05 | Là khách hàng, tôi muốn nhận mã đơn và tra cứu trạng thái đơn của mình để biết khi nào nhận món. | Must |
| US06 | Là quản trị viên, tôi muốn đăng nhập để truy cập chức năng quản lý. | Must |
| US07 | Là quản trị viên, tôi muốn thêm, sửa, ẩn món và cập nhật giá, tình trạng còn/hết để quản lý thực đơn. | Must |
| US08 | Là quản trị viên, tôi muốn xem đơn mới và chi tiết từng đơn để chuẩn bị món. | Must |
| US09 | Là quản trị viên, tôi muốn xác nhận, hủy và cập nhật trạng thái đơn để quản lý quá trình phục vụ. | Must |
| US10 | Là quản trị viên, tôi muốn ghi nhận đã thu tiền để theo dõi thanh toán. | Must |
| US11 | Là khách hàng, tôi muốn ghi chú cho đơn để thông báo yêu cầu khi chuẩn bị món. | Should |
| US12 | Là khách hàng, tôi muốn xem lịch sử đơn trong tài khoản để thuận tiện đặt lại. | Could |
| US13 | Là khách hàng, tôi muốn AI gợi ý món theo ngân sách và sở thích để dễ lựa chọn. | Won't |
| US14 | Là khách hàng, tôi muốn thanh toán trực tuyến và được xác nhận tự động để thuận tiện thanh toán. | Won't |

## 4. Phạm vi MVP
MVP là bản nhỏ nhất có thể phục vụ một lượt đặt và nhận món thực tế.

MVP gồm các User Story mức Must:
US01, US03, US04, US05, US06, US07, US08, US09, US10.

Chức năng tìm kiếm, lọc món và ghi chú vẫn nằm trong kế hoạch
bản đầu, nhưng được thực hiện sau khi luồng Must chạy ổn định.

AI và thanh toán trực tuyến tự động để giai đoạn sau.
Việc chuyển AI sang giai đoạn sau cần được giảng viên xác nhận.

## 5. Quy tắc nghiệp vụ

### 5.1. Thực đơn và giỏ hàng
- Chỉ đặt được món đang bán và còn hàng.
- Số lượng mỗi món phải là số nguyên dương.
- Giỏ hàng phải có ít nhất một món mới được đặt.
- Backend kiểm tra lại giá và tình trạng món khi nhận yêu cầu đặt đơn.
- Nếu giá thay đổi, thông báo để khách xác nhận lại trước khi tạo đơn.
- Tổng tiền do backend tính, không lấy số tiền khách gửi lên làm căn cứ.

### 5.2. Đặt và nhận món
- Khách cung cấp họ tên và số điện thoại liên hệ.
- Khách chọn khung giờ và điểm nhận do quán cung cấp.
- Mỗi đơn được tạo thành công có một mã đơn riêng.
- Lưu giá từng món tại thời điểm đặt.
- Thay đổi giá thực đơn không làm thay đổi tổng tiền của đơn đã tạo.
- Chỉ thông báo đặt thành công khi đơn đã được lưu.
- Ngăn tạo đơn trùng khi khách bấm nút đặt nhiều lần.

### 5.3. Trạng thái đơn
Luồng chính:
Chờ xác nhận → Đã xác nhận → Đang chuẩn bị → Sẵn sàng nhận → Hoàn thành.

- Quản trị viên chỉ được chuyển trạng thái theo luồng hợp lệ.
- Đơn chưa hoàn thành có thể bị hủy theo quy định đã thống nhất với quán.
- Khi hủy, phải ghi nhận lý do.
- Đơn hoàn thành hoặc đã hủy không tiếp tục chuyển trạng thái
  trong phạm vi bản đầu.

### 5.4. Thanh toán
- Bản đầu thanh toán tiền mặt khi nhận món.
- Trạng thái thanh toán: Chưa thanh toán hoặc Đã thanh toán.
- Trạng thái thanh toán được lưu riêng với trạng thái xử lý đơn.
- Chỉ quản trị viên được xác nhận đã thu tiền.
- Đơn chỉ hoàn thành khi đã giao món và ghi nhận đã thanh toán.

### 5.5. Quyền truy cập
- Khách không bắt buộc tạo tài khoản trong MVP.
- Khách tra cứu đơn bằng mã đơn kèm mã tra cứu bí mật riêng.
- Không dùng mã đơn tăng dần làm căn cứ duy nhất để xem thông tin đơn.
- Chức năng quản trị phải được kiểm tra quyền tại backend.
- Không công khai danh sách đơn và thông tin liên hệ của khách.

## 6. Yêu cầu phi chức năng
- Giao diện sử dụng được trên điện thoại và máy tính.
- Có thông báo khi đang tải, không có dữ liệu hoặc xảy ra lỗi.
- Dữ liệu đơn vẫn tồn tại sau khi tải lại trang hoặc khởi động lại ứng dụng.
- Mật khẩu quản trị được lưu bằng hàm băm mật khẩu phù hợp.
- Thông tin cấu hình bí mật không đưa vào repo công khai.
- Website triển khai thực tế sử dụng HTTPS.
- Có cách sao lưu và khôi phục cơ sở dữ liệu.
- Mục tiêu ban đầu: danh sách món tải trong khoảng 2 giây
  với dữ liệu mẫu và điều kiện mạng kiểm thử được ghi rõ.
- Mức tải cần phục vụ sẽ được xác nhận với quán và kiểm thử
  trước khi vận hành thực tế.

## 7. Tiêu chí kiểm tra MVP
- Khách đặt được một đơn hợp lệ và nhận được thông tin tra cứu.
- Đơn xuất hiện trong trang quản trị.
- Quản trị viên cập nhật trạng thái và khách nhìn thấy thay đổi.
- Thông tin đơn vẫn còn sau khi tải lại trang.
- Tổng tiền chính xác và giá đơn cũ không đổi khi sửa giá món.
- Yêu cầu đặt món hết hàng hoặc số lượng không hợp lệ bị từ chối.
- Bấm đặt nhiều lần không tạo nhiều đơn cho cùng một yêu cầu.
- Người chưa đăng nhập không truy cập được API quản trị.
- Người không có thông tin tra cứu hợp lệ không xem được đơn.
- Có thể hoàn thành luồng đặt → chuẩn bị → nhận món → thu tiền.

## 8. Các điểm còn cần xác nhận
- Thực đơn và quán hợp tác.
- Khung giờ, điểm nhận và cách giao món.
- Quy định hủy đơn và khách không đến nhận.
- Phạm vi đề tài được giảng viên duyệt.
