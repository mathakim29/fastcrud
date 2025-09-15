from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .security import hash_password, verify_password
from .db import run_query
from nanoid import generate
from pydantic import BaseModel, validator, EmailStr
import regex
from loguru import logger
router = APIRouter()



# --- Pydantic models ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator("password")
    def password_regex(cls, v):
        # At least 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
        pattern = regex.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$")
        if not pattern.match(v):
            raise ValueError(
                "Password must be ≥8 chars, include uppercase, lowercase, number, and special char"
            )
        return v

class UserAccess(BaseModel):
    username: str
    email: EmailStr
    password: str



# --- Routes ---
@router.post("/users/add")
async def create_user(user: UserCreate):
    user_id = generate(size=14)           # Generate nanoid
    hashed = hash_password(user.password) # Hash password
    query = "INSERT INTO users (id, username, email, password) VALUES (%s, %s, %s, %s)"
    try:
        await run_query(query, [user_id, user.username, user.email, hashed])
        return {"id": user_id, "username": user.username, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/users/login")
async def login(user: UserAccess):
    query = "SELECT password FROM users WHERE username=%s"
    hashed = await run_query(query, [user.username], fetch="val")
    if not hashed or not verify_password(user.password, hashed):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}

@router.get("/users/list")
async def list_users():
    query = "SELECT id, username, email FROM users"
    try:
        rows = await run_query(query, fetch="all")
        users = [{"id": r[0], "username": r[1], "email": r[2]} for r in rows]
        logger.info("Listing users")
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/reset")
async def reset_users():
    try:
        query = "TRUNCATE TABLE users RESTART IDENTITY CASCADE;"
        rows = await run_query(query, fetch="none")
        logger.success("Successfull user database reset")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/users/remove")
async def remove_users(user: UserAccess):
    try:
        query = "DELETE FROM users WHERE email = %s RETURNING email"
        deleted_id = await run_query(query, [user.email], fetch="val")
        if not deleted_id:
            logger.error("User not found")
            raise HTTPException(status_code=404, detail="User not found")
        logger.success("Successfully removed user")
        return {"message": f"User {deleted_id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))