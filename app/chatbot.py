# app/chatbot.py
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
    print("- LỖI: Chưa set GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

# ================= CÁC TOOLS (CÔNG CỤ TRA CỨU) =================

def search_products(query: str):
    """
    Tìm kiếm sản phẩm. Trả về thông tin chi tiết gồm: Giá, Tồn kho, Bảo hành, Vận chuyển, Ảnh.
    """
    print(f"--> [BOT] Tìm sản phẩm: {query}")
    try:
        # Tìm trong title, brand hoặc category
        products = list(products_collection.find({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"brand": {"$regex": query, "$options": "i"}},
                {"category": {"$regex": query, "$options": "i"}}
            ]
        }).limit(3)) # Lấy 3 sản phẩm phù hợp nhất
        
        if not products:
            return "Hiện tại kho không tìm thấy sản phẩm nào khớp với yêu cầu."
            
        result_str = ""
        for p in products:
            # Format dữ liệu từ Mock Data mới
            price = f"${p.get('price', 0)}"
            stock = "Còn hàng" if p.get('stock', 0) > 0 else "Hết hàng"
            warranty = p.get('warrantyInformation', 'Không có thông tin')
            shipping = p.get('shippingInformation', 'Tiêu chuẩn')
            return_policy = p.get('returnPolicy', 'Không hỗ trợ')
            thumbnail = p.get('thumbnail', '')
            
            result_str += f"""
            Sản phẩm: {p.get('title')}
            - Hãng: {p.get('brand')} | Giá: {price} | Kho: {stock}
            - Bảo hành: {warranty}
            - Vận chuyển: {shipping}
            - Đổi trả: {return_policy}
            - Ảnh: {thumbnail}
            --------------------------------
            """
        return result_str
    except Exception as e:
        return f"Lỗi truy vấn sản phẩm: {str(e)}"

def track_order(order_id: str):
    """
    Tra cứu chi tiết một đơn hàng cụ thể dựa trên Mã Đơn Hàng (VD: ORD001).
    """
    print(f"--> [BOT] Tra cứu đơn: {order_id}")
    try:
        # Mock data dùng field 'id' là string (ORD001)
        order = orders_collection.find_one({"id": order_id})
        
        if not order:
            return f"Hệ thống không tìm thấy đơn hàng nào có mã {order_id}."
            
        # Lấy chi tiết từng món trong đơn
        items_detail = ""
        for item in order.get('items', []):
            product_name = "Sản phẩm (Đang tải...)"
            # Thử tìm tên sản phẩm từ bảng products dựa vào ID
            try:
                # Mock orders lưu product dưới dạng ObjectId hoặc ID số
                p_ref = item.get('product') or item.get('productId')
                if p_ref:
                    # Thử tìm theo _id trước
                    p_obj = products_collection.find_one({"_id": p_ref})
                    if not p_obj:
                         # Nếu không thấy, thử tìm theo id số (trường hợp mock data cũ)
                         p_obj = products_collection.find_one({"id": p_ref})
                    
                    if p_obj: product_name = p_obj.get('title')
            except:
                pass
            
            items_detail += f"- {item.get('quantity')}x {product_name}\n"

        info = f"""
        Đơn hàng: {order.get('id')}
        - Trạng thái: {order.get('status')}
        - Tổng tiền: {order.get('total'):,} VNĐ
        - Ngày đặt: {order.get('date')}
        - Địa chỉ: {order.get('shippingAddress')}
        - Chi tiết:
        {items_detail}
        """
        return info
    except Exception as e:
        return f"Lỗi tra cứu đơn hàng: {str(e)}"

def get_my_orders(user_id: str):
    """
    Lấy danh sách các đơn hàng gần đây của người dùng hiện tại.
    """
    print(f"--> [BOT] Lấy ds đơn của user: {user_id}")
    try:
        # Tìm đơn hàng có user_id khớp (Convert sang ObjectId vì DB lưu dạng Reference)
        # Nếu mock data user_id lưu string thì bỏ ObjectId đi
        try:
            u_oid = ObjectId(user_id)
            query = {"user": u_oid}
        except:
            # Fallback cho trường hợp mock data lưu email hoặc string
            query = {"email": user_id} 

        orders = list(orders_collection.find(query).sort("date", -1).limit(5))
        
        if not orders:
            return "Bạn chưa có đơn hàng nào trong lịch sử."
        
        res = "Danh sách đơn hàng gần đây của bạn:\n"
        for o in orders:
            res += f"- {o.get('date')}: Mã {o.get('id')} | {o.get('status')} | {o.get('total'):,} đ\n"
        return res
    except Exception as e:
        return f"Lỗi lấy lịch sử đơn: {str(e)}"

