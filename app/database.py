from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi 
import sys

load_dotenv()

# Lấy URL từ .env
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ecommerce_db")

if not MONGODB_URL:
    print("LỖI: Chưa tìm thấy MONGODB_URL trong file .env")
    sys.exit(1)

# Cấu hình kết nối
try:
    client = MongoClient(MONGODB_URL, tlsCAFile=certifi.where())
    
    client.admin.command('ping')
    print("Đã kết nối thành công đến MongoDB Atlas!")
    
    db = client[DATABASE_NAME]

    # Collections
    users_collection = db["users"]
    products_collection = db["products"]
    interactions_collection = db["interactions"]
    vouchers_collection = db["vouchers"]
    orders_collection = db["orders"]

except Exception as e:
    print(f"Kết nối thất bại: {e}")
    sys.exit(1)

def get_database():
    return db