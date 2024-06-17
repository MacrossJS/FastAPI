import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/sum/")
def calculate_sum(a: int, b: int):
    return {"result": a + b}


if __name__ == "__main__":
    uvicorn.run("main_errors:app", host='127.0.0.1', port=8066, reload=True, workers=3)
