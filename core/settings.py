from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

#Configurações do banco de Dados
user: str = "postgres"
password: str = "Junior32720131%"
host: str = "localhost"
port: str = "5432"
DB: str = "faculdade"


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{DB}"
    DBbaseModel:ClassVar = declarative_base() #esse tipo, pois esta dentro de uma classe

    JWT_SECRET: str = "qpvTFURLFTFrVmcKcEGi8CWlqCCvY7pJ1BMaiyDaNFY"

    #terminal:

    #import secrets
    #token: str = secrets.token_urlsafe(32)
    #token

    #para maior segurança, importa secret, colocar segredo na variavel e colocar no JWT_SECRET


    ALGORITHM: str = "HS256"

    #60 minutos x 24 horas x 7 dias => 10080 minutos => 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    class Config:
        case_sensitive = True


settings: Settings = Settings()
