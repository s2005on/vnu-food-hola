# Bàn giao giữa kỳ - Lâm Hải Sơn / 23110216

Mục tiêu: chứng minh một luồng đặt món hoạt động từ khách đến quán trên bản triển khai,
đối chiếu nhận xét “PR chưa merge; cần đánh giá ứng dụng”. Không tự ghi hoàn thành khi chưa có bằng chứng.

## Trạng thái
| Hạng mục | Trạng thái khi chuẩn bị bản này |
|---|---|
| V7.3 vào main | PR #10 đã merge 14/11/2026 |
| CI bản V7.3 | PR #11: CI Ubuntu 3.12 và Windows 3.14 đạt; khi nộp cần kèm đường dẫn run/commit chính xác |
| Sửa giữa kỳ | PR #11 đã merge vào main ngày 15/11/2026, commit `d3b1f0a`; CI Ubuntu 3.12 và Windows 3.14 đạt tại HEAD của PR |
| PR #2–#8 | Đã rà soát và đóng 7 PR cũ (Closed, not merged), có bình luận, đối chiếu SHA và biên bản [PR-REVIEW.md](PR-REVIEW.md); không thay thế đánh giá thầy |
| Hosting trên SV27 | **Có minh chứng trình duyệt HTTPS** tại `https://sv27.bcse-vju.com/` ngày 15/11/2026; còn phụ thuộc thời hạn block và gateway trường |
| Demo khách–quán | **Đã quan sát ảnh chụp luồng đặt → quản trị xác nhận/chuẩn bị/sẵn sàng → ghi nhận thanh toán → hoàn thành → khách thấy hoàn thành**. Chưa quay video liên tục, chưa thử hai thiết bị độc lập |

## Bảng kiểm nghiệm thu thủ công
Điền kết quả, ngày giờ và đường dẫn bằng chứng sau khi chạy, không chỉ đánh dấu theo suy đoán.

| ID | Thao tác | Kết quả cần đạt | Kết quả thực tế / bằng chứng |
|---|---|---|---|
| M01 | Mở URL HTTPS trên mạng khác | Đúng trang 16 món, ảnh/CSS tải được | **Một phần:** đã có ảnh trình duyệt Chrome HTTPS với trang 16 món hiển thị đầy đủ; chưa chứng minh thử từ mạng ngoài độc lập |
| M02 | Khách thường đặt đơn hợp lệ | Có mã đơn, tổng đúng, quán son nhìn thấy | **Đạt theo ảnh 15/11:** đơn thử 2 món tổng 65.000đ hiện trên cả giao diện khách và quản trị; không đưa mã đơn/số điện thoại vào tài liệu công khai |
| M03 | Quán cập nhật và thu tiền | Khách thấy trạng thái; chỉ hoàn thành sau thu tiền | **Đạt về luồng giao diện:** nhật ký `pending → confirmed → preparing → ready → paid → completed`, khách thấy **Hoàn thành** và **Đã thanh toán** (15/11/2026, khoảng 22:30 giờ Việt Nam). Đây là ghi nhận thanh toán thử trên hệ thống, **không chứng minh tiền mặt đã nhận thực tế** |
| M04 | Reload và restart máy chủ thử | Đơn giữ nguyên | Chưa thực hiện |
| M05 | Sai điện thoại/thiếu địa điểm | Báo lỗi, không tạo đơn | Chưa thực hiện |
| M06 | Món hết/ẩn hoặc giá thay đổi | Backend từ chối nội dung không còn hợp lệ | Chưa thực hiện |
| M07 | Gửi lại cùng yêu cầu | Không tạo hai đơn | Chưa thực hiện |
| M08 | Chọn giờ quá hạn | Không chấp nhận; có giờ hợp lệ mới | Chưa thực hiện |
| M09 | Thử API quản trị khi chưa đăng nhập | Không truy cập được dữ liệu quản trị | Chưa thực hiện |
| M10 | Khách demo rồi hết/thoát phiên | Đơn demo tách khỏi dữ liệu quán | Chưa thực hiện |
| M11 | Màn hình điện thoại | Giỏ hàng/đăng nhập/đặt món sử dụng được | Chưa thực hiện |
| M12 | Sao lưu SQLite ở nơi riêng | Bản sao integrity_check=ok | **Đạt với backup:** đã sao lưu dưới `/home/student/vju-food-data/backups/`, Terminal hiển thị `SQLite integrity: ok` trước nâng cấp. Chưa thử khôi phục backup trên môi trường riêng |

