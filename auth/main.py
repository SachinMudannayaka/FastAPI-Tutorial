from fastapi import FastAPI,Depends,HTTPException,status
import os
from sqlalchemy.orm import Session 
import models,schemas,utils
from auth_database import get_db
from jose import jwt
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import JWTError
from h11._readers import Http10Reader
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Helper Function that takes user data
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

app = FastAPI()

@app.post("/sign-up")
def register_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    #Check the user exits or not
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="UserName Already Exist")
    
    # Hashed the Password
    hashed_pass = utils.hash_password(user.password)
    # Create New User instance
    new_user = models.User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_pass,
        role = user.role
    )

    # Save User to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"id":new_user.id,"user_name":new_user.username,"email":new_user.email,"role":new_user.role}

# @app.post("/login")
# def login(form_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.username == form_data.username).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid User Name")
    
#     if not utils.verify_password(form_data.password,user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong Password")
    
#     token_data = {'sub':user.username,'role':user.role}
#     token = create_access_token(token_data)
#     return{"access_token":token, "token_type": "bearer"}

@app.post("/login")
def login(user_data: schemas.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.username == user_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid User Name"
        )

    if not utils.verify_password(
        user_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong Password"
        )

    token_data = {
        "sub": user.username,
        "role": user.role
    }

    token = create_access_token(token_data)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def getCurrentUser(token: str = Depends(oauth2_scheme)):
    credential_exception  = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Couldn't validate credentials", 
                                          headers={"WWW-Authenticate":"Bearer"})

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username : str = payload.get("sub") 
        role: str = payload.get("role")
        if username is None or role is None:
            raise credential_exception
    except JWTError:
        raise credential_exception

    return {"username" :username, "role": role}
    
@app.get("/protected")
def protected_route(current_user:dict = Depends(getCurrentUser)) :
    return {"Messege": f"Hello, {current_user['username']}| You access a protected route"}

def require_roles(allowed_roles:list[str]):
    def role_checker(current_user: dict = Depends(getCurrentUser)):
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code=status.Http_403,detail="Not enough Permission")
        return current_user
    return role_checker