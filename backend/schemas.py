# from pydantic import BaseModel, EmailStr, Field
# from typing import List, Dict, Any, Optional
# import datetime

# # --- REVIEW SCHEMAS ---
# class ReviewCreate(BaseModel):
#     name: str = Field(..., min_length=2, max_length=50)
#     rating: int = Field(..., ge=1, le=5)
#     comment: str = Field(..., min_length=5, max_length=500)

# class ReviewOut(BaseModel):
#     id: int
#     product_id: int
#     name: str
#     rating: int
#     date: datetime.date
#     comment: str

#     model_config = {
#         "from_attributes": True
#     }

# # --- PRODUCT SCHEMAS ---
# class ProductOut(BaseModel):
#     id: int
#     name: str
#     tagline: Optional[str] = None
#     price: float
#     category: str
#     rating: float
#     reviews_count: int
#     image: Optional[str] = None
#     description: Optional[str] = None
#     specs: Optional[Dict[str, Any]] = None
#     features: Optional[List[str]] = None
#     reviews: List[ReviewOut] = []

#     model_config = {
#         "from_attributes": True
#     }

# # --- ORDER SCHEMAS ---
# class OrderItem(BaseModel):
#     id: int
#     name: str
#     price: float
#     quantity: int = Field(..., ge=1)

# class OrderCreate(BaseModel):
#     name: str = Field(..., min_length=2)
#     email: str
#     address: str = Field(..., min_length=10)
#     city: str = Field(..., min_length=2)
#     zip_code: str = Field(..., min_length=5)
#     card_name: str = Field(..., min_length=2)
#     card_number: str = Field(..., min_length=12)
#     items: List[OrderItem]
#     total_amount: float

# class OrderOut(BaseModel):
#     id: int
#     order_code: str
#     customer_name: str
#     customer_email: str
#     address: str
#     city: str
#     zip_code: str
#     items: List[Dict[str, Any]]
#     total_amount: float
#     status: str
#     created_at: datetime.datetime

#     model_config = {
#         "from_attributes": True
#     }

from pydantic import BaseModel, Field  # <-- Yahan se EmailStr hata diya
from typing import List, Dict, Any, Optional
import datetime

# --- REVIEW SCHEMAS ---
class ReviewCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=5, max_length=500)

class ReviewOut(BaseModel):
    id: int
    product_id: int
    name: str
    rating: int
    date: datetime.date
    comment: str

    model_config = {
        "from_attributes": True
    }

# --- PRODUCT SCHEMAS ---
class ProductOut(BaseModel):
    id: int
    name: str
    tagline: Optional[str] = None
    price: float
    category: str
    rating: float
    reviews_count: int
    image: Optional[str] = None
    description: Optional[str] = None
    specs: Optional[Dict[str, Any]] = None
    features: Optional[List[str]] = None
    reviews: List[ReviewOut] = []

    model_config = {
        "from_attributes": True
    }

# --- ORDER SCHEMAS ---
class OrderItem(BaseModel):
    id: int
    name: str
    price: float
    quantity: int = Field(..., ge=1)

class OrderCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: str  # <-- Yahan EmailStr ko simple str kar diya
    address: str = Field(..., min_length=10)
    city: str = Field(..., min_length=2)
    zip_code: str = Field(..., min_length=5)
    card_name: str = Field(..., min_length=2)
    card_number: str = Field(..., min_length=12)
    items: List[OrderItem]
    total_amount: float

class OrderOut(BaseModel):
    id: int
    order_code: str
    customer_name: str
    customer_email: str
    address: str
    city: str
    zip_code: str
    items: List[Dict[str, Any]]
    total_amount: float
    status: str
    created_at: datetime.datetime

    model_config = {
        "from_attributes": True
    }