from fastapi import FastAPI
from app import models, database
from app.routers import users,auth
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="ScoreMyCV")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "ScoreMyCV API is live"}

app.include_router(users.router)
app.include_router(auth.router)