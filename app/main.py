from fastapi import FastAPI
from models import user_modele
from routers import test_router, user_router
from db.database import engine, Base

app = FastAPI()

app.include_router(test_router.router)
app.include_router(user_router.router)

# Créer la table des utilisateurs
Base.metadata.create_all(bind=engine)
