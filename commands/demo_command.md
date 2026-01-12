# Command 示例: demo_command

描述：简单的命令示例，展示如何在 `commands/` 中加入可执行脚本并说明用法。

示例脚本：`hello_command.sh`

```bash
#!/usr/bin/env bash
echo "Hello from demo command!"
```

使用：为脚本添加可执行权限并运行：

```bash
chmod +x commands/hello_command.sh
./commands/hello_command.sh
```

你可以将脚本封装为更复杂的工具（接收参数、输出 JSON、与 skills 交互）。
