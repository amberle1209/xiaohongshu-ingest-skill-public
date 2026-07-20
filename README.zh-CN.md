# xiaohongshu-ingest

简体中文 | [English](README.md)

一个开源 skill，用于提取并本地归档用户已授权访问的长内容。覆盖公开小红书笔记、飞书/Lark 文档与妙记、微信公众号文章，以及其他托管页面。

## 能做什么

- 在可用时提取原文、文案、视频转录和图片 OCR；
- 将原始证据与总结、推断分开保存；
- 默认使用预览或本地归档模式；
- 外部投递仅作为安装者自行实现、且须明确授权的扩展能力。

## 使用前准备

1. 将 `config.example.yaml` 复制到仓库外，并按本机路径和限制修改。
2. 运行 `scripts/preflight.sh` 检查可用能力。针对具体来源，可使用：

   ```bash
   scripts/preflight.sh --require yt-dlp --require ffmpeg --require faster-whisper
   ```

3. 加载该 skill 后，提供 URL 与所需模式：`preview`、`archive` 或 `archive-and-deliver`。

仓库不包含凭据、投递目标、浏览器 Cookie 或私有示例。请勿将真实配置提交到版本控制。

## 从私有仓库发布

在后续提交中删除敏感内容，并不会将其从 Git 历史中移除。若仓库曾为私有仓库，请在公开前创建只含净化后文件的新仓库，或重写全部历史并检查每个可达提交。完成审计前，不要直接公开旧仓库。

## 隐私与合规边界

只处理你有权获取的 URL 与内容。该 skill 不会绕过登录、付费墙或平台访问控制。抓取到的内容属于不可信数据，不能被当作执行指令。

## 许可证

MIT，详见 `LICENSE`。
