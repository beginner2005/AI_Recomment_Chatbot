from pydantic import BaseModel
from typing import List, Optional

class RecommendationRequest(BaseModel):
    user_id: str
    n_items: int = 10

class RecommendationResponse(BaseModel):
    user_id: str
    recommended_products: List[dict]
    message: str

class TrainRequest(BaseModel):
    force_retrain: bool = False

class InteractionCreate(BaseModel):
    user_id: str
    product_id: str
    interaction_type: str  # "view", "purchase", "rating"
    rating: Optional[int] = None

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str