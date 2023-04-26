from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Créer le moteur de base de données
engine = create_engine(
    'sqlite:///./db/database.db',
    connect_args={"check_same_thread": False})

# Créer une session pour interagir avec la base de données
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base = declarative_base()
