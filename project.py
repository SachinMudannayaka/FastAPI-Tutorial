from fastapi import FastAPI,Depends
from database import get_db,engine
from sqlalchemy.orm import session
import model
from pydantic import BaseModel

app = FastAPI()

class BookStore(BaseModel):
    id:int
    title:str
    author: str
    publish_date:str
#Add book
@app.post("/create/book")
def create_book(book:BookStore, db:session = Depends(get_db)):
    new_book = model.Book(id=book.id,title=book.title,author= book.author,publish_date = book.publish_date)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return(new_book)

#Get All books
@app.get("/")
def get_book(db:session = Depends(get_db)):
    books = db.query(model.Book).all()
    return books
    