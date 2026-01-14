---
name: github_read_file
description: 读取 GitHub 仓库中单个文件的完整内容
category: github
version: 1.0.0
---

## 功能说明

获取 GitHub 仓库中指定文件的原始内容，支持大文件自动截断。

## 输入参数

| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|--------|------|------|------|--------|
| repo | string | ✅ | 仓库标识，格式 "owner/repo" | - |
| path | string | ✅ | 文件路径 | - |
| ref | string | ❌ | 分支/tag/commit SHA | 默认分支 |
| max_size | number | ❌ | 最大读取字节数 | 102400 (100KB) |
| token | string | ❌ | GitHub Personal Access Token | - |

## 输出格式

### 正常文件

```json
{
  "path": "src/core/plugin.ts",
  "name": "plugin.ts",
  "content": "export class PluginSystem {\n...",
  "size": 5420,
  "sha": "abc123...",
  "encoding": "utf-8",
  "truncated": false
}
```

### 截断文件（超过 max_size）

```json
{
  "path": "dist/bundle.js",
  "name": "bundle.js",
  "content": "import {...",
  "size": 250000,
  "sha": "def456...",
  "encoding": "utf-8",
  "truncated": true,
  "max_size": 102400
}
```

## 使用方式

### 命令行调用

```bash
# 读取文件（使用默认 100KB 限制）
python scripts/github_read_file.py vitejs/vite README.md

# 指定分支
python scripts/github_read_file.py vitejs/vite package.json main

# 自定义大小限制
python scripts/github_read_file.py vitejs/vite src/core/plugin.ts main 50000

# 读取较大文件
python scripts/github_read_file.py vuejs/vue-router src/router.ts main 200000
```

### 错误处理

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 404 | 文件不存在 | 检查文件路径 |
| 403 | API 限流或无权限 | 等待重试或提供 Token |
| - | 路径指向目录而非文件 | 检查 path 参数 |

## 注意事项

- 文件内容自动从 base64 解码为 UTF-8
- 超过 `max_size` 的文件会被截断
- `truncated=true` 时表示文件内容不完整
- 建议根据需求调整 `max_size` 参数
- 二进制文件解码可能失败，会显示替换字符
