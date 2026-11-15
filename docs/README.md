# Tài liệu dự án VNU Food Hola

Đây là mục lục tài liệu kỹ thuật, quản lý học phần và minh chứng. Trang giới thiệu và cách chạy nhanh: [README chính](../README.md).

## Hồ sơ tổng kết và bàn giao

- [Báo cáo tổng kết và bàn giao dự án](FINAL-HANDOVER.md) — phạm vi MVP, chức năng, công nghệ, kết quả triển khai, minh chứng và giới hạn còn lại.
- [Kết quả kiểm chứng](../VERIFICATION.md) — môi trường, commit triển khai, kiểm thử và các nội dung chưa xác minh.
- [Bộ ảnh minh chứng SV27](evidence/sv27-2026-11-15/README.md) — 7 ảnh đã che thông tin riêng tư.

## Phiên bản và lịch sử

- [Quy ước phiên bản, timeline B2–B7/V2–V7.3](VERSIONING.md)
- [Changelog các bản phát hành và mốc tích hợp](../CHANGELOG.md)
- [Kế hoạch kiểm chứng trước release v0.2.0](RELEASE-v0.2.0.md) — dự kiến, chưa tạo tag

## Sản phẩm và thiết kế

| Tài liệu | Nội dung |
|---|---|
| [01 — Project Charter](01-project-charter.md) | Mục tiêu, phạm vi, tiêu chí nghiệm thu |
| [02 — Requirements](02-requirements.md) | Yêu cầu và user stories |
| [03 — System Design](03-system-design.md) | Thiết kế hệ thống, API và dữ liệu |
| [04 — WBS](04-wbs.md) | Cấu trúc phân rã công việc |
| [05 — Schedule](05-schedule.md) | Tiến độ và các mốc |
| [08 — MVP Demo](08-mvp-demo.md) | Minh họa demo tĩnh giai đoạn đầu (không phải V7.3) |

## Hồ sơ học phần và quản lý dự án

| Tài liệu | Nội dung |
|---|---|
| [B2 — Git, rủi ro và VPS](B2-REPORT.md) | Báo cáo B2, pre-mortem, ảnh minh chứng ngày 20/10/2026 |
| [06 — Scrum / Team](06-scrum-team.md) | Vai trò và cách làm việc |
| [07 — Sprint 0 Backlog](07-sprint-0-backlog.md) | Danh sách công việc Sprint 0 |
| [Git / PR](GIT.md) | Quy tắc nhánh, commit, review và phát hành |
| [Rủi ro](RISKS.md) | Risk register B5 |
| [Chất lượng](QUALITY.md) | Kế hoạch bảo đảm chất lượng |
| [Nhóm và phân công](TEAM.md) | Vai trò, trách nhiệm và giao tiếp |
| [Báo cáo Sprint 0](SPRINT0-REPORT.md) | Tổng hợp tiến độ ban đầu |
| [Bên liên quan](STAKEHOLDERS.md) | Xác định stakeholder |
| [Quản lý cấu hình](CONFIG.md) | Phiên bản, thay đổi và lưu trữ |

## Chạy thử và hồ sơ lịch sử

| Tài liệu | Nội dung |
|---|---|
| [Chạy trên Windows](../START-HERE.md) | Khởi động và kịch bản demo MVP |
| [Nâng cấp V7.3](../START-V7.3.md) | Lưu ý sao lưu và giữ database |
| [Bàn giao giữa kỳ](MIDTERM.md) | Bảng kiểm và ghi nhận ở mốc giữa kỳ |
| [Biên bản rà soát PR #2–#8](PR-REVIEW.md) | Đã đóng các PR cũ, lưu kết quả so sánh Git blob SHA và giải thích |
| [Triển khai VPS](../deploy/README.md) | FastAPI, systemd, Nginx, backup |

## Hồ sơ bài thực hành

Các báo cáo B2–B7 được giữ trong `docs/` để lưu lịch sử học phần; chúng không đại diện cho trạng thái phát hành hiện tại.

Ảnh và log minh chứng nằm tại [`docs/evidence/`](evidence/). Không dùng minh chứng từ bản tĩnh B2/B4 để kết luận bản MVP đã được triển khai.
