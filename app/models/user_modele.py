# Libs Imports
from sqlalchemy import Column, Integer, String, Sequence
from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    role = Column(String(50))
    fk_company = Column(Integer, ForeignKey("companies.id"))

    # Relationship with the Company model
    company = relationship("Company", back_populates="users")
