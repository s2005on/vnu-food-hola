# vnu-food-hola

Website đặt đồ ăn cho sinh viên VNU

\## Người thực hiện



\- Lâm Hải Sơn — MSSV: 23110216.

\- Hiện tại dự án có một người thực hiện, phụ trách tài liệu,

&#x20; giao diện, backend, kiểm thử và triển khai.



\## Quy trình Git của dự án



\- main: phiên bản ổn định.

\- develop: nhánh tích hợp các thay đổi.

\- feature/\*: nhánh thực hiện từng công việc.

\- Quy trình: tạo nhánh từ develop → sửa và kiểm tra →

&#x20; commit → push → mở Pull Request vào develop → review → merge.

\- Mỗi PR trình bày: thay đổi gì, vì sao, cách kiểm tra

&#x20; và phần có AI hỗ trợ.

\- Do hiện chỉ có một thành viên, việc review chéo cần được

&#x20; giảng viên hướng dẫn cách thay thế. Tự kiểm tra và AI hỗ trợ

&#x20; không được ghi nhận thành review của thành viên khác.



\## Pre-mortem: Vì sao đồ án có thể thất bại?



Giả định cuối kỳ sản phẩm không đạt yêu cầu, các nguyên nhân

có thể xảy ra và cách phòng ngừa gồm:



| STT | Nguy cơ thất bại | Nhóm nguyên nhân CHAOS | Hành động phòng ngừa |

|---|---|---|---|

| 1 | Chưa hiểu sinh viên cần gì khi đặt đồ ăn | Yêu cầu | Hỏi thử sinh viên mục tiêu, ghi lại nhu cầu và tiêu chí chấp nhận trước khi làm tính năng. |

| 2 | Liên tục thêm thanh toán, giao hàng, khuyến mãi khiến phạm vi quá lớn | Yêu cầu | Chốt phạm vi MVP; đưa ý tưởng mới vào danh sách chờ và chỉ thêm khi việc cốt lõi đã chạy. |

| 3 | Làm xong mới cho người dùng xem, phát hiện luồng đặt món khó dùng | Con người/bên liên quan | Cho người dùng thử từng luồng nhỏ và ghi nhận phản hồi sớm. |

| 4 | Một người phải làm mọi phần, bị quá tải khi trùng lịch học | Quản lý/nguồn lực | Chia công việc thành nhiệm vụ nhỏ, ưu tiên chức năng bắt buộc và dành thời gian dự phòng. |

| 5 | Ước lượng thiếu thời gian kiểm thử và triển khai | Quản lý/nguồn lực | Tính cả thời gian sửa lỗi, kiểm thử và deploy; chỉ đánh dấu hoàn thành khi có kết quả kiểm tra. |

| 6 | Hết block VPS hoặc lỗi môi trường sát hạn nộp | Quản lý/nguồn lực | Đặt block sớm, lưu mã trên GitHub, ghi lại lệnh chạy và kiểm tra triển khai trước hạn. |





