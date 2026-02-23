from sqlalchemy import Column,Integer,String,Boolean
import datetime  
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from backend.login.database import Base

class User(Base):
    __tablename__='users'
    id= Column(Integer, unique=True, index=True, autoincrement=True,nullable=False,primary_key=True)
    name= Column(String,nullable=False)
    email=Column(String, unique=True,nullable=False)
    password= Column(String,nullable=False)
    created_at= Column(TIMESTAMP(timezone=True),nullable=False, server_default=text("now()"))
    is_verified= Column(Boolean,nullable=False, default=False)