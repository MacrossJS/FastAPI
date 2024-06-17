import uvicorn
from fastapi import FastAPI
from http_client import CMCHTTPClient
from config import settings

app = FastAPI()

cmc_client = CMCHTTPClient(
    base_url="https://pro-api.coinmarketcap.com",
    api_key=settings.CMC_API_KEY
)


@app.get("/cryptocurrencies")
async def get_cryptocurrencies():
    return await cmc_client.get_listings()


@app.get("/cryptocurrencies/{currency_id}")
async def get_cryptocurrency(currency_id: int):
    return await cmc_client.get_currency(currency_id)

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8066, reload=True)
