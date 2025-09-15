from psycopg_pool import AsyncConnectionPool
from typing import Any, Sequence, Optional, Union
from dotenv import load_dotenv
import os

# Load .env file from current directory
load_dotenv()

USERNAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("DB_PASSWORD")
ADDRESS  = os.environ.get("DB_HOSTNAME")
PORT     = int(os.environ.get("DB_PORT"))
DATABASE = os.environ.get("DB_NAME")

DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{ADDRESS}:{PORT}/{DATABASE}"

# --- Pool ---
pool = AsyncConnectionPool(
    DATABASE_URL,
    min_size=2,
    max_size=10,
    num_workers=2,
    open=False,
)

# -- query help util --
async def run_query(
    query: str,
    params: Optional[Sequence[Any]] = None,
    fetch: str = "none"
) -> Union[None, tuple, list[tuple], int]:
    """
    Run a query with the pool.

    fetch = "one"  -> returns single row (tuple)
    fetch = "all"  -> returns list of rows
    fetch = "val"  -> returns single scalar value
    fetch = "none" -> returns rowcount (INSERT/UPDATE/DELETE)
    """
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params or [])
            
            if fetch == "one":
                return await cur.fetchone()
            elif fetch == "all":
                return await cur.fetchall()
            elif fetch == "val":
                row = await cur.fetchone()
                return row[0] if row else None
            else:
                return cur.rowcount

