# Traveller MCP Server

## Running the Server

```bash
python main.py
```

## Registering Tools

1. Create a new Python file in the `tools` directory, e.g., `tools/tool_name.py`.
2. In your tool file, import the `mcp` instance from `main.py`:

```python
from main import mcp

@mcp.tool()
def my_tool(...):
    ...
```

3. The server will automatically discover and register all tools in the `tools` directory when started.
