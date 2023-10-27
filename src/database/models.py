from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    birthday = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), default=None)
    user = relationship("User", backref="contacts")
         
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    avatar = Column(String(250), nullable=True)
    refresh_token = Column(String(250), nullable=True)
    confirmed = Column(Boolean, default=False)