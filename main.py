from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import connect_and_init, close
from app.routes.user import user_router
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_and_init()
    print("message hello")
    yield
    await close()
    print("message Goodbye")

app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/users", tags=["users"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
