from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import RecommendationRequest, RecommendationResponse, TrainRequest, InteractionCreate
from app.recommender import recommender 
from app.database import interactions_collection
from app.models import ChatRequest, ChatResponse 
from app.chatbot import chat_process
from bson import ObjectId
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

app = FastAPI(title="AI Recommendation Service", version="1.0.0")
scheduler = AsyncIOScheduler()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Load model VÀ Khởi động lịch train"""
    print("Đang khởi động AI")
    
    # Load model
    print("\nĐang load model")
    success = recommender.load_model()
    if success:
        print("Model loaded successfully!")
    else:
        print("Model load failed")
    
    # Setup scheduler
    print("\nĐang cài đặt lịch train")
    scheduler.add_job(
        recommender.train_model, 
        "cron", 
        hour=1, 
        minute=0,
        id="auto_train_job"
    )
    scheduler.start()
    print("Lịch train đã được cài đặt")

@app.on_event("shutdown")
async def shutdown_event():
    """Tắt lịch khi tắt server"""
    print("\nĐang tắt lịch train")
    scheduler.shutdown()
    print("Đã tắt scheduler")

@app.get("/")
async def root():
    return {
        "message": "AI is running!",
        "status": "healthy",
        "model_loaded": recommender.cf_model is not None,
        "endpoints": {
            "recommend": "GET /recommend/{user_id}?n_items=10",
            "train": "POST /train",
            "add_interaction": "POST /interaction",
            "health": "GET /health"
        }
    }

@app.get("/recommend/{user_id}")
async def get_recommendations(user_id: str, n_items: int = 10):
    """
    Lấy gợi ý sản phẩm cho user
    
    - **user_id**: ID của user cần gợi ý
    - **n_items**: Số lượng sản phẩm cần gợi ý (mặc định 10)
    """
    try:
        if n_items < 1 or n_items > 100:
            raise HTTPException(
                status_code=400, 
                detail="n_items phải trong khoảng 1-100"
            )
        
        recommendations = recommender.recommend(user_id, n_items)
        
        return {
            "user_id": user_id,
            "recommended_products": recommendations,
            "count": len(recommendations),
            "message": "Success"
        }
    except Exception as e:
        print(f"Lỗi khi recommend: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train")
async def train_model(request: TrainRequest):
    """
    Train lại model với dữ liệu mới
    
    - **force_retrain**: Bắt buộc train lại (mặc định False)
    """
    try:
        print("Bắt đầu training model")
        
        success = recommender.train_model()
        
        if success:
            return {
                "message": "Model trained successfully",
                "status": "success"
            }
        else:
            raise HTTPException(
                status_code=500, 
                detail="Training failed. Kiểm tra logs để biết thêm chi tiết."
            )
    except Exception as e:
        print(f"Lỗi khi train model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/interaction")
async def add_interaction(interaction: InteractionCreate):
    """
    Thêm interaction mới (view, purchase, rating)
    
    - **user_id**: ID của user
    - **product_id**: ID của product
    - **interaction_type**: Loại tương tác (view/purchase/rating)
    - **rating**: Điểm rating (optional, chỉ dùng khi interaction_type="rating")
    """
    try:
        # Validate interaction_type
        valid_types = ["view", "purchase", "rating"]
        if interaction.interaction_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"interaction_type phải là một trong: {valid_types}"
            )
        
        # Validate rating nếu là rating interaction
        if interaction.interaction_type == "rating":
            if interaction.rating is None:
                raise HTTPException(
                    status_code=400,
                    detail="rating là bắt buộc khi interaction_type='rating'"
                )
            if interaction.rating < 1 or interaction.rating > 5:
                raise HTTPException(
                    status_code=400,
                    detail="rating phải trong khoảng 1-5"
                )
        
        # Tạo interaction document
        interaction_doc = {
            "user_id": ObjectId(interaction.user_id),
            "product_id": ObjectId(interaction.product_id),
            "interaction_type": interaction.interaction_type,
            "timestamp": datetime.utcnow()
        }
        
        if interaction.rating is not None:
            interaction_doc["rating"] = interaction.rating
        
        # Lưu vào database
        result = interactions_collection.insert_one(interaction_doc)
        
        return {
            "message": "Interaction added successfully",
            "interaction_id": str(result.inserted_id),
            "interaction_type": interaction.interaction_type
        }
    except Exception as e:
        print(f"Lỗi khi thêm interaction: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Recommendation Service",
        "model_loaded": recommender.model is not None,
        "model_type": "Hybrid (Collaborative + Content-based)"
    }

@app.get("/stats")
async def get_stats():
    """Thống kê hệ thống"""
    try:
        from app.database import users_collection, products_collection
        
        n_users = users_collection.count_documents({})
        n_products = products_collection.count_documents({})
        n_interactions = interactions_collection.count_documents({})
        
        return {
            "users": n_users,
            "products": n_products,
            "interactions": n_interactions,
            "model_loaded": recommender.model is not None,
            "trained_users": len(recommender.user_id_map) if recommender.user_id_map else 0,
            "trained_products": len(recommender.product_id_map) if recommender.product_id_map else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    Chat với nhân viên ảo (Gemini Native)
    """
    # Gọi hàm xử lý trực tiếp, không cần await vì thư viện google dùng sync request (hoặc có thể dùng async version nếu muốn tối ưu sau)
    response_text = chat_process(request.user_id, request.message)
    
    return {
        "response": response_text
    }