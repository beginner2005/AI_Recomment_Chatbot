
# *****Setup mongoDB*****
## Chạy trong MongoDB Compass hoặc mongosh
use ecommerce_db;

## users mẫu
db.users.insertMany([
  { username: "user1", email: "user1@test.com", created_at: new Date() },
  { username: "user2", email: "user2@test.com", created_at: new Date() },
  { username: "user3", email: "user3@test.com", created_at: new Date() }
]);

## products mẫu
db.products.insertMany([
  { name: "Áo thun trắng", description: "Áo thun cotton", category: "Thời trang", price: 150000, tags: ["áo", "thun", "trắng"], created_at: new Date() },
  { name: "Quần jean xanh", description: "Quần jean slim fit", category: "Thời trang", price: 350000, tags: ["quần", "jean", "xanh"], created_at: new Date() },
  { name: "Giày thể thao", description: "Giày chạy bộ", category: "Giày dép", price: 800000, tags: ["giày", "thể thao"], created_at: new Date() },
  { name: "Áo khoác đen", description: "Áo khoác hoodie", category: "Thời trang", price: 450000, tags: ["áo", "khoác", "đen"], created_at: new Date() },
  { name: "Túi xách", description: "Túi da cao cấp", category: "Phụ kiện", price: 600000, tags: ["túi", "da"], created_at: new Date() }
]);

## interactions mẫu
const users = db.users.find().toArray();
const products = db.products.find().toArray();

db.interactions.insertMany([
  { user_id: users[0]._id, product_id: products[0]._id, interaction_type: "view", timestamp: new Date() },
  { user_id: users[0]._id, product_id: products[0]._id, interaction_type: "purchase", timestamp: new Date() },
  { user_id: users[0]._id, product_id: products[1]._id, interaction_type: "view", timestamp: new Date() },
  { user_id: users[1]._id, product_id: products[0]._id, interaction_type: "view", timestamp: new Date() },
  { user_id: users[1]._id, product_id: products[2]._id, interaction_type: "purchase", timestamp: new Date() },
  { user_id: users[2]._id, product_id: products[1]._id, interaction_type: "rating", rating: 5, timestamp: new Date() }
]);

## Tạo indexes để tăng performance
db.interactions.createIndex({ user_id: 1, timestamp: -1 });
db.interactions.createIndex({ product_id: 1 });
db.products.createIndex({ category: 1 });


# *****Cài đặt và chạy AI Server*****
## (1) 
    cd ai-recommendation-service
## (2)(chỉ chạy nếu không có file venv )
### Nếu xài python 3.10
    py -3.10 -m venv venv        
### nếu không
    py -m venv venv
## (3) 
    venv\Scripts\activate
## (4) 
    pip install -r requirements.txt
## (5) 
    uvicorn app.main:app --reload

# *****Test*****
- Sau khi chạy xong lệnh (uvicorn app.main:app --reload) thì vào trình duyệt gõ URL sau:
- http://127.0.0.1:8000/recommend/USER_ID
- Ví dụ: http://127.0.0.1:8000/recommend/69196b0138e3e94921f33a34
- Nó sẽ hiện ra các collection, document của các sản phẩm mà nó đề xuất

# *****Cách thức hoạt động*****
- Khi User A truy cập web, web gọi API /recommend/user_A
- Model xem lịch sử của User A (ví dụ: đã mua P0)
- Nó dùng các "mẫu" đã học để tìm các User B, C "giống" User A (ví dụ: họ cũng mua P0)
- Nó xem User B, C còn thích gì nữa (ví dụ: User B mua P2)
- Nó dự đoán rằng User A cũng sẽ thích P2, và gán cho P2 một điểm số (score) cao
- Model lọc bỏ P0 (sản phẩm User A đã mua) ra khỏi danh sách, để đảm bảo không gợi ý lại đồ cũ
- Nó trả về 10 sản phẩm có điểm cao nhất
**Trường hợp đặc biệt
- Nếu có User Mới (chưa có trong data train) vào web, AI sẽ không bị lỗi
- Thay vào đó, nó sẽ tự động chuyển sang chế độ _get_popular_products() và gợi ý các sản phẩm phổ biến nhất (được nhiều người tương tác nhất) cho họ