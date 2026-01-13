# MCP Servers

本目录包含 Model Context Protocol (MCP) 服务器示例，可被 Claude Code 调用。

## 概述

MCP 是一个开放协议，用于在应用和 LLM 之间提供上下文。每个 MCP 服务器提供一组工具，Claude 可以通过调用这些工具来扩展其能力。

## 可用的 MCP 服务器

| 服务器 | 语言 | 功能描述 |
|--------|------|----------|
| [web-search-mcp](./web-search-mcp/) | Node.js | 联网搜索，使用 DuckDuckGo API |
| [project-analyzer-mcp](./project-analyzer-mcp/) | Python | 项目分析：目录结构、代码行数、依赖列表 |
| [file-ops-mcp](./file-ops-mcp/) | Python | 文件操作：读写文件、搜索文件 |

## 快速开始

### 1. 安装依赖

```bash
# Node.js MCP (web-search-mcp)
cd mcps/web-search-mcp && npm install

# Python MCP (project-analyzer-mcp, file-ops-mcp)
pip install -r requirements.txt  # 在各自的目录中运行
```

### 2. 配置 Claude Code

找到 Claude Code 的配置文件：

- **Linux**: `~/.config/claude-code/config.json`
- **macOS**: `~/Library/Application Support/Claude Code/config.json`
- **Windows**: `%APPDATA%\Claude Code\config.json`

添加以下配置（替换路径为实际路径）：

```json
{
  "mcpServers": {
    "web-search": {
      "command": "node",
      "args": ["/absolute/path/to/claude-playbook/mcps/web-search-mcp/server.js"]
    },
    "project-analyzer": {
      "command": "python3",
      "args": ["/absolute/path/to/claude-playbook/mcps/project-analyzer-mcp/server.py"]
    },
    "file-ops": {
      "command": "python3",
      "args": ["/absolute/path/to/claude-playbook/mcps/file-ops-mcp/server.py"],
      "env": {
        "FILE_OPS_ROOT": "/your/project/path"
      }
    }
  }
}
```

### 3. 重启 Claude Code

配置完成后，重启 Claude Code 使更改生效。

### 4. 使用 MCP 工具

在 Claude Code 中，你可以直接调用 MCP 提供的工具。例如：

```
请搜索 "TypeScript 最新版本"
分析当前项目的目录结构
搜索项目中包含 "TODO" 的文件
```

## 测试

每个 MCP 服务器都包含测试文件：

```bash
# web-search-mcp
cd mcps/web-search-mcp && npm test

# project-analyzer-mcp
cd mcps/project-analyzer-mcp && python test.py

# file-ops-mcp
cd mcps/file-ops-mcp && python test.py
```

## 开发新的 MCP 服务器

### 目录结构

```
my-mcp/
├── server.py (或 server.js)    # MCP 服务器实现
├── package.json / requirements.txt
├── test.py (或 test.js)        # 测试文件
└── README.md                   # 文档
```

### Python MCP 模板

```python
#!/usr/bin/env python3
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("my-mcp")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="my_tool",
            description="工具描述",
            inputSchema={
                "type": "object",
                "properties": {
                    "param": {"type": "string", "description": "参数描述"}
                },
                "required": ["param"]
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "my_tool":
        result = do_something(arguments["param"])
        return [TextContent(type="text", text=json.dumps(result))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Node.js MCP 模板

```javascript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server({ name: 'my-mcp', version: '1.0.0' }, {
  capabilities: { tools: {} },
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: 'my_tool',
    description: '工具描述',
    inputSchema: {
      type: 'object',
      properties: {
        param: { type: 'string', description: '参数描述' }
      },
      required: ['param']
    }
  }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  if (name === 'my_tool') {
    const result = doSomething(args.param);
    return { content: [{ type: 'text', text: JSON.stringify(result) }] };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

## 参考资源

- [MCP 协议规范](https://modelcontextprotocol.io)
- [Claude Code 文档](https://github.com/anthropics/claude-code)
- [MCP SDK Python](https://github.com/modelcontextprotocol/python-sdk)
- [MCP SDK TypeScript](https://github.com/modelcontextprotocol/typescript-sdk)
