from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings as s

DB_URL = f"postgresql://{s.fastapi_db_user}:{s.fastapi_db_password}@{s.fastapi_db_url}:{s.fastapi_db_port}/{s.fastapi_db_name}"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
