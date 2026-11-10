# Chạy trên VPS học phần

Chỉ làm trong block được cấp. Các ví dụ dưới dùng SV21 và tài khoản student.
Không thực thi nguyên mẫu nếu đang ở VPS khác hoặc đường dẫn/cổng đã được nhóm khác sử dụng.

## 1. Chuẩn bị mã

Đẩy các tệp v3 lên nhánh `feature/backend-v3` của repo trước.
Trên VPS:

```bash
hostname -I
mkdir -p ~/projects
cd ~/projects
git clone --branch feature/backend-v3 https://github.com/s2005on/vnu-food-hola.git vju-food-live
cd vju-food-live
python3 -m venv .venv-vju
.venv-vju/bin/python -m pip install -r server/requirements.txt
mkdir -p ~/vju-food-data
chmod 700 ~/vju-food-data
export VJU_DB="$HOME/vju-food-data/food.sqlite3"
.venv-vju/bin/python -m server.manage admin --username son
```

Nếu thư mục vju-food-live đã có, kiểm tra git status và remote trước khi cập nhật; không xóa hay clone đè.
Nếu thiếu module venv, cài gói python3-venv theo quy định VPS của lớp.
Dữ liệu được đặt ngoài checkout để đổi phiên bản code không làm mất đơn.

## 2. Kiểm tra cổng rồi chạy service

```bash
ss -ltnp | grep ':8016 '
```

Nếu có tiến trình đang nghe, kiểm tra đó là gì; chọn cổng trống và sửa **cả** service và location Nginx.
Không dừng dịch vụ của nhóm khác.

Đọc `deploy/vju-food.service`, đối chiếu User, WorkingDirectory, ExecStart, VJU_DB và VJU_BASE_PATH.
Nếu các đường dẫn đúng và chưa có service trùng tên:

```bash
sudo install -m 0644 deploy/vju-food.service /etc/systemd/system/vju-food-23110216.service
sudo systemctl daemon-reload
sudo systemctl enable --now vju-food-23110216
sudo systemctl status vju-food-23110216 --no-pager
curl -i http://127.0.0.1:8016/api/health
```

Kỳ vọng JSON `{"ok":true}`. Nếu lỗi:
`sudo journalctl -u vju-food-23110216 -n 50 --no-pager`.
Không mở trực tiếp cổng 8016 ra Internet.

## 3. Nginx, đường dẫn riêng

Địa chỉ dự kiến: `https://sv21.bcse-vju.com/b1-23110216/v3/`.
Đọc cấu hình hiện tại bằng `sudo nginx -T`. Sao lưu file server hiện hành ra ngoài sites-enabled.
Chèn hai khối trong `deploy/nginx-location.conf` **bên trong server của tên miền được cấp**.
Không thay nguyên server block, không xóa location / của ShiloSkin hoặc đường dẫn B1/V2.
Đường dẫn v3 dài hơn nên được Nginx ưu tiên so với location B1.
Dấu `/` cuối proxy_pass bắt buộc để bỏ tiền tố trước khi gửi sang FastAPI.

```bash
sudo nginx -t && sudo systemctl reload nginx
curl -i -H 'Host: sv21.bcse-vju.com' http://127.0.0.1/b1-23110216/v3/api/health
```

Sau khi local OK, mở HTTPS trên trình duyệt; thử đặt đơn và đăng nhập trang:
`https://sv21.bcse-vju.com/b1-23110216/v3/admin.html`.
Bản này dùng cookie Secure nên không đăng nhập qua HTTP ngoài localhost.

## 4. Sao lưu và thử khôi phục

Tại thư mục repo, dùng cùng VJU_DB với service:

```bash
export VJU_DB="$HOME/vju-food-data/food.sqlite3"
.venv-vju/bin/python -m server.manage backup --output "$HOME/vju-food-data/backup-$(date +%Y%m%d-%H%M%S).sqlite3"
```

Sao lưu chứa thông tin đơn và bí mật truy cập: giữ riêng, không đưa vào repo/public web.
Kiểm tra bản sao bằng SQLite `PRAGMA integrity_check` và chạy thử bằng VJU_DB trỏ tới **bản sao của backup**,
trên cổng thử riêng, không thay dữ liệu đang chạy. Khi cần khôi phục thật: dừng service, giữ toàn bộ thư mục
dữ liệu hiện tại làm bản dự phòng, khôi phục backup vào thư mục dữ liệu mới và đổi VJU_DB của service.
Không chép đè tệp DB khi tiến trình còn mở; không bỏ qua các tệp WAL/SHM đang tồn tại.

## 5. Cập nhật và quay lại phiên bản

Sao lưu DB, ghi lại `git rev-parse HEAD`. Fetch code, kiểm tra commit và chạy tests trước khi đổi bản.
Chỉ khi checkout sạch, cập nhật nhánh bằng `git pull --ff-only`, cài lại requirements nếu thay đổi rồi
`sudo systemctl restart vju-food-23110216`. Kiểm tra health và luồng đặt/tra cứu.
Nếu cần rollback code: quay về commit đã ghi, cài requirements tương ứng và restart.
Phiên bản v3 hiện không có migration tự động cho thay đổi schema tương lai; không rollback schema một cách mù quáng.

Block hết hạn không bảo đảm web vẫn hoạt động. Code nằm trên GitHub; giữ backup DB riêng và tuân thủ lịch VPS.
