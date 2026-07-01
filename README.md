# AI Travel Roadbook Builder

把零散旅行攻略、酒店和交通信息整理成可执行网页路书的 Codex Skill + 静态网页 demo。

## 这个 repo 包含什么

- `skills/travel-roadbook-builder/`：Codex skill。它指导 Agent 从粘贴资料生成 `roadbook.json`，再渲染成 HTML 路书。
- `skills/travel-roadbook-builder/scripts/render_roadbook.py`：纯 Python 标准库渲染器。
- `skills/travel-roadbook-builder/examples/`：Paris demo 的粘贴资料和结构化 JSON。
- `docs/`：GitHub Pages 静态站点和生成后的 demo 页面。

## V0 工作流

1. 用户粘贴攻略正文、酒店信息、航班/高铁/火车/巴士信息。
2. Agent 按 skill 生成 `roadbook.json`。
3. 渲染器把 JSON 转成静态 HTML。
4. 用户打开网页路书，按 Day-by-Day 时间线执行行程。

## 本地生成 demo

```bash
python skills/travel-roadbook-builder/scripts/render_roadbook.py \
  skills/travel-roadbook-builder/examples/paris-roadbook.json \
  --out docs/generated/paris-demo.html \
  --css ../assets/roadbook.css
```

本地预览：

```bash
python -m http.server 8008 --directory docs
```

打开 `http://localhost:8008/`。

## V0 不做什么

- 不自动抓取小红书全文。
- 不读取邮箱、携程、飞猪或航空/铁路账号。
- 不做实时公共交通规划。
- 不做用户账号、社区分享或商业化。

这些会放到后续版本，V0 先证明“粘贴资料 -> 结构化 JSON -> 网页路书”的闭环。
