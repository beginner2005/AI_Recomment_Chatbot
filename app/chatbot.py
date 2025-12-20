# app/chatbot.py
import os
import google.generativeai as genai
from app.database import get_database
from app.recommender import recommender
from dotenv import load_dotenv

load_dotenv()

# --- CẤU HÌNH KEY ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("LỖI: Chưa set GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

# --- TOOLS ---

def search_products(query: str):
    """
    Tìm kiếm sản phẩm theo tên (title) hoặc mô tả.
    """
    print(f"--> [BOT] Tìm kiếm: {query}")
    db = get_database()
    try:
        # Tìm trong title hoặc description (case-insensitive)
        products = list(db["products"].find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        }).limit(5))
        
        if not products:
            return "Không tìm thấy sản phẩm nào trong kho."
        
        # Format kết quả trả về cho Gemini đọc
        result_str = ""
        for p in products:
            result_str += f"- {p.get('title')} | Hãng: {p.get('brand')} | Giá: ${p.get('price')} | Stock: {p.get('stock')}\n"
        
        return result_str
    except Exception as e:
        return f"Lỗi DB: {str(e)}"

def get_personal_recommendations(user_id: str):
    """
    Gợi ý sản phẩm cho User ID cụ thể.
    """
    print(f"--> [BOT] Gợi ý cho user: {user_id}")
    try:
        items = recommender.recommend(user_id, n_items=5)
        if not items:
            return "Chưa có đủ dữ liệu để gợi ý (User mới)."
        
        result_str = "Gợi ý riêng cho bạn:\n"
        for item in items:
            result_str += f"- {item['title']} (Giá: ${item['price']})\n"
        return result_str
    except Exception as e:
        return f"Lỗi Recommender: {str(e)}"

# --- MODEL SETUP ---
tools_list = [search_products, get_personal_recommendations]

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=tools_list,
    system_instruction="""
    Bạn là trợ lý bán hàng AI chuyên nghiệp cho cửa hàng đồ công nghệ.
    
    Quy tắc:
    1. Khi khách hỏi tìm đồ (ví dụ: "có iphone không?", "tìm chuột logitech"), MỞ tool `search_products`.
    2. Khi khách nhờ tư vấn chung (ví dụ: "tôi nên mua gì?", "gợi ý cho tôi"), MỞ tool `get_personal_recommendations`.
    3. Trả lời ngắn gọn, lịch sự bằng Tiếng Việt.
    4. Hiển thị giá tiền nếu có.
    """
)

def chat_process(user_id: str, message: str) -> str:
    try:
        chat = model.start_chat(enable_automatic_function_calling=True)
        full_prompt = f"[Context UserID: {user_id}] User: {message}"
        response = chat.send_message(full_prompt)
        return response.text
    except Exception as e:
        print(f"Lỗi Chat: {e}")
        return "Xin lỗi, tôi đang gặp chút trục trặc. Bạn thử lại sau nhé!"