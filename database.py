from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import dotenv
import os

# Environment Vars
dotenv.load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
TARGET_DB = os.getenv("TARGET_DB")

# Database URL
URL_DATABASE = f"postgresql://postgres:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TARGET_DB}"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()