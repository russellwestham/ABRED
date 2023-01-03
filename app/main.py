from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware
from db import session 
from model import UserTable, User, TargetItem, TargetItemTable

app = FastAPI()

# TODO : define CORS policy 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------APIs------------
@app.get("/users")
async def read_users():
    users = session.query(UserTable).all()
    return users

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    user = session.query(UserTable).\
        filter(UserTable.id == user_id).first()
    return user

@app.post("/user")
async def create_user(name: str, age: int, email: str):
    user = UserTable()
    user.name = name
    user.age = age
    user.email = email
    session.add(user)
    session.commit()

@app.put("/users")
async def update_users(users: List[User]):
    for new_user in users:
        user = session.query(UserTable).\
            filter(UserTable.id == new_user.id).first()
        user.name = new_user.name
        user.age = new_user.age
        user.email = new_user.email
        session.commit()

@app.get("/target_items")
async def read_target_items():
    users = session.query(TargetItemTable).all()
    return users
    
@app.post("/target_item")
async def create_target_item(name: str, keywords: str):
    target_item = TargetItemTable()
    target_item.name = name
    target_item.keywords = keywords
    session.add(target_item)
    session.commit()
