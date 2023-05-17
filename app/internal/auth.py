# Libs Imports
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
# Local Imports
from db.database import Session, get_session
from routers.user_router import inner_get_user
from models.user_modele import User
# System Imports

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key"  # Clé secrète pour signer les tokens JWT
ALGORITHM = "HS256"  # Algorithme de chiffrement pour les tokens JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Durée de validité des tokens en minutes


async def verify_password(plain_password, hashed_password):
    """
     Verify a plain password against a hashed password.

     @param plain_password - The plain password to verify
     @param hashed_password - The hashed password to verify against

     @return True if the password is correct False if it is not.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
     Hashes and encrypts a password. 

     @param password - The password to hash.

     @return A hash of the password that can be used as a key in the attacker's account. The hash is stored in the database
    """
    return pwd_context.hash(password)


async def authenticate_user(email: str, password: str):
    """
     Authenticates a user by email and password. 

     @param email - The email of the user to authenticate. 
     @param password - The password of the user to authenticate.

     @return True if the user was authenticated False otherwise.
    """
    for session in get_session():
        user = await inner_get_user(email, session)
    # Return True if user is not logged in.
    if not user:
        return False
    # Returns True if the password is valid and the user has a hashed password.
    if not await verify_password(password, user["password"]):
        return False
    return user


def decode_access_token(token: str):
    """
    Decode an access token and retrieve the data.

    @param token - The access token to decode.

    @return The decoded token data.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def create_access_token(data: dict, expires_delta: timedelta):
    """
     Create an access token for the given data.

     @param data - The data to encode in the access token.
     @param expires_delta - The number of seconds until the token expires.

     @return The encoded access token as a byte string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    expire_str = expire.strftime("%Y-%m-%dT%H:%M:%S")
    to_encode.update({"exp": expire_str})
    print(to_encode)
    print(SECRET_KEY)
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm), session: Session = Depends(get_session)):
    """
     Log in to Twitter and return access token.

     @param form_data - Form data to be used for authenticating

     @return OAuth2 access token and token type
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["id"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
