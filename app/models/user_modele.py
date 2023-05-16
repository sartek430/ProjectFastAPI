# Libs Imports
from sqlalchemy import Column, Integer, String, Sequence
from db.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    role = Column(String(50))

    # Relationship with the Company model
    companies = relationship("Company", back_populates="user")
