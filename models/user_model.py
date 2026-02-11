from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from core.settings import settings


class UserModel(settings.DBbaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=True)
    lastname = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    admin = Column(Boolean, default=False)
    articles = relationship(
        "ArticleModel",
        cascade="all,delete-orphan",
        back_populates="creator",
        uselist=True,
        lazy="joined"
    )
