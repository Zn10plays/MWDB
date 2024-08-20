from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import dotenv
import os 

dotenv.load_dotenv()

engine = create_engine(os.getenv('SQL_DATABASE_URL'), echo=bool(os.getenv('DEV')))

def get_session():
    return Session(bind=engine)