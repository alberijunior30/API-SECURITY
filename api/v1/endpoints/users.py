from typing import List, Optional, Any
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import  OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaCreate, UserSchemaArticles, UserSchemaUp
from core.deps import get_session, get_current_user
from core. security import generate_password_hash
from core.auth import authenticate, create_token_access


router = APIRouter()


@router.get("/logado", response_model=UserSchemaBase)
def get_logado(user_log: UserModel = Depends(get_current_user)):
    return user_log


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        try:
            new_user: UserModel = UserModel(name=user.name,
                                            lastname=user.lastname,
                                            email=user.email,
                                            password=generate_password_hash(user.password),
                                            admin=user.admin)
            session.add(new_user)
            await session.commit()
            return new_user
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Já existe um usúario cadastrado com esse email!")


@router.get("/", response_model=List[UserSchemaBase])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserSchemaBase] = result.scalars().unique().all()
        return users


@router.get("/{user_id}", response_model=UserSchemaArticles, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(detail="Usuário não encontrado", status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{user_id}", response_model=UserSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_user(user_id: int, edit_user:UserSchemaUp,db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserSchemaBase = result.scalars().unique().one_or_none()

        if user:
            if edit_user.name:
                user.name = edit_user.name
            if edit_user.lastname:
                user.lastname = edit_user.lastname
            if edit_user.email:
                user.email = edit_user.email
            if edit_user.password:
                user.password = generate_password_hash(edit_user.password)
            if edit_user.admin:
                user.admin = edit_user.admin

            await session.commit()
            return user
        else:
            raise HTTPException(detail="Usuário não encontrado!", status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        del_user = result.scalars().unique().one_or_none()

        if del_user:
            await session.delete(del_user)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Usuário não foi encontrado!", status_code=status.HTTP_404_NOT_FOUND)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(email=form_data.username,
                              password=form_data.password,
                              db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dados de acesso incorretos!")

    return JSONResponse(content={"access_token": create_token_access(sub=user.id),
                                 "token_type": "bearer"}, status_code=status.HTTP_200_OK)


