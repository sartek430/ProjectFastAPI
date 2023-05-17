# Libs Imports
from sqlalchemy import Column, Integer, String, Sequence
from db.database import Base
from sqlalchemy.orm import relationship


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, Sequence('company_id_seq'), primary_key=True)
    name = Column(String(50))
    adress = Column(String(100))

    #  Relationship with the User model
    users = relationship("User", back_populates="company")
