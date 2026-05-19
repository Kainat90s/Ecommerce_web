import os
import random
import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

# Database imports
from database import get_db, engine, Base
import models
import schemas

# Create tables in case they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AURA Audio E-Commerce Backend",
    description="FastAPI Backend connected to PostgreSQL (Ecommerce database)",
    version="2.0.0"
)
handler = app

# Enable CORS for React Frontend running on Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to AURA Audio E-Commerce API (PostgreSQL Backed)", "status": "running"}

# 1. Retrieve all products with their cached ratings and review counts
@app.get("/api/products", response_model=List[schemas.ProductOut])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).order_by(models.Product.id).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found in the database")
    return products

# 2. Retrieve a specific product in detail (including all reviews)
@app.get("/api/products/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 3. Add a user review for a product and recalculate rolling ratings
@app.post("/api/products/{product_id}/reviews", status_code=status.HTTP_201_CREATED)
def add_review(product_id: int, review_in: schemas.ReviewCreate, db: Session = Depends(get_db)):
    # Verify product exists
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Create the review record
    new_review = models.Review(
        product_id=product_id,
        name=review_in.name,
        rating=review_in.rating,
        comment=review_in.comment,
        date=datetime.date.today()
    )
    db.add(new_review)
    db.flush()  # Generate review ID
    
    # Recalculate average rating and reviews count for the product
    reviews = db.query(models.Review).filter(models.Review.product_id == product_id).all()
    total_rating = sum(r.rating for r in reviews)
    reviews_count = len(reviews)
    
    product.reviews_count = reviews_count
    product.rating = round(total_rating / reviews_count, 1)
    
    db.commit()
    db.refresh(product)
    
    return {
        "success": True,
        "message": "Review submitted and ratings updated successfully",
        "review_id": new_review.id,
        "new_rating": product.rating,
        "new_reviews_count": product.reviews_count
    }

# 4. Create an order, validating details and saving items as JSON in PostgreSQL
@app.post("/api/orders", status_code=status.HTTP_201_CREATED)
def create_order(order_in: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Validate items and price details against our DB
    order_items_list = []
    for item in order_in.items:
        product = db.query(models.Product).filter(models.Product.id == item.id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Product with ID {item.id} does not exist"
            )
        
        # Sane validation of price
        if abs(product.price - item.price) > 0.01:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Price mismatch for '{item.name}'. Database expects {product.price} but got {item.price}"
            )
            
        order_items_list.append({
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "quantity": item.quantity
        })
        
    # Generate unique order code: AUR-[YYYYMMDD]-[RANDOM]
    order_code = f"AUR-{datetime.date.today().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    
    # Create the order record
    new_order = models.Order(
        order_code=order_code,
        customer_name=order_in.name,
        customer_email=order_in.email,
        address=order_in.address,
        city=order_in.city,
        zip_code=order_in.zip_code,
        items=order_items_list,
        total_amount=order_in.total_amount,
        status="Processing"
    )
    
    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to record order: {e}"
        )
        
    return {
        "success": True,
        "message": "Your order has been placed successfully",
        "order_id": new_order.order_code,
        "total_amount": new_order.total_amount
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
