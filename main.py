from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.database import DatabaseConnection
from app.routes.user import user_router
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    await DatabaseConnection.connect_and_init()
    print(" hello")
    yield
    await DatabaseConnection.close()
    print(" Goodbye")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/users", tags=["users"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
