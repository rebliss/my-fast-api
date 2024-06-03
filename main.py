from fastapi import FastAPI, HTTPException
from sqlalchemy import MetaData
from databases import Database
from typing import List

from config import settings
from models import users
from schemas import User, UserCreate

DATABASE_URL = settings.database_url

database = Database(DATABASE_URL)
metadata = MetaData()

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    query = users.insert().values(name=user.name, email=user.email)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}

@app.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10):
    query = users.select().offset(skip).limit(limit)
    return await database.fetch_all(query)

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    query = users.update().where(users.c.id == user_id).values(name=user.name, email=user.email)
    await database.execute(query)
    return {**user.dict(), "id": user_id}

@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    delete_query = users.delete().where(users.c.id == user_id)
    await database.execute(delete_query)
    return user
