from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI(title="ScoreMyCV")

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