import os
from dotenv import load_dotenv

load_dotenv()
class Config():
    secret_key = os.getenv("secret_key")
    DB_URL = os.getenv("DB_URL")
    ALGORITHM = os.getenv("ALGORITHM")
    EXP_MINUTES = 10