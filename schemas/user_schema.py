from typing import Optional, List
from pydantic import BaseModel as SCBaseModel, EmailStr, Field

from schemas.article_schema import ArticleSchema


class UserSchemaBase(SCBaseModel):
    id: Optional[int] = None
    name: str
    lastname: str
    email: EmailStr
    admin: bool = False

    class Sett:
        orm_mode = True


class UserSchemaCreate(UserSchemaBase):
    password: str = Field(..., max_length=72)


class UserSchemaArticles(UserSchemaBase):
    articles: Optional[List[ArticleSchema]]


class UserSchemaUp(UserSchemaBase):
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    admin: Optional[bool] = None



