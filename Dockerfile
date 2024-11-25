# Sử dụng Python 3.11-alpine
FROM python:3.10-alpine

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Mở cổng 5001
EXPOSE 5001 
EXPOSE 8501

# Chạy ứng dụng Flask
CMD ["sh", "-c", "python app.py & streamlit run home.py --server.port=8501 --server.address=0.0.0.0"]
