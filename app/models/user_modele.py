from sqlalchemy import Column, Integer, String, Sequence
from db.database import Base, engine
# Définir le modèle de données pour l'utilisateur


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    password_hash = Column(String(255))
    job = Column(String(100))


Base.metadata.create_all(bind=engine)
