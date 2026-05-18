import datetime
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, JSON, Date, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    """
    SQLAlchemy model representing a luxury AURA Audio product.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    tagline = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    image = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    specs = Column(JSON, nullable=True)      # Holds dynamic specifications key-value map
    features = Column(JSON, nullable=True)   # Holds bullet point features array

    # Relational field: a product has multiple reviews
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")

class Review(Base):
    """
    SQLAlchemy model representing a user-submitted review for a product.
    """
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False)
    date = Column(Date, default=datetime.date.today)
    comment = Column(Text, nullable=False)

    # Relational field: review points back to its parent product
    product = relationship("Product", back_populates="reviews")

class Order(Base):
    """
    SQLAlchemy model representing a checkout customer order.
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_code = Column(String(50), unique=True, index=True, nullable=False)
    customer_name = Column(String(100), nullable=False)
    customer_email = Column(String(150), nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    
    # Store order items as a JSON list: [{"id": 1, "name": "...", "price": 349.99, "quantity": 1}]
    items = Column(JSON, nullable=False)
    
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), default="Processing")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