def lookup_vouchers(query: str = ""):
    """
    Tìm mã giảm giá đang hoạt động.
    """
    print(f"--> [BOT] Tìm voucher: {query}")
    try:
        filter_query = {"isActive": True}
        if query and query.strip():
            filter_query["$or"] = [
                {"code": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}}
            ]
        vouchers = list(vouchers_collection.find(filter_query).limit(5))
        
        if not vouchers:
            return "Hiện tại không có mã giảm giá nào phù hợp."
            
        res = "Các mã giảm giá đang có:\n"
        for v in vouchers:
            res += f"- Mã: {v.get('code')} - {v.get('description')} (Đơn tối thiểu: ${v.get('minimumPurchase', 0)})\n"
        return res
    except Exception as e:
        return f"Lỗi voucher: {str(e)}"

def get_personal_recommendations(user_id: str):
    """
    Gợi ý sản phẩm dựa trên AI Recommender System.
    """
    print(f"--> [BOT] Gợi ý cho: {user_id}")
    try:
        items = recommender.recommend(user_id, n_items=5)
        if not items:
            return "Bạn là khách hàng mới, hãy thử xem các sản phẩm Best Seller của shop nhé!"
        
        return str([f"{item['title']} (Giá: ${item['price']})" for item in items])
    except Exception as e:
        return f"Lỗi hệ thống gợi ý: {str(e)}"

# ================= HÀM HỖ TRỢ (HELPER) =================

def get_user_name(user_id: str):
    """
    Lấy tên người dùng từ DB để AI chào hỏi.
    """
    try:
        user = None
        # Case 1: user_id là ObjectId
        if len(user_id) == 24:
            try:
                user = users_collection.find_one({"_id": ObjectId(user_id)})
            except: pass
        
        # Case 2: Nếu không tìm thấy, thử tìm theo username (nếu user_id gửi lên là username)
        if not user:
             user = users_collection.find_one({"username": user_id})

        if user:
            return user.get("username") or user.get("email", "Bạn")
    except Exception as e:
        print(f"Lỗi lấy tên user: {e}")
    return "Bạn"

# ================= CẤU HÌNH AI MODEL =================

tools_list = [
    search_products, 
    track_order, 
    get_my_orders, 
    lookup_vouchers, 
    get_personal_recommendations
]

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=tools_list,
    system_instruction="""
    Bạn là Trợ lý Ảo chuyên nghiệp của TechShop.
    
    1. NHIỆM VỤ CHÍNH:
       - Trả lời thắc mắc về sản phẩm (Giá, Ảnh, Bảo hành...).
       - Tra cứu đơn hàng (Theo mã đơn hoặc xem lịch sử).
       - Gợi ý sản phẩm và cung cấp mã giảm giá.
    
    2. PHONG CÁCH:
       - Thân thiện, tự nhiên, sử dụng Emoji.
       - Luôn gọi tên khách hàng nếu biết tên.
       - Trả lời ngắn gọn, đi thẳng vào vấn đề.
    
    3. LƯU Ý DỮ LIỆU:
       - Giá tiền hiển thị là USD ($) hoặc VNĐ tùy dữ liệu trả về.
       - Nếu có link ảnh (thumbnail), hãy hiển thị ra.
    """
)

# Biến lưu trữ phiên chat (Memory)
user_chat_sessions = {}

# ================= 4. HÀM XỬ LÝ CHÍNH =================

def chat_process(user_id: str, message: str) -> str:
    global user_chat_sessions
    
    try:
        # Nếu user chưa có session, tạo mới
        if user_id not in user_chat_sessions:
            print(f"- Khởi tạo phiên chat cho: {user_id}")
            
            # Lấy tên người dùng để nạp vào ngữ cảnh (Context Injection)
            customer_name = get_user_name(user_id)
            
            # Tạo lịch sử giả để AI biết tên ngay lập tức
            history = [
                {
                    "role": "user",
                    "parts": [f"Chào shop, tôi tên là {customer_name}. ID của tôi là {user_id}."]
                },
                {
                    "role": "model",
                    "parts": [f"Chào {customer_name}! Rất vui được gặp bạn. Mình có thể giúp gì cho bạn hôm nay?"]
                }
            ]
            
            # Khởi tạo chat session
            user_chat_sessions[user_id] = model.start_chat(
                history=history,
                enable_automatic_function_calling=True
            )
        
        # Lấy session hiện tại và gửi tin nhắn
        chat_session = user_chat_sessions[user_id]
        response = chat_session.send_message(message)
        
        return response.text
        
    except Exception as e:
        print(f" Lỗi Chat Process: {e}")
        # Nếu session bị lỗi (timeout/disconnect), xóa đi để tạo lại
        if user_id in user_chat_sessions:
            del user_chat_sessions[user_id]
        return "Ui, kết nối bị gián đoạn một chút. Bạn nhắn lại giúp mình nhé! "