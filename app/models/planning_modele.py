# Libs Imports
from sqlalchemy import Column, Integer, Date, Time, Sequence
from sqlalchemy.orm import relationship
from db.database import Base
from models.activity_modele import Activity


class Planning(Base):
    __tablename__ = 'planning'
    id = Column(Integer, Sequence('planning_id_seq'), primary_key=True)
    day = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

    # Relationship with the Activity model
    activities = relationship(Activity, back_populates="planning")
