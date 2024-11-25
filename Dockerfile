# Sử dụng Python 3.10-alpine
FROM python:3.10-alpine

# Đặt thư mục làm việc
WORKDIR /app

# Cài đặt các thư viện hệ thống cần thiết
RUN apk add --no-cache \
    gcc musl-dev python3-dev libffi-dev openssl-dev \
    libxml2-dev libxslt-dev g++ make bash libstdc++

# Sao chép file requirements.txt
COPY requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn
COPY . .

# Mở cổng 5001 và 8501
EXPOSE 5001
EXPOSE 8501

# Chạy Flask và Streamlit
CMD ["sh", "-c", "python app.py & streamlit run home.py --server.port=8501 --server.address=0.0.0.0"]
