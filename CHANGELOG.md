# Changelog

Các mốc phát triển nội bộ và Git tag phát hành được ghi riêng. Xem [quy ước phiên bản](docs/VERSIONING.md).

## Chưa phát hành — dự kiến v0.2.0

- [PR #14](https://github.com/s2005on/vnu-food-hola/pull/14): thêm đăng ký/đăng nhập khách hàng và lịch sử đơn theo tài khoản; giữ luồng khách không đăng nhập và quyền quản trị riêng.
- **Triển khai thử trên SV27 (15/11/2026):** commit ứng dụng `0eba90e`; kiểm tra giao diện khách, quản trị, nhật ký trạng thái đơn và trạng thái hoàn thành.
- **Minh chứng:** ảnh trình duyệt và Terminal đã được che thông tin riêng tư tại [docs/evidence/sv27-2026-11-15/](docs/evidence/sv27-2026-11-15/).
- [PR #15](https://github.com/s2005on/vnu-food-hola/pull/15): chuẩn hóa hồ sơ giữa kỳ, kết quả kiểm chứng và hướng dẫn triển khai; đã merge tại commit `43ea617`.
- [PR #16](https://github.com/s2005on/vnu-food-hola/pull/16): chuẩn hóa hồ sơ bàn giao, bổ sung báo cáo tổng kết và 7 ảnh minh chứng SV27; loại bỏ hướng dẫn/script xuất bản giữa kỳ lỗi thời.
- **Chưa có tag `v0.2.0`.** Còn thiếu một số kiểm thử thủ công, thử khôi phục backup và nghiệm thu cuối cùng.

## MVP giữa kỳ — 14/11/2026

- [PR #10](https://github.com/s2005on/vnu-food-hola/pull/10): giao diện và luồng đặt món khách/quán, thực đơn 16 món, quản lý đơn và chế độ demo.
- [PR #9](https://github.com/s2005on/vnu-food-hola/pull/9): backend FastAPI, SQLite và quản trị đơn.
- V7.3/V3 là tên mốc phát triển, không phải Git tag.

## v0.1.0 — 31/10/2026

- Mốc Sprint 1 với tài liệu dự án và demo tĩnh.
- Tại commit gắn tag này, backend đặt món chưa được triển khai.
- [Xem tag v0.1.0](https://github.com/s2005on/vnu-food-hola/tree/v0.1.0).

## Hồ sơ học phần

Các báo cáo B2–B7 được giữ trong `docs/` để lưu lịch sử học phần; chúng không đại diện cho trạng thái phát hành hiện tại.
