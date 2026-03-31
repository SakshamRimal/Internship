from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.wallet_schema import TokenData
from app.core.db import SessionDep
from app.models.wallet_model import User
from sqlmodel import select


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("user_id")   # must match create_access_token

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(id=user_id)
        return token_data

    except JWTError:
        raise credentials_exception



async def get_current_user(session: SessionDep , token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token , credentials_exception)

    statement = select(User).where(User.id == token.id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user