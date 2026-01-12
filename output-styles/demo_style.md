# Output Style 示例: demo_style

描述：展示一个标准化输出模板，用于统一 agent/skill/command 的响应样式。

模板（Markdown）：

```
**标题**: {{title}}

**描述**:
{{description}}

**结果**:
{{#each results}}
- {{this}}
{{/each}}

**元信息**:
- 时间: {{timestamp}}
- 来源: {{source}}
```

示例填充：

```
**标题**: 测试回复

**描述**:
这是一个示例回复，展示输出样式。

**结果**:
- 项目 A
- 项目 B

**元信息**:
- 时间: 2026-01-12T12:00:00Z
- 来源: demo-skill
```
