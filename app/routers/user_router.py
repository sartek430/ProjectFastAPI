# Libs Imports
import hashlib
from fastapi import APIRouter, status, HTTPException, Depends
from db.database import session
from models.user_modele import User
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.hash import bcrypt


router = APIRouter()

key = Fernet.generate_key()
fernet = Fernet(key)

# Définition du modèle Pydantic pour créer un nouvel utilisateur


class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str
    role: str
# Dependency


def get_session():
    try:
        yield session
    finally:
        session.close()


def encrypt_fields(firstName: str, lastName: str, email: str) -> tuple:
    encrypted_firstName = fernet.encrypt(firstName.encode())
    encrypted_lastName = fernet.encrypt(lastName.encode())
    encrypted_email = fernet.encrypt(email.encode())
    return encrypted_firstName, encrypted_lastName, encrypted_email


def decrypt_fields(firstName: str, lastName: str, email: str) -> tuple:
    decrypt_firstName = fernet.decrypt(firstName.encode())
    decrypt_lastName = fernet.decrypt(lastName.encode())
    decrypt_email = fernet.decrypt(email.encode())
    return decrypt_firstName, decrypt_lastName, decrypt_email


@router.get("/users")
async def get_users(session: Session = Depends(get_session)):
    """
     Retourne tous les utilisateurs
     @return liste des utilisateurs trouvés
    """
    users = session.query(User).all()
    # Aucun utilisateur trouvés
    if not users:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail="Aucun utilisateur trouvé")
    return users


@router.post("/users")
async def create_user(user: UserCreate):
    hashed_password = bcrypt.hash(user.password)
    encrypted_firstName, encrypted_lastName, encrypted_email = encrypt_fields(
        user.firstName, user.lastName, user.email)
    user = User(firstName=encrypted_firstName, lastName=encrypted_lastName, email=encrypted_email,
                password=hashed_password, role=user.role)
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400, detail="L'utilisateur avec cet email existe déjà")
    return {"id": user.id, "firstName": user.firstName.decode(), "lastName": user.lastName.decode(), "email": user.email.decode(), "password": user.password, "role": user.role}
