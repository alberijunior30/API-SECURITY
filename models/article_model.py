from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.settings import settings


class ArticleModel(settings.DBbaseModel):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(256))
    url_font = Column(String(256))
    description = Column(String(256))
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship(
        "UserModel", back_populates="articles", lazy="joined")
