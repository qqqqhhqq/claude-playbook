# claude-playbook

一个用于集中管理 Claude（及其相关技能、命令、提示和工作流）配置的仓库。旨在标准化使用模式、提高协作效率并复用可版本控制的能力模块。

## 目录结构
- `agents/`：代理实现与编排示例。
- `commands/`：可复用的命令与工具脚本。
- `skills/`：独立技能实现（意图、处理逻辑、示例）。
- `output-styles/`：标准化输出样式与模板。
- 其他文档文件：`CLAUDE.md`、`README.md` 等。

## 快速开始
1. 克隆仓库：

```bash
git clone <仓库地址>
cd claude-playbook
```

2. 浏览目录并查看示例：

```bash
ls -la
```

3. 根据需要编辑或复用 `agents/`、`skills/` 或 `commands/` 中的示例。

## 使用建议
- 按模块抽离技能以利于测试与复用。
- 为每个命令或技能添加 README 或示例输入输出。
- 在变更重要接口时更新 `CLAUDE.md`（项目的规范文档）。

## 贡献
欢迎通过 Pull Request 贡献：请添加清晰的描述、测试用例和示例用法。

## 许可证
遵循仓库根目录中的 `LICENSE` 文件。

---

如果你希望我为某个子目录添加更详细的 README（例如 `agents/` 或 `skills/`），告诉我想要包含的示例或模板，我可以继续添加。
