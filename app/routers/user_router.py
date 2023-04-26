# Libs Imports
import hashlib
from fastapi import APIRouter, status, HTTPException, Depends
from db.database import session
from models.user_modele import User
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session

router = APIRouter()

key = Fernet.generate_key()
fernet = Fernet(key)

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


def hash_password(password: str):
    return hashlib.sha256(f'{password}'.encode('utf-8')).hexdigest()


@router.get("/users")
async def get_users(session: Session = Depends(get_session)):
    """
     Retourne tous les utilisateurs
     @return liste des utilisateurs trouvés
    """
    users = session.query(User).all()
    # Aucun utilisateur trouvées aucun utilisateur.
    if not users:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail="Aucun utilisateur trouvé")
    return users


@router.post("/user")
async def create_user(firstName: str, lastName: str, email: str, password: str, session: Session = Depends(get_session)):
    hashed_password = hash_password(password)
    encrypted_firstName, encrypted_lastName, encrypted_email = encrypt_fields(
        firstName, lastName, email)
    user = User(firstName=encrypted_firstName, lastName=encrypted_lastName,
                email=encrypted_email, password=hashed_password)
    session.add(user)
    try:
        session.commit()
        session.refresh(user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="L'utilisateur avec cet email existe déjà")
    return {"id": user.id, "firstName": user.firstName, "lastName": user.lastName, "email": user.email}
