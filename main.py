from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return{"Messege":"Hellow world"}

@app.get("/greet")
def greet():
    return{"Messege":"Hellow SACHIN"}
# Pass path paramter
@app.get("/greet/{name}")
def greetname(name: str):
    return {"Messege":f"Hellow {name}"}