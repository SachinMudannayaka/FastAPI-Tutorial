from fastapi import FastAPI
from typing import Optional
app = FastAPI()

@app.get("/")
def read_root():
    return{"Messege":"Hellow world"}

@app.get("/greet")
def greet():
    return{"Messege":"Hellow SACHIN"}

# pass path paramter
# @app.get("/greet/{name}")
# def greetname(name: str):
#     return {"Messege":f"Hellow {name}"}

#pass path & query parameter
@app.get("/greet/{name}")
def greet_path_q(name: str,age:Optional[int] = None):
    return {"Messege":f"Hellow {name} your age is {age}"}
