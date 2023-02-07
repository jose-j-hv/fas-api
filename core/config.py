import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path = env_path)

###print(os.getenv('POSTGRES_DB'))

class Settings:
    PROJECT_NAME: str = os.getenv("PROYECTO-FAST-API")
    PROYECT_VERSION:str = os.getenv("1.0")
    POSTGRES_DB:str = os.getenv("POSTGRES_DB")
    POSTGRES_USER:str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD:str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER:str = os.getenv("POSTGRES_SERVER")    
    POSTGRES_PORT:int = os.getenv("POSTGRES_PORT")
    ###SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/uno"
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

settings = Settings()