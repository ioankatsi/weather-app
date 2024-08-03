from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    database_url: str
    secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
