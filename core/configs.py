from pydantic import BaseSettings
from sqlalchemy.ext.declarative  import declarative_base

class Settings(BaseSettings):
  # Configs gerais da app
  API_V1_STR: str = '/api/v1'
  DB_URL: str =  'postgresql+asyncpg://thauan:password@localhost:5432/faculdade'
  DB_BASE_MODEL = declarative_base()

  class Config:
    case_sensitive = True 


settings = Settings()

