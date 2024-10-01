# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymongo
import json
# from bson.objectid import ObjectId
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import csv

class MongoDBCafeLandPipeline:
    def __init__(self):
        
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client['dbmycrawler'] #Database      
        pass
    
    def process_item(self, item, spider):
        
        collection =self.db['tblcafeland'] #Table
        try:
            collection.insert_one(dict(item))
            return item
        except Exception as e:
            raise DropItem(f"Error inserting item: {e}")       
        pass

class JsonDBCafeLandPipeline:
    def process_item(self, item, spider):
        with open('jsondatacafeland.json', 'a', encoding='utf-8') as file:
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            file.write(line)
        return item

# class CSVDBCafelandPipeline:
#     '''
#     mỗi thông tin cách nhau với dấu $
#     Ví dụ: coursename$lecturer$intro$describe$courseUrl
#     Sau đó, cài đặt cấu hình để ưu tiên Pipline này đầu tiên
#     '''
#     def process_item(self, item, spider):
#         with open('csvdatacafeland.csv', 'a', encoding='utf-8', newline='') as file:
#             writer = csv.writer(file, delimiter='$')
#             writer.writerow([
#                 item['Loại dự án'],
#                 item['Tên dự án'],
#                 item['Đường'],
#                 item['Thành phố'],
#                 item['Chủ đầu tư'],
#                 item['Trạng thái'],
#                 item['Diện tích:'],
#                 item['Ngày đăng'],
#                 item['Tổng vốn đầu tư'],
#                 item['Xếp hạng'],
#                 item['Mô tả']
#             ])
#         return item
#     pass

import os

class CSVDBCafeLandPipeline:
    def __init__(self):
        # Mở file để ghi (ở chế độ 'a' - append), kiểm tra xem có phải là file mới không
        self.file_path = 'Cafeland.csv'
        self.file = open(self.file_path, 'a', encoding='utf-8', newline='')
        self.writer = csv.writer(self.file, delimiter=',')  # Sử dụng dấu phẩy để phân tách

        # Kiểm tra xem file có rỗng hay không để ghi tiêu đề
        if os.path.getsize(self.file_path) == 0:  # Kiểm tra kích thước file
            self.writer.writerow([
                'Loại dự án',
                'Tên dự án',
                'Đường',
                'Thành phố',
                'Chủ đầu tư',
                'Trạng thái',
                'Diện tích:',
                'Ngày đăng',
                'Tổng vốn đầu tư',
                'Xếp hạng',
                'Mô tả',
            ])
    
    def process_item(self, item, spider):
        print(f"Processing item: {item}")
        self.writer.writerow([
            item.get('Loại dự án', 'N/A'),
            item.get('Tên dự án', 'N/A'),
            item.get('Đường', 'N/A'),
            item.get('Thành phố', 'N/A'),
            item.get('Chủ đầu tư', 'N/A'),
            item.get('Trạng thái', 'N/A'), 
            item.get('Diện tích:', 'N/A'),
            item.get('Ngày đăng', 'N/A'),
            item.get('Tổng vốn đầu tư', 'N/A'),
            item.get('Xếp hạng', 'N/A'),
            item.get('Mô tả', 'N/A'),
        ])
        return item
    
    def close_spider(self, spider):
        self.file.close()  # Đảm bảo đóng file khi spider kết thúc

        pass