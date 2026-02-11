from core.settings import settings
from core.database import engine


async def create_tables() -> None:
    import models.__all_models
    print("Criando as tabelas do Banco de Dados")

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBbaseModel.metadata.drop_all) #limpar o banco, cuidado!
        await conn.run_sync(settings.DBbaseModel.metadata.create_all)
    print("Tabelas criadas com sucesso...")


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())