## Kiểm tra tài khoản khách — bổ sung sau PR #14

| ID | Kiểm tra | Kết quả hiện tại |
|---|---|---|
| A01 | Đăng nhập khách và hiển thị thông tin tài khoản | **Đã quan sát** trên HTTPS bằng ảnh trình duyệt, không lưu dữ liệu nhận dạng cá nhân vào repo |
| A02 | Khách xem lịch sử và nhận trạng thái cập nhật từ quản trị | **Đạt theo ảnh**, gồm trạng thái Sẵn sàng nhận và Hoàn thành |
| A03 | Khách đăng nhập lại trên thiết bị/trình duyệt thứ hai vẫn thấy đơn | **Chưa kiểm thử thủ công** (đã có kiểm thử tự động backend) |
| A04 | Tài khoản khách B không xem được đơn A | **Chưa kiểm thử thủ công trên hosting** (đã có kiểm thử tự động) |
| A05 | Đăng ký trùng số, sai mật khẩu, đăng xuất và cookie HTTPS | **Chưa kiểm thử đủ trên hosting** |

## Minh chứng đã nhận và giới hạn

- Ngày 15/11/2026, ảnh chụp trong quá trình thực hành cho thấy trang HTTPS `sv27.bcse-vju.com`, thực đơn 16 món, tài khoản khách, đơn có tổng 65.000đ, nhật ký quản trị và kết quả Hoàn thành.
- Terminal SV27 xác nhận service systemd `active`, `enabled`, HTTP health `{"ok":true}`, commit ứng dụng đã deploy `0eba90e451312ddfc5b57dff268322e4ddb8cf7e` (PR #14), 46 bài kiểm thử Python đạt; backup SQLite được kiểm tra `integrity_check=ok`.
- **Ảnh chưa được tải lên GitHub** vì cần che tên/số điện thoại và mã đơn trước khi công khai. Không ghi nhận video quay liên tục hay kết quả hai mạng khác nhau khi chưa có bằng chứng.
- Chưa xác minh hosting liên tục sau khi block SV27 hết hạn; `systemd` không vượt được chính sách cấp VPS của trường.

## Minh chứng gửi thầy
- Link GitHub main, PR #10 và PR bản sửa; link CI đúng commit đã triển khai.
- URL công khai, commit triển khai, ngày giờ kiểm tra theo giờ Việt Nam.
- Video 2-3 phút: khách đặt, son xử lý, khách cập nhật, tải lại giữ đơn.
- Ảnh web và kết quả service/health; che điện thoại, mật khẩu, mã tra cứu bí mật.
- Kết quả bảng kiểm trên và lỗi còn biết. Không đưa database/backup vào Git.
- Ghi rõ SV27/VPS được cấp theo block; nếu chỉ chạy trong buổi demo, nêu thời gian khả dụng và không cam kết link 24/24.

## Đóng góp cá nhân và giải thích
Sơn làm dự án cá nhân có AI hỗ trợ. Ghi link commit/PR/tài liệu và phần đã tự kiểm tra.
Không tạo review giả hoặc chia đóng góp theo số commit. Cần giải thích được tính tiền phía server,
khóa chống đơn trùng, khác biệt demo/khách, phiên quản trị, SQLite và cấu hình Nginx.

Điểm hồ sơ 9,29 và dấu chờ chất lượng trong ảnh là dữ liệu thầy đã ghi tại mốc chụp;
tài liệu này không tự cập nhật điểm hoặc khẳng định đã được thầy nghiệm thu.
