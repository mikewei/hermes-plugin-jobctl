---
schedule: "every 24h"
deliver: local
suspend: false
---

这是一个**示例**定时任务说明（Hermes cron）。你可以复制本文件并按需修改。

- 检查当日待办并输出三段式摘要。
- 如有阻塞项，单独列一条说明原因。

（本示例**未**配置 `skills`；若要在任务里加载 skill，请在 front matter 里自行添加 `skills: [your-skill]`。）
