from fastapi import FastAPI
from models import user_modele
from routers import test_router, user_router
from db.database import engine, Base

app = FastAPI()

custom_reponses = {
    200: {"description": "OK"},
    201: {"description": "Created"},
    204: {"description": "No Content"},
    400: {"description": "Bad Request"},
    401: {"description": "Unauthorized"},
    403: {"description": "Forbidden"},
    404: {"description": "Not Found"},

}

app.include_router(test_router.router,
                   responses=custom_reponses, tags=["users"])
app.include_router(user_router.router)

# Créer la table des utilisateurs
Base.metadata.create_all(bind=engine)
