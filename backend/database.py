import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load custom environment variables from backend/.env explicitly
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=dotenv_path, override=True)

# Get PostgreSQL URL from environment variables, otherwise default to standard localhost credentials
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/aura_db"
)

try:
    # Create the SQLAlchemy engine
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True  # Automatically checks connection health before executing queries
    )
    
    # Session factory for handling requests
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Base class for SQLAlchemy ORM models
    Base = declarative_base()

except Exception as e:
    print(f"CRITICAL ERROR: Failed to initialize PostgreSQL connection engine.\n"
          f"Ensure PostgreSQL is running locally on port 5432.\n"
          f"Error message: {e}", file=sys.stderr)
    raise e

def get_db():
    """
    FastAPI Dependency to yield a database session per request
    and close it automatically once the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
