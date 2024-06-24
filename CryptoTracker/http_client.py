from httpx import AsyncClient
# import asyncio


class HTTPClient:
    def __init__(self, base_url: str, api_key: str):
        self._session = AsyncClient(
            base_url=base_url,
            headers={
                'X-CMC_PRO_API_KEY': api_key,
            },
        )


class CMCHTTPClient(HTTPClient):
    async def get_listings(self):
        response = await self._session.get(
            "/v1/cryptocurrency/listings/latest"
        )
        return response.json()["data"]

    async def get_currency(self, currency_id: int):
        response = await self._session.get(
            "/v2/cryptocurrency/quotes/latest",
            params={"id": currency_id}
        )
        return response.json()["data"][str(currency_id)]
