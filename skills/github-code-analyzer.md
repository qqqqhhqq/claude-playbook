---
name: github_code_analyzer
description: 智能分析 GitHub 仓库代码，帮助理解项目结构、学习开源实现、参考解决方案
version: 1.0.0
category: code-analysis
author: claude-playbook
---

## 技能概述

本技能用于智能采集和分析 GitHub 仓库代码，为开发、调试、学习提供上下文支持。

**核心能力**：
- 📊 项目概览：理解项目目标、技术栈、使用方式
- 🔍 关键词定位：快速找到相关代码文件
- 🏗️ 架构分析：理解项目结构和模块划分
- 💡 实现参考：学习优秀开源项目的实现方式

## 意图检测

当用户表达以下需求时，触发此技能：

### 1. 分析类意图
- "分析 [repo] 的..."
- "看看 [repo] 如何实现..."
- "理解 [repo] 的架构设计"
- "研究 [repo] 的 [feature]"

### 2. 学习类意图
- "学习 [repo] 的代码"
- "研究 [repo] 的实现"
- "[repo] 是怎么做的"

### 3. 参考类意图
- "参考 [repo] 的实现来解决..."
- "看看 [repo] 是怎么处理 [issue] 的"
- "类似 [repo] 的做法"

## 输入解析

### 解析规则

```yaml
仓库识别:
  - 支持完整 URL: "https://github.com/vitejs/vite"
  - 支持短格式: "vitejs/vite"
  - 支持别名: "vite" (需上下文)

版本引用:
  - 分支: "@main", "@develop"
  - Tag: "@v4.0.0", "@2.3.0"
  - Commit: "@abc123def"

问题关键词:
  - 从自然语言中提取核心词汇
  - 中英文混合识别
  - 支持技术术语和业务术语
```

### 解析示例

```
输入: "分析 vitejs/vite@v4 的插件系统如何实现"

解析结果:
  repo: "vitejs/vite"
  ref: "v4"
  query: "插件系统如何实现"
  keywords: ["插件", "plugin", "system", "实现", "implement"]
  intent: "学习理解"
```

## 启发式采集策略

### 阶段 1: 项目概览 (Token 预算: ~500)

**目标**: 了解项目基本信息

```yaml
动作序列:
  1. 调用 github_get_repo_info
     - 获取: 名称、描述、语言、默认分支

  2. 读取项目文档
     - 优先级: README.md > README_zh.md > README.en.md
     - 调用: github_read_file(repo, "README.md", ref)

  3. 读取配置文件（根据语言判断）
     - JavaScript/TypeScript: package.json
     - Python: setup.py, pyproject.toml
     - Rust: Cargo.toml
     - Go: go.mod
     - Java: pom.xml
     - 调用: github_read_file(repo, config_file, ref)

输出结构:
  {
    "项目名称": "...",
    "项目描述": "...",
    "技术栈": ["TypeScript", "Rollup", "..."],
    "默认分支": "main",
    "Star 数": 65000,
    "README 摘要": "...",
    "依赖项": ["react", "react-dom", "..."]
  }
```

### 阶段 2: 关键词匹配 (Token 预算: ~3000)

**目标**: 直接定位用户关心的代码

```yaml
触发条件: 用户提供了明确的关键词

动作序列:
  1. 构建搜索查询
     - 关键词: ["插件", "plugin"]
     - 查询: "plugin" + "repo:vitejs/vite" + "language:TypeScript"

  2. 调用 github_search_code
     - 参数: repo, query, ref, language
     - 限制: 前 5 个结果

  3. 读取匹配文件
     - 对每个搜索结果，调用 github_read_file
     - 限制单文件: 50KB（代码文件）

  4. 提取相关片段
     - 定位关键词所在行
     - 提取上下文代码段

输出结构:
  {
    "搜索关键词": ["plugin"],
    "匹配文件数": 5,
    "文件列表": [
      {
        "path": "src/core/plugin.ts",
        "相关代码": "export class PluginSystem {...}",
        "匹配位置": [42, 156, 203]
      }
    ]
  }
```

### 阶段 3: 结构探索 (Token 预算: ~4500)

**目标**: 理解项目整体架构

```yaml
动作序列:
  1. 获取根目录结构
     - 调用: github_get_repo_structure(repo, "/", ref)

  2. 识别主源码目录
     - 常见模式: src/, lib/, app/, core/, packages/
     - 排除: test/, tests/, spec/, __tests__/
     - 排除: dist/, build/, out/, .next/

  3. 递归获取主目录结构
     - 对每个主目录，调用 github_get_repo_structure
     - 深度限制: 2-3 层

  4. 读取入口文件和核心文件
     - src/index.ts, src/main.rs, lib/core.py
     - package.json 中的 main/entry 字段
     - 调用: github_read_file

输出结构:
  {
    "目录结构": {
      "src/": ["core/", "plugin/", "server/"],
      "tests/": ["unit/", "integration/"],
      "docs/": ["guide/", "api/"]
    },
    "入口文件": "src/index.ts",
    "核心模块": [
      "src/core/plugin.ts",
      "src/server/index.ts"
    ],
    "架构概览": "..."
  }
```

