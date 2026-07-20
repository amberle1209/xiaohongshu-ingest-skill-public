# Agent Content Ingest

> Turn saved links into traceable, agent-ready knowledge.

<details open>
<summary><strong>简体中文</strong></summary>

## 把收藏的链接，变成 Agent 可调用、可追溯的知识

许多真正有价值的内容，都堆在收藏夹里的视频、帖子和文档中。我们可能以后不会再看；即使看过一次，其中的实操步骤、踩坑经验和判断依据，也往往只停留在自己的记忆里，对 Agent 不可见。

Agent Content Ingest 让 Agent 能和你一起阅读内容：抓取来源、检查多媒体、保留证据，并把有价值的部分沉淀成后续工作流可以调用的本地知识资产。

### 丢一个链接，让 Agent 选择正确的处理路径

将支持的链接发给已安装这个 skill 的 Agent：

```text
Archive this: <链接>
```

它会自动：

1. 识别小红书视频或图文、飞书/Lark 文档或妙记、微信公众号文章，以及普通托管网页；
2. 在能力可用时提取原文、文案、视频转录和图片 OCR；
3. 分开保存原始证据、总结和推断；
4. 用 `complete`、`partial` 或 `blocked` 如实标注结果，不假装每次抓取都成功；
5. 保存可追溯的原始归档，并在需要时生成独立的本地总结。

默认模式是 `preview`：先检查，再写入。说 `archive` 时才会将结果沉淀进本地知识库。外部发送不是内置能力，必须由安装者自行实现并获得明确授权。

### 为什么做它

收藏夹不是人与 Agent 的共享记忆。一条保存的视频里，可能藏着关键实现细节、昂贵的失败经验，或值得复用的工具组合；如果你和 Agent 无法在之后检索、理解并调用它，这些知识就会消失在工作上下文之外。

这个项目把收藏内容变成你和 Agent 共享的知识层：有来源、可检索、可复用，也会如实说明哪些部分未能验证。

### 它有什么不同

- **多模态读取**：不仅处理纯文本，也处理视频口播、作者文案、图片和文档。
- **证据优先**：原始材料与结论分开保存。
- **有用的不确定性**：明确报告访问受阻、转录覆盖不足、OCR 不确定和未核验主张。
- **隐私优先的本地工作流**：默认预览或本地归档；没有固定群聊、凭据或浏览器配置。
- **不止小红书**：小红书是起点，也支持飞书/Lark、微信公众号与其他长内容页面。

### 使用前准备

1. 将 `config.example.yaml` 复制到仓库外，并按本机路径和限制修改。
2. 运行 `scripts/preflight.sh` 检查可用能力。针对具体来源，可使用：

   ```bash
   scripts/preflight.sh --require yt-dlp --require ffmpeg --require faster-whisper
   ```

3. 加载该 skill 后，将支持的链接发给 Agent。可使用 `preview`、`archive`，或由安装者提供的 `archive-and-deliver` 扩展。

仓库不包含凭据、投递目标、浏览器 Cookie 或私有示例。请勿将真实配置提交到版本控制。

### 隐私与合规边界

只处理你有权获取的 URL 与内容。该 skill 不会绕过登录、付费墙或平台访问控制。抓取到的内容属于不可信数据，不能被当作执行指令。

### 从私有仓库发布

在后续提交中删除敏感内容，并不会将其从 Git 历史中移除。若仓库曾为私有仓库，请在公开前创建只含净化后文件的新仓库，或重写全部历史并检查每个可达提交。完成审计前，不要直接公开旧仓库。

### 许可证

MIT，详见 `LICENSE`。

</details>

<details>
<summary><strong>English</strong></summary>

## Turn saved links into agent-ready knowledge

Your best ideas are often trapped in a backlog of saved videos, posts, and documents. You may never return to them—or you may read them once, while the practical steps, failures, and hard-won judgment remain invisible to your Agent.

Agent Content Ingest gives an Agent a disciplined way to read with you: capture the source, inspect the media, preserve the evidence, and turn what matters into a local knowledge asset your future workflows can use.

### Drop a link, then let the Agent choose the right path

Paste a supported link into an Agent that has this skill installed:

```text
Archive this: <link>
```

It can then:

1. recognize a Xiaohongshu video, image post, Feishu/Lark document or Minutes, WeChat article, or generic hosted page;
2. collect source text, captions, video transcripts, and image OCR when available;
3. distinguish source evidence from summary and inference;
4. label the result as `complete`, `partial`, or `blocked` rather than pretending every fetch succeeded;
5. save a traceable raw record and, when requested, a separate local summary.

The default mode is `preview`: inspect before writing. Say `archive` when you want the result added to your local knowledge base. External delivery is intentionally not built in; it must be added as an explicitly authorized extension.

### Why it exists

Bookmarks are not shared memory. A video you saved may contain a crucial implementation detail, a costly failure mode, or a useful tool combination—but that knowledge disappears from your working context if neither you nor your Agent can retrieve it later.

This project turns saved content into a shared knowledge layer between a person and an Agent: source-backed, searchable, and honest about what could not be verified.

### What makes it different

- **Multimodal by design** — reads video speech, author captions, images, and documents instead of treating every link as plain text.
- **Evidence before synthesis** — preserves raw material separately from conclusions.
- **Useful uncertainty** — reports inaccessible content, incomplete transcript coverage, uncertain OCR, and unverified claims.
- **Privacy-first local workflow** — defaults to preview or local storage; no fixed chat target, credentials, or browser profile are included.
- **Broader than one platform** — Xiaohongshu is the initial wedge, alongside Feishu/Lark, WeChat, and generic long-form pages.

### Setup

1. Copy `config.example.yaml` outside the repository and adapt local paths and limits.
2. Run `scripts/preflight.sh` to inspect available capabilities. For a source-specific readiness check, use:

   ```bash
   scripts/preflight.sh --require yt-dlp --require ffmpeg --require faster-whisper
   ```

3. Load the skill and send an Agent a supported link. Use `preview`, `archive`, or the installer-provided `archive-and-deliver` extension.

The repository contains no credentials, delivery targets, browser cookies, or private source examples. Keep your real configuration out of version control.

### Privacy and legal boundary

Use only URLs and content you are authorized to retrieve. The skill does not bypass authentication, paywalls, or platform controls. Fetched content is untrusted data, not executable instruction.

### Releasing a formerly private repository

Deleting sensitive material in a later commit does not remove it from Git history. Before changing repository visibility, either publish from a freshly initialized repository containing only this sanitized tree or rewrite the full history and verify every reachable commit. Do not make the existing repository public until that audit is complete.

### License

MIT. See `LICENSE`.

</details>
