import httpx
from fastmcp import FastMCP

API_BASE_URL = "http://localhost:8000"

mcp = FastMCP(name="Weather MCP Server")


@mcp.tool()
async def get_city_temperature(city: str) -> dict:
    """Get the current temperature and weather condition for a given city.

    Args:
        city: Name of the city (e.g. London, New York, Tokyo)
    """
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        response = await client.get(f"/weather/temperature/{city}")
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def get_city_forecast(city: str) -> dict:
    """Get the 5-day weather forecast for a given city.

    Args:
        city: Name of the city (e.g. London, New York, Tokyo)
    """
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        response = await client.get(f"/weather/forecast/{city}")
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    mcp.run(transport="stdio")
