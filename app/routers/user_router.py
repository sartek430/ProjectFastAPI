# Libs Imports
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.hash import bcrypt
# Local Imports
from db.database import get_session
from models.user_modele import User
# System Imports


router = APIRouter()

key = b'S8nKUCy6kqF32UfD3NcJbS0VeXL4mADxe4xC4f7IJ7U='
fernet = Fernet(key)


class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str
    role: str
    fk_company: int


def encrypt_fields(firstName: str, lastName: str, email: str) -> tuple:
    """
     Encrypt first name last name and email.

     @param firstName - The first name of the user
     @param lastName - The last name of the user
     @param email - The email address of the user ( must be unique )

     @return A tuple containing the encrypted first name last name and email
    """
    encrypted_firstName = fernet.encrypt(firstName.encode())
    encrypted_lastName = fernet.encrypt(lastName.encode())
    encrypted_email = fernet.encrypt(email.encode())
    return encrypted_firstName, encrypted_lastName, encrypted_email


def decrypt_fields(firstName: str, lastName: str, email: str) -> tuple:
    """
     Decrypt first name last name and email.

     @param firstName - The first name of the user
     @param lastName - The last name of the user
     @param email - The email address of the user ( must be unique )

     @return A tuple of decrypted fields for use in an email. If any of the fields are invalid it will return None
    """
    decrypt_firstName = fernet.decrypt(firstName).decode()
    decrypt_lastName = fernet.decrypt(lastName).decode()
    decrypt_email = fernet.decrypt(email).decode()
    return decrypt_firstName, decrypt_lastName, decrypt_email


@router.get("/users")
async def get_users(session: Session = Depends(get_session)):
    """
     Get all users

     @param session - User object

     @return list of founded user(s)
    """
    users = session.query(User).all()
    # Aucun utilisateur trouvés
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Aucun utilisateur trouvé")
    return users


async def inner_get_user(emailUser: str, session: Session):
    findUser = False
    users = session.query(User).all()
    i = 0
    for emails in session.query(User.email):
        for email in emails:
            print(fernet.decrypt(email).decode() == emailUser)
            if fernet.decrypt(email).decode() == emailUser:
                findUser = True
                user = users[i]
        i += 1

    if findUser:
        return {
            "id": user.id,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "email": user.email,
            "password": user.password,
            "role": user.role,
            "fk_company": user.fk_company
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")


@router.get("/user/{emailUser}")
async def get_user(emailUser: str, session: Session = Depends(get_session)):
    """
    Get a user by email.

    @param email - Email address of the user to retrieve
    @param session - SQLAlchemy session to use for database operations

    @return The user as JSON (dict) or HTTPException with status code 404 if the user is not found
    """
    return await inner_get_user(emailUser, session)


@router.post("/user")
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """
    Create a user.

    @param user - UserCreate with information about the user to create
    @param session - SQLAlchemy session to use for database operations

    @return The newly created user as JSON ( dict ) or HTTPException with status code 409 if email exist
    """
    # Check if the email already exist in the database
    for emails in session.query(User.email):
        for email in emails:
            if fernet.decrypt(email).decode() == user.email:
                raise HTTPException(
                    status_code=409, detail="L'utilisateur avec cet e-mail existe déjà")

    encrypted_firstName, encrypted_lastName, encrypted_email = encrypt_fields(
        user.firstName, user.lastName, user.email)

    hashed_password = bcrypt.hash(user.password)

    user = User(firstName=encrypted_firstName, lastName=encrypted_lastName, email=encrypted_email,
                password=hashed_password, role=user.role, fk_company=user.fk_company)

    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=500, detail="Erreur lors de la création de l'utilisateur")

    decrypted_firstName, decrypted_lastName, decrypted_email = decrypt_fields(
        encrypted_firstName, encrypted_lastName, encrypted_email)

    return {
        "id": user.id,
        "firstName": decrypted_firstName,
        "lastName": decrypted_lastName,
        "email": decrypted_email,
        "password": user.password,
        "role": user.role,
        "fk_company": user.fk_company
    }


@router.delete("/user/{user_id}")
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    """
    Delete a user from the database. This is a no - op if the user doesn't exist

    @param user_id - id of the user to delete
    @param session - session to use for database operations.

    @return success or error message
    """
    user = session.query(User).get(user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail="Utilisateur non trouvé")

    session.delete(user)
    session.commit()

    return {"message": "Utilisateur supprimé avec succès"}


@router.put("/user/{user_id}")
async def update_user(user_id: int, user_update: UserCreate, session: Session = Depends(get_session)):
    """
     Update a user in the database.

     @param user_id - id of the user to update
     @param user_update - User object with new information to update
     @param session - Session to use for database operations.

     @return Returns a dictionary with the result of the request
    """
    user = session.query(User).get(user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail="Utilisateur non trouvé")

    encrypted_firstName, encrypted_lastName, encrypted_email = encrypt_fields(
        user_update.firstName, user_update.lastName, user_update.email)

    # Mise à jour des champs de l'utilisateur
    user.firstName = encrypted_firstName
    user.lastName = encrypted_lastName
    user.email = encrypted_email
    user.role = user_update.role
    user.fk_company = user_update.fk_company

    session.commit()

    return {
        "message": "Utilisateur mis à jour avec succès",
        "user": user_update
    }
