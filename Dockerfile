# Sử dụng Python 3.9
FROM python:3.9-slim

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép các file yêu cầu vào container
COPY requirements.txt requirements.txt

# Cài đặt các gói phụ thuộc
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn của bạn vào container
COPY . .
# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
# Entry point for the application
CMD ["python", "-m", "scrapy", "runspider", "CafeLand/demo/spiders/myscraper.py"]