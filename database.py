from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', os.getenv("DATABASE_URL_LOCAL"))

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)
