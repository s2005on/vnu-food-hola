# Rà soát PR cũ - 15/11/2026

PR #10 đã merge vào main tại b2fce97027dc61bd73a4ce6fab71488ffbe3f738.
PR #2-#8 còn mở ở thời điểm kiểm tra. Bản sửa này không tự merge hoặc đóng chúng.

| PR | Nội dung | Cách xử lý cần đối chiếu |
|---|---|---|
| #2 | B2 / quy trình Git, rủi ro, VPS | So sánh hồ sơ với docs hiện tại |
| #3 | B3 / phạm vi và kế hoạch | Giữ phần hồ sơ còn thiếu |
| #4 | B4 / Scrum và backlog | So sánh docs và minh chứng |
| #5 | B5 / rủi ro và chất lượng | So sánh RISKS.md, QUALITY.md |
| #6 | B6 / RACI, giao tiếp, báo cáo | So sánh TEAM.md, SPRINT0-REPORT.md |
| #7 | B7 / cấu hình và phát hành | So sánh CONFIG.md, STAKEHOLDERS.md |
| #8 | UI demo V2 | Đối chiếu với UI V7.3, tránh đưa giao diện cũ trở lại |

Với từng PR, đọc Files changed và so sánh nội dung hiện hành. Nếu phần cần thiết đã có hoặc
được thay thế, đóng PR kèm giải thích và dẫn PR #10/bản sửa; nếu còn thiếu, chuyển riêng phần
cần giữ lên nhánh mới từ main, kiểm thử rồi merge. Không đóng chỉ vì PR cũ hoặc trùng tên tệp.
Không force-push main. Lưu link review làm bằng chứng học phần.
