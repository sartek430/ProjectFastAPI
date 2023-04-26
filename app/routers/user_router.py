# Libs Imports
import hashlib
from fastapi import APIRouter, Response
from db.database import session
from models.user_modele import User


router = APIRouter()


def hash_password(password: str):
    return hashlib.sha256(f'{password}'.encode('utf-8')).hexdigest()


@router.get("/users")
async def get_users(response: Response):
    """
     Retourne tous les utilisateurs
     @return liste des utilisateurs trouvés
    """
    users = session.query(User).all()
    # Aucun utilisateur trouvé.
    if not users:
        response.status_code = 204
        return {"error": "pas d'utilisateur trouvé"}
    return users
