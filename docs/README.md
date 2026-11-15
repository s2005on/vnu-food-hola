# Tài liệu dự án VNU Food Hola

Đây là mục lục tài liệu kỹ thuật, quản lý học phần và minh chứng. Trang giới thiệu và cách chạy nhanh: [README chính](../README.md).

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

## Chạy thử, kiểm thử và bàn giao

| Tài liệu | Nội dung |
|---|---|
| [Chạy trên Windows](../START-HERE.md) | Khởi động và kịch bản demo V7.3 |
| [Nâng cấp V7.3](../START-V7.3.md) | Lưu ý sao lưu và giữ database |
| [Kết quả kiểm chứng](../VERIFICATION.md) | Kiểm thử đã làm và giới hạn |
| [Bàn giao giữa kỳ](MIDTERM.md) | Bảng kiểm nghiệm thu, minh chứng cần bổ sung |
| [Đối chiếu PR #2–#8](PR-REVIEW.md) | Tránh merge lại các thay đổi lịch sử |
| [Triển khai VPS](../deploy/README.md) | FastAPI, systemd, Nginx, backup |

Ảnh và log minh chứng nằm tại [`docs/evidence/`](evidence/); không dùng minh chứng từ bản tĩnh B2/B4 để kết luận bản V7.3 đã được triển khai.

**Lưu ý:** các hồ sơ B2–B7 phản ánh từng giai đoạn học phần; với thông tin tính năng và trạng thái hiện tại, ưu tiên README chính, thiết kế được cập nhật và kết quả xác minh có ghi ngày/commit.
