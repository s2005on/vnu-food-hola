# Quy ước Git

## Nhánh và commit

- `main`: mã ổn định, thay đổi qua pull request.
- `develop`: tích hợp khi cần; nhánh công việc dùng `feat/`, `fix/`, `docs/` hoặc `chore/`.
- Commit dùng tiền tố `feat:`, `fix:`, `docs:`, `test:` hoặc `chore:`.
- PR mô tả thay đổi, nhánh đích và kết quả kiểm thử. Trước merge, rà soát diff và CI.

## Phát hành

Tag theo [SemVer](VERSIONING.md), gắn vào commit đã kiểm tra trên `main` và có ghi chú trong [CHANGELOG](../CHANGELOG.md). Giữ nguyên tag đã công bố.

## Dữ liệu và lịch sử

Database, backup, mật khẩu/token và môi trường ảo nằm ngoài Git. Các nhánh `feature/*` và hồ sơ B2–B7 được giữ làm lịch sử học phần. Biên bản đối chiếu PR cũ: [PR-REVIEW.md](PR-REVIEW.md).
