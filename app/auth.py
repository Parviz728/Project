from .config import Config
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .user import User

class Auth():
    config = Config()
    engine = create_engine(config.DB_URL)

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def get_user(self, username: str, password: str):
        with Session(self.engine) as session:
            user = session.query(User).filter(User.username == username and User.password == password).first()
            if user:
                return user


    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username, password)
        if user:
            if self.verify_password(password, user.password):
                return True
            return False
        return False