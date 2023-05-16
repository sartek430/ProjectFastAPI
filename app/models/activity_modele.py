# Libs Imports
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship
from db.database import Base


class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, Sequence('activity_id_seq'), primary_key=True)
    name = Column(String(100))

    # Relationship with the Planning model
    planning = relationship("Planning", back_populates="activities")
