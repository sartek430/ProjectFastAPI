from sqlalchemy import Column, Integer, String, Sequence
from db.database import Base, engine
# Définir le modèle de données pour l'utilisateur


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    email = Column(String(100), unique=True)
    password = Column(String(255))


Base.metadata.create_all(bind=engine)
