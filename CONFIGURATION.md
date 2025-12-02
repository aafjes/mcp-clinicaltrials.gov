# Configuration Guide for ClinicalTrials.gov MCP Server

This guide provides configuration instructions for various MCP clients.

## Claude Desktop

### macOS Configuration

1. Locate your Claude Desktop config file:
   ```bash
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

2. Add the server configuration:
   ```json
   {
     "mcpServers": {
       "clinicaltrials": {
         "command": "python3",
         "args": ["/absolute/path/to/clinicaltrials_mcp_server.py"]
       }
     }
   }
   ```

3. Restart Claude Desktop

### Windows Configuration

1. Locate your Claude Desktop config file:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Add the server configuration:
   ```json
   {
     "mcpServers": {
       "clinicaltrials": {
         "command": "python",
         "args": ["C:\\path\\to\\clinicaltrials_mcp_server.py"]
       }
     }
   }
   ```

3. Restart Claude Desktop

### Using with virtual environment

If you're using a Python virtual environment:

```json
{
  "mcpServers": {
    "clinicaltrials": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/clinicaltrials_mcp_server.py"]
    }
  }
}
```

### Using installed package

If you installed the package with pip:

```json
{
  "mcpServers": {
    "clinicaltrials": {
      "command": "clinicaltrials-mcp"
    }
  }
}
```

## Cline (VS Code Extension)

1. Open VS Code settings
2. Search for "Cline: MCP Settings"
3. Edit the MCP settings JSON:

```json
{
  "mcpServers": {
    "clinicaltrials": {
      "command": "python3",
      "args": ["/absolute/path/to/clinicaltrials_mcp_server.py"]
    }
  }
}
```

## Continue.dev

Add to your Continue configuration (~/.continue/config.json):

```json
{
  "mcpServers": [
    {
      "name": "clinicaltrials",
      "command": "python3",
      "args": ["/absolute/path/to/clinicaltrials_mcp_server.py"]
    }
  ]
}
```

## Custom MCP Client (Python)

### Using stdio transport

```python
import asyncio
from mcp.client.stdio import stdio_client
from mcp.types import CallToolRequest

async def use_clinicaltrials_server():
    async with stdio_client(
        server_params={
            "command": "python3",
            "args": ["/path/to/clinicaltrials_mcp_server.py"]
        }
    ) as (read, write):
        # List available tools
        tools = await write.list_tools()
        print(f"Available tools: {[tool.name for tool in tools.tools]}")
        
        # Call a tool
        result = await write.call_tool(
            CallToolRequest(
                name="search_clinical_trials",
                arguments={
                    "query_cond": "Depression",
                    "page_size": 5
                }
            )
        )
        
        print(result.content[0].text)

asyncio.run(use_clinicaltrials_server())
```

### Using SSE transport (for web applications)

```python
from mcp.client.sse import sse_client
import httpx

async def use_clinicaltrials_via_sse():
    async with httpx.AsyncClient() as client:
        async with sse_client(
            client,
            "http://localhost:8000/sse"
        ) as (read, write):
            # Use the client
            pass
```

## Environment Variables

You can set environment variables for configuration:

```bash
# For debugging
export MCP_DEBUG=1

# For custom API timeout
export CLINICALTRIALS_TIMEOUT=60
```

## Troubleshooting

### "Command not found" error

Make sure Python is in your PATH:
```bash
which python3  # macOS/Linux
where python   # Windows
```

Update the command path to the full Python executable path.

### "Module not found" error

Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

Or use the full path to your virtual environment's Python.

### Permission denied

Make the script executable:
```bash
chmod +x clinicaltrials_mcp_server.py
```

### Server not appearing in Claude

1. Check the config file syntax (must be valid JSON)
2. Verify the file paths are absolute, not relative
3. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`

### Testing the server manually

Test the server directly:
```bash
python3 clinicaltrials_mcp_server.py
```

This should start the server in stdio mode. If it starts without errors, the server is working.

## Advanced Configuration

### Custom API Settings

Modify the server file to add custom settings:

```python
# In clinicaltrials_mcp_server.py

# Custom timeout
API_TIMEOUT = 60  # seconds

# Custom page size defaults
DEFAULT_PAGE_SIZE = 50

# Custom base URL (for testing)
API_BASE_URL = "https://clinicaltrials.gov/api/v2"
```

### Logging Configuration

Enable detailed logging:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='clinicaltrials_mcp.log'
)
```

### Rate Limiting

Add rate limiting to be respectful of the API:

```python
import asyncio
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests=100, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    async def acquire(self):
        now = datetime.now()
        self.requests = [r for r in self.requests 
                        if now - r < timedelta(seconds=self.time_window)]
        
        if len(self.requests) >= self.max_requests:
            wait_time = (self.requests[0] + 
                        timedelta(seconds=self.time_window) - 
                        now).total_seconds()
            await asyncio.sleep(wait_time)
        
        self.requests.append(now)
```

## Security Considerations

1. **API Access**: The ClinicalTrials.gov API is public and doesn't require authentication
2. **Data Privacy**: All data is publicly available on ClinicalTrials.gov
3. **Local Execution**: The server runs locally and doesn't send data to third parties
4. **Network Access**: The server only connects to clinicaltrials.gov

## Production Deployment

For production use:

1. Use a proper Python package installation
2. Implement error handling and logging
3. Add monitoring and alerting
4. Consider caching frequently accessed studies
5. Implement retry logic for transient failures
6. Use connection pooling for better performance

Example production-ready configuration:

```json
{
  "mcpServers": {
    "clinicaltrials": {
      "command": "/usr/local/bin/python3",
      "args": [
        "/opt/mcp-servers/clinicaltrials/clinicaltrials_mcp_server.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## Support

For configuration help:
- Check the logs in Claude Desktop's log directory
- Run the test script: `python3 test_server.py`
- Test manually: `python3 clinicaltrials_mcp_server.py`
- Review the README.md for general documentation
