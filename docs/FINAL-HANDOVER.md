# Báo cáo tổng kết và bàn giao dự án

**Dự án:** VNU Food Hola  
**Học phần:** CSE3045 – Học theo dự án Khoa học và Kỹ thuật  
**Người thực hiện:** Lâm Hải Sơn · **MSSV:** 23110216  
**Ngày chốt hồ sơ:** 16/11/2026  
**Repository:** https://github.com/s2005on/vnu-food-hola  
**Demo đã kiểm tra:** https://sv27.bcse-vju.com/

## 1. Tóm tắt dự án

VNU Food Hola là website đặt món thử nghiệm dành cho sinh viên Trường Đại học Việt Nhật (VJU). Phiên bản MVP phục vụ một quán với thực đơn và dữ liệu mẫu, hỗ trợ khách xem món, đặt món, theo dõi đơn; phía quản trị tiếp nhận và cập nhật trạng thái đơn.

**Trạng thái bàn giao:** mã nguồn MVP đã được tích hợp; phiên bản chạy thử đã được kiểm tra trên SV27 ngày 15/11/2026 và có ảnh minh chứng. Đây là kết quả triển khai phục vụ học phần, không phải dịch vụ thương mại. Một số kiểm thử thủ công bổ sung và nghiệm thu cuối cùng của giảng viên chưa được xác nhận.

## 2. Chức năng đã xây dựng

### Khách hàng
- Xem thực đơn 16 món mẫu, tìm kiếm và lọc món.
- Thêm món vào giỏ, chọn số lượng, địa điểm và giờ nhận.
- Đăng ký tài khoản bằng họ tên, số điện thoại và mật khẩu; đăng nhập và xem lịch sử đơn theo tài khoản.
- Khách không đăng nhập vẫn có thể đặt món và tra cứu bằng mã đơn cùng mã bí mật.
- Theo dõi trạng thái xử lý đơn và thông tin thanh toán được hệ thống ghi nhận.

### Quản trị
- Đăng nhập khu vực quản trị.
- Quản lý món ăn, giá và tình trạng còn/hết.
- Xem đơn, xác nhận, chuyển sang chuẩn bị, sẵn sàng nhận, hoàn thành hoặc hủy đơn.
- Ghi nhận thanh toán tách biệt với trạng thái xử lý đơn.
- Xem nhật ký thay đổi trạng thái.

### Kiểm soát nghiệp vụ
- Backend tự tính tổng tiền từ dữ liệu món.
- Có kiểm tra dữ liệu đầu vào và cơ chế hạn chế tạo đơn trùng.
- Luồng demo dùng dữ liệu riêng, không thay thế dữ liệu quán chính.

## 3. Công nghệ và cấu trúc

| Thành phần | Công nghệ |
|---|---|
| Backend/API | Python, FastAPI |
| Cơ sở dữ liệu | SQLite |
| Giao diện | HTML, CSS, JavaScript |
| Chạy ứng dụng | Uvicorn |
| Reverse proxy | Nginx |
| Kiểm thử | Python unittest, Node.js test runner, GitHub Actions |
| Triển khai thử nghiệm | Ubuntu 24.04, systemd, VPS SV27 |

Các thư mục chính:
- `server/`: backend, giao diện hiện hành và dữ liệu mẫu.
- `tests/`: kiểm thử backend và JavaScript.
- `deploy/`: hướng dẫn triển khai, systemd, Nginx và backup.
- `docs/`: yêu cầu, thiết kế, kế hoạch, hồ sơ học phần và minh chứng.
- `demo/`: bản giao diện tĩnh của giai đoạn đầu.

## 4. Kết quả triển khai và kiểm thử đã ghi nhận

**Mốc kiểm tra:** 15/11/2026 · **Môi trường:** SV27, Ubuntu 24.04.

