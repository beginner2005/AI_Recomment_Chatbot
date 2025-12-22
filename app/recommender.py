# app/recommender.py
"""
Hybrid Recommender System (Updated for Mock Data)
Sử dụng: Surprise (Collaborative) + Scikit-learn (Content-based)
Dữ liệu: Tự động lấy từ Orders (Purchase) và Products (Content)
"""
import numpy as np
import pandas as pd
from surprise import SVD, Dataset, Reader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bson import ObjectId
from app.database import get_database
import pickle
import os

class HybridRecommender:
    def __init__(self):
        self.cf_model = None
        self.trainset = None
        self.content_similarity_matrix = None
        
        # Mappings
        self.product_map = {} # Map int_id -> product_doc
        self.product_internal_id_to_idx = {} # Map id "104" -> index ma trận 0,1,2...
        self.user_ids = []
        self.product_ids = [] # List các ID sản phẩm 
        
        self.model_path = "trained_model.pkl"
        
    def prepare_data(self):
        """Chuẩn bị dữ liệu từ Products và Orders"""
        print("--> ĐANG CHUẨN BỊ DỮ LIỆU HUẤN LUYỆN...")
        db = get_database()
        
        # 1. Lấy dữ liệu Products
        products = list(db["products"].find())
        print(f"   - Tìm thấy {len(products)} sản phẩm.")
        
        self.product_map = {str(p.get("id", p["_id"])): p for p in products}
        self.product_ids = list(self.product_map.keys())
        
        # 2. Lấy dữ liệu Users để map Email -> ID
        # Vì orders dùng email, nhưng hệ thống recommend theo User ID
        users = list(db["users"].find())
        email_to_userid = {u.get("email"): str(u["_id"]) for u in users if "email" in u}
        print(f"   - Tìm thấy {len(users)} người dùng.")

        # 3. Tổng hợp Interactions từ ORDERS (Thay vì interactions collection)
        orders = list(db["orders"].find())
        print(f"   - Tìm thấy {len(orders)} đơn hàng.")
        
        cf_data = []
        
        # Duyệt qua đơn hàng để tạo data training
        for order in orders:
            email = order.get("email")
            if not email or email not in email_to_userid:
                continue
                
            user_id = email_to_userid[email]
            
            # Duyệt qua từng sản phẩm trong đơn hàng
            for item in order.get("items", []):
                # Mock order dùng 'productId': 119
                p_id = str(item.get("productId"))
                
                # Nếu sản phẩm này có trong kho
                if p_id in self.product_ids:
                    cf_data.append({
                        "user_id": user_id,
                        "product_id": p_id,
                        "rating": 5.0 # Mua hàng là thích nhất -> 5 điểm
                    })

        # Nếu có bảng interactions (view, rating) thì cộng thêm vào đây
        # interactions = list(db["interactions"].find()) ... (Code cũ của bạn ở đây)
        
        if not cf_data:
            print("- Cảnh báo: Không có dữ liệu tương tác (đơn hàng). Model CF sẽ không học được gì.")
            df = pd.DataFrame(columns=["user_id", "product_id", "rating"])
        else:
            df = pd.DataFrame(cf_data)
            print(f"   - Tổng hợp được {len(df)} tương tác mua hàng.")

        # 4. Train Collaborative Filtering (Surprise)
        if not df.empty:
            reader = Reader(rating_scale=(1, 5))
            surprise_data = Dataset.load_from_df(df[['user_id', 'product_id', 'rating']], reader)
            self.trainset = surprise_data.build_full_trainset()
            self.user_ids = df['user_id'].unique().tolist()
        
        # 5. Train Content-Based (TF-IDF)
        # Dùng title, brand, category, tags để tìm độ tương đồng
        print("   - Đang tính toán độ tương đồng nội dung...")
        product_features = []
        
        # Sắp xếp product_ids để index khớp với ma trận
        self.product_ids.sort()
        self.product_internal_id_to_idx = {pid: i for i, pid in enumerate(self.product_ids)}
        
        for pid in self.product_ids:
            p = self.product_map[pid]
            # Gộp các text quan trọng
            content_str = f"{p.get('title', '')} {p.get('brand', '')} {p.get('category', '')}"
            if 'tags' in p and isinstance(p['tags'], list):
                content_str += " " + " ".join(p['tags'])
            
            product_features.append(content_str)
            
        if product_features:
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform(product_features)
            self.content_similarity_matrix = cosine_similarity(tfidf_matrix)
        
        print("- Chuẩn bị dữ liệu hoàn tất!")
        return True

    def train_model(self):
        print("TRAINING MODEL...")
        if not self.prepare_data():
            return False
            
        if self.trainset:
            self.cf_model = SVD(n_factors=20, n_epochs=20, random_state=42)
            self.cf_model.fit(self.trainset)
            print("- Đã train xong Collaborative Filtering Model.")
            self.save_model()
            return True
        else:
            print("- Không đủ data để train CF.")
            return False

    def save_model(self):
        data = {
            'cf_model': self.cf_model,
            'trainset': self.trainset,
            'content_similarity_matrix': self.content_similarity_matrix,
            'product_map': self.product_map, # Lưu cache product info
            'product_ids': self.product_ids,
            'user_ids': self.user_ids,
            'product_internal_id_to_idx': self.product_internal_id_to_idx
        }
        with open(self.model_path, 'wb') as f:
            pickle.dump(data, f)
        print("- Đã lưu model ra file.")

    def load_model(self):
        if not os.path.exists(self.model_path):
            return self.train_model()
        try:
            with open(self.model_path, 'rb') as f:
                data = pickle.load(f)
            self.cf_model = data['cf_model']
            self.trainset = data['trainset']
            self.content_similarity_matrix = data['content_similarity_matrix']
            self.product_map = data.get('product_map', {})
            self.product_ids = data['product_ids']
            self.user_ids = data['user_ids']
            self.product_internal_id_to_idx = data.get('product_internal_id_to_idx', {})
            print("- Đã load model từ file.")
            return True
        except Exception as e:
            print(f"Lỗi load model: {e}. Retraining...")
            return self.train_model()

    def recommend(self, user_id: str, n_items: int = 10):
        # 1. Load model
        if self.cf_model is None:
            self.load_model()
            
        # 2. Lấy lịch sử mua hàng của user này (để loại trừ và tính content-based)
        db = get_database()
        user_email = None
        try:
            u_obj = db["users"].find_one({"_id": ObjectId(user_id)})
            if u_obj: user_email = u_obj.get("email")
        except:
            pass

        purchased_ids = set()
        if user_email:
            # Tìm trong orders
            user_orders = db["orders"].find({"email": user_email})
            for o in user_orders:
                for item in o.get("items", []):
                    purchased_ids.add(str(item.get("productId")))
        
        # 3. Tính điểm Hybrid
        scores = []
        is_new_user = user_id not in self.user_ids
        
        for pid in self.product_ids:
            if pid in purchased_ids: continue # Bỏ qua món đã mua
            
            # --- A. Điểm CF (Nếu user cũ) ---
            cf_score = 0
            if not is_new_user and self.cf_model:
                try:
                    est = self.cf_model.predict(user_id, pid).est
                    cf_score = (est - 1) / 4 # Normalize 0-1
                except:
                    cf_score = 0
            
            # --- B. Điểm Content (Dựa trên món đã mua) ---
            content_score = 0
            if self.content_similarity_matrix is not None and purchased_ids:
                if pid in self.product_internal_id_to_idx:
                    idx = self.product_internal_id_to_idx[pid]
                    # Tính trung bình độ giống với các món đã mua
                    sims = []
                    for bought_id in purchased_ids:
                        if bought_id in self.product_internal_id_to_idx:
                            b_idx = self.product_internal_id_to_idx[bought_id]
                            sims.append(self.content_similarity_matrix[idx][b_idx])
                    if sims:
                        content_score = np.mean(sims)
            
            # Nếu user mới tinh (Cold Start): Ưu tiên ContentScore hoặc Popularity
            if is_new_user:
                final_score = content_score 
            else:
                final_score = 0.7 * cf_score + 0.3 * content_score
                
            scores.append((pid, final_score))
            
        # 4. Sort và trả về
        scores.sort(key=lambda x: x[1], reverse=True)
        top_ids = scores[:n_items]
        
        results = []
        for pid, score in top_ids:
            p = self.product_map.get(pid)
            if p:
                results.append({
                    "id": p.get("id"),
                    "_id": str(p.get("_id")),
                    "title": p.get("title"),
                    "price": p.get("price"),
                    "thumbnail": p.get("thumbnail"),
                    "score": round(score, 4)
                })
        return results

recommender = HybridRecommender()