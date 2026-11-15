# Chuẩn bị phát hành v0.2.0 — chưa phát hành

**Dự án:** VNU Food Hola · **Trạng thái:** BẢN KẾ HOẠCH, **chưa có tag `v0.2.0`**.  
**Ngày lập:** 15/11/2026 · **Phiên bản mã nguồn đã tích hợp:** MVP giữa kỳ (nhãn nội bộ V7.3).  
**Mốc Git đã merge:** [PR #10](https://github.com/s2005on/vnu-food-hola/pull/10), [PR #11](https://github.com/s2005on/vnu-food-hola/pull/11), `main` sau PR #11: `d3b1f0a905e3f3c9142f286ab89aeefb6e0c36ab`.

Không đổi tên V7.3 thành `v0.7.3` hay `v7.3.0`. Tag `v0.1.0` hiện có chỉ là mốc tài liệu + demo tĩnh. Tất cả định nghĩa release xem [VERSIONING.md](VERSIONING.md).

## Phạm vi dự kiến cho v0.2.0

- Ứng dụng thử nghiệm một quán, thực đơn 16 món mẫu, có ảnh, tìm kiếm và giỏ hàng.
- Đặt món, lưu trong SQLite, tra cứu mã đơn + mã bí mật; kiểm tra giá và hạn chế gửi trùng ở backend.
- Quản trị quán đăng nhập, cập nhật trạng thái đơn và ghi nhận tiền mặt riêng với trạng thái xử lý.
- Tách dữ liệu demo và luồng khách/quán chính; tài liệu cấu trúc, kiểm thử, hướng dẫn chạy và triển khai.
- **Ngoài phạm vi:** thanh toán online, shipper, nhiều quán, hoạt động thương mại thực tế hay xác nhận bảo mật cho dữ liệu khách thật.

## Điều kiện cần đạt trước khi tạo tag

| Mã | Điều kiện | Trạng thái tại 15/11/2026 | Minh chứng cần lưu |
|---|---|---|---|
| R01 | PR #11 đã merge, ghi SHA để truy xuất | **Đạt** | PR #11, commit `d3b1f0a` |
| R02 | CI Ubuntu/Python 3.12 + Windows/Python 3.14 | **Đạt trên HEAD PR #11** | GitHub Actions của PR, link run |
| R03 | Demo trình duyệt khách → quản trị → khách cập nhật | **Chưa xác minh** | Video/ảnh + ngày giờ + URL |
| R04 | Đặt lại trang/khởi động lại, đơn SQLite vẫn còn | **Chưa xác minh trên VPS** | Lệnh & ảnh/biên bản, tránh lộ dữ liệu |
| R05 | Thử dữ liệu không hợp lệ, hết món, giờ quá hạn, quyền quản trị | **Chưa xác minh thủ công trên hosting** | Kết quả checklist [MIDTERM.md](MIDTERM.md) |
| R06 | HTTPS, API health/menu và trang/ảnh/CSS trên URL công khai | **Chưa xác minh** | URL, status, thời gian, commit đã deploy |
| R07 | Sao lưu và kiểm tra khôi phục dữ liệu thử | **Chưa xác minh trên VPS** | Log `integrity_check`, kiểm tra khôi phục |
| R08 | Tài liệu/CHANGELOG nhất quán và kiểm tra thay đổi cuối | **Đang chuẩn bị** | Diff và link PR của phần chuẩn bị |
| R09 | Gắn annotated tag `v0.2.0` đúng commit đã xác minh | **Chưa thực hiện** | Link tag + commit + ghi chú release |

**Nguyên tắc:** không đánh dấu đạt khi thiếu bằng chứng. CI không thay thế kiểm thử trình duyệt hoặc chứng minh VPS hoạt động. VPS theo block không bảo đảm liên kết mở được sau khi hết phiên.

## Hướng dẫn xác minh triển khai

- Theo [deploy/README.md](../deploy/README.md): kiểm tra cổng, service, Nginx và backup; không tự ghi đè cấu hình nhóm khác.
- Sau khi đã deploy đúng commit, chạy script chỉ đọc: `bash deploy/verify-public.sh https://sv21.bcse-vju.com/b1-23110216/v3/` nếu đây là URL được cấp và truy cập được.
- Hoàn thành ít nhất M01–M12 trong [MIDTERM.md](MIDTERM.md), ghi kết quả khách/quản trị trên **hai trình duyệt** cùng hệ thống thật và che thông tin riêng tư.
- Ghi commit đang chạy trên VPS, ngày/giờ theo Việt Nam, link GitHub Actions, lỗi còn tồn đọng.

## Quy trình công bố khi đủ bằng chứng

1. Xem lại `main` và CI; hoàn thành điều kiện R01–R08, ghi commit thực tế.
2. Chốt `CHANGELOG.md`, ghi rõ chức năng, giới hạn, hướng dẫn nâng cấp và phiên bản phụ thuộc.
3. Tạo **annotated tag** `v0.2.0` **trên commit main đã xác minh**, không tạo trên nhánh tạm:
   ```bash
   git fetch origin --tags
   git checkout main
   git pull --ff-only origin main
   git tag -a v0.2.0 -m "VNU Food Hola v0.2.0 — verified MVP"
   git push origin v0.2.0
   ```
   Chỉ chạy khi tag chưa tồn tại và đã xác nhận commit; không tự đặt tag dựa vào ngày hoặc tên nhánh.
4. Tạo GitHub Release với tag này (sau khi tag thực tồn tại), nêu URL demo/giới hạn đã được xác minh; cập nhật R09.
5. Đối chiếu bản đang chạy trên VPS với tag; nếu khác, ghi lại rõ ràng, không gán nhầm release cho deployment.

**Chưa thực hiện bước 3–5.** Không dùng tài liệu chuẩn bị này làm bằng chứng ứng dụng đã được phát hành hoặc chạy công khai.

## Kiểm thử bổ sung cho tài khoản khách (nhánh tính năng chưa phát hành)

Trước khi đưa lên VPS công khai: kiểm tra đăng ký/đăng nhập/đăng xuất, số điện thoại trùng, brute-force, cookie Secure, phân quyền khách–quản trị, lịch sử đơn giữa nhiều trình duyệt, thao tác thêm mã đơn cũ và phục hồi từ backup SQLite. **Chưa có xác nhận OTP/SMS hoặc khôi phục mật khẩu.** Không gắn tag v0.2.0 chỉ vì các kiểm thử tự động đạt.
