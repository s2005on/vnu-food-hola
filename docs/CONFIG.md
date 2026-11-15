# Kế hoạch quản lý cấu hình — VNU Food Hola

Hồ sơ quản lý dự án CSE3045. Bản gốc được lập trong giai đoạn B7; nội dung dưới đây được làm rõ theo trạng thái mã nguồn tại 15/11/2026. B2–B7 là **mã bài thực hành**, không phải release.

## 1. Hạng mục được quản lý

- Mã nguồn backend/frontend, dữ liệu mẫu không nhạy cảm, cấu hình và dependencies.
- Yêu cầu, thiết kế, WBS, tiến độ, rủi ro, kiểm thử và minh chứng.
- Commit, nhánh, Pull Request, Git tag, kịch bản triển khai và backup.

Không lưu trong repo: mật khẩu, token, file `.env` có bí mật, SQLite chứa dữ liệu khách thật, môi trường ảo hoặc backup nhạy cảm.

## 2. Vai trò và kiểm soát thay đổi

Dự án do một sinh viên thực hiện; tự rà soát không được ghi thành review độc lập. Giảng viên đánh giá qua học phần; một PR được tạo không đồng nghĩa đã được duyệt.

Quy trình: tạo Issue/đề xuất thay đổi → chọn nhánh phù hợp → triển khai → kiểm thử phần liên quan → mở PR và rà soát diff/CI → merge có kiểm soát → cập nhật tài liệu/tag (nếu thực sự phát hành).

## 3. Phiên bản và release

**Quy ước chi tiết và timeline:** [VERSIONING.md](VERSIONING.md).  
**Lịch sử thay đổi:** [CHANGELOG.md](../CHANGELOG.md).

| Tên | Trạng thái xác minh | Ý nghĩa |
|---|---|---|
| `v0.1.0` | Đã có annotated Git tag, 31/10/2026 | Sprint 1: tài liệu và demo tĩnh; chưa có backend/database tại commit tag |
| V2, V3, V4, V5, V7.2, V7.3 | Tên mốc nội bộ lịch sử | Không phải tag phát hành theo SemVer |
| MVP giữa kỳ / V7.3 | Đã tích hợp PR #10 và tài khoản khách qua PR #14 | Đã kiểm tra trên SV27 ngày 15/11/2026; VPS theo block |
| `v0.2.0` | **Dự kiến, chưa tạo tag** | Mốc phát hành tiếp theo khi đã review, kiểm thử và chốt commit |
| `v1.0.0` | Mục tiêu dài hạn, chưa phát hành | Chỉ cân nhắc khi đạt tiêu chí nghiệm thu sản phẩm |

Chỉ dùng `vMAJOR.MINOR.PATCH` cho release; không tự đổi mốc nội bộ V7.3 thành v7.3.0 hoặc v0.7.3. Chỉ gắn tag trên commit đã xác minh, ghi rõ tính năng/giới hạn và không ghi đè tag cũ.

## 4. Nhánh, commit và PR

- `main`: nhánh mã nguồn ổn định; `develop`: nhánh tích hợp khi phù hợp.
- Nhánh mới: `feat/*`, `fix/*`, `docs/*`, `chore/*`; các nhánh `feature/*` cũ giữ nguyên để truy dấu.
- Commit: `feat:`, `fix:`, `docs:`, `test:`, `chore:` + mô tả ngắn.
- PR vào nhánh đích đã thống nhất; không merge hàng loạt PR B2–B7 và không force-push `main`.
- Ghi rõ PR nào đã merge, kiểm thử nào đạt, điều gì chưa được nghiệm thu; không gọi mỗi PR là “release” nếu không có tag.

## 5. Sao lưu, kiểm tra và khôi phục

- Commit/push phần đã kiểm tra, giữ bản sao mã nguồn ở nơi riêng ngoài GitHub.
- Sao lưu SQLite an toàn trước cập nhật và thử khôi phục trên môi trường tách biệt; không ghi backup vào Git.
- Check lại đường dẫn, cấu hình VPS, cổng dịch vụ, database và CI trước khi triển khai.
- Checkout tag chỉ khôi phục **mã nguồn**; muốn khôi phục dữ liệu phải có backup phù hợp.
- Các kế hoạch này không được đánh dấu “đã hoàn thành” nếu chưa có bằng chứng.

## 6. Tham chiếu lịch sử B7

B7 ban đầu đề xuất `v0.1.0` cho tài liệu + demo tĩnh, và tag này hiện thực sự tồn tại. Các kế hoạch tăng phiên bản trong bản B7 cũ không tự tạo tag và không phải xác nhận backend/DB đã có ở thời điểm tag. Xem [Git/PR](GIT.md), [VERSIONING.md](VERSIONING.md) để phân biệt tiến độ học phần với tiến độ phần mềm.
