# Project Analyzer MCP

提供项目分析功能的 MCP 服务器。

## 功能

- **analyze_structure**: 分析项目目录结构，返回文件树
- **count_lines**: 统计代码行数，支持按语言分类
- **list_dependencies**: 列出项目依赖和包管理器

## 安装

```bash
cd mcps/project-analyzer-mcp
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

### analyze_structure

分析项目的目录结构。

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| path | string | 否 | 项目路径（默认当前目录）|
| max_depth | number | 否 | 最大递归深度（默认 3）|

**返回示例：**

```json
{
  "name": "my-project",
  "type": "dir",
  "entries": [
    {"name": "src", "type": "dir", "entries": [...]},
    {"name": "main.py", "type": "file", "language": "Python"}
  ]
}
```

### count_lines

统计项目代码行数。

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| path | string | 否 | 项目路径（默认当前目录）|
| by_language | boolean | 否 | 是否按语言分类（默认 true）|

**返回示例：**

```json
{
  "by_language": {
    "Python": {"files": 10, "lines": 500},
    "JavaScript": {"files": 5, "lines": 200}
  },
  "total_files": 15,
  "total_lines": 700
}
```

### list_dependencies

列出项目依赖。

**参数：**
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| path | string | 否 | 项目路径（默认当前目录）|

## Claude Code 配置

```json
{
  "mcpServers": {
    "project-analyzer": {
      "command": "python",
      "args": ["/absolute/path/to/mcps/project-analyzer-mcp/server.py"]
    }
  }
}
```