- Website được mở qua HTTPS tại https://sv27.bcse-vju.com/.
- Commit ứng dụng được ghi nhận trên VPS: `0eba90e451312ddfc5b57dff268322e4ddb8cf7e` (PR #14).
- Service `vju-food-23110216.service` được ghi nhận ở trạng thái `active` và `enabled` tại thời điểm chụp.
- API `/api/health` trả HTTP 200 và `{"ok":true}` tại thời điểm kiểm tra.
- Terminal ghi nhận 46 Python tests chạy thành công (`OK`).
- Luồng giao diện được quan sát bằng ảnh: khách xem thực đơn và lịch sử đơn; quản trị xử lý đơn đến trạng thái sẵn sàng; nhật ký ghi nhận thanh toán thử và hoàn thành; tài khoản khách hiển thị đơn hoàn thành.
- Bản sao SQLite có kết quả `PRAGMA integrity_check = ok`.

Các kết quả trên là bằng chứng của phiên kiểm tra ngày 15/11/2026, không phải cam kết trạng thái hiện tại của VPS hoặc khả năng hoạt động liên tục.

## 5. Bộ ảnh minh chứng

Bảy ảnh đã được đưa vào repository tại [docs/evidence/sv27-2026-11-15/](evidence/sv27-2026-11-15/README.md). Thông tin nhận dạng khách hàng, mã đơn và tên đăng nhập quản trị đã được che trước khi công bố.

1. [Trang chủ và thực đơn](evidence/sv27-2026-11-15/01-sv27-homepage.jpg)
2. [Lịch sử đơn phía khách – Chờ xác nhận](evidence/sv27-2026-11-15/02-customer-order-pending.jpg)
3. [Quản trị – đơn Sẵn sàng nhận](evidence/sv27-2026-11-15/03-admin-order-ready.jpg)
4. [Nhật ký xử lý đơn](evidence/sv27-2026-11-15/04-order-audit-log.jpg)
5. [Khách xem đơn Hoàn thành/Đã thanh toán](evidence/sv27-2026-11-15/05-customer-order-completed.jpg)
6. [46 kiểm thử Python, service và API health](evidence/sv27-2026-11-15/06-vps-tests-health.jpg)
7. [Kiểm tra tính toàn vẹn backup SQLite](evidence/sv27-2026-11-15/07-sqlite-backup-integrity.jpg)

## 6. Giới hạn và công việc chưa xác minh

| Hạng mục | Trạng thái |
|---|---|
| Kiểm thử thủ công bằng hai tài khoản khách để xác nhận cách ly lịch sử đơn | Chưa hoàn tất trên hosting |
| Đăng nhập trên thiết bị/trình duyệt thứ hai | Chưa kiểm thử thủ công |
| Kiểm tra giao diện trên điện thoại | Chưa thực hiện đầy đủ |
| Thử khôi phục SQLite từ bản backup | Chưa thực hiện; mới có `integrity_check = ok` |
| Tải lại/khởi động lại VPS và xác nhận dữ liệu còn nguyên | Chưa có biên bản kiểm thử thủ công |
| Truy cập độc lập từ mạng ngoài và uptime sau khi hết block VPS | Chưa xác minh |
| Video demo liên tục từ đặt món đến hoàn thành | Chưa có trong bộ minh chứng |
| Nghiệm thu cuối cùng của giảng viên | Chưa được xác nhận |

**Giới hạn sản phẩm:** chưa có thanh toán trực tuyến, OTP/SMS, chức năng khôi phục mật khẩu tự động, giao hàng qua shipper hoặc quản lý nhiều quán. Ghi nhận “Đã thanh toán” trong ảnh là thao tác kiểm thử, không phải chứng từ đã nhận tiền thật. VPS SV27 được cấp theo block nên không cam kết hoạt động 24/7. Dự án dùng dữ liệu mẫu; không dùng dữ liệu khách thật khi chưa có quy trình bảo vệ dữ liệu phù hợp.

## 7. Cách chạy và tài liệu liên quan

- Chạy trên Windows: [START-HERE.md](../START-HERE.md).
- Lưu ý nâng cấp và giữ dữ liệu: [START-V7.3.md](../START-V7.3.md).
- Kết quả kiểm chứng chi tiết: [VERIFICATION.md](../VERIFICATION.md).
- Hồ sơ giữa kỳ và bảng kiểm: [MIDTERM.md](MIDTERM.md).
- Hướng dẫn VPS: [deploy/README.md](../deploy/README.md).
- Mục lục tài liệu: [docs/README.md](README.md).
- Lịch sử thay đổi: [CHANGELOG.md](../CHANGELOG.md).

## 8. Minh bạch và trách nhiệm thực hiện

Một số công cụ AI được sử dụng để hỗ trợ phát triển và biên soạn tài liệu. Người thực hiện chịu trách nhiệm rà soát, kiểm thử, hiểu và giải thích phần mã nguồn cũng như các quyết định thiết kế của dự án. Dự án được thực hiện theo hình thức cá nhân; không ghi nhận review độc lập hoặc phê duyệt của giảng viên khi chưa có xác nhận thực tế.

---

**Kết luận:** VNU Food Hola đã có phiên bản MVP, mã nguồn, tài liệu kỹ thuật, kết quả kiểm thử và bộ ảnh ghi nhận triển khai SV27 để giảng viên xem xét. Các giới hạn và phần chưa xác minh được công khai trong hồ sơ này; báo cáo không tự thay thế biên bản nghiệm thu của giảng viên.
