# MCP Practice: Weather Tool with FastMCP

A hands-on learning project that demonstrates the **Model Context Protocol (MCP)** using a real three-component architecture: a FastAPI weather API, an MCP server that wraps it, and an MCP client that drives it.

---

## What Was Built

```
MCP_PRACTICE/
├── api/              # FastAPI weather REST API (mock data)
├── mcp-server/       # FastMCP server exposing weather tools over stdio
└── mcp-client/       # FastMCP client that calls those tools programmatically
```

### Component Roles

| Component | Tech | Purpose |
|---|---|---|
| `api/` | FastAPI + Uvicorn | Serves weather data over HTTP on `localhost:8000` |
| `mcp-server/` | FastMCP + httpx | Wraps the API as MCP tools over stdio transport |
| `mcp-client/` | FastMCP Client | Connects to the server, lists tools, calls them |

---

## Architecture

```
mcp-client (Python)
    │
    │  stdio (subprocess)
    ▼
mcp-server (FastMCP)
    │
    │  HTTP (httpx)
    ▼
api (FastAPI)  ←── returns mock weather JSON
```

The client spawns the server as a subprocess and communicates via **stdio transport** — the standard MCP pattern for local tool servers.

---

## Requirements

### Python
Python 3.10+ recommended (project was built with Python 3.11).

### Per-component dependencies

**`api/requirements.txt`**
```
fastapi
uvicorn[standard]
```

**`mcp-server/requirements.txt`**
```
fastmcp
httpx
```

**`mcp-client/requirements.txt`**
```
fastmcp
```

---

## Setup & Running

### 1. Clone the repo

```bash
git clone <repo-url>
cd MCP_PRACTICE
```

### 2. Create virtual environments (recommended — one per component)

```bash
# API
cd api
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# MCP Server
cd ../mcp-server
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# MCP Client
cd ../mcp-client
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> Or use a single shared venv at the root — install all three `requirements.txt` files into it.

### 3. Start the FastAPI weather API

```bash
cd api
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

### 4. Run the MCP client (it launches the server automatically)

Open a second terminal:

```bash
cd mcp-client
python client.py
```

The client starts the MCP server as a subprocess via stdio, then:
- Lists all available tools
- Calls `get_city_temperature` for London, New York, and Tokyo
- Calls `get_city_forecast` for each city
- Tests error handling with an unsupported city (Paris)

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/weather/temperature/{city}` | Current temperature and condition |
| GET | `/weather/forecast/{city}` | 5-day forecast |

Supported cities: **London**, **New York**, **Tokyo**  
Any other city returns a `404` with the list of available cities.

### Example response — `/weather/temperature/london`

```json
{
  "city": "London",
  "temperature_celsius": 12.5,
  "condition": "Cloudy"
}
```

---

## MCP Tools

The server exposes two tools that any MCP-compatible client (or LLM agent) can call:

### `get_city_temperature`
- **Input:** `city` (string)  e.g. `"London"`
- **Output:** current temperature in Celsius and weather condition

### `get_city_forecast`
- **Input:** `city` (string)
- **Output:** 5-day forecast array with high/low temps and condition per day

---

## Key Learnings

### What is MCP?
**Model Context Protocol** is an open standard that lets AI models (like Claude) call external tools in a structured, typed way. Think of it as a contract between an AI client and a tool server.

### FastMCP
`fastmcp` is a Python library that makes building MCP servers and clients simple:
- Decorate any async function with `@mcp.tool()` to expose it as a tool
- Tools get automatic JSON schema generation from Python type hints and docstrings
- The server runs over **stdio** (subprocess) or **SSE** (HTTP streaming)

### stdio Transport
The client spawns the server as a subprocess (`python server.py`) and communicates via stdin/stdout. This is the simplest and most common MCP transport for local tools — no ports to open, no auth to configure.

### Tool Discovery
MCP clients can call `list_tools()` at runtime to discover what a server offers — name, description, and input schema — without any hardcoded knowledge. This is what allows LLMs to dynamically use tools.

### Separation of Concerns
- The **API** owns the data and business logic
- The **MCP server** is purely an adapter it converts HTTP responses into MCP tool responses
- The **MCP client** is the consumer it could be swapped for Claude Desktop, an LLM agent, or another tool runner

### Error Handling
HTTP `4xx` errors from the API (raised as `HTTPException`) propagate through `httpx` and surface as exceptions in the MCP tool call the client catches them cleanly.

---

## Project Structure Deep Dive

```
api/main.py          — FastAPI app, mock WEATHER_DATA dict, two GET endpoints
mcp-server/server.py — FastMCP instance, two @mcp.tool() functions, stdio runner
mcp-client/client.py — StdioTransport, async Client context manager, tool calls
```

---

## Next Steps / Ideas

- Add real weather data using OpenWeatherMap or WeatherAPI
- Expose the MCP server over SSE/HTTP so Claude Desktop can connect to it
- Add more tools: humidity, wind speed, UV index
- Wire the MCP server into a Claude agent using the Anthropic API
- Add unit tests for the FastAPI endpoints
