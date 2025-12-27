import os
import google.generativeai as genai
from datetime import datetime
from bson import ObjectId
from app.database import (
    products_collection, 
    vouchers_collection, 
    orders_collection, 
    users_collection
)
from app.recommender import recommender
from dotenv import load_dotenv

# --- CẤU HÌNH ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print(" LỖI: Chưa set GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

# ================= 1. CÁC TOOLS (CÔNG CỤ TRA CỨU) =================

def search_products(query: str):
    """
    Tìm kiếm sản phẩm. Trả về thông tin chi tiết.
    """
    print(f"--> [BOT] Tìm sản phẩm: {query}")
    try:
        products = list(products_collection.find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"brand": {"$regex": query, "$options": "i"}},
                {"category": {"$regex": query, "$options": "i"}}
            ]
        }).limit(3))
        
        if not products:
            return "Hiện tại kho không tìm thấy sản phẩm nào khớp với yêu cầu."
            
        result_str = ""
        for p in products:
            price = f"${p.get('price', 0)}"
            stock = "Còn hàng" if p.get('stock', 0) > 0 else "Hết hàng"
            # Ưu tiên lấy ID số cho dễ nhìn
            p_id = p.get('id', str(p.get('_id')))
            
            result_str += f"""
             Sản phẩm: {p.get('title')} (ID: {p_id})
            - Hãng: {p.get('brand')} | Giá: {price} | Kho: {stock}
            - Bảo hành: {p.get('warrantyInformation', 'N/A')}
            - Ảnh: {p.get('thumbnail', '')}
            --------------------------------
            """
        return result_str
    except Exception as e:
        return f"Lỗi truy vấn sản phẩm: {str(e)}"

def track_order(order_id: str):
    """
    Tra cứu chi tiết đơn hàng theo Mã (VD: ORD001).
    """
    print(f"--> [BOT] Tra cứu đơn: {order_id}")
    try:
        # 1. Tìm đơn hàng
        order = orders_collection.find_one({"id": order_id})
        
        if not order:
            return f"Không tìm thấy đơn hàng mã {order_id}."
            
        # 2. Lấy tên sản phẩm trong đơn (Logic Fix ID)
        items_detail = ""
        for item in order.get('items', []):
            product_name = "Sản phẩm ẩn"
            
            # Lấy ID sản phẩm từ order (có thể là số 104 hoặc chuỗi "104")
            # Trong mock_orders.js dùng field 'productId'
            raw_p_id = item.get('productId') or item.get('product')
            
            # --- ĐOẠN FIX QUAN TRỌNG ---
            # Thử tìm theo 'id' (số/chuỗi) trước, vì mock data dùng cái này
            p_obj = products_collection.find_one({"id": raw_p_id})
            
            # Nếu không thấy, thử ép kiểu sang số (nếu DB lưu số mà Order lưu chuỗi)
            if not p_obj and isinstance(raw_p_id, str) and raw_p_id.isdigit():
                 p_obj = products_collection.find_one({"id": int(raw_p_id)})

            # Nếu vẫn không thấy, bước đường cùng mới tìm theo ObjectId
            if not p_obj:
                try: p_obj = products_collection.find_one({"_id": ObjectId(raw_p_id)})
                except: pass
            
            if p_obj: 
                product_name = p_obj.get('title')
            
            items_detail += f"- {item.get('quantity')}x {product_name}\n"

        info = f"""
         Đơn hàng: {order.get('id')}
        - Trạng thái: {order.get('status')}
        - Tổng tiền: {order.get('total'):,} VNĐ
        - Ngày: {order.get('date')}
        - Chi tiết:
        {items_detail}
        """
        return info
    except Exception as e:
        return f"Lỗi tra cứu đơn hàng: {str(e)}"

def get_my_orders(user_id: str):
    """Lấy danh sách đơn hàng của user."""
    print(f"--> [BOT] Lấy ds đơn của user: {user_id}")
    try:
        query = {}
        # Cố gắng khớp user_id theo nhiều kiểu (ObjectId hoặc Email)
        if len(user_id) == 24:
            try: query = {"user": ObjectId(user_id)}
            except: query = {"email": user_id}
        else:
            query = {"email": user_id}

        orders = list(orders_collection.find(query).sort("date", -1).limit(5))
        
        if not orders: return "Bạn chưa có đơn hàng nào."
        
        res = "Đơn hàng gần đây:\n"
        for o in orders:
            res += f"- {o.get('date')}: Mã {o.get('id')} | {o.get('status')} | {o.get('total'):,} đ\n"
        return res
    except Exception as e: return f"Lỗi: {str(e)}"

def get_personal_recommendations(user_id: str):
    """Gợi ý sản phẩm (dùng Recommender đã fix ID)."""
    try:
        items = recommender.recommend(user_id, n_items=5)
        if not items: return "Gợi ý các sản phẩm hot: iPhone 15, MacBook Air..."
        return str([f"{i['title']} (${i['price']})" for i in items])
    except: return "Lỗi hệ thống gợi ý."

def lookup_vouchers(query: str = ""):
    """Tra cứu voucher."""
    try:
        filter_q = {"isActive": True}
        if query: filter_q["code"] = {"$regex": query, "$options": "i"}
        vouchers = list(vouchers_collection.find(filter_q).limit(5))
        if not vouchers: return "Không có mã giảm giá phù hợp."
        return "\n".join([f" {v['code']}: {v.get('description')}" for v in vouchers])
    except: return "Lỗi voucher."

# ================= 2. HELPER: LẤY TÊN USER =================
def get_user_name(user_id: str):
    try:
        u = None
        if len(user_id) == 24:
            try: u = users_collection.find_one({"_id": ObjectId(user_id)})
            except: pass
        if not u: u = users_collection.find_one({"username": user_id})
        if not u: u = users_collection.find_one({"email": user_id}) # Thử tìm theo email
        
        if u: return u.get("username") or u.get("email")
    except: pass
    return "Bạn"

# ================= 3. SETUP MODEL =================
tools_list = [search_products, track_order, get_my_orders, lookup_vouchers, get_personal_recommendations]

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=tools_list,
    system_instruction="""
    Bạn là Trợ lý Ảo TechShop.
    - Nhiệm vụ: Hỗ trợ tìm sản phẩm, tra cứu đơn hàng, voucher.
    - Phong cách: Thân thiện, ngắn gọn, dùng Emoji.
    - Luôn xưng hô tên khách nếu biết.
    """
)

user_chat_sessions = {}

def chat_process(user_id: str, message: str) -> str:
    global user_chat_sessions
    try:
        if user_id not in user_chat_sessions:
            c_name = get_user_name(user_id)
            history = [
                {"role": "user", "parts": [f"Tôi tên {c_name}, ID: {user_id}."]},
                {"role": "model", "parts": [f"Chào {c_name}! Shop giúp gì được cho bạn?"]}
            ]
            user_chat_sessions[user_id] = model.start_chat(history=history, enable_automatic_function_calling=True)
        
        response = user_chat_sessions[user_id].send_message(message)
        return response.text
    except Exception as e:
        if user_id in user_chat_sessions: del user_chat_sessions[user_id]
        return "Kết nối bị gián đoạn, bạn thử lại nhé!"