---
name: github_get_repo_structure
description: 获取 GitHub 仓库的目录树结构
category: github
version: 1.0.0
---

## 功能说明

递归获取 GitHub 仓库中指定目录下的文件和子目录列表。

## 输入参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| repo | string | ✅ | 仓库标识，格式 "owner/repo" | "vitejs/vite" |
| path | string | ❌ | 目录路径，空字符串或"/"表示根目录 | "src/core" |
| ref | string | ❌ | 分支/tag/commit SHA，默认为默认分支 | "main", "v4.0.0" |
| token | string | ❌ | GitHub Personal Access Token | "ghp_xxxxx" |

## 输出格式

### 根目录示例

```json
{
  "type": "dir",
  "path": "/",
  "total_count": 15,
  "entries": [
    {
      "name": "src",
      "type": "dir",
      "path": "src",
      "size": 0
    },
    {
      "name": "README.md",
      "type": "file",
      "path": "README.md",
      "size": 2048
    },
    {
      "name": "package.json",
      "type": "file",
      "path": "package.json",
      "size": 1024
    }
  ]
}
```

### 单个文件示例

```json
{
  "type": "file",
  "name": "README.md",
  "path": "README.md",
  "size": 2048,
  "sha": "abc123..."
}
```

## 使用方式

### 命令行调用

```bash
# 获取根目录结构
python scripts/github_get_repo_structure.py vitejs/vite

# 获取子目录结构
python scripts/github_get_repo_structure.py vitejs/vite src/core

# 指定分支
python scripts/github_get_repo_structure.py vitejs/vite /src main
```

### 错误处理

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 404 | 目录或文件不存在 | 检查路径是否正确 |
| 403 | API 限流 | 等待重试或提供 Token |

## 注意事项

- 路径参数不需要前导 `/`，但脚本会兼容处理
- 对于大型仓库，建议逐层获取目录结构
- 返回结果未递归展开子目录内容
