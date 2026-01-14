# GitHub 代码分析器 - 使用指南

本指南介绍如何使用 GitHub 代码分析器来学习开源项目、理解代码实现、解决开发问题。

## 目录

- [快速开始](#快速开始)
- [命令行工具](#命令行工具)
- [使用场景](#使用场景)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)

## 快速开始

### 前置要求

- Python 3.6+
- 网络连接（访问 GitHub API）

### 安装

无需额外安装，直接使用提供的 Python 脚本：

```bash
cd /path/to/claude-playbook
export PATH=$PATH:$(pwd)/scripts
```

### 基本使用

#### 1. 获取仓库信息

```bash
python scripts/github_get_repo_info.py vitejs/vite
```

**输出示例**：
```json
{
  "name": "vite",
  "full_name": "vitejs/vite",
  "description": "Next generation frontend tooling",
  "language": "TypeScript",
  "default_branch": "main",
  "stargazers_count": 65000
}
```

#### 2. 查看目录结构

```bash
# 根目录
python scripts/github_get_repo_structure.py vitejs/vite

# 子目录
python scripts/github_get_repo_structure.py vitejs/vite src/core
```

#### 3. 读取文件内容

```bash
python scripts/github_read_file.py vitejs/vite README.md

# 指定分支和大小限制
python scripts/github_read_file.py vitejs/vite package.json main 50000
```

#### 4. 搜索代码

```bash
python scripts/github_search_code.py vitejs/vite "plugin"

# 过滤语言
python scripts/github_search_code.py vitejs/vite "hmr" main TypeScript
```

## 命令行工具

### github_get_repo_info

获取 GitHub 仓库的基本信息。

**用法**：
```bash
python scripts/github_get_repo_info.py <repo> [token]
```

**参数**：
- `repo`: 仓库标识（格式：`owner/repo`）
- `token`: GitHub PAT（可选，提高 API 限流）

**示例**：
```bash
# 基本用法
python scripts/github_get_repo_info.py vuejs/vue-router

# 使用 Token
export GITHUB_TOKEN="ghp_xxxxx"
python scripts/github_get_repo_info.py facebook/react $GITHUB_TOKEN
```

### github_get_repo_structure

获取仓库的目录树结构。

**用法**：
```bash
python scripts/github_get_repo_structure.py <repo> [path] [ref] [token]
```

**参数**：
- `repo`: 仓库标识
- `path`: 目录路径（默认：根目录）
- `ref`: 分支/tag/commit（默认：默认分支）

**示例**：
```bash
# 查看根目录
python scripts/github_get_repo_structure.py vitejs/vite

# 查看特定目录
python scripts/github_get_repo_structure.py vitejs/vite src

# 查看特定分支
python scripts/github_get_repo_structure.py vuejs/vue-router src main
```

### github_read_file

读取仓库中单个文件的内容。

**用法**：
```bash
python scripts/github_read_file.py <repo> <path> [ref] [max_size] [token]
```

**参数**：
- `repo`: 仓库标识
- `path`: 文件路径
- `ref`: 分支/tag（默认：默认分支）
- `max_size`: 最大字节数（默认：100KB）

**示例**：
```bash
# 读取 README
python scripts/github_read_file.py vitejs/vite README.md

# 读取大文件（增加限制）
python scripts/github_read_file.py vuejs/vue-router src/router.ts main 200000
```

### github_search_code

在仓库中搜索包含关键词的代码。

**用法**：
```bash
python scripts/github_search_code.py <repo> <query> [ref] [language] [token]
```

**参数**：
- `repo`: 仓库标识
- `query`: 搜索关键词
- `ref`: 限定分支
- `language`: 语言过滤

**示例**：
```bash
# 基本搜索
python scripts/github_search_code.py vitejs/vite "plugin"

# 组合搜索
python scripts/github_search_code.py vuejs/vue-router "navigation guard" main TypeScript

# 搜索函数
python scripts/github_search_code.py facebook/react "useState" main JavaScript
```

## 使用场景

### 场景 1: 学习新技术

**目标**：理解 Vite 的 HMR 实现原理

**步骤**：

1. 获取项目概览
```bash
python scripts/github_get_repo_info.py vitejs/vite
```

2. 读取文档
```bash
python scripts/github_read_file.py vitejs/vite README.md
```

3. 搜索相关代码
```bash
python scripts/github_search_code.py vitejs/vite "hmr" main TypeScript
```

4. 读取核心实现
```bash
python scripts/github_read_file.py vitejs/vite src/server/hmr.ts main
```

### 场景 2: 理解项目架构

**目标**：分析 vue-router 的路由系统

**步骤**：

1. 查看目录结构
```bash
python scripts/github_get_repo_structure.py vuejs/vue-router
```

2. 探索源码目录
```bash
python scripts/github_get_repo_structure.py vuejs/vue-router src
```

3. 识别入口文件
```bash
python scripts/github_read_file.py vuejs/vue-router src/index.ts
```

4. 分析核心模块
```bash
python scripts/github_read_file.py vuejs/vue-router src/router.ts
python scripts/github_read_file.py vuejs/vue-router src/history/createWebHistory.ts
```

### 场景 3: 解决问题参考

**目标**：参考 React 如何处理状态管理

**步骤**：

1. 搜索相关代码
```bash
python scripts/github_search_code.py facebook/react "useState" main JavaScript
```

2. 读取实现文件
```bash
# 从搜索结果获取文件路径
python scripts/github_read_file.py facebook/react packages/react/src/ReactHooks.js
```

3. 理解调用流程
```bash
# 搜索调度器
python scripts/github_search_code.py facebook/react "scheduleUpdate" main JavaScript
```

## 最佳实践

### 1. 使用 GitHub Token

创建 Token 提高限制：
1. 访问 https://github.com/settings/tokens
2. 生成新 Token（scope: `public_repo`）
3. 设置环境变量：

```bash
export GITHUB_TOKEN="ghp_xxxxx"
python scripts/github_get_repo_info.py owner/repo $GITHUB_TOKEN
```

### 2. 优化搜索查询

| 目标 | 好的查询 | 差的查询 |
|------|---------|---------|
| 类名 | "PluginSystem" | "system" |
| 函数 | "createRouter" | "create" |
| 概念 | "hot module replacement" | "replacement" |
| 组合 | "async" + "function" | "code" |

### 3. 分步骤探索大型项目

```bash
# 步骤 1: 了解项目
python scripts/github_get_repo_info.py facebook/react

# 步骤 2: 查看结构
python scripts/github_get_repo_structure.py facebook/react

# 步骤 3: 聚焦目录
python scripts/github_get_repo_structure.py facebook/react packages/react

# 步骤 4: 读取关键文件
python scripts/github_read_file.py facebook/react packages/react/src/React.js
```

### 4. 组合使用 Bash 工具

```bash
# 批量读取文件
for file in README.md package.json tsconfig.json; do
  python scripts/github_read_file.py vitejs/vite $file
done

# 保存到本地
python scripts/github_read_file.py vitejs/vite README.md > vite_readme.md
```

## 故障排除

### 常见错误

#### 1. API 速率限制

**错误**：
```json
{"error": "API rate limit exceeded or access forbidden"}
```

**解决**：
```bash
# 使用 Token 提高限制
export GITHUB_TOKEN="your_token_here"
python scripts/github_get_repo_info.py owner/repo $GITHUB_TOKEN

# 或等待 1 小时后重试
```

#### 2. 仓库不存在

**错误**：
```json
{"error": "Repository not found: invalid/repo"}
```

**解决**：
- 检查仓库名称拼写
- 确认仓库为公开仓库
- 访问 GitHub 验证：https://github.com/owner/repo

#### 3. 文件过大

**警告**：
```json
{"truncated": true, "max_size": 102400}
```

**解决**：
```bash
# 增加 max_size 参数
python scripts/github_read_file.py owner/repo large-file.json main 500000
```

#### 4. 网络超时

**错误**：
```json
{"error": "Network error: Connection timed out"}
```

**解决**：
- 检查网络连接
- 尝试使用代理
- 稍后重试

### 性能优化

#### 1. 减少文件读取

```bash
# 先搜索，定位文件
python scripts/github_search_code.py owner/repo "keyword"

# 再读取相关文件（避免读取整个目录）
python scripts/github_read_file.py owner/repo src/core/file.ts
```

#### 2. 使用并发（需脚本修改）

```python
# 在脚本中添加并发支持
import asyncio
# 实现并发请求...
```

#### 3. 缓存结果

```bash
# 保存常用信息到本地
python scripts/github_get_repo_info.py vitejs/vite > vite_info.json

# 后续直接读取
cat vite_info.json | jq '.description'
```

## 高级用法

### 与 Claude Code 集成

在 Claude Code 中使用此技能：

```
用户: 分析 vitejs/vite 的插件系统实现

Claude 会自动：
1. 调用 github_get_repo_info 获取项目信息
2. 调用 github_search_code 搜索 "plugin"
3. 调用 github_read_file 读取相关文件
4. 生成结构化的分析报告
```

### 构建自定义工具链

```bash
#!/bin/bash
# analyze_repo.sh

REPO=$1
QUERY=$2

echo "=== 仓库信息 ==="
python scripts/github_get_repo_info.py $REPO

echo "=== 搜索结果 ==="
python scripts/github_search_code.py $REPO "$QUERY"

echo "=== 目录结构 ==="
python scripts/github_get_repo_structure.py $REPO
```

使用：
```bash
chmod +x analyze_repo.sh
./analyze_repo.sh vitejs/vite "plugin"
```

## 相关资源

- [GitHub REST API 文档](https://docs.github.com/en/rest)
- [GitHub Token 创建指南](https://github.com/settings/tokens)
- [Claude Playbook 主文档](../README.md)
- [技能定义](../skills/github-code-analyzer.md)

## 反馈与贡献

如有问题或建议，请：
1. 提交 Issue
2. 创建 Pull Request
3. 查看 `CLAUDE.md` 了解贡献规范
