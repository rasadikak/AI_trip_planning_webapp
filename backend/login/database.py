from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from backend.config import SQLALCHEMY_DATABASE_URL
from backend.logger import logger

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    logger.info("Database engine created successfully")
except Exception as e:
    logger.critical(f"Failed to create database engine: {e}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified/created successfully")
except Exception as e:
    logger.critical(f"Failed to create database tables: {e}")
    raise


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()