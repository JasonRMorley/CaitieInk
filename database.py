from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:Jits123@localhost:5432/CaitlinsDB"
engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)


