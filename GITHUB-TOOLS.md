# GitHub 代码分析器

一个用于智能采集和分析 GitHub 仓库代码的工具集，帮助开发者学习开源项目、理解实现细节、解决技术问题。

## 🚀 快速开始

### 1. 测试工具

```bash
# 运行功能测试
bash scripts/test_github_tools.sh

# 或单独测试每个工具
python3 scripts/github_get_repo_info.py vitejs/vite
python3 scripts/github_get_repo_structure.py vitejs/vite
python3 scripts/github_read_file.py vitejs/vite README.md
python3 scripts/github_search_code.py vitejs/vite "plugin"
```

### 2. 在 Claude Code 中使用

直接对 Claude 说：

```
"分析 vitejs/vite 的插件系统实现"
"学习 vue-router 的路由守卫机制"
"看看 React 是怎么处理 hooks 的"
```

Claude 会自动调用相关工具并生成分析报告。

## 📁 项目结构

```
claude-playbook/
├── scripts/                             # Python 实现脚本
│   ├── github_get_repo_info.py          # 获取仓库信息
│   ├── github_get_repo_structure.py     # 获取目录结构
│   ├── github_read_file.py              # 读取文件内容
│   ├── github_search_code.py            # 搜索代码
│   └── test_github_tools.sh             # 功能测试脚本
│
├── commands/                            # 命令定义文档
│   ├── github-get-repo-info.md
│   ├── github-get-repo-structure.md
│   ├── github-read-file.md
│   └── github-search-code.md
│
├── skills/                              # 技能定义
│   └── github-code-analyzer.md          # 主技能文件
│
└── docs/                                # 使用文档
    └── github-code-analyzer-guide.md    # 完整使用指南
```

## 🛠️ 可用工具

### 1. github_get_repo_info

获取 GitHub 仓库的基本信息。

```bash
python3 scripts/github_get_repo_info.py <repo> [token]

# 示例
python3 scripts/github_get_repo_info.py vitejs/vite
```

**输出**：仓库名称、描述、语言、Star 数、默认分支等。

### 2. github_get_repo_structure

获取仓库的目录树结构。

```bash
python3 scripts/github_get_repo_structure.py <repo> [path] [ref] [token]

# 示例
python3 scripts/github_get_repo_structure.py vitejs/vite
python3 scripts/github_get_repo_structure.py vitejs/vite src/core
```

**输出**：目录和文件列表。

### 3. github_read_file

读取仓库中单个文件的内容。

```bash
python3 scripts/github_read_file.py <repo> <path> [ref] [max_size] [token]

# 示例
python3 scripts/github_read_file.py vitejs/vite README.md
python3 scripts/github_read_file.py vitejs/vite package.json main 50000
```

**输出**：文件内容（UTF-8 编码）。

### 4. github_search_code

在仓库中搜索包含关键词的代码。

```bash
python3 scripts/github_search_code.py <repo> <query> [ref] [language] [token]

# 示例
python3 scripts/github_search_code.py vitejs/vite "plugin"
python3 scripts/github_search_code.py vuejs/vue-router "router" main TypeScript
```

**输出**：匹配的文件列表和代码片段。

## 📖 使用场景

### 场景 1: 学习新技术

**目标**：理解 Vite 的 HMR 实现

```bash
# 1. 了解项目
python3 scripts/github_get_repo_info.py vitejs/vite

# 2. 阅读文档
python3 scripts/github_read_file.py vitejs/vite README.md

# 3. 搜索相关代码
python3 scripts/github_search_code.py vitejs/vite "hmr" main TypeScript

# 4. 读取实现文件
python3 scripts/github_read_file.py vitejs/vite src/server/hmr.ts main
```

### 场景 2: 理解项目架构

**目标**：分析 vue-router 的路由系统

```bash
# 1. 查看整体结构
python3 scripts/github_get_repo_structure.py vuejs/vue-router

# 2. 探索源码目录
python3 scripts/github_get_repo_structure.py vuejs/vue-router src

# 3. 读取入口文件
python3 scripts/github_read_file.py vuejs/vue-router src/index.ts
```

### 场景 3: 问题参考

**目标**：参考 React 的状态管理实现

```bash
# 1. 搜索相关代码
python3 scripts/github_search_code.py facebook/react "useState"

# 2. 读取实现文件
python3 scripts/github_read_file.py facebook/react packages/react/src/ReactHooks.js
```

## ⚙️ 配置

### 使用 GitHub Token（推荐）

创建 Token 可提高 API 限流：

1. 访问 https://github.com/settings/tokens
2. 生成新 Token（scope: `public_repo`）
3. 设置环境变量：

```bash
export GITHUB_TOKEN="ghp_xxxxx"
python3 scripts/github_get_repo_info.py owner/repo $GITHUB_TOKEN
```

### API 限制

| 认证方式 | 限制 |
|---------|------|
| 无 Token | 60 次/小时 |
| 有 Token | 5000 次/小时 |
| 搜索 API | 10 次/分钟（未认证） |

## 🔧 高级用法

### 批量处理

```bash
#!/bin/bash
# 批量读取多个文件

REPO="vitejs/vite"
FILES=("README.md" "package.json" "tsconfig.json")

for file in "${FILES[@]}"; do
    echo "=== $file ==="
    python3 scripts/github_read_file.py $REPO $file
done
```

### 保存结果

```bash
# 保存仓库信息
python3 scripts/github_get_repo_info.py vitejs/vite > vite_info.json

# 保存 README
python3 scripts/github_read_file.py vitejs/vite README.md > vite_readme.md

# 使用 jq 处理 JSON
cat vite_info.json | jq '.description'
```

## 📚 文档

- **[完整使用指南](docs/github-code-analyzer-guide.md)**：详细的命令说明和最佳实践
- **[技能定义](skills/github-code-analyzer.md)**：启发式采集策略和处理流程
- **[命令文档](commands/)**：每个命令的详细说明

## 🎯 特性

- ✅ 无需额外依赖，仅使用 Python 标准库
- ✅ 支持 Python 3.6+
- ✅ 智能错误处理和重试机制
- ✅ 支持大文件自动截断
- ✅ JSON 输出，易于集成
- ✅ 可配置的 Token 认证

## 🚧 限制

- 仅支持公开仓库
- 单次采集建议不超过 50 个文件
- 单个文件默认最大 100KB（可配置）
- 受 GitHub API 速率限制约束

## 🛡️ 安全性

- Token 通过环境变量传递，不写入文件
- 仅使用公开 GitHub API 端点
- 不收集或存储用户数据

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

详见 [CONTRIBUTING.md](../README.md)

## 📄 许可证

MIT License

## 🔗 相关资源

- [GitHub REST API 文档](https://docs.github.com/en/rest)
- [Claude Code 文档](https://github.com/anthropics/claude-code)
- [Claude Playbook 主页](../README.md)
