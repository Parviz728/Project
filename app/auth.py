from config import Config
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from user import User

class Auth():
    hasher = CryptContext(schemes=['bcrypt'])
    config = Config()
    engine = create_engine(config.DB_URL)

    def encode_password(self, password):
        return self.hasher.hash(password + self.config.salt)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.hasher.verify(plain_password + self.config.salt, hashed_password)

    def get_user(self, username: str):
        with Session(self.engine) as session:
            return session.query(User).filter(User.username == username).first()

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user or not self.verify_password(password, user.password):
            return False
        return True