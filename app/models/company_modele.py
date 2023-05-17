# Libs Imports
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence
from db.database import Base
from sqlalchemy.orm import relationship


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, Sequence('company_id_seq'), primary_key=True)
    name = Column(String(50))
    adress = Column(String(100))

    #  Relationship with the User model
    user = relationship("User", back_populates="companies")
