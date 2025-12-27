# app/recommender.py
import numpy as np
import pandas as pd
from surprise import SVD, Dataset, Reader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bson import ObjectId  # <--- ĐÃ THÊM DÒNG NÀY
from app.database import get_database
import pickle
import os

class HybridRecommender:
    def __init__(self):
        self.cf_model = None
        self.trainset = None
        self.content_similarity_matrix = None
        
        # Mappings
        self.product_map = {} 
        self.product_internal_id_to_idx = {} 
        self.user_ids = []
        self.product_ids = [] 
        
        self.model_path = "trained_model_final.pkl"
        
    def prepare_data(self):
        print("-->  ĐANG ĐỒNG BỘ DỮ LIỆU & ID...")
        db = get_database()
        
        # 1. Lấy dữ liệu Products
        products = list(db["products"].find())
        
        # Map theo trường "id" (số)
        self.product_map = {}
        for p in products:
            if "id" in p:
                str_id = str(p["id"]) 
                self.product_map[str_id] = p
        
        self.product_ids = list(self.product_map.keys())
        print(f"   - Đã index {len(self.product_ids)} sản phẩm theo ID số.")

        # 2. Lấy Users (Map Email -> UserID)
        users = list(db["users"].find())
        email_to_userid = {u.get("email"): str(u["_id"]) for u in users if "email" in u}

        # 3. Lấy Orders
        orders = list(db["orders"].find())
        cf_data = []
        
        count_match = 0
        for order in orders:
            email = order.get("email")
            if email and email in email_to_userid:
                user_id = email_to_userid[email]
                
                for item in order.get("items", []):
                    raw_p_id = item.get("productId") or item.get("product")
                    p_id_str = str(raw_p_id)
                    
                    if p_id_str in self.product_map:
                        cf_data.append({
                            "user_id": user_id,
                            "product_id": p_id_str,
                            "rating": 5.0 
                        })
                        count_match += 1
        
        print(f"   - Tìm thấy {count_match} tương tác mua hàng hợp lệ.")

        # 4. Train CF Model
        if cf_data:
            df = pd.DataFrame(cf_data)
            reader = Reader(rating_scale=(1, 5))
            surprise_data = Dataset.load_from_df(df[['user_id', 'product_id', 'rating']], reader)
            self.trainset = surprise_data.build_full_trainset()
            self.user_ids = df['user_id'].unique().tolist()
            
            self.cf_model = SVD(n_factors=20, n_epochs=20, random_state=42)
            self.cf_model.fit(self.trainset)
            print("   -  Đã train xong Collaborative Filtering.")
        else:
            print("   -  Cảnh báo: Không có dữ liệu order khớp ID sản phẩm. Bỏ qua CF.")

        # 5. Train Content-Based (TF-IDF)
        self.product_ids.sort()
        self.product_internal_id_to_idx = {pid: i for i, pid in enumerate(self.product_ids)}
        
        features = []
        for pid in self.product_ids:
            p = self.product_map[pid]
            text = f"{p.get('title', '')} {p.get('brand', '')} {p.get('category', '')} {p.get('description', '')}"
            features.append(text)
            
        if features:
            tfidf = TfidfVectorizer(stop_words='english', max_features=500)
            tfidf_matrix = tfidf.fit_transform(features)
            self.content_similarity_matrix = cosine_similarity(tfidf_matrix)
            print("   -  Đã tính toán xong độ tương đồng nội dung.")
            
        return True

    def train_model(self):
        print("TRAINING MODEL (FIXED ID)...")
        if self.prepare_data():
            self.save_model()
            return True
        return False

    def save_model(self):
        data = {
            'cf_model': self.cf_model,
            'product_map': self.product_map,
            'product_ids': self.product_ids,
            'user_ids': self.user_ids,
            'content_similarity_matrix': self.content_similarity_matrix,
            'product_internal_id_to_idx': self.product_internal_id_to_idx
        }
        with open(self.model_path, 'wb') as f:
            pickle.dump(data, f)

    def load_model(self):
        if not os.path.exists(self.model_path): return self.train_model()
        try:
            with open(self.model_path, 'rb') as f:
                data = pickle.load(f)
            self.cf_model = data.get('cf_model')
            self.product_map = data.get('product_map', {})
            self.product_ids = data.get('product_ids', [])
            self.user_ids = data.get('user_ids', [])
            self.content_similarity_matrix = data.get('content_similarity_matrix')
            self.product_internal_id_to_idx = data.get('product_internal_id_to_idx', {})
            return True
        except: return self.train_model()

    def recommend(self, user_id: str, n_items: int = 10):
        if not self.product_map: self.load_model()
            
        # 1. Lấy lịch sử mua (theo ID số)
        db = get_database()
        purchased_ids = set()
        try:
            # Tìm user thật để lấy email (Dùng ObjectId ở đây nên cần import)
            u = None
            if len(user_id) == 24:
                try:
                    u = db["users"].find_one({"_id": ObjectId(user_id)})
                except: pass
            
            if u and "email" in u:
                user_orders = db["orders"].find({"email": u["email"]})
                for o in user_orders:
                    for item in o.get("items", []):
                        raw_id = item.get("productId") or item.get("product")
                        purchased_ids.add(str(raw_id))
        except Exception as e:
            print(f"Lỗi lấy lịch sử mua: {e}")

        scores = []
        is_new_user = user_id not in self.user_ids
        
        for pid in self.product_ids:
            if pid in purchased_ids: continue 
            
            # A. CF Score
            cf_score = 0
            if not is_new_user and self.cf_model:
                try: cf_score = (self.cf_model.predict(user_id, pid).est - 1) / 4
                except: pass
            
            # B. Content Score
            content_score = 0
            if self.content_similarity_matrix is not None and purchased_ids:
                if pid in self.product_internal_id_to_idx:
                    idx = self.product_internal_id_to_idx[pid]
                    sims = []
                    for bought in purchased_ids:
                        if bought in self.product_internal_id_to_idx:
                            b_idx = self.product_internal_id_to_idx[bought]
                            sims.append(self.content_similarity_matrix[idx][b_idx])
                    if sims: content_score = np.mean(sims)
            
            final_score = content_score if is_new_user else (0.7 * cf_score + 0.3 * content_score)
            scores.append((pid, final_score))
            
        scores.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for pid, score in scores[:n_items]:
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