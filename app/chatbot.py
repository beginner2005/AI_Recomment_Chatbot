# app/chatbot.py
import os
import google.generativeai as genai
from datetime import datetime
from app.database import products_collection, vouchers_collection
from app.recommender import recommender
from dotenv import load_dotenv

load_dotenv()

# --- CẤU HÌNH ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print(" LỖI: Chưa set GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

# ---  CÁC TOOLS ---
def search_products(query: str):
    """Tìm sản phẩm theo tên, hãng hoặc mô tả."""
    print(f"--> [BOT] Đang tìm sản phẩm: {query}")
    try:
        products = list(products_collection.find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"brand": {"$regex": query, "$options": "i"}},
                {"category": {"$regex": query, "$options": "i"}}
            ]
        }).limit(5))
        
        if not products: return "Không tìm thấy sản phẩm nào."
            
        result_str = ""
        for p in products:
            price = f"${p.get('price', 0)}"
            stock = "Còn hàng" if p.get('stock', 0) > 0 else "Hết hàng"
            result_str += f"- {p.get('title')} | Hãng: {p.get('brand')} | Giá: {price} | {stock}\n"
        return result_str
    except Exception as e: return f"Lỗi DB: {str(e)}"

def get_personal_recommendations(user_id: str):
    """Lấy gợi ý cá nhân hóa."""
    print(f"--> [BOT] Gợi ý cho user: {user_id}")
    try:
        items = recommender.recommend(user_id, n_items=5)
        if not items: return "Khách mới, gợi ý sản phẩm bán chạy."
        return str([f"{item['title']} (${item['price']})" for item in items])
    except Exception as e: return f"Lỗi RecSys: {str(e)}"

def lookup_vouchers(query: str = ""):
    """Tra cứu mã giảm giá."""
    print(f"--> [BOT] Tìm voucher: {query}")
    try:
        filter_query = {"isActive": True}
        if query and query.strip():
            filter_query["$or"] = [
                {"code": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        vouchers = list(vouchers_collection.find(filter_query).limit(5))
        if not vouchers: return "Không có mã giảm giá nào phù hợp."
        
        res = ""
        for v in vouchers:
            res += f" {v.get('code')} - {v.get('description')} (Min: ${v.get('minimumPurchase', 0)})\n"
        return res
    except Exception as e: return f"Lỗi Voucher: {str(e)}"

# ---  CẤU HÌNH AI & MEMORY ---
tools_list = [search_products, get_personal_recommendations, lookup_vouchers]

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=tools_list,
    system_instruction="""
    Bạn là Trợ lý AI của cửa hàng TechShop.
    - Xưng hô: "Mình" (hoặc Shop) và "Bạn" (hoặc Khách).
    - Tính cách: Thân thiện, nhiệt tình, nhớ thông tin khách đã nói.
    - Nếu khách giới thiệu tên, hãy nhớ tên đó để xưng hô.
    - Giá tiền luôn dùng đơn vị USD ($).
    """
)

# Biến toàn cục để lưu bộ nhớ chat của từng user
# Dạng: { "user_id_1": chat_session_object, "user_id_2": ... }
user_chat_sessions = {}

def chat_process(user_id: str, message: str) -> str:
    global user_chat_sessions
    
    try:
        # 1. Kiểm tra xem User này đã có session chưa
        if user_id not in user_chat_sessions:
            print(f"- Tạo phiên chat MỚI cho user: {user_id}")
            # Nếu chưa, tạo mới và lưu vào từ điển
            user_chat_sessions[user_id] = model.start_chat(
                history=[
                    # Có thể thêm lịch sử mẫu nếu muốn
                ],
                enable_automatic_function_calling=True
            )
        else:
            print(f"- Dùng lại phiên chat CŨ cho user: {user_id}")

        # 2. Lấy session của user đó ra dùng
        chat_session = user_chat_sessions[user_id]
        
        # 3. Gửi tin nhắn (Không cần nhét User ID vào prompt nữa vì session đã riêng biệt)
        response = chat_session.send_message(message)
        
        return response.text
        
    except Exception as e:
        print(f"- Lỗi Chat: {e}")
        # Nếu lỗi session (ví dụ để lâu quá bị timeout), xóa đi để lần sau tạo mới
        if user_id in user_chat_sessions:
            del user_chat_sessions[user_id]
        return "Hệ thống đang khởi động lại trí nhớ, bạn hỏi lại giúp mình nhé! 🥺"