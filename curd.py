from fastapi import FastAPI,status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

books = [
    {
        "id": 1,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publish_date": "1960-07-11"
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "publish_date": "1949-06-08"
    },
    {
        "id": 3,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publish_date": "1925-04-10"
    },
    {
        "id": 4,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "publish_date": "1813-01-28"
    },
    {
        "id": 5,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "publish_date": "1937-09-21"
    }
]
app = FastAPI()

@app.get("/")
def get_books():
    return books

@app.get("/book/{book_id}")
def get_a_book(book_id:int):
    for book in books:
        if book['id']== book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book Not Found")

class Book(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str

@app.post("/create/book")
def create_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)

class BookUpdate(BaseModel):
    title: str
    author: str
    publish_date: str 

@app.put("/update/book/{book_id}")
def update_book(book_id: int,book_update:BookUpdate):
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update.title
            book["author"] = book_update.author
            book["publish_date"] = book_update.publish_date
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book Not Found")      

@app.delete("/delete/book/{book_id}")
def delete_book(book_id:int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return{"Messege":"Book is deleted"}
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Book Not Found")        