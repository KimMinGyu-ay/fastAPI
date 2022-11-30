from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware

from model import UserTable, User
from db import session

app = FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/users")
def read_users():
    users = session.query(UserTable)

    return users


@app.get("/users/{user_id}")
def read_users(user_id: int):
   
    user = session.query(UserTable).filter(UserTable.id == user_id)
    
    return user


@app.post("/users")
def create_users(name : str, age : int):
    # name과 age를 받아 user table 작성

    user = UserTable()
    user.name = name
    user.age = age

    session.add(user)
    session.commit()


    return f"{name} created...."

@app.put("/users") # put은 업데이트
def update_users(users : List(User)):
    for i in users:
        user = session.query(UserTable).filter(UserTable.id == i.id).first()
        user.name = i.name
        user.age = i.age
    
    # users[0].name

    return f"{users[0].name.name} updated..."

@app.delete("/users")
def read_users(user_id : int):
    user = user = session.query(UserTable).filter(UserTable.id == user_id).first()
    session.commit()
    return read_users