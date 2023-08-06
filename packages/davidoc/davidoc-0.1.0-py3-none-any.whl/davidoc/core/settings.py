import os
from pydantic import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('davidoc/config/.env'))

class Settings(BaseSettings):
    secret_key: str = os.getenv('secret_key')