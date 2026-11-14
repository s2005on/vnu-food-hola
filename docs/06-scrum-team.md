# B4 — Phân vai và cách làm việc

## 1. Thông tin
- Dự án: Website đặt đồ ăn cho sinh viên VJU.
- Người thực hiện: Lâm Hải Sơn — MSSV 23110216.
- Nhân lực: một sinh viên, kiêm nhiệm các vai trò.
- Phạm vi: một quán, không tích hợp AI trong đồ án kỳ này.

## 2. Quy trình được chọn
Chọn Scrum làm định hướng tổ chức phát triển theo yêu cầu B4.
Do thực hiện cá nhân, áp dụng cách làm điều chỉnh cho một người:
lập mục tiêu ngắn hạn, chọn công việc, theo dõi tiến độ,
demo kết quả và rút kinh nghiệm.

Sprint 0 là giai đoạn chuẩn bị theo bài thực hành:
lập backlog, chuẩn bị môi trường và mô hình demo ý tưởng.

## 3. Bảng phân vai

| Vai trò / phần việc | Người phụ trách | Trách nhiệm |
|---|---|---|
| Product Owner (kiêm nhiệm) | Lâm Hải Sơn | Tổng hợp nhu cầu, sắp xếp ưu tiên và giới hạn phạm vi MVP; lấy phản hồi từ quán và giảng viên |
| Scrum Master / điều phối (kiêm nhiệm) | Lâm Hải Sơn | Lập lịch làm việc, theo dõi trở ngại và duy trì việc cập nhật tiến độ |
| Backend | Lâm Hải Sơn | Xây dựng FastAPI, xử lý đặt đơn, tính tiền và kiểm tra quyền |
| Frontend | Lâm Hải Sơn | Xây dựng giao diện thực đơn, giỏ hàng, đặt món và quản trị |
| Kiểm thử | Lâm Hải Sơn | Viết test, kiểm tra luồng sử dụng và ghi nhận lỗi |
| Báo cáo / tài liệu | Lâm Hải Sơn | Cập nhật tài liệu, lưu bằng chứng và chuẩn bị demo |

Giảng viên và quán là bên góp ý; không ghi nhận họ là thành viên
phát triển hoặc người đã review khi chưa có phản hồi thực tế.

## 4. Cách theo dõi công việc
- Dự kiến mỗi sprint phát triển kéo dài một tuần.
- Đầu sprint: chọn mục tiêu và công việc phù hợp quỹ thời gian.
- Mỗi buổi: ghi việc đã làm, việc tiếp theo và trở ngại.
- Bảng công việc gồm: To do, Doing, Done.
- Chỉ thực hiện một công việc chính tại một thời điểm.
- Cuối sprint: demo phần đã làm, ghi phản hồi và điều chỉnh backlog.
- Ghi ngắn điều làm tốt và điều cần cải thiện cho sprint sau.

## 5. Điều kiện đánh dấu Done
- Đáp ứng tiêu chí hoàn thành của công việc.
- Đã tự kiểm tra; có test nếu công việc liên quan xử lý nghiệp vụ.
- Mã nguồn hoặc tài liệu đã được commit và push.
- Có bằng chứng phù hợp: kết quả test, ảnh hoặc link demo.
- Ghi riêng trạng thái chờ review; không coi tự kiểm tra là review độc lập.
