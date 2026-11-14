\# Báo cáo Sprint 0 và kế hoạch Sprint 1



\## 1. Thông tin chung

\- Dự án: Website đặt đồ ăn cho sinh viên VJU.

\- Người thực hiện: Lâm Hải Sơn — MSSV 23110216.

\- Ngày lập báo cáo: 25/10/2026.

\- Nhân lực: một người.

\- Mục tiêu Sprint 0: chuẩn bị phạm vi, cách làm việc, môi trường

&#x20; và bản mẫu để minh họa ý tưởng.

\- Đề tài đã được giảng viên duyệt; không tích hợp AI trong kỳ này.



Báo cáo phân biệt sản phẩm đã tạo với việc được review hoặc nghiệm thu.

Có PR không đồng nghĩa PR đã được duyệt hoặc đã merge.



\## 2. Bằng chứng liên quan

\- \[B2 — Thiết lập dự án và môi trường](https://github.com/s2005on/vnu-food-hola/pull/2)

\- \[B3 — Phạm vi, thiết kế, WBS và lịch](https://github.com/s2005on/vnu-food-hola/pull/3)

\- \[B4 — Phân vai, backlog và bản mẫu](https://github.com/s2005on/vnu-food-hola/pull/4)

\- \[B5 — Rủi ro và kế hoạch chất lượng](https://github.com/s2005on/vnu-food-hola/pull/5)



Các tài liệu B4 nằm trên nhánh feature/b4-scrum.

Nếu chưa được merge vào develop, xem nội dung trong PR B4.



\## 3. Đối chiếu backlog Sprint 0



“Xong” trong bảng là hoàn thành sản phẩm nội bộ theo phạm vi

của công việc, không phải xác nhận nghiệm thu từ giảng viên.



| Mã | Công việc | Trạng thái | Kết quả và bằng chứng |

|---|---|---|---|

| S0-01 | Phân vai và thống nhất cách làm việc | Xong | Có docs/06-scrum-team.md trong PR B4; B6 bổ sung RACI và quy ước giao tiếp trong TEAM.md |

| S0-02 | Rà soát phạm vi và yêu cầu | Xong | Charter và yêu cầu đã cập nhật đề tài được duyệt, phạm vi không AI; PR B3 |

| S0-03 | Chuẩn bị câu hỏi trao đổi với quán | Xong phần chuẩn bị | Có danh sách câu hỏi trong docs/07-sprint-0-backlog.md, PR B4; chưa coi là đã thỏa thuận với quán |

| S0-04 | Kiểm tra môi trường phát triển | Xong ở mức phục vụ bản mẫu | Bằng chứng môi trường ở PR B2; bản mẫu B4 mở được trên trình duyệt; chưa xác nhận backend và DB hoàn chỉnh |

| S0-05 | Dựng bản mẫu luồng đặt món | Xong | demo/index.html trong PR B4 minh họa thực đơn, giỏ hàng và xác nhận đơn bằng dữ liệu giả |

| S0-06 | Kiểm tra bản mẫu và lưu ảnh | Xong ở mức luồng demo | Có ảnh docs/evidence/b4-demo.png và hướng dẫn docs/08-mvp-demo.md trong PR B4 |

| S0-07 | Demo ý tưởng và ghi nhận phản hồi | Đang dở | Đã có bản mẫu và hướng dẫn demo trong PR B4; chưa có biên bản demo trước lớp hoặc phản hồi bên ngoài |

| S0-08 | Chọn việc cho Sprint tiếp theo | Xong phần lập kế hoạch | Có hướng ưu tiên trong backlog B4; mục 6 báo cáo này cụ thể hóa phạm vi Sprint 1, chưa phải kết quả triển khai |



Không có hạng mục nào bị bỏ tại thời điểm lập báo cáo.

Phần còn dở của S0-07 được tiếp tục theo dõi trong Sprint 1.



\## 4. Kết quả và giới hạn



\### Đã có

\- Hồ sơ phạm vi, yêu cầu, thiết kế sơ bộ, WBS và lịch dự kiến.

\- Quy trình làm việc và backlog Sprint 0.

\- Bản mẫu giao diện thực đơn, giỏ hàng và xác nhận đơn giả.

\- Ảnh minh chứng và hướng dẫn mở bản mẫu.

\- Danh sách rủi ro và kế hoạch kiểm soát chất lượng.



\### Chưa hoàn thành

\- Backend và cơ sở dữ liệu phục vụ đặt món thực tế.

\- Đăng nhập và chức năng quản trị thực tế.

\- Xác nhận quán hợp tác, thực đơn, giá và quy trình nhận món.

\- Demo có ghi nhận phản hồi từ giảng viên hoặc người dùng.

\- Kiểm thử đầy đủ các tiêu chí chất lượng của sản phẩm.



Bản mẫu hiện tại dùng dữ liệu giả và dữ liệu trong trình duyệt;

không phải hệ thống nhận đơn thật, chưa chứng minh việc lưu đơn vào DB.



\## 5. Vướng mắc và bài học



| Vấn đề | Ảnh hưởng | Hướng xử lý |

|---|---|---|

| Một người kiêm nhiều vai trò | Khó làm nhiều phần cùng lúc | Chọn một luồng nhỏ mỗi Sprint, làm lần lượt |

| Chưa chốt thông tin với quán | Chưa có dữ liệu nghiệp vụ thực tế | Dùng dữ liệu mẫu có ghi rõ; tiếp tục trao đổi với quán |

| Tài liệu nằm ở nhiều nhánh | Có thể không thấy tệp khi đang ở nhánh khác | Dẫn PR làm bằng chứng; kiểm tra nhánh trước khi sửa |

| Chưa có phản hồi demo bên ngoài | Chưa kiểm chứng mức phù hợp của giao diện | Chuẩn bị demo ngắn và ghi nhận phản hồi thực tế |



Không có nhật ký giờ thực tế đầy đủ nên báo cáo không khẳng định

đã hoàn thành đúng số giờ ước lượng của Sprint 0.



\## 6. Phạm vi Sprint 1



\### Mục tiêu

Khách xem được thực đơn lấy từ API và cơ sở dữ liệu SQLite,

thay cho danh sách món viết cố định trong giao diện.



\### Thời gian và nguồn lực

\- Dự kiến: 26/10/2026–08/11/2026, điều chỉnh theo lịch học thực tế.

\- Người thực hiện và điều phối: Lâm Hải Sơn.

\- Quỹ thời gian dự kiến: 12 buổi, mỗi buổi 2 giờ.

\- Công việc: 20 giờ; dự phòng: 4 giờ.

\- Đây là kế hoạch, không phải hạn nộp chính thức hoặc tiến độ đã đạt.



\### Các Product Backlog Item được chọn



| Mã | Kết quả cần bàn giao | Giờ | Phụ thuộc | Điều kiện hoàn thành |

|---|---|---:|---|---|

| PBI-01 | Nền tảng FastAPI và SQLite chạy được | 4 | Không | Có hướng dẫn khởi động; tạo được bảng món và ít nhất 4 món mẫu; dữ liệu còn sau khi khởi động lại |

| PBI-02 | API đọc thực đơn | 4 | PBI-01 | GET /api/dishes trả dữ liệu từ DB, gồm tên, giá và tình trạng món; món đã ẩn không xuất hiện |

| PBI-03 | Giao diện thực đơn gọi API | 6 | PBI-02 | Hiển thị món từ API; có trạng thái tải, danh sách rỗng và lỗi kết nối |

| PBI-04 | Kiểm thử và minh chứng luồng xem món | 4 | PBI-03 | Có test API cho danh sách có dữ liệu, rỗng và lọc món ẩn; ảnh giao diện; hướng dẫn chạy lại |

| PBI-05 | Demo, ghi phản hồi và cập nhật backlog | 2 | PBI-04 | Có kịch bản và nhật ký demo; ghi phản hồi thực tế hoặc ghi rõ đang chờ, kèm việc theo dõi |



Tất cả PBI hiện ở trạng thái To do.

PBI-03 được tách thành các việc nhỏ: gọi API, hiển thị dữ liệu,

và xử lý trạng thái; mỗi việc khoảng 2 giờ.



\### Ngoài phạm vi Sprint 1

\- Tạo đơn thật và thanh toán.

\- Đăng nhập, quản lý món và quản lý đơn.

\- AI, thanh toán trực tuyến và theo dõi giao hàng.

\- Triển khai toàn bộ sản phẩm lên VPS.



\### Cách xử lý khi chậm

\- Dùng quỹ dự phòng cho lỗi môi trường hoặc tích hợp.

\- Ưu tiên luồng xem món, hoãn chỉnh sửa trang trí giao diện.

\- Nếu vẫn vượt quỹ thời gian, cập nhật backlog và báo rõ phần dở.

\- Không đánh dấu Done khi chưa có kết quả kiểm tra và bằng chứng.



\## 7. Cách cập nhật báo cáo

\- Liên kết PR/commit khi từng PBI hoàn thành.

\- Ghi thời gian thực tế từ Sprint 1.

\- Cập nhật phản hồi demo và các quyết định thay đổi phạm vi.

\- Tách rõ tự kiểm tra, phản hồi bên ngoài và trạng thái merge PR.

