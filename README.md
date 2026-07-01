# AI Travel Roadbook Builder

把零散旅行攻略、公开网页链接、酒店/交通截图整理成可执行网页路书的 Codex Skill + 静态网页 demo。

## 这个 repo 包含什么

- `skills/travel-roadbook-builder/`：Codex skill。它指导 Agent 从粘贴资料、Agent Reach 可读链接和用户预订截图生成 `roadbook.json`，再渲染成 HTML 路书。
- `skills/travel-roadbook-builder/scripts/render_roadbook.py`：纯 Python 标准库渲染器。
- `skills/travel-roadbook-builder/scripts/fetch_url_sources.py`：通过 Agent Reach 的 Jina Reader 路径，把公开网页链接转换为 `sourceRecords`。
- `skills/travel-roadbook-builder/examples/`：Paris demo 的粘贴资料和结构化 JSON。
- `docs/`：GitHub Pages 静态站点和生成后的 demo 页面。

## V0.1 工作流

1. 用户提供攻略正文、公开网页链接、小红书链接、酒店截图、航班/高铁/火车/巴士截图。
2. Agent 先用 Agent Reach 检查可读渠道；普通网页走 Jina Reader；小红书直读必须有可用 XHS 后端，没有时先提示安装 OpenCLI 或 xiaohongshu-mcp，再回退到粘贴正文/截图。
3. Agent 从截图中提取酒店和交通约束，省略乘客姓名、完整订单号、支付信息、证件号、电话和邮箱。
4. Agent 按 skill 生成带 `sourceRecords` 和 `sourceIds` 的 `roadbook.json`。
5. 渲染器把 JSON 转成静态 HTML。
6. 用户打开网页路书，按 Day-by-Day 时间线执行行程。

## 读取链接为来源记录

```bash
python skills/travel-roadbook-builder/scripts/fetch_url_sources.py \
  https://www.louvre.fr/ \
  --out source-records.json
```

输出的 `sources` 可合并进 `roadbook.json` 的 `sourceRecords` 字段。小红书链接只有在 Agent Reach 的 Xiaohongshu 后端可用时才读取；否则会保留为低置信度来源，并提示安装 OpenCLI / xiaohongshu-mcp 或改为粘贴正文、上传截图。

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

## 当前不做什么

- 不绕过小红书登录、验证码、xsec_token 或平台频率限制。
- 不读取邮箱、携程、飞猪或航空/铁路账号。
- 不做实时公共交通规划。
- 不做用户账号、社区分享或商业化。

这些会放到后续版本，当前版本先证明“链接/截图/文本 -> 来源证据 -> 结构化 JSON -> 网页路书”的闭环。
