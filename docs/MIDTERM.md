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
| Hosting V7.3 | Chưa xác minh; yêu cầu kiểm tra URL công khai |
| Demo khách-quán | Cần quay trên bản hosting bằng hai trình duyệt |

## Bảng kiểm nghiệm thu thủ công
Điền kết quả, ngày giờ và đường dẫn bằng chứng sau khi chạy, không chỉ đánh dấu theo suy đoán.

| ID | Thao tác | Kết quả cần đạt | Kết quả thực tế / bằng chứng |
|---|---|---|---|
| M01 | Mở URL HTTPS trên mạng khác | Đúng trang 16 món, ảnh/CSS tải được | Chưa thực hiện |
| M02 | Khách thường đặt đơn hợp lệ | Có mã đơn, tổng đúng, quán son nhìn thấy | Chưa thực hiện |
| M03 | Quán cập nhật và thu tiền | Khách thấy trạng thái; chỉ hoàn thành sau thu tiền | Chưa thực hiện |
| M04 | Reload và restart máy chủ thử | Đơn giữ nguyên | Chưa thực hiện |
| M05 | Sai điện thoại/thiếu địa điểm | Báo lỗi, không tạo đơn | Chưa thực hiện |
| M06 | Món hết/ẩn hoặc giá thay đổi | Backend từ chối nội dung không còn hợp lệ | Chưa thực hiện |
| M07 | Gửi lại cùng yêu cầu | Không tạo hai đơn | Chưa thực hiện |
| M08 | Chọn giờ quá hạn | Không chấp nhận; có giờ hợp lệ mới | Chưa thực hiện |
| M09 | Thử API quản trị khi chưa đăng nhập | Không truy cập được dữ liệu quản trị | Chưa thực hiện |
| M10 | Khách demo rồi hết/thoát phiên | Đơn demo tách khỏi dữ liệu quán | Chưa thực hiện |
| M11 | Màn hình điện thoại | Giỏ hàng/đăng nhập/đặt món sử dụng được | Chưa thực hiện |
| M12 | Sao lưu SQLite ở nơi riêng | Bản sao integrity_check=ok | Chưa thực hiện |

## Minh chứng gửi thầy
- Link GitHub main, PR #10 và PR bản sửa; link CI đúng commit đã triển khai.
- URL công khai, commit triển khai, ngày giờ kiểm tra theo giờ Việt Nam.
- Video 2-3 phút: khách đặt, son xử lý, khách cập nhật, tải lại giữ đơn.
- Ảnh web và kết quả service/health; che điện thoại, mật khẩu, mã tra cứu bí mật.
- Kết quả bảng kiểm trên và lỗi còn biết. Không đưa database/backup vào Git.
- Ghi rõ SV21/VPS được cấp theo block; nếu chỉ chạy trong buổi demo, nêu thời gian khả dụng.

## Đóng góp cá nhân và giải thích
Sơn làm dự án cá nhân có AI hỗ trợ. Ghi link commit/PR/tài liệu và phần đã tự kiểm tra.
Không tạo review giả hoặc chia đóng góp theo số commit. Cần giải thích được tính tiền phía server,
khóa chống đơn trùng, khác biệt demo/khách, phiên quản trị, SQLite và cấu hình Nginx.

Điểm hồ sơ 9,29 và dấu chờ chất lượng trong ảnh là dữ liệu thầy đã ghi tại mốc chụp;
tài liệu này không tự cập nhật điểm hoặc khẳng định đã được thầy nghiệm thu.
