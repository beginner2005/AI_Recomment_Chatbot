from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi # Thêm thư viện này để fix lỗi SSL
import sys

load_dotenv()

# Lấy URL từ .env
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ecommerce_db")

if not MONGODB_URL:
    print("LỖI: Chưa tìm thấy MONGODB_URL trong file .env")
    sys.exit(1)

# Cấu hình kết nối (Thêm tlsCAFile để tránh lỗi SSLHandshakeError)
try:
    client = MongoClient(MONGODB_URL, tlsCAFile=certifi.where())
    
    # Thử "ping" server để xem kết nối được chưa
    client.admin.command('ping')
    print("Đã kết nối thành công đến MongoDB Atlas!")
    
    db = client[DATABASE_NAME]

    # Collections
    users_collection = db["users"]
    products_collection = db["products"]
    interactions_collection = db["interactions"]

except Exception as e:
    print(f"Kết nối thất bại: {e}")
    # Nếu kết nối DB lỗi thì app không nên chạy tiếp
    sys.exit(1)

def get_database():
    return db