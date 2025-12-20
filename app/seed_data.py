import pymongo
import os
import re
import ast
from datetime import datetime
from dotenv import load_dotenv
import certifi

# --- 1. CẤU HÌNH ---
load_dotenv()
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ecommerce_db")

if not MONGODB_URL:
    print("❌ LỖI: Chưa có MONGODB_URL trong file .env")
    exit()

try:
    client = pymongo.MongoClient(MONGODB_URL, tlsCAFile=certifi.where())
    db = client[DATABASE_NAME]
    print(f"✅ Đã kết nối MongoDB: {DATABASE_NAME}")
except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")
    exit()

# --- 2. HÀM XỬ LÝ THÔNG MINH (FINAL VERSION) ---
def smart_parse_js(file_path):
    if not os.path.exists(file_path):
        print(f"⚠️ Bỏ qua: Không tìm thấy file {file_path}")
        return []
    
    print(f"--> Đang đọc file: {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # [BƯỚC 1] Cắt lấy phần mảng dữ liệu [...]
    start_idx = content.find('[')
    end_idx = content.rfind(']') + 1
    if start_idx == -1:
        print("❌ Không tìm thấy mảng dữ liệu [...]")
        return []
    list_content = content[start_idx:end_idx]

    # [BƯỚC 2] Bảo vệ URL (https://) trước khi xóa comment
    # Thay thế :// thành __COLON_SLASH_SLASH__ để regex không xóa nhầm
    list_content = list_content.replace("://", "__COLON_SLASH_SLASH__")

    # [BƯỚC 3] Xóa comment
    # Xóa // ... (Comment 1 dòng)
    list_content = re.sub(r'//.*', '', list_content)
    # Xóa /* ... */ (Comment nhiều dòng)
    list_content = re.sub(r'/\*.*?\*/', '', list_content, flags=re.DOTALL)

    # [BƯỚC 4] Khôi phục URL
    list_content = list_content.replace("__COLON_SLASH_SLASH__", "://")

    # [BƯỚC 5] Xử lý cú pháp JS -> Python
    # Date: new Date("...") -> datetime(...)
    list_content = re.sub(r'new Date\((["\'])(.*?)\1\)', r'datetime.fromisoformat("\2".replace("Z", "+00:00"))', list_content)
    
    # Boolean & Null
    list_content = list_content.replace("true", "True").replace("false", "False").replace("null", "None")
    
    # Enum constants: STATUS.Xyz -> "Xyz"
    list_content = re.sub(r'STATUS\.(\w+)', r'"\1"', list_content)
    list_content = re.sub(r'ROLE\.(\w+)', r'"\1"', list_content)

    # [BƯỚC 6] Định nghĩa biến môi trường cho eval
    # Liệt kê tất cả các key có thể có trong file mock của bạn
    keys_to_mock = [
        "id", "title", "description", "brand", "category", "price", "discountPercentage", 
        "rating", "stock", "availabilityStatus", "sku", "minimumOrderQuantity", "returnPolicy",
        "warrantyInformation", "shippingInformation", "tags", "weight", "dimensions", "width", 
        "height", "depth", "thumbnail", "images", "meta", "createdAt", "updatedAt", "barcode", 
        "qrCode", "reviews", "comment", "reviewerName", "customer", "email", "originalTotal", 
        "discount", "total", "status", "date", "items", "productId", "quantity", "appliedVouchers", 
        "voucherCode", "discountAmount", "shippingAddress", "paymentMethod", "note", "code", 
        "receiveStartTime", "receiveEndTime", "validityDays", "minimumPurchase", "discountPercent", 
        "maxDiscount", "totalQuantity", "claimedCount", "usedCount", "isActive", "username", 
        "password", "dob", "address", "role", "avatar", "isVerified", "vouchers", "claimedAt", "isUsed"
    ]
    
    eval_context = {key: key for key in keys_to_mock}
    eval_context["datetime"] = datetime

    try:
        # Chuyển chuỗi text thành List Dictionary Python
        data = eval(list_content, {}, eval_context)
        return data
    except Exception as e:
        print(f"❌ Lỗi cú pháp khi parse: {e}")
        # Mẹo: In ra 100 ký tự đầu tiên để debug nếu vẫn lỗi
        # print("DEBUG CONTENT:", list_content[:100])
        return []

# --- 3. SEED DATA ---
def seed_all():
    # 1. Products
    products = smart_parse_js("mock_products.js")
    if products:
        db["products"].drop()
        db["products"].insert_many(products)
        print(f"✅ Đã thêm {len(products)} sản phẩm.")

    # 2. Vouchers
    vouchers = smart_parse_js("mock_vouchers.js")
    if vouchers:
        db["vouchers"].drop()
        db["vouchers"].insert_many(vouchers)
        print(f"✅ Đã thêm {len(vouchers)} voucher.")

    # 3. Users
    users = smart_parse_js("mock_users.js")
    if users:
        for u in users:
            # Chuẩn hóa role thành chữ thường (admin/user)
            if isinstance(u.get('role'), str): u['role'] = u['role'].lower()
        db["users"].drop()
        db["users"].insert_many(users)
        print(f"✅ Đã thêm {len(users)} users.")

    # 4. Orders
    orders = smart_parse_js("mock_orders.js")
    if orders:
        db["orders"].drop()
        db["orders"].insert_many(orders)
        print(f"✅ Đã thêm {len(orders)} đơn hàng.")

if __name__ == "__main__":
    print("🚀 BẮT ĐẦU SEED DATA (FINAL)...")
    seed_all()
    print("🎉 HOÀN TẤT!")