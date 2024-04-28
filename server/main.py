from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine
from db.models import Base
from routers.router import router
from dotenv import load_dotenv


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="devSecOpsThon"
)

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def hello():
    return {"message": "Hello World"}

app.include_router(router, prefix="/api/v1")