### Token 预算管理

```yaml
总预算: 8000 tokens (约 6KB 文本)

分配策略:
  阶段 1 (概览): 500 tokens
  阶段 2 (关键词): 3000 tokens
  阶段 3 (结构): 4500 tokens
  预留: 1000 tokens

超出预算时的处理:
  - 停止继续采集
  - 提示用户: "已采集 X 个文件，Token 使用接近上限"
  - 建议: "可以指定更具体的目录聚焦分析"

估算方式:
  - 英文: 1 token ≈ 4 字符
  - 中文: 1 token ≈ 1.5 字符
  - 代码: 1 token ≈ 3-4 字符（含缩进）
```

## 处理流程

### 主流程图

```
用户输入
    ↓
[步骤 1] 解析输入
    - 提取 repo, ref, query
    - 识别关键词
    ↓
[步骤 2] 项目概览
    - 获取仓库信息
    - 读取 README 和配置
    ↓
[步骤 3] 关键词搜索
    - 搜索代码
    - 读取匹配文件
    ↓
[步骤 4] 结构探索
    - 获取目录树
    - 识别主目录
    - 读取核心文件
    ↓
[步骤 5] 上下文组装
    - 整合采集数据
    - 估算 Token 使用
    ↓
[步骤 6] 分析输出
    - 生成结构化报告
    - 回答用户问题
```

### 详细执行步骤

#### Step 1: 输入解析

```python
# 伪代码
def parse_input(user_input: str) -> dict:
    # 提取仓库
    repo_match = re.search(r'([\w-]+/[\w-]+)', user_input)
    repo = repo_match.group(1) if repo_match else None

    # 提取版本引用
    ref_match = re.search(r'@([\w\d.]+)', user_input)
    ref = ref_match.group(1) if ref_match else None

    # 提取查询意图
    query = user_input
    if repo:
        query = query.replace(repo, '')
    if ref:
        query = query.replace(f'@{ref}', '')
    query = query.strip()

    # 提取关键词
    keywords = extract_keywords(query)  # 中英文分词

    return {
        'repo': repo,
        'ref': ref,
        'query': query,
        'keywords': keywords
    }
```

#### Step 2-4: 采集执行

```python
# 阶段 1: 项目概览
info = github_get_repo_info(parsed['repo'])
ref = parsed['ref'] or info['default_branch']

readme = github_read_file(
    repo=parsed['repo'],
    path='README.md',
    ref=ref
)

config = detect_and_read_config(
    repo=parsed['repo'],
    language=info['language'],
    ref=ref
)

# 阶段 2: 关键词搜索
if parsed['keywords']:
    results = github_search_code(
        repo=parsed['repo'],
        query=parsed['keywords'][0],  # 主要关键词
        ref=ref,
        language=info['language']
    )

    for item in results['results'][:5]:
        file_content = github_read_file(
            repo=parsed['repo'],
            path=item['path'],
            ref=ref,
            max_size=50000
        )
        context[item['path']] = file_content

# 阶段 3: 结构探索
structure = github_get_repo_structure(
    repo=parsed['repo'],
    path='/',
    ref=ref
)

src_dirs = identify_source_dirs(structure)

for dir in src_dirs:
    if token_budget_exceeded():
        break
    dir_structure = github_get_repo_structure(
        repo=parsed['repo'],
        path=dir,
        ref=ref
    )
    entry_files = get_entry_files(dir_structure)
    for file in entry_files:
        content = github_read_file(
            repo=parsed['repo'],
            path=file,
            ref=ref
        )
        context[file] = content
```

#### Step 5-6: 输出生成

```markdown
# 仓库分析报告

## 项目概览
**仓库**: [vitejs/vite](https://github.com/vitejs/vite)
**描述**: Next generation frontend tooling
**技术栈**: TypeScript, Rollup, esbuild
**Star 数**: 65k
**默认分支**: main

### 项目简介
[从 README 提取的项目介绍]

### 核心依赖
- rollup: ^4.0.0
- esbuild: ^0.19.0
- postcss: ^8.4.0

## 架构分析
### 目录结构
```
src/
├── core/          # 核心逻辑
│   ├── plugin.ts  # 插件系统
│   └── config.ts  # 配置处理
├── server/        # 开发服务器
└── client/        # 客户端运行时
```

### 入口文件
主入口: `src/node/cli.ts`

核心模块:
- `src/core/plugin.ts`: 插件系统实现
- `src/server/index.ts`: 开发服务器
- `src/node/config.ts`: 配置解析

## 核心实现分析

### 插件系统
[基于关键词搜索和代码阅读的详细分析]

**关键代码片段**:
\`\`\`typescript
export class PluginSystem {
  // [从采集的代码中提取]
}
\`\`\`

**实现原理**:
1. [步骤 1]
2. [步骤 2]

### [其他相关模块...]

## 参考资料
- 仓库地址: https://github.com/vitejs/vite
- 文档: https://vitejs.dev
- 相关文件: [列出分析的关键文件]
```

