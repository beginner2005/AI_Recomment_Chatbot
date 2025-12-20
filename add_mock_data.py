"""
Script để thêm mock data cho testing
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import users_collection, products_collection, interactions_collection
from bson import ObjectId
from datetime import datetime, timedelta
import random

def add_mock_products():
    """Thêm mock products"""
    categories = ["Electronics", "Fashion", "Home", "Books", "Sports"]
    
    mock_products = []
    for i in range(20):  # Thêm 20 products
        product = {
            "_id": ObjectId(),
            "name": f"Product {i+1}",
            "price": random.randint(100000, 1000000),
            "category": random.choice(categories),
            "description": f"Description for product {i+1}",
            "created_at": datetime.utcnow()
        }
        mock_products.append(product)
    
    # Xóa products cũ (nếu muốn)
    # products_collection.delete_many({})
    
    result = products_collection.insert_many(mock_products)
    print(f"✅ Đã thêm {len(result.inserted_ids)} products")
    return [str(id) for id in result.inserted_ids]

def add_mock_users():
    """Thêm mock users"""
    mock_users = []
    for i in range(10):  # Thêm 10 users
        user = {
            "_id": ObjectId(),
            "username": f"user_{i+1}",
            "email": f"user{i+1}@example.com",
            "created_at": datetime.utcnow()
        }
        mock_users.append(user)
    
    # Xóa users cũ (nếu muốn)
    # users_collection.delete_many({})
    
    result = users_collection.insert_many(mock_users)
    print(f"✅ Đã thêm {len(result.inserted_ids)} users")
    return [str(id) for id in result.inserted_ids]

def add_mock_interactions(user_ids, product_ids):
    """Thêm mock interactions"""
    interaction_types = ["view", "purchase", "rating"]
    
    mock_interactions = []
    
    # Mỗi user tương tác với 5-10 products ngẫu nhiên
    for user_id in user_ids:
        n_interactions = random.randint(5, 10)
        selected_products = random.sample(product_ids, n_interactions)
        
        for product_id in selected_products:
            interaction_type = random.choice(interaction_types)
            
            interaction = {
                "user_id": ObjectId(user_id),
                "product_id": ObjectId(product_id),
                "interaction_type": interaction_type,
                "timestamp": datetime.utcnow() - timedelta(days=random.randint(0, 30))
            }
            
            # Thêm rating nếu là rating interaction
            if interaction_type == "rating":
                interaction["rating"] = random.randint(1, 5)
            
            mock_interactions.append(interaction)
    
    # Xóa interactions cũ (nếu muốn)
    # interactions_collection.delete_many({})
    
    result = interactions_collection.insert_many(mock_interactions)
    print(f"✅ Đã thêm {len(result.inserted_ids)} interactions")
    return len(result.inserted_ids)

def show_stats():
    """Hiển thị thống kê"""
    print("\n" + "="*60)
    print("📊 DATABASE STATISTICS")
    print("="*60)
    
    n_users = users_collection.count_documents({})
    n_products = products_collection.count_documents({})
    n_interactions = interactions_collection.count_documents({})
    
    print(f"👥 Users: {n_users}")
    print(f"📦 Products: {n_products}")
    print(f"🔗 Interactions: {n_interactions}")
    
    # Thống kê categories
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    categories = list(products_collection.aggregate(pipeline))
    print(f"\n📋 Categories:")
    for cat in categories:
        print(f"   - {cat['_id']}: {cat['count']} products")
    
    # Thống kê interaction types
    pipeline = [
        {"$group": {"_id": "$interaction_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    interaction_types = list(interactions_collection.aggregate(pipeline))
    print(f"\n🔗 Interaction types:")
    for it in interaction_types:
        print(f"   - {it['_id']}: {it['count']}")
    
    print("="*60)

if __name__ == "__main__":
    print("="*60)
    print("🎭 MOCK DATA GENERATOR")
    print("="*60)
    
    print("\n⚠️ Script này sẽ thêm dữ liệu giả vào database!")
    print("   - 20 products")
    print("   - 10 users")
    print("   - 50-100 interactions")
    
    choice = input("\nBạn có muốn tiếp tục? (yes/no): ").lower()
    
    if choice != "yes":
        print("❌ Đã hủy")
        sys.exit(0)
    
    print("\n" + "="*60)
    print("🚀 Bắt đầu thêm mock data...")
    print("="*60)
    
    try:
        # Thêm products
        print("\n1️⃣ Thêm products...")
        product_ids = add_mock_products()
        
        # Thêm users
        print("\n2️⃣ Thêm users...")
        user_ids = add_mock_users()
        
        # Thêm interactions
        print("\n3️⃣ Thêm interactions...")
        add_mock_interactions(user_ids, product_ids)
        
        # Hiển thị thống kê
        show_stats()
        
        print("\n✅ HOÀN TẤT! Bây giờ bạn có thể chạy training.")
        
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        import traceback
        traceback.print_exc()