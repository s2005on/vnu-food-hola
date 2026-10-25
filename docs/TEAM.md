\# Phân vai và quy ước giao tiếp



\## 1. Thông tin nhóm

\- Dự án: Website đặt đồ ăn cho sinh viên VJU.

\- Học phần: CSE3045.

\- Người thực hiện: Lâm Hải Sơn — MSSV 23110216.

\- Nhân lực: một người, kiêm nhiệm các vai trò.

\- Đề tài đã được giảng viên duyệt.

\- Phạm vi kỳ này không tích hợp AI.



\## 2. Bảng RACI



Quy ước:

\- R: người trực tiếp thực hiện.

\- A: người chịu trách nhiệm cuối cùng, kiểm tra và chấp nhận kết quả nội bộ.

\- C: bên cần tham vấn khi có vấn đề liên quan.

\- I: bên được thông báo kết quả khi cần.



Mỗi mảng có đúng một R và một A. Do dự án cá nhân,

Lâm Hải Sơn kiêm R và A; việc tự kiểm tra không được

coi là phản biện độc lập hoặc phê duyệt của giảng viên.



| Mảng công việc | R | A | C | I |

|---|---|---|---|---|

| Phạm vi, yêu cầu và ưu tiên backlog | Lâm Hải Sơn | Lâm Hải Sơn | Giảng viên; quán khi xác định được bên hợp tác | Giảng viên qua báo cáo |

| Thiết kế kiến trúc, API và dữ liệu | Lâm Hải Sơn | Lâm Hải Sơn | Giảng viên khi cần góp ý | Giảng viên qua PR |

| Backend và cơ sở dữ liệu | Lâm Hải Sơn | Lâm Hải Sơn | Giảng viên khi gặp vấn đề vượt khả năng xử lý | Giảng viên qua báo cáo |

| Giao diện khách hàng và quản trị | Lâm Hải Sơn | Lâm Hải Sơn | Người dùng thử khi có | Giảng viên qua demo |

| Kiểm thử và quản lý lỗi | Lâm Hải Sơn | Lâm Hải Sơn | Người dùng thử khi có | Giảng viên qua kết quả kiểm thử |

| Triển khai và sao lưu | Lâm Hải Sơn | Lâm Hải Sơn | Người quản lý VPS khi có lỗi hạ tầng | Giảng viên khi bàn giao bản chạy |

| Tài liệu và báo cáo tiến độ | Lâm Hải Sơn | Lâm Hải Sơn | Giảng viên khi cần làm rõ yêu cầu | Giảng viên qua LMS/PR |



Các bên C/I là đối tượng dự kiến trao đổi, không phải

thành viên đã cam kết tham gia hoặc đã duyệt sản phẩm.



\## 3. Điều phối theo Sprint



\- Mỗi Sprint dự kiến kéo dài 1–2 tuần.

\- Hiện tại Sơn điều phối mọi Sprint vì dự án chỉ có một người.

\- Chưa thể luân phiên giữa các thành viên; không tạo tên người giả.

\- Đầu Sprint: chọn mục tiêu, công việc ưu tiên và quỹ thời gian.

\- Trong Sprint: mỗi thời điểm tập trung một công việc chính.

\- Cuối Sprint: kiểm tra sản phẩm, ghi phần còn dở và chọn việc tiếp theo.

\- Nếu bổ sung thành viên, luân phiên điều phối theo thứ tự tên

&#x20; đã thống nhất; ghi người điều phối của từng Sprint trong báo cáo.

\- Khi bàn giao điều phối, chuyển backlog, trở ngại và các quyết định

&#x20; chưa chốt cho người tiếp nhận.



\## 4. Kênh và nhịp giao tiếp



| Kênh | Khi sử dụng | Cách lưu kết quả |

|---|---|---|

| GitHub Issue | Công việc, lỗi, câu hỏi và trở ngại không cần trao đổi ngay | Mô tả, người phụ trách, trạng thái và liên kết bằng chứng |

| GitHub Pull Request | Đề xuất thay đổi mã nguồn hoặc tài liệu | Mục đích, thay đổi, cách kiểm tra và kết quả |

| Trao đổi trực tiếp trong giờ học | Cần làm rõ yêu cầu hoặc xin góp ý demo | Ghi tóm tắt vào Issue/PR sau buổi trao đổi |

| Kênh liên hệ được thống nhất với quán | Xác nhận món, giá và quy trình nhận đơn | Ghi kết luận nghiệp vụ; không đưa thông tin riêng tư lên repo |

| LMS | Nộp bài theo yêu cầu học phần | Link PR/repo và ghi chú kết quả |



\- Cuối mỗi buổi làm: ghi việc đã làm, việc tiếp theo và trở ngại.

\- Cuối mỗi tuần: đối chiếu mục tiêu, thời gian thực tế và việc còn lại.

\- Khi chưa có người phản hồi, ghi rõ đang chờ; không tự ghi là đã duyệt.

\- Các nhịp trên là quy ước áp dụng từ tài liệu này, không phải

&#x20; khẳng định đã thực hiện đầy đủ trong các tuần trước.



\## 5. Ghi lại quyết định



Quyết định ảnh hưởng phạm vi, kỹ thuật hoặc lịch phải ghi trong Issue/PR:

\- Ngày và vấn đề cần quyết định.

\- Các phương án đã cân nhắc.

\- Phương án chọn và lý do.

\- Người quyết định; người góp ý nếu thực sự có.

\- Ảnh hưởng tới yêu cầu, WBS, lịch và kiểm thử.

\- Link thay đổi liên quan.



Phân biệt quyết định nội bộ với ý kiến giảng viên hoặc thỏa thuận

của quán. Chỉ ghi xác nhận bên ngoài khi đã nhận được phản hồi.



\## 6. Quy tắc báo tin xấu



\- Nếu bị chặn quá một buổi làm việc, ghi Issue ngay trong ngày.

\- Nếu có nguy cơ trễ mục tiêu Sprint, báo sớm trước buổi kiểm tra.

\- Nếu phát hiện lỗi mất dữ liệu hoặc lộ thông tin, dừng thao tác

&#x20; gây lỗi và báo ngay cho bên liên quan qua kênh phù hợp.

\- Nội dung báo gồm: vấn đề, bằng chứng, ảnh hưởng, cách đã thử,

&#x20; phương án xử lý, hỗ trợ cần thiết và thời điểm cập nhật tiếp.

\- Nếu thay đổi phạm vi hoặc mốc đã thống nhất với giảng viên,

&#x20; trao đổi lại và ghi kết quả vào tài liệu.

\- Không giấu lỗi, không ghi hoàn thành khi chưa có bằng chứng.

\- Không đưa mật khẩu, token hoặc dữ liệu khách hàng vào Issue/PR.

