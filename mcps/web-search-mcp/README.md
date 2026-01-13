# Web Search MCP

提供联网搜索功能的 MCP 服务器，使用 DuckDuckGo Instant Answer API。

## 功能

- **search_web**: 在互联网上搜索信息，返回相关结果摘要
- 无需 API key，免费使用
- 支持中文搜索

## 安装

```bash
cd mcps/web-search-mcp
npm install
```

## 使用

### 启动服务器

```bash
npm start
```

### 测试

```bash
npm test
```

## 工具接口

### search_web

搜索互联网上的信息。

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| query | string | 是 | 搜索查询字符串 |
| limit | number | 否 | 返回结果最大数量（默认 5，最大 10）|

**返回示例：**

```json
{
  "query": "TypeScript",
  "count": 3,
  "results": [
    {
      "title": "TypeScript: JavaScript With Syntax For Types.",
      "url": "https://www.typescriptlang.org/",
      "snippet": "TypeScript is a strongly typed programming language that builds on JavaScript..."
    }
  ]
}
```

## Claude Code 配置

在 Claude Code 配置文件中添加：

```json
{
  "mcpServers": {
    "web-search": {
      "command": "node",
      "args": ["/absolute/path/to/mcps/web-search-mcp/server.js"]
    }
  }
}
```
