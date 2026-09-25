# Sử dụng base image Python phiên bản nhẹ (slim)
FROM python:3.12.14-slim

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Khắc phục lỗi thiếu thư viện hệ thống khi cài psycopg2 trên Linux
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Cài đặt các thư viện Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code vào container
COPY . .

# Mở cổng 8000 để giao tiếp ra bên ngoài
EXPOSE 8000

# Lệnh khởi chạy server khi container bật lên
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]