from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware

from model import UserTable, User
from db import session

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/users")
def read_users():
    users = session.query(UserTable).all()
    return users


@app.get("/users/{user_id}")
def read_user(user_id: int):
    user = session.query(UserTable).filter(UserTable.id == user_id).first()
    return user


@app.post("/user")
def create_users(name : str, age : int):
    # name과 age를 받아 user table 작성

    user = UserTable()
    user.name = name
    user.age = age

    session.add(user)
    session.commit()


    return f"{name} created...."

@app.put("/users") # put은 업데이트
def update_users(users : List[User]):

    for i in users:
        user = session.query(UserTable).filter(UserTable.id == i.id).first()
        user.name = i.name
        user.age = i.age
        session.commit()
    # users[0].name

    return f"{users[0].name} updated..."

@app.delete("/user")
def delete_users(userid: int):
    user = session.query(UserTable).filter(UserTable.id == userid).delete()
    session.commit()
    return f"User deleted..."