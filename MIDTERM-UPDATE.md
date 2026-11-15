# Cập nhật bản sửa giữa kỳ

Bản này xây từ main b2fce97027dc61bd73a4ce6fab71488ffbe3f738, không chứa database hoặc mật khẩu.
Sửa README/hướng dẫn/thiết kế API; bổ sung bảng kiểm nghiệm thu, rà soát PR, đủ bộ CI,
kiểm tra web công khai và sửa health probe của installer. Không thay giao diện hay dữ liệu món.

## Đưa lên GitHub trên máy bạn

Mở PowerShell trong thư mục đã giải nén bản sửa (có README.md này), chạy:

```powershell
powershell -ExecutionPolicy Bypass -File .\PUBLISH-MIDTERM.ps1
```

Script tạo checkout mới cạnh thư mục giải nén, chỉ áp dụng các tệp sửa; không sửa repository
cũ hoặc database. Nếu main đã đổi kể từ bản gốc, script dừng để đối chiếu, không ghi đè.
Git phải đăng nhập để push; tên/email tác giả phải được cấu hình. Sau push, mở link PR mà
script in ra; xem diff/CI rồi merge. Không ghi mật khẩu quản trị lên GitHub.

## Chạy thử / cập nhật VPS

Chạy RUN-WINDOWS.bat; đọc START-V7.3.md để giữ dữ liệu cũ.
Sau khi PR sửa giữa kỳ đã merge, thực hiện deploy/README.md trên VPS trong block được cấp.
Ghi link web, commit và kết quả thực tế vào docs/MIDTERM.md. Không chỉ nộp file ZIP thay hosting.
