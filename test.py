"""
Test Hybrid Recommender (Surprise + Content-based)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.recommender import recommender
from app.database import users_collection, products_collection, interactions_collection

# 1. Kiểm tra database
print("\n- DATABASE STATS:")
n_users = users_collection.count_documents({})
n_products = products_collection.count_documents({})
n_interactions = interactions_collection.count_documents({})

print(f"  - Users: {n_users}")
print(f"  - Products: {n_products}")
print(f"  - Interactions: {n_interactions}")

if n_interactions < 5:
    print("\n- Dataset quá nhỏ!")
    sys.exit(1)

# 2. Train model
input("Nhấn Enter để bắt đầu training...")
try:
    success = recommender.train_model()
    
    if success:
        print("TRAINING THÀNH CÔNG!")
        
        # 3. Test recommendation
        print("\n- TEST")
        
        first_user = users_collection.find_one()
        if first_user:
            user_id = str(first_user["_id"])
            print(f"\n- User ID: {user_id}")
            recommendations = recommender.recommend(user_id, 5)
            if recommendations:
                print(f"\nTop {len(recommendations)} recommendations:\n")
                for i, rec in enumerate(recommendations, 1):
                    print(f"{i}. {rec['name']}")
                    print(f"   Category: {rec['category']}")
                    print(f"   Price: {rec['price']:,.0f} VNĐ")
                    print(f"   Hybrid Score: {rec['score']:.4f}")
                    print(f"   - CF Score: {rec['cf_score']:.4f}")
                    print(f"   - Content Score: {rec['content_score']:.4f}")
                    print()
            else:
                print("Không có recommendations")
    else:
        print("\n- TRAINING THẤT BẠI!")
        
except KeyboardInterrupt:
    print("\n\nĐã hủy")
except Exception as e:
    print(f"\nLỖI: {e}")
    import traceback
    traceback.print_exc()