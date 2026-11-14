\# Kế hoạch quản lý cấu hình



\## 1. Quản lý những gì?

\- Mã nguồn, giao diện mẫu và tài nguyên ảnh.

\- Tài liệu yêu cầu, thiết kế, WBS, lịch, rủi ro và báo cáo Sprint.

\- Kiểm thử, hướng dẫn chạy và bằng chứng kiểm tra.

\- Danh sách thư viện, tệp khóa phiên bản và cấu hình mẫu khi bổ sung.

\- Script khởi tạo, migration và dữ liệu mẫu khi có cơ sở dữ liệu.



Không đưa vào Git: môi trường ảo, tệp tạm, mật khẩu, token,

tệp .env chứa bí mật và dữ liệu khách hàng thực tế.

Cấu hình mẫu chỉ chứa tên biến và giá trị minh họa.



\## 2. Vai trò và trách nhiệm

\- Lâm Hải Sơn thực hiện thay đổi, kiểm tra, quản lý nhánh,

&#x20; tạo PR, gắn tag và sao lưu.

\- Do dự án cá nhân, Sơn kiêm người thực hiện và tự kiểm tra;

&#x20; đây không phải review độc lập.

\- Giảng viên góp ý, đánh giá theo học phần; không mặc định

&#x20; mọi PR hoặc bản phát hành đã được giảng viên duyệt.

\- Thay đổi nghiệp vụ liên quan quán cần được trao đổi với quán

&#x20; khi xác định được bên hợp tác.



\## 3. Công cụ

\- Git: lưu lịch sử và so sánh thay đổi.

\- GitHub: lưu repo từ xa, quản lý Issue, PR và tag.

\- PowerShell và trình soạn thảo: thao tác trên máy cá nhân.

\- Công cụ kiểm thử: được ghi trong hướng dẫn của từng phần

&#x20; khi có mã nguồn triển khai.

\- VPS học phần: môi trường triển khai khi cần; không phải

&#x20; nơi lưu duy nhất của mã nguồn hoặc bản sao dữ liệu.



\## 4. Điểm mốc và phiên bản



\### Quy tắc SemVer

Phiên bản có dạng MAJOR.MINOR.PATCH; tag Git thêm tiền tố v.



\- MAJOR: thay đổi không tương thích với giao diện/API đã công bố.

\- MINOR: bổ sung chức năng tương thích.

\- PATCH: sửa lỗi hoặc hiệu chỉnh nhỏ tương thích.

\- Giai đoạn 0.x.y là phát triển ban đầu, chưa cam kết API ổn định.

\- Trong giai đoạn 0.x, thay đổi phá vỡ tương thích tăng MINOR

&#x20; và phải mô tả rõ trong ghi chú phát hành.

\- Chỉ dùng 1.0.0 khi phạm vi bản đầu đạt tiêu chí nghiệm thu;

&#x20; không tăng phiên bản chỉ vì đến buổi học mới.



\### Mốc dự kiến

| Phiên bản | Nội dung | Điều kiện gắn tag |

|---|---|---|

| v0.1.0 | Mốc hiện tại của Sprint 1: tài liệu đã tích hợp và demo tĩnh | Kiểm tra tài liệu, chạy lại demo và ghi rõ giới hạn |

| v0.2.0 | Luồng xem thực đơn từ API và DB | Chạy được luồng, có kiểm thử và hướng dẫn |

| v1.0.0 | Bản đầu đáp ứng phạm vi nghiệm thu | Đối chiếu tiêu chí, có kết quả kiểm thử và vận hành thử |



Đây là các mốc dự kiến; trạng thái thực tế được xác định bằng

tag và bằng chứng trong repo.



v0.1.0 không khẳng định Sprint 1 đã hoàn thành.

Bản này chưa có backend/DB đặt món thực tế hoặc quản trị hoàn chỉnh.



Mỗi mốc phát hành sử dụng annotated tag trỏ tới commit đã kiểm tra.

Ghi chú tag nêu nội dung, giới hạn và kết quả kiểm tra.

Không di chuyển hoặc ghi đè tag đã công bố; tạo phiên bản mới khi sửa.



\## 5. Quy ước đặt tên

\- Nhánh chức năng: feature/<noi-dung>, ví dụ feature/b7-config-release.

\- Nhánh sửa lỗi: fix/<noi-dung>.

\- Commit: docs:, feat:, fix:, test: hoặc chore: kèm mô tả ngắn.

\- Tài liệu B7: docs/CONFIG.md, docs/STAKEHOLDERS.md, docs/GIT.md.

\- Tệp bằng chứng: tên thể hiện bài hoặc chức năng được kiểm tra.

\- Tag: vMAJOR.MINOR.PATCH, ví dụ v0.1.0.

\- Không dùng tên như final-new-final để thay thế quản lý phiên bản.



\## 6. Quy ước thay đổi

1\. Ghi vấn đề hoặc mục tiêu trong Issue/PR.

2\. Xem ảnh hưởng tới phạm vi, dữ liệu, giao diện và lịch.

3\. Thực hiện trên nhánh riêng.

4\. Kiểm tra phần bị ảnh hưởng; ghi kết quả thật và giới hạn.

5\. Tạo PR về develop, tự rà soát và xử lý góp ý nếu có.

6\. Tích hợp thay đổi; cập nhật tài liệu liên quan.

7\. Khi đạt mốc, kiểm tra commit đích rồi tạo và push tag.



Với B7, các nhánh B2–B6 được tích hợp trên feature/b7-config-release.

Tag đầu tiên có thể trỏ tới commit đã kiểm tra trên nhánh này

trong khi PR về develop còn chờ xử lý; phải ghi rõ trạng thái đó.



Thay đổi phạm vi đã thống nhất với giảng viên cần trao đổi lại.

Không coi việc tạo PR là đã được phê duyệt.



\## 7. Sao lưu và khôi phục

\- Cuối mỗi buổi làm: commit phần hoàn chỉnh và push nhánh lên GitHub.

\- Sau mỗi mốc phát hành: tạo thêm bản sao repo có lịch sử Git

&#x20; ở thiết bị hoặc nơi lưu riêng, tách khỏi máy làm việc.

\- Kiểm tra bản sao mở được và đọc được tag phát hành.

\- GitHub lưu mã nguồn, không thay thế bản sao dữ liệu vận hành.

\- Khi có DB thực tế: sao lưu ít nhất hằng ngày và trước migration;

&#x20; dùng cách sao lưu nhất quán của DB, lưu riêng ngoài repo công khai.

\- Trước vận hành thật: thử khôi phục DB và ghi kết quả.

\- Bí mật cấu hình được lưu riêng, có kiểm soát truy cập.



Khôi phục mã nguồn bằng cách clone repo và checkout tag cần dùng.

Khôi phục DB cần bản sao tương thích với phiên bản mã nguồn.

Không coi checkout tag là tự động khôi phục dữ liệu.



Các quy tắc sao lưu là kế hoạch áp dụng; chưa khẳng định

đã hoàn thành kiểm thử khôi phục hệ thống thực tế.

