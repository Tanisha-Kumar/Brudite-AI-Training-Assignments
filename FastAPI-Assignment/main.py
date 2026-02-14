from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

#------------------------------------------------
#1.

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Application"}

# Health endpoint
@app.get("/health")
def health_check():
    return {"status": "UP", "service": "FastAPI App"}

#----------------------------------------------------
#2.

#PATH PARAM
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/products/{product_name}")
def get_product(product_name: str):
    return {"user_id": product_name.upper()}

@app.get("/items/{item_id}")
def get_item(item_id: int = Path(gt=0)):
    return {"item_id": item_id}

@app.get("/users/{user_id}/orders/{order_id}")
def get_user_order(user_id: int, order_id:int):
    return{
        "user_id": user_id, 
        "order_id":  order_id
    }

#------------------------------------------------
#3.

#QUERY PARAMS
@app.get("/search")
def search(q: str, page: int = 1, limit: int = 10, price: float = Query(gt=0), tags: Optional[List[str]] = Query(None)):
    return {
        "query": q,
        "page": page,
        "limit": limit,
        "price": price,
        "tags": tags
    }

@app.get("/filter")
def filter_items(category: str, min_price: float, max_price: float):
    return {
        "category": category,
        "min_price": min_price,
        "max_price": max_price
    }
#-----------------------------------------------
#4. Request Body & Pydantic Models

class User(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(gt=18)
    address: Optional[str] = None
    phone_number: Optional[str] = None

@app.post("/users")
def create_user(user: User):
    return {
        "message": "User created successfully!",
        "user": user
    }

#-------------------------------------------------
5.

USERS : List[User] = []

@app.get("/user", response_model=List[User], status_code=status.HTTP_200_OK)
def get_users():
    return  USERS

@app.post("/user", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    USERS.append(user)
    return{"message": "user added successfully"}

@app.put("/user/{user_id}")
def update_user(user_id: int, data: User):
    if user_id >= len(USERS):
        raise HTTPException(status_code=404, detail="User not found")
    USERS[user_id] = data
    return {"message": "User updated", "user": data}

@app.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id >= len(USERS):
        raise HTTPException(status_code=404, detail="User not found")
    USERS.pop(user_id)

#-----------------------------------------------
6.

class Student(BaseModel):
    name: str
    age: int = Field(gt=0)
    email: EmailStr
    phone_number: Optional[str] = None

@app.post("/students")
def create_student(student: Student):
    return {"message": "Student created successfully", "student": student}

class AuthUser(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=6)
    email: EmailStr

class Item(BaseModel):
    name: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=1)