## 使用示例

### 示例 1: 功能学习

```
用户输入:
"学习 Vite 的 HMR 热更新实现原理"

执行流程:
1. 解析: repo="vitejs/vite", query="HMR 热更新实现原理"
2. 关键词: ["HMR", "hot", "module", "replacement"]
3. 采集:
   - README.md → 了解项目
   - 搜索 "hmr" → 找到 plugin-hmr.ts, hmr.ts
   - 读取 server/hmr.ts
4. 输出: HMR 原理分析 + WebSocket 通信流程 + 代码示例
```

### 示例 2: 架构理解

```
用户输入:
"分析 vue-router 的路由系统架构"

执行流程:
1. 解析: repo="vuejs/vue-router", query="路由系统架构"
2. 采集:
   - README.md
   - 搜索 "router", "route", "history"
   - 读取 src/router.ts, src/history/*.ts
3. 输出:
   - 架构图（文字描述）
   - 核心类关系
   - 路由跳转流程
```

### 示例 3: 问题参考

```
用户输入:
"看看 React 是怎么处理 useEffect 的"

执行流程:
1. 解析: repo="facebook/react", query="useEffect 处理"
2. 采集:
   - 搜索 "useEffect"
   - 读取 packages/react-reconciler/src/ReactFiberHooks.js
3. 输出:
   - Hook 调度机制
   - 依赖比较逻辑
   - 副作用执行时机
```

## 边界条件与限制

### 功能限制

- ✅ 仅支持公开仓库
- ✅ 单次采集不超过 50 个文件
- ✅ 单个文件最大 100KB（可配置）
- ✅ Token 预算约 8000 tokens

### API 限流

| 认证方式 | 限制 |
|---------|------|
| 无 Token | 60 次/小时 |
| 有 Token | 5000 次/小时 |
| 搜索 API | 10 次/分钟（未认证） |

### 不支持的场景

- ❌ 私有仓库
- ❌ 企业 GitHub 账号
- ❌ 二进制文件分析（图片、视频等）
- ❌ 超大仓库（>1GB）

## 错误处理

| 错误场景 | 检测方式 | 处理策略 |
|---------|---------|---------|
| 仓库不存在 | HTTP 404 | 提示检查仓库名称，建议搜索 GitHub |
| 分支/tag 无效 | HTTP 404 | 获取可用分支列表供选择 |
| API 速率超限 | HTTP 403 | 等待后重试，显示剩余时间 |
| 文件过大 | size > max_size | 提供头部摘要，询问是否深入 |
| 网络超时 | URLError | 重试 3 次，指数退避 |
| 搜索无结果 | total_count = 0 | 建议更换关键词 |

## 优化建议

### 后续增强方向

1. **缓存机制**
   - 缓存仓库结构和常用文件
   - 使用文件系统或内存数据库
   - 设置过期时间（如 1 小时）

2. **并发采集**
   - 使用 async/await 并行读取
   - 提高采集速度 3-5 倍

3. **智能摘要**
   - 对大文件生成摘要而非截断
   - 使用 LLM 提取关键信息
   - 保留函数签名和类型定义

4. **依赖分析**
   - 解析 import/require 关系
   - 生成依赖图谱
   - 识别循环依赖

5. **多轮对话**
   - 支持基于前次采集的追问
   - 维护会话上下文
   - 增量采集新文件

### 配置化参数

```yaml
# 可在技能中调整的参数
token_budget: 8000           # Token 预算
max_files: 50                # 最大文件数
max_file_size: 100000        # 100KB
search_results_limit: 5      # 搜索结果数量
structure_depth: 3           # 目录结构深度
cache_ttl: 3600             # 缓存过期时间（秒）
concurrent_requests: 3       # 并发请求数
```

## 相关命令

本技能依赖以下命令：

- `github_get_repo_info`: 获取仓库信息
- `github_get_repo_structure`: 获取目录结构
- `github_read_file`: 读取文件内容
- `github_search_code`: 搜索代码

详见 `commands/` 目录中的文档。

## 版本历史

- **v1.0.0** (2024-01): 初始版本
  - 支持基础的代码采集和分析
  - 实现启发式采集策略
  - Token 预算管理
