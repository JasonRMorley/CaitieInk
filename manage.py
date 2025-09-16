from models import Base  # wherever your models live
from database import engine  # wherever you create your SQLAlchemy engine

Base.metadata.create_all(bind=engine)
