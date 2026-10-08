import asyncio

import httpx


async def main() -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
        print(f"Status Code: {response.status_code}")
        print(f"JSON Response: {response.json()}")


if __name__ == "__main__":
    asyncio.run(main())