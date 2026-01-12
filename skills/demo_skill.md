# Skill 示例: demo_skill

描述：一个独立技能的清单与示例输入/输出，用于说明技能的契约（接口）。

技能清单（JSON）：

```json
{
  "name": "echo-skill",
  "description": "将输入原样返回，附加元信息",
  "inputs": {
    "text": {"type": "string", "required": true}
  },
  "outputs": {
    "echo": {"type": "string"},
    "length": {"type": "integer"}
  }
}
```

示例：

Input:

```json
{ "text": "测试技能" }
```

Output:

```json
{ "echo": "测试技能", "length": 4 }
```

实现提示：实现时保持清晰的输入校验和错误返回结构（例如 HTTP 400 + 错误消息）。
