from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Créer le moteur de base de données
engine = create_engine(
    'sqlite:///./db/database.db',
    connect_args={"check_same_thread": False})

# Créer une session pour interagir avec la base de données
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_session() -> Session:
    """
     Get a session for use in tests. This is a context manager that can be used to make sure that the session is closed when the context exits
    """
    session = Session()
    try:
        yield session
    finally:
        session.close()
