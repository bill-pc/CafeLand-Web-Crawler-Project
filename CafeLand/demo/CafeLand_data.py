import pandas as pd
import json
from pymongo import MongoClient

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["cafeland_clean"]
collection = db["Clear"]

# Đọc file CSV
df = pd.read_csv(r'cleaned_cafeland.csv/part-00000-49b3ad0f-f262-439e-b701-b6d06a147cfa-c000.csv')

# Chuyển đổi mỗi hàng thành dictionary và đổ vào MongoDB
data = df.to_dict(orient="records")

# Xóa tất cả dữ liệu cũ trong collection trước khi chèn dữ liệu mới (tùy chọn)
collection.delete_many({})

# Chèn dữ liệu mới vào MongoDB
collection.insert_many(data)

# Lấy tất cả dữ liệu từ MongoDB để xuất ra file JSON
data_from_mongo = list(collection.find())

# Mở file để ghi dữ liệu có số thứ tự
with open('CafeLand_data_with_numbered_records.json', 'w', encoding='utf-8') as file:
    for index, record in enumerate(data_from_mongo, start=1):
        # Ghi số thứ tự trước mỗi bản ghi
        file.write(f"{index} " + json.dumps(record, ensure_ascii=False, indent=4, default=str) + "\n")

print("Dữ liệu đã được xuất ra file JSON tổng hợp thành công!")
