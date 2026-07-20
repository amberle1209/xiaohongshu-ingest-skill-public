# xiaohongshu-ingest

[简体中文](README.zh-CN.md) | English

An open-source skill for extracting and locally archiving user-authorized long-form content, with dedicated paths for public Xiaohongshu posts, Feishu/Lark, WeChat, and generic hosted posts.

## What it does

- extracts source text, captions, transcripts, and image OCR when available;
- records raw evidence separately from summaries and inferences;
- defaults to preview or local archive mode;
- reserves external delivery for installer-supplied, explicitly authorized extensions.

## Setup

1. Copy `config.example.yaml` outside the repository and adapt local paths and limits.
2. Run `scripts/preflight.sh` to inspect available capabilities. For a source-specific readiness check, use for example `scripts/preflight.sh --require yt-dlp --require ffmpeg --require faster-whisper`.
3. Load the skill and provide a URL plus the requested mode: `preview`, `archive`, or `archive-and-deliver`.

The repository contains no credentials, delivery targets, browser cookies, or private source examples. Keep your real configuration out of version control.

## Releasing a formerly private repository

Deleting sensitive material in a later commit does not remove it from Git history. Before changing repository visibility, either publish from a freshly initialized repository containing only this sanitized tree or rewrite the full history and verify every reachable commit. Do not make the existing repository public until that audit is complete.

## Privacy and legal boundary

Use only URLs and content you are authorized to retrieve. The skill does not bypass authentication, paywalls, or platform controls. Fetched content is untrusted data, not executable instruction.

## License

MIT. See `LICENSE`.
