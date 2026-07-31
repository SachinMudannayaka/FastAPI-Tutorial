from pydantic import BaseModel,EmailStr

# Schema for new user create
class UserCreate(BaseModel):
    username : str
    email : EmailStr
    password : str
    role : str

class UserLogin(BaseModel):
    username: str
    password: str
