from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
app = FastAPI()

# GET REQUESTS
# @app.get("/")
# def read_root():
#     return{"Messege":"Hellow world"}

# @app.get("/greet")
# def greet():
#     return{"Messege":"Hellow SACHIN"}

# pass path paramter
# @app.get("/greet/{name}")
# def greetname(name: str):
#     return {"Messege":f"Hellow {name}"}

#pass path & query parameter
# @app.get("/greet/{name}")
# def greet_path_q(name: str,age:Optional[int] = None):
#     return {"Messege":f"Hellow {name} your age is {age}"}

# POST REQUESTS
class Student(BaseModel):
    name:str
    age:int
    role:int

@app.post("/create_student")
def create_student(student:Student):
    return{
        "name":student.name,
        "age":student.age,
        "role":student.role
    }
