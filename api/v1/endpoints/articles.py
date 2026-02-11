from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.article_model import ArticleModel
from models.user_model import UserModel
from schemas.article_schema import ArticleSchema
from core.deps import get_session, get_current_user


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArticleSchema)
async def post_article(article: ArticleSchema, user_log: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:

        new_article: ArticleModel = ArticleModel(titulo=article.titulo,
                                                 description=article.description,
                                                 url_font=article.url_font,
                                                 user_id=user_log.id)

        session.add(new_article)
        await session.commit()
        return new_article


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ArticleSchema])
async def get_articles(db: AsyncSession = Depends(get_session)):
    async with db as session:

        query = select(ArticleModel)
        result = await session.execute(query)
        article: List[ArticleModel] = result.scalars().unique().all()
        return article


@router.get("/{article_id}", response_model=ArticleSchema, status_code=status.HTTP_200_OK)
async def get_article(article_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id)
        result = await session.execute(query)
        article: ArticleModel = result.scalars().unique().one_or_none()

        if article:
            return article
        else:
            raise HTTPException(detail="Artigo não encontrado!", status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{article_id}", response_model=ArticleSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_article(article_id: int, edit_article: ArticleSchema, db: AsyncSession = Depends(get_session), user_log: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id)
        result = await session.execute(query)
        article: ArticleModel = result.scalars().unique().one_or_none()

        if article:
            article.titulo = edit_article.titulo
            article.description = edit_article.description
            article.url_font = edit_article.url_font
            if user_log.id != article.user_id:
                article.id = user_log.id
            await  session.commit()
            return article
        else:
            raise HTTPException(detail="Artigo não encontrado", status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_id: int, db: AsyncSession = Depends(get_session), user_log: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id).filter(ArticleModel.user_id == user_log.id)
        result = await session.execute(query)
        del_article = result.scalars().unique().one_or_none()

        if del_article:
            await session.delete(del_article)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Artigo não encontrado", status_code=status.HTTP_404_NOT_FOUND)






