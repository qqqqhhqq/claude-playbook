# Agent 示例: demo_agent

描述：一个简单的 agent 配置示例，展示如何声明输入、处理流程与示例交互。

示例配置（YAML）：

```yaml
name: demo-agent
description: 示例代理，接收 user_message 并返回回复
inputs:
  - name: user_message
    type: string
    required: true
handler: |
  # 伪代码处理逻辑：读取 user_message 并返回固定格式回复
  if user_message:
    return {"reply": f"已收到: {user_message}"}

examples:
  - input:
      user_message: "你好，代理！"
    output:
      reply: "已收到: 你好，代理！"
```

使用说明：将此配置作为参考，适配您实际的运行时（Python、Node、或框架提供的 agent 运行器）。
