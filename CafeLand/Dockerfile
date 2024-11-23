FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Sử dụng lệnh trực tiếp và không cần "sh -c"
CMD ["python", "-m", "scrapy", "runspider", "demo/spiders/myscraper.py"]
