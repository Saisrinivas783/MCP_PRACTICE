import asyncio
import json
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

SERVER_PATH = "../mcp-server/server.py"
CITIES = ["London", "New York", "Tokyo"]


def print_section(title: str):
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print(f"{'=' * 50}")


def pretty(data) -> str:
    # call_tool returns a list of content objects; extract the text payload
    if isinstance(data, list):
        for item in data:
            if hasattr(item, "text"):
                return json.dumps(json.loads(item.text), indent=2)
    return str(data)


async def main():
    transport = StdioTransport(command="python", args=[SERVER_PATH])

    async with Client(transport) as client:

        # ── List available tools ──────────────────────────────────────
        print_section("Available MCP Tools")
        tools = await client.list_tools()
        for tool in tools:
            print(f"  • {tool.name}: {tool.description}")

        # ── Test: get_city_temperature for all cities ─────────────────
        print_section("Current Temperature — All Cities")
        for city in CITIES:
            result = await client.call_tool("get_city_temperature", {"city": city})
            print(f"\n[{city}]")
            print(pretty(result))

        # ── Test: get_city_forecast for each city ─────────────────────
        print_section("5-Day Forecast — All Cities")
        for city in CITIES:
            result = await client.call_tool("get_city_forecast", {"city": city})
            print(f"\n[{city}]")
            print(pretty(result))

        # ── Test: invalid city (error handling) ───────────────────────
        print_section("Error Handling — Invalid City")
        try:
            await client.call_tool("get_city_temperature", {"city": "Paris"})
        except Exception as e:
            print(f"  Expected error caught: {e}")


if __name__ == "__main__":
    asyncio.run(main())
