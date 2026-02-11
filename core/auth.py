from pytz import timezone
from typing import Optional
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from pydantic import EmailStr

from models.user_model import UserModel
from core.settings import settings
from core.security import check_password


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)

async def authenticate(email: EmailStr, password: str, db: AsyncSession) -> Optional[UserModel]:
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None

        if not check_password(password, user.password):
            return None

        return user


def create_token(type_token: str, life_time: timedelta, sub: str) -> str:

    payload = {}
    time_zone = timezone("America/Fortaleza")
    expire = datetime.now(tz=time_zone) + life_time

    payload["type"] = type_token
    payload["exp"] = expire
    payload["iat"] =  datetime.now(tz=time_zone)
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def create_token_access(sub:str)->str:
    return create_token(
        type_token="access_token",
        life_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )

