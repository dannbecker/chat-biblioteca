import uvicorn
from fastapi import FastAPI
from database import engine, Base
from app.routers import chat

app = FastAPI()

@app.get("/")
def check_api():
    return {"response": "Api Online!"}

app.include_router(chat.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5002, reload=True)


