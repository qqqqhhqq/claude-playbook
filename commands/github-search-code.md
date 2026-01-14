---
name: github_search_code
description: 在 GitHub 仓库中搜索匹配关键词的代码
category: github
version: 1.0.0
---

## 功能说明

在指定 GitHub 仓库中搜索包含关键词的文件和代码片段，返回匹配结果列表。

## 输入参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| repo | string | ✅ | 仓库标识，格式 "owner/repo" | "vitejs/vite" |
| query | string | ✅ | 搜索关键词 | "plugin system" |
| ref | string | ❌ | 限定分支 | "main" |
| language | string | ❌ | 语言过滤 | "TypeScript" |
| token | string | ❌ | GitHub Personal Access Token | "ghp_xxxxx" |

## 输出格式

```json
{
  "total_count": 23,
  "count": 10,
  "query": "plugin system",
  "results": [
    {
      "name": "plugin.ts",
      "path": "src/core/plugin.ts",
      "sha": "abc123...",
      "html_url": "https://github.com/vitejs/vite/blob/main/src/core/plugin.ts",
      "score": 123.45,
      "matches": [
        {
          "line_number": 42,
          "fragment": "export class PluginSystem {"
        }
      ]
    }
  ]
}
```

## 使用方式

### 命令行调用

```bash
# 基本搜索
python scripts/github_search_code.py vitejs/vite "plugin"

# 限定分支
python scripts/github_search_code.py vuejs/vue-router "router" main

# 过滤语言
python scripts/github_search_code.py vitejs/vite "hmr" main TypeScript

# 复杂关键词
python scripts/github_search_code.py vuejs/vue-router "navigation guard"
```

### 搜索技巧

| 目标 | 查询示例 |
|------|----------|
| 类名 | "PluginSystem" |
| 函数名 | "createRouter" |
| 关键字 | "export class", "async function" |
| 组合搜索 | "plugin" + "system" |

## 错误处理

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 403 | API 限流 | 等待重试或提供 Token |
| 422 | 搜索参数无效 | 检查 query 格式 |
| - | 无匹配结果 | total_count 为 0 |

## 注意事项

- 搜索 API 有速率限制（未认证 10 次/分钟）
- 每次最多返回 10 个结果
- `text_matches` 需要设置请求头，可能不总是返回
- 建议使用具体关键词提高匹配准确度
- 搜索结果按相关性排序
