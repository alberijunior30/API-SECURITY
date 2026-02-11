from typing import Optional
from pydantic import BaseModel as SCBaseModel, HttpUrl, field_validator

class ArticleSchema(SCBaseModel):
    id: Optional[int] = None
    titulo: str
    url_font: HttpUrl
    description: str
    user_id: Optional[int] = None

    @field_validator('url_font', mode='after')
    @classmethod
    def transform_url_to_str(cls, v: HttpUrl) -> str:
        return str(v)

    class Config:
        from_attributes = True