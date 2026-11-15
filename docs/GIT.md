# Quy ước Git và Pull Request — VNU Food Hola

## Repository

- Dự án: https://github.com/s2005on/vnu-food-hola
- Bài tập tuần riêng: https://github.com/s2005on/cse3045-23110216

## Nhánh và luồng thay đổi

- `main`: nhánh ổn định để bàn giao, không sửa trực tiếp.
- `develop`: nhánh tích hợp khi áp dụng quy trình feature → develop → main.
- Từ nay tạo nhánh theo `feat/<mo-ta>`, `fix/<mo-ta>`, `docs/<mo-ta>` hoặc `chore/<mo-ta>`.
- Giữ nguyên các nhánh lịch sử `feature/b2-setup` đến `feature/release-v7.3`; **không đổi tên/force-push** để tránh mất dấu vết PR và bài đã nộp.

Tùy công việc, PR có thể vào `develop` để tích hợp hoặc `main` nếu được chuẩn bị trực tiếp từ bản ổn định; **phải ghi rõ nhánh base**. PR #9, #10, #11 thực tế nhắm vào main, khác luồng B2–B7 ban đầu. Không merge nhánh lịch sử mà chưa đối chiếu với mã hiện tại.

## Commit và Pull Request

- Tiền tố commit: `feat:`, `fix:`, `docs:`, `test:`, `chore:`.
- Mỗi commit có một mục đích; không commit database thật, mật khẩu/token, môi trường ảo hoặc bản backup.
- Mỗi PR nêu: mục đích, thay đổi, cách thử, giới hạn và nhánh đích.
- Trước merge: xem `Files changed`, kết quả CI, kiểm tra phần ảnh hưởng và xử lý xung đột nếu có.
- Vì dự án một người, tự rà soát không được ghi là review độc lập; không suy ra giảng viên đã phê duyệt.

## Phát hành phiên bản

Chỉ dùng tên Git tag `vMAJOR.MINOR.PATCH` theo [VERSIONING.md](VERSIONING.md) và cập nhật [CHANGELOG](../CHANGELOG.md). B2–B7 là bài thực hành; V2/V3/V7.3 là nhãn giai đoạn, không phải tag.

- Tag `v0.1.0` thực sự tồn tại (31/10/2026), mô tả demo tĩnh + tài liệu ở commit lúc đó.
- `v0.2.0` mới **dự kiến**; không ghi “đã release” trước khi tag được tạo.
- Khi phát hành, chọn commit đã kiểm tra trên main, tạo annotated tag và ghi chú hạn chế, ghi lại SHA/link.
- Không chuyển tag cũ sang commit mới; sửa lỗi bằng commit mới + phiên bản mới.
- Không `git push --tags` nếu chưa kiểm tra tất cả tag địa phương.

## Bằng chứng học phần và xử lý PR cũ

- PR B2–B7 có giá trị làm hồ sơ quá trình ngay cả khi chưa merge; xem [PR-REVIEW.md](PR-REVIEW.md).
- Nếu một PR cũ đã được thay thế: đối chiếu tài liệu, ghi lý do và chỉ đóng sau khi chắc chắn không mất nội dung cần nộp.
- Nếu lỗi ở bản tích hợp: dùng commit sửa hoặc revert, không dùng `reset --hard`/force-push khi chưa hiểu tác động.
- Lưu kết quả kiểm thử thực tế (CI ≠ đã triển khai) và mã commit dùng cho demo.

Giai đoạn B7 từng tích hợp các nhánh B2–B6 lên `feature/b7-config-release`. Việc tích hợp không đồng nghĩa đã có review độc lập hay giảng viên duyệt.
