import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def func():
    return "Hellow World!!"

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)