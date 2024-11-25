# Sử dụng Python 3.11-alpine
FROM python:3.11-alpine

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Mở cổng 5001
EXPOSE 5001 8501

# Chạy ứng dụng Flask
CMD ["bash", "init.sh"]
