# Lịch sử thay đổi — VNU Food Hola

Các mục dưới đây tách biệt **Git tag phát hành** và **mốc phát triển nội bộ**. Quy tắc chi tiết: [docs/VERSIONING.md](docs/VERSIONING.md).

## Chưa phát hành (Unreleased) — hồ sơ giữa kỳ

- [PR #11](https://github.com/s2005on/vnu-food-hola/pull/11) (đang mở tại thời điểm ghi): cập nhật tài liệu V7.3, bảng kiểm nghiệm thu, hướng dẫn triển khai, CI và quy ước phiên bản.
- Bổ sung mục lục `docs/`, tách minh chứng B2 khỏi README, hiệu chỉnh định dạng Markdown.
- **Chưa có tag mới** và chưa xác nhận bản MVP được triển khai công khai trên VPS. Không coi kết quả CI là bằng chứng hosting.

## Đã tích hợp vào main nhưng chưa gắn tag phát hành mới

### 14/11/2026 — MVP giữa kỳ (nhãn nội bộ V7.3)

- [PR #10](https://github.com/s2005on/vnu-food-hola/pull/10) đã merge: giao diện và luồng đặt món cho khách/quán, thực đơn 16 món, quản lý đơn và chế độ demo.
- [PR #9](https://github.com/s2005on/vnu-food-hola/pull/9) đã merge: backend FastAPI, SQLite và quản trị đơn (nhãn lịch sử V3).
- Đây là các mốc tích hợp mã nguồn, **không phải** tag `v7.3.0`, `v0.7.3` hay `v0.2.0`.

## v0.1.0 — 31/10/2026 (Git tag hiện có)

- Mốc Sprint 1 với tài liệu dự án tích hợp và demo tĩnh.
- Tại commit được gắn tag, backend và database đặt món **chưa được triển khai**.
- [Xem tag v0.1.0](https://github.com/s2005on/vnu-food-hola/tree/v0.1.0).

## Lịch sử học phần trước đó

- **B2 (20/10/2026):** quy trình Git, pre-mortem và minh chứng chạy thử tĩnh trên VPS nội bộ — xem [docs/B2-REPORT.md](docs/B2-REPORT.md).
- **B3–B7:** tài liệu yêu cầu, kế hoạch, Scrum, rủi ro, chất lượng và quản lý cấu hình trong `docs/`. Các tên B2–B7 là mã bài thực hành, không biểu thị thứ tự release.

## Dự kiến lần phát hành tiếp theo

`v0.2.0` là **đề xuất**, chỉ cân nhắc sau khi PR cần thiết đã merge, kiểm thử/CI đạt và ghi lại tình trạng triển khai thực tế. Chưa tạo tag, chưa coi phần chưa xác minh là đã hoàn thành.
