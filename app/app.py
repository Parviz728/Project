from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import Auth
from .models import Item

auth = Auth()
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=auth.config.EXP_MINUTES)
    data.setdefault("exp", expire)
    return jwt.encode(data, auth.config.secret_key, algorithm=auth.config.ALGORITHM)

@app.post('/login')
def get_token(user_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = user_data.username
    password = user_data.password

    if not auth.authenticate_user(username, password):
        raise HTTPException(status_code=401, detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token({"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected_resource")
async def protected_resource(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, auth.config.secret_key, algorithms=[auth.config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})

    return {"message": "Access granted to protected resource"}

@app.get('/get_data')
def get_data(date_from: datetime, date_to: datetime):
    with Session(auth.engine) as session:
        return session.query(Item).filter(Item.date >= date_from, Item.date <= date_to).all()




