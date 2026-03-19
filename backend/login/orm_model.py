from sqlalchemy import Column,Integer,String,Boolean, ForeignKey, Text
import datetime  
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from backend.login.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__='users'
    id= Column(Integer, unique=True, index=True, autoincrement=True,nullable=False,primary_key=True)
    name= Column(String,nullable=False)
    email=Column(String, unique=True,nullable=False)
    password= Column(String,nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),nullable=False, server_default=text("now()"))
    is_verified= Column(Boolean,nullable=False, default=False)
    chat_history = relationship("chatHistory", back_populates="user", cascade="all, delete") 

    


class chatHistory(Base):
    __tablename__='chatHistory'
    id= Column(Integer, unique=True, index=True, autoincrement=True,nullable=False,primary_key=True)
    user_id= Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    role=Column(String, nullable=False)
    content= Column(Text,nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),nullable=False, server_default=text("now()"))
    user = relationship("User", back_populates="chat_history")
    

class favouritePlaces(Base):
    __tablename__='favourite_places'
    id= Column(Integer, unique=True, index=True, autoincrement=True,nullable=False,primary_key=True)
    user_id= Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    destination= Column(String,nullable=True)
    created_at= Column(TIMESTAMP(timezone=True),nullable=False, server_default=text("now()"))



class savedPlans(Base):
    __tablename__='saved_plan'
    id= Column(Integer, unique=True, index=True, autoincrement=True,nullable=False,primary_key=True)
    user_id= Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    plan= Column(Text,nullable=True)
    created_at= Column(TIMESTAMP(timezone=True),nullable=False, server_default=text("now()"))