from .db import pool
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .users import router as user_router
from loguru import logger
import sys



# --- Lifespan (startup / shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.open()
    logger.info("DB pool opened")
    yield
    await pool.close()
    logger.info("DB pool closed")

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)  # <-- include the router


