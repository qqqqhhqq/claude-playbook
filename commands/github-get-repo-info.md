---
name: github_get_repo_info
description: 获取 GitHub 仓库的基本信息（描述、语言、星标数等）
category: github
version: 1.0.0
---

## 功能说明

获取 GitHub 仓库的元数据信息，包括：
- 仓库名称和描述
- 主要编程语言
- 默认分支
- Star 和 Fork 数量
- 项目主题标签
- 创建和更新时间
- 开源协议

## 输入参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| repo | string | ✅ | 仓库标识，格式 "owner/repo" | "vitejs/vite" |
| token | string | ❌ | GitHub Personal Access Token | "ghp_xxxxx" |

## 输出格式

```json
{
  "name": "vite",
  "full_name": "vitejs/vite",
  "description": "Next generation frontend tooling",
  "language": "TypeScript",
  "default_branch": "main",
  "stargazers_count": 65000,
  "forks_count": 5200,
  "open_issues_count": 340,
  "homepage": "https://vitejs.dev",
  "topics": ["frontend-tooling", "bundler", "dx"],
  "created_at": "2020-04-12T15:33:00Z",
  "updated_at": "2024-01-10T08:22:00Z",
  "size": 45020,
  "license": "MIT"
}
```

## 使用方式

### 命令行调用

```bash
# 基本用法
python scripts/github_get_repo_info.py vitejs/vite

# 使用 Token（提高 API 限流）
python scripts/github_get_repo_info.py vitejs/vite ghp_xxxxx
```

### 错误处理

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 404 | 仓库不存在 | 检查仓库名称拼写 |
| 403 | API 限流或无权限 | 等待重试或提供 Token |

## 注意事项

- 仅支持公开仓库
- 无 Token 时限制 60 次/小时
- 有 Token 时限制 5000 次/小时
- 建议在需要频繁调用时使用 Token
