from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import config_instance

# Create a SQLAlchemy engine
# echo=True will make SQLAlchemy log SQL queries, which can be useful for debugging
engine = create_engine(config_instance.database_url, echo=True, connect_args={"check_same_thread": False})

# SessionLocal will be our factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base will be used for our SQLAlchemy model definitions
Base = declarative_base()
