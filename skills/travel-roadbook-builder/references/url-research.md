# URL Research

Use the installed `agent-reach` skill whenever the user provides travel URLs, public guide links, Xiaohongshu links, blog posts, map pages, or article links.

## Backend Check

Run this before URL collection:

```bash
agent-reach doctor --json
```

Record the relevant backend status in your working notes. If a platform backend is unavailable, keep the URL as an unread or user-provided source and follow the platform gate below.

Current routing rules:

- Ordinary webpages: use Agent Reach web routing through Jina Reader.
- GitHub reference repos: use Agent Reach GitHub routing through `gh`.
- Xiaohongshu: use the Agent Reach Xiaohongshu backend only when `xiaohongshu.active_backend` is non-null.
- If Xiaohongshu has no active backend, do not continue as if direct reading is possible. Offer setup first; fall back to pasted text or screenshots only if the user declines setup.

## Ordinary Webpages

Read public pages through Jina Reader:

```bash
curl -s "https://r.jina.ai/https://example.com/article"
```

For batch extraction, use:

```bash
python skills/travel-roadbook-builder/scripts/fetch_url_sources.py \
  https://example.com/article \
  --out source-records.json
```

The output should be merged into `roadbook.json` as `sourceRecords`.

## Xiaohongshu Links

When Agent Reach reports an active Xiaohongshu backend, follow its backend-specific commands:

- OpenCLI: `opencli xiaohongshu search "query" -f yaml`, then read notes using the full result URL.
- xiaohongshu-mcp: search first, then pass both `feed_id` and `xsec_token` to note detail calls.
- xhs-cli: use only when already available; prefer full URLs from search results.

When the user wants Xiaohongshu links to be read directly, treat an inactive backend as a setup gate:

```text
我现在有 Agent Reach，但没有可用的小红书后端，所以不能直接读取小红书链接。

方案 A（推荐，桌面）：安装 OpenCLI 后端
1. 运行：agent-reach install --channels opencli
2. 打开 Chrome，登录小红书网页版
3. 重新运行：agent-reach doctor --json
4. 看到 xiaohongshu.active_backend 不为空后，我再读取链接

方案 B（服务器/无桌面）：配置 xiaohongshu-mcp
https://github.com/xpzouying/xiaohongshu-mcp

方案 C（不安装）：直接粘贴笔记正文或发截图，我继续生成路书
```

Do not describe this as "install Agent Reach" when `agent-reach doctor` already runs. The missing piece is the Xiaohongshu backend.

Rules:

- Do not bypass login, captcha, platform rate limits, or xsec_token requirements.
- Do not ask the user for passwords, cookies, SMS codes, or captcha answers.
- Do not read a bare note ID when the platform requires a full URL or token.
- Space manual reads apart if the backend warns about rate limits.

If the backend is unavailable and the user declines setup, ask for one of:

- note text pasted directly;
- screenshots of the note;
- a short user summary of why they saved the note.

## Source Record Shape

For every readable source, create a record like:

```json
{
  "id": "web-001",
  "type": "guide",
  "platform": "web",
  "url": "https://example.com/article",
  "readerUrl": "https://r.jina.ai/https://example.com/article",
  "title": "Paris First-Time Guide",
  "author": null,
  "capturedAt": "2026-07-01T12:00:00Z",
  "excerpt": "Short evidence excerpt used for itinerary planning.",
  "accessStatus": "read",
  "confidence": "medium"
}
```

For sources that cannot be read:

```json
{
  "id": "xhs-001",
  "type": "guide",
  "platform": "xhs",
  "url": "https://www.xiaohongshu.com/explore/...",
  "title": null,
  "capturedAt": "2026-07-01T12:00:00Z",
  "excerpt": "",
  "accessStatus": "unreadable",
  "confidence": "low"
}
```

For unavailable Xiaohongshu links, the `excerpt` should include the setup gate in one sentence, for example:

```text
Xiaohongshu direct reading requires Agent Reach plus an active Xiaohongshu backend. Run `agent-reach install --channels opencli`, log into Xiaohongshu in Chrome, rerun doctor, or paste the note text/screenshots.
```

## Borrowed Logic From Reference Skills

Adopt these patterns:

- From `SPUERSAIYAN/xhs-travel-planner`: keep stable `sourceIds`, capture platform, URL, title, author, query, engagement fields when visible, and separate `confirmed`, `candidate`, `avoid`, and `assumption` claims.
- From `Panniantong/Agent-Reach`: use platform-specific backends and never invent a scraping path.
- From `Ab4ndon/one-click-travel-skill`: keep source links separate from rendered map and booking buttons so the page can omit unavailable links cleanly.

## Use In Roadbook Generation

- Add source records to top-level `sourceRecords`.
- Add `sourceIds` to lodging, transport, and stop items whenever possible.
- Use `confidence: high` only for official pages, user booking screenshots, or details explicitly provided by the user.
- Use `confidence: medium` for readable guide pages and user-pasted guides.
- Use `confidence: low` for unreadable links, inferred duration, or ambiguous place details.
- If sources conflict, add a warning rather than silently choosing one.
