import uvicorn
from fastapi import FastAPI
from CryptoTracker.router import router as router_crypto

app = FastAPI()

app.include_router(router_crypto)

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8066, reload=True)
