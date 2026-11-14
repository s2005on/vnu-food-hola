\# Quy ước Git và Pull Request



\## 1. Repo sử dụng

\- Repo dự án: https://github.com/s2005on/vnu-food-hola

\- Repo bài tập tuần riêng: https://github.com/s2005on/cse3045-23110216



Tài liệu và sản phẩm thực hành của dự án được lưu trong vnu-food-hola.



\## 2. Quy ước nhánh

\- main: bản ổn định đã được chọn để bàn giao.

\- develop: tích hợp các thay đổi của dự án.

\- feature/<noi-dung>: chức năng hoặc phần tài liệu mới.

\- fix/<noi-dung>: sửa lỗi.



Tạo nhánh mới từ develop đã cập nhật.

Không làm việc trực tiếp trên main.

Không force-push các nhánh dùng chung.



Riêng B7, nhánh feature/b7-config-release tích hợp các nhánh

B2–B6 để tạo một mốc có đủ tài liệu và demo.

Việc tích hợp này không đồng nghĩa các PR cũ đã được giảng viên duyệt.



\## 3. Quy ước commit

Dùng tiền tố:

\- feat: thêm chức năng.

\- fix: sửa lỗi.

\- docs: cập nhật tài liệu.

\- test: bổ sung hoặc sửa kiểm thử.

\- chore: cấu hình và công việc hỗ trợ.



Mỗi commit tập trung một mục đích, có mô tả rõ.

Chỉ thêm các tệp liên quan; kiểm tra thay đổi trước khi commit.

Không commit mật khẩu, token, môi trường ảo hoặc dữ liệu khách thật.



\## 4. Quy trình Pull Request

1\. Cập nhật develop và tạo nhánh riêng.

2\. Thực hiện thay đổi và kiểm tra phần bị ảnh hưởng.

3\. Commit, push nhánh lên GitHub.

4\. Tạo PR với base là develop.

5\. Ghi mục đích, nội dung thay đổi, cách kiểm tra và giới hạn.

6\. Rà soát Files changed; xử lý lỗi và góp ý nếu có.

7\. Merge sau khi các kiểm tra cần thiết đạt và đã xử lý góp ý.

8\. Khi chọn bản ổn định để bàn giao, tạo PR từ develop về main.



Dự án một người nên Sơn tự rà soát theo checklist.

Không ghi là có review độc lập nếu chưa có người khác review.

Không tự suy ra giảng viên đã duyệt chỉ vì PR không có bình luận.



PR B7 chứa cả phần tích hợp B2–B6 và ba tài liệu mới;

số tệp thay đổi có thể nhiều hơn ba.



\## 5. Checklist trước merge hoặc gắn tag

\- Đúng repo, đúng nhánh và đúng phạm vi thay đổi.

\- Tài liệu đọc được, đường dẫn và nội dung nhất quán.

\- Không có dấu xung đột Git chưa xử lý.

\- Không có bí mật hoặc dữ liệu riêng tư.

\- Phần chức năng bị ảnh hưởng đã được chạy thử.

\- Ghi rõ kiểm tra nào đã chạy, kiểm tra nào chưa chạy.

\- Có bằng chứng phù hợp; không dùng ảnh demo thay cho test backend.



\## 6. Quy ước phát hành

\- Áp dụng SemVer và kế hoạch trong CONFIG.md.

\- Mỗi bản phát hành dùng annotated tag, ví dụ v0.1.0.

\- Tag trỏ tới commit cụ thể đã được kiểm tra.

\- Ghi chú tag nêu nội dung và giới hạn của bản phát hành.

\- Push riêng nhánh và tag cần công bố; không dùng push --tags

&#x20; khi chưa kiểm tra toàn bộ tag trên máy.

\- Tag đã công bố không bị di chuyển hoặc ghi đè.

\- Khi sửa bản phát hành, tạo commit và phiên bản mới phù hợp.



Mốc đầu v0.1.0 dự kiến gồm tài liệu tích hợp và demo tĩnh.

Đây là mốc hiện tại của Sprint 1, không phải xác nhận hoàn thành

backend, DB hoặc toàn bộ mục tiêu Sprint 1.



Tag B7 có thể được công bố trên commit của nhánh B7 trước khi

PR được merge; mô tả PR phải ghi rõ trạng thái này.



Sau khi tạo tag, bổ sung vào mô tả PR:

\- Tên và link tag.

\- Commit mà tag trỏ tới.

\- Các kiểm tra đã thực hiện.

\- Các chức năng còn thiếu.



\## 7. Xử lý lỗi và khôi phục

\- Nếu merge có xung đột: dừng, đọc các phần xung đột,

&#x20; giữ nội dung cần thiết và kiểm tra lại trước khi commit.

\- Không dùng reset --hard để bỏ thay đổi khi chưa kiểm tra.

\- Với lỗi đã được tích hợp, ưu tiên commit sửa lỗi hoặc revert

&#x20; để giữ lịch sử rõ ràng.

\- Có thể checkout tag trong bản clone riêng để xem lại bản cũ.

\- Khôi phục mã nguồn không đồng nghĩa khôi phục cơ sở dữ liệu.

