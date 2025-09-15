from app.store.database.sqlalchemy_base import BaseModel
from sqlalchemy import Column, Integer, String



class AdminModel(BaseModel):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)

    
