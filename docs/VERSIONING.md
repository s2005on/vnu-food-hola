# Quy ước phiên bản và các mốc phát triển

**Dự án:** VNU Food Hola · CSE3045.  
**Quy tắc áp dụng từ 15/11/2026:** phân biệt **phiên bản phát hành** và **tên mốc phát triển**; không sửa lịch sử Git đã công bố.

## 1. Một cách đánh số cho các bản phát hành

- **Git tag chính thức:** `vMAJOR.MINOR.PATCH` (SemVer), viết chữ `v` thường, ví dụ `v0.1.0`, `v0.2.0`.
- **MAJOR**: phiên bản tương thích lớn sau khi sản phẩm ổn định; **MINOR**: thêm chức năng hoặc thay đổi đáng kể; **PATCH**: sửa lỗi tương thích, tài liệu đi kèm bản phát hành.
- Dự án đang phát triển giai đoạn `0.x.y`. Những thay đổi không tương thích cần ghi rõ, thường tăng MINOR.
- Chỉ tạo tag **sau khi** xác định commit trên `main`, kiểm tra phần liên quan, ghi chú tính năng/giới hạn; không gắn tag chỉ vì có bài tập mới.
- Không di chuyển/xóa tag đã công bố và không gắn lại phiên bản vào commit khác.

**Hiện đã có tag `v0.1.0`; `v0.2.0` mới là đề xuất cho lần phát hành kế tiếp, chưa được tạo và không được ghi là đã phát hành.**

## 2. Phân biệt ba loại mốc

| Loại | Cách đặt tên | Ý nghĩa |
|---|---|---|
| Bài thực hành học phần | `B2` đến `B7` | Hồ sơ / minh chứng; **không phải** release phần mềm |
| Mốc nội bộ cũ | `V2`, `V3`, `V4`, `V5`, `V7.2`, `V7.3` | Nhãn dùng khi phát triển giao diện, backend và thử nghiệm; **không phải** Git tag SemVer |
| Bản phát hành | `v0.1.0`, `v0.2.0`, ... | Chỉ ghi "đã phát hành" nếu **tag thực sự tồn tại** và có ghi chú |

Khi nhắc tới V7.3 trong tài liệu, viết **“MVP giữa kỳ (mốc nội bộ V7.3)”**. Không tự động chuyển tên V7.3 thành v7.3.0 hoặc v0.7.3; hai kiểu tên không tương đương.

## 3. Dòng thời gian đã đối chiếu GitHub

| Thời điểm | Mốc / PR | Cách hiểu đúng |
|---|---|---|
| 20/10/2026 | Hồ sơ B2 | Thử dịch vụ tĩnh trên VPS nội bộ, không phải release/hosting MVP |
| 31/10/2026 | [Tag v0.1.0](https://github.com/s2005on/vnu-food-hola/tree/v0.1.0) | Mốc Sprint 1: tài liệu tích hợp và demo tĩnh; chưa có backend/database ở commit gắn tag |
| 07/11/2026 | [PR #8](https://github.com/s2005on/vnu-food-hola/pull/8), UI V2 | PR giao diện mẫu lịch sử; đã đóng sau khi xác minh 4/4 tệp V2 có trên main (15/11), không phải release |
| 14/11/2026 | [PR #9](https://github.com/s2005on/vnu-food-hola/pull/9), backend V3 | Đã merge vào `main`; “V3” là tên giai đoạn backend |
| 14/11/2026 | [PR #10](https://github.com/s2005on/vnu-food-hola/pull/10), V7.3 | Đã merge vào `main`; MVP giữa kỳ có 16 món, khách/quản trị, SQLite |
| 15/11/2026 | [PR #11](https://github.com/s2005on/vnu-food-hola/pull/11) | Đã merge vào `main` (commit `d3b1f0a`), chuẩn hóa tài liệu, CI và lịch sử phiên bản |
| Tương lai | `v0.2.0` (dự kiến) | Chỉ gắn tag khi thống nhất nội dung, merge và xác minh; **chưa tồn tại** |

Lưu ý: thời điểm PR được tạo/merge không chứng minh một tên phiên bản đã trở thành Git tag. Các tên V4/V5/V7.2 chỉ dùng như thông tin lịch sử nếu có tài liệu đi kèm; không tự gán ngày phát hành hoặc mức độ hoàn thành.

Bảng kiểm phát hành dự kiến: [RELEASE-v0.2.0.md](RELEASE-v0.2.0.md). Bản `v0.2.0` chưa được gắn tag.

## 4. Quy tắc đặt tên cho công việc mới

- Nhánh: `feat/<chuc-nang>`, `fix/<loi>`, `docs/<chu-de>`, `chore/<cong-viec>`; chữ thường và dấu `-`. Giữ các nhánh `feature/*` cũ để truy xuất lịch sử.
- Commit: `feat:`, `fix:`, `docs:`, `test:`, `chore:` + hành động ngắn, ví dụ `docs: clarify release history`.
- PR: viết **thay đổi gì và vì sao**, không gọi mỗi PR là “bản V8” hay “release” nếu chưa gắn tag. Khi là release, ghi rõ tag dự kiến/đã tạo và commit.
- Mỗi bản phát hành: ghi vào [CHANGELOG](../CHANGELOG.md), mô tả commit, kết quả kiểm thử, giới hạn chưa xác minh và link PR liên quan.
- `main` là dòng mã ổn định để đối chiếu; `develop` có thể dùng tích hợp công việc học phần. PR mới phải chọn base theo tình trạng tích hợp thực tế, không gộp các nhánh cũ hàng loạt.

## 5. Tên file cũ và tương thích

Giữ `START-V7.3.md`, `deploy/install-v4.sh` và tên nhánh/PR lịch sử để không làm gãy đường dẫn, script hoặc bằng chứng đã nộp. Đây là **tên tương thích lịch sử**, không phải tên phiên bản chính thức của ứng dụng hiện hành.

Không chỉnh commit cũ, không force-push `main`, không xóa hay chuyển tag `v0.1.0`. Nếu cần thu gọn folder trong tương lai, tạo đường dẫn mới và giữ đường dẫn cũ làm lối chuyển tiếp trước khi bỏ.
