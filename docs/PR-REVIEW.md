# Kết quả rà soát các Pull Request lịch sử #2–#8

**Dự án:** VNU Food Hola · **Ngày đối chiếu:** 15/11/2026.  
**Nhánh chuẩn đối chiếu:** `main`, commit `7fdc74da024514c83c74652d631649ef2ef81d7c` (sau PR #12).  
**Kết quả GitHub:** PR #2–#8 đều đã chuyển sang **Closed, not merged**, kèm bình luận giải thích riêng trong từng PR.

## Lý do và phương pháp

Các PR này được tạo trong giai đoạn thực hành B2–B7 hoặc demo V2, hầu hết nhắm vào `develop` / `feature/b7-config-release`. Sau đó dự án phát triển lên MVP FastAPI/SQLite V7.3 trên `main` qua các PR #9–#12. Vì thế **không merge hàng loạt** các PR cũ: có nguy cơ ghi đè README/thiết kế hiện tại hoặc đưa lại giao diện đã được thay thế.

Đã đối chiếu danh sách `Files changed` của từng PR với cây tệp tại `main`. Với các tệp còn cùng đường dẫn, so sánh Git blob SHA để nhận biết **trùng nội dung chính xác**. Những tệp có SHA khác được kiểm tra sự hiện diện và mục đích của tài liệu hiện tại; không coi là trùng byte, mà là **đã cập nhật hoặc chuyển nơi lưu**. Việc so sánh tệp **không chứng minh** PR cũ đã được merge vào `main` theo lịch sử Git.

## Kết quả theo từng PR

| PR | Nội dung lịch sử | Đối chiếu với `main` | Xử lý |
|---|---|---|---|
| [#2](https://github.com/s2005on/vnu-food-hola/pull/2) | Git, bảng rủi ro CHAOS và minh chứng VPS B2 | **3/4 tệp trùng SHA** (ba ảnh B2). Nội dung README cũ đã đưa vào [B2-REPORT.md](B2-REPORT.md); quy ước Git hiện tại ở [GIT.md](GIT.md) | Đóng, không merge lại README |
| [#3](https://github.com/s2005on/vnu-food-hola/pull/3) | Project Charter, Requirements, Design, Schedule B3 | **3/4 tệp trùng SHA:** Charter, Requirements, Schedule. [System Design](03-system-design.md) được cập nhật cho backend/API V7.3 | Đóng, giữ thiết kế mới |
| [#4](https://github.com/s2005on/vnu-food-hola/pull/4) | Scrum, Sprint 0, demo tĩnh B4 | **5/5 tệp trùng SHA**, gồm demo HTML và ảnh chứng cứ B4 | Đóng, giữ demo lịch sử |
| [#5](https://github.com/s2005on/vnu-food-hola/pull/5) | Risk Register và Quality Plan B5 | **2/2 tệp trùng SHA:** [RISKS.md](RISKS.md), [QUALITY.md](QUALITY.md) | Đóng, hồ sơ giữ nguyên |
| [#6](https://github.com/s2005on/vnu-food-hola/pull/6) | Phân vai, RACI, giao tiếp, báo cáo Sprint 0 | **2/2 tệp trùng SHA:** [TEAM.md](TEAM.md), [SPRINT0-REPORT.md](SPRINT0-REPORT.md) | Đóng, hồ sơ giữ nguyên |
| [#7](https://github.com/s2005on/vnu-food-hola/pull/7) | Tổng hợp B2–B7, cấu hình, bên liên quan và tag | **16/20 tệp trùng SHA**; README, thiết kế, CONFIG, GIT đã được cập nhật cho MVP; [STAKEHOLDERS.md](STAKEHOLDERS.md) và hồ sơ khác còn nguyên. Tag [v0.1.0](https://github.com/s2005on/vnu-food-hola/tree/v0.1.0) vẫn tồn tại | Đóng, không merge lại bản cũ |
| [#8](https://github.com/s2005on/vnu-food-hola/pull/8) | Giao diện demo V2 | **4/4 tệp trùng SHA** tại `demo/v2/`; giao diện có backend hiện tại ở `server/web/` | Đóng, không đưa UI cũ trở lại |

Tổng số mục thay đổi được đối chiếu theo từng PR: **41 lượt tệp**, trong đó **35 lượt trùng SHA** và **6 lượt đã được thay đổi/cập nhật**; các PR tích hợp cùng nội dung nên không phải 41 tệp duy nhất.

## Lịch sử và minh chứng được bảo toàn

- Các PR, nhánh `feature/b2-setup` đến `feature/ui-v2`, commit và ảnh chứng cứ vẫn được giữ để giảng viên xem theo từng bài.
- PR **Closed, not merged** có nghĩa yêu cầu kéo cũ đã kết thúc **mà không merge trực tiếp PR đó**. Không ghi đây là PR đã merge, được review độc lập hay được giảng viên chấp thuận.
- Mã ứng dụng hiện tại, cơ sở dữ liệu, menu và script triển khai **không bị sửa** trong lần xử lý các PR lịch sử.
- Bản demo B2/B4/V2 **không phải** bằng chứng backend V7.3 đã triển khai lên VPS công khai.
- Luồng chức năng hiện hành và kiểm thử: [README](../README.md), [VERIFICATION](../VERIFICATION.md), [MIDTERM](MIDTERM.md), [RELEASE-v0.2.0](RELEASE-v0.2.0.md).

## Bảng kiểm sau khi đóng PR

| Kiểm tra | Kết quả |
|---|---|
| PR #2–#8 trên GitHub | Closed, not merged; mỗi PR có bình luận đối chiếu |
| PR #9, #10, #11, #12 | Đã merge vào `main` trước cuộc rà soát này |
| Tệp/ảnh B2–B7 và demo V2 | Có trên `main` hoặc được giữ ở tài liệu hiện hành như bảng trên |
| Lịch sử Git và tag `v0.1.0` | Giữ nguyên, không force-push hay di chuyển tag |
| Xác nhận hosting công khai / nghiệm thu thầy | **Chưa xác minh**, cần bổ sung theo [MIDTERM.md](MIDTERM.md) |

**Lưu ý:** đây là biên bản rà soát repository, không thay thế quyết định chấm điểm/đánh giá của giảng viên.
