from core.configs import  settings
from core.database import engine

async def create_tables() -> None:
  import models.__all_models
  print('criando tabelas')
  async with  engine.begin() as conn:
    await conn.run_sync(settings.DB_BASE_MODEL.metadata.drop_all)
    await conn.run_sync(settings.DB_BASE_MODEL.metadata.create_all)
  print('tabelas criadas')


if __name__ == '__main__':
  import asyncio
  asyncio.run(create_tables())