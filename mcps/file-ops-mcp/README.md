# File Operations MCP

提供基础文件操作功能的 MCP 服务器。

## 功能

- **read_file**: 读取文件内容
- **write_file**: 写入文件内容，支持自动创建目录
- **search_files**: 搜索文件，支持文件名通配符和内容搜索

## 安全特性

- 路径访问限制：只允许访问指定根目录下的文件
- 可通过 `FILE_OPS_ROOT` 环境变量配置允许的根目录
- 默认允许访问当前工作目录

## 安装

```bash
cd mcps/file-ops-mcp
pip install -r requirements.txt
```

## 使用

### 启动服务器

```bash
python server.py
```

### 测试

```bash
python test.py
```

## 工具接口

### read_file

读取文件内容。

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| path | string | 是 | 文件路径 |
| encoding | string | 否 | 文件编码（默认 utf-8）|

**返回示例：**

```json
{
  "path": "/path/to/file.txt",
  "name": "file.txt",
  "size": 1024,
  "encoding": "utf-8",
  "content": "文件内容...",
  "line_count": 42
}
```

### write_file

写入文件内容。

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| path | string | 是 | 文件路径 |
| content | string | 是 | 文件内容 |
| encoding | string | 否 | 文件编码（默认 utf-8）|
| create_dirs | boolean | 否 | 自动创建父目录（默认 false）|

**返回示例：**

```json
{
  "success": true,
  "path": "/path/to/file.txt",
  "bytes_written": 1024
}
```

### search_files

在目录中搜索文件。

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| directory | string | 否 | 搜索目录（默认当前目录）|
| pattern | string | 否 | 文件名模式，支持通配符（默认 *）|
| content_pattern | string | 否 | 文件内容模式 |
| max_results | number | 否 | 最大结果数（默认 100）|

## Claude Code 配置

```json
{
  "mcpServers": {
    "file-ops": {
      "command": "python",
      "args": ["/absolute/path/to/mcps/file-ops-mcp/server.py"],
      "env": {
        "FILE_OPS_ROOT": "/your/project/path"
      }
    }
  }
}
```
