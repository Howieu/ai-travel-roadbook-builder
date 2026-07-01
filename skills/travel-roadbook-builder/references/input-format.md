# Input Format

Ask for the minimum reliable input:

```text
目的地：
日期：
节奏：轻松 / 标准 / 紧凑
兴趣：
必去：
避开：

攻略资料：
粘贴小红书、网页攻略、Notion、飞书或聊天记录正文。

攻略链接：
每行一个公开网页、小红书、博客、地图或攻略链接。普通网页会通过 Agent Reach / Jina Reader 读取；小红书直读需要 Agent Reach 之外还存在可用小红书后端。没有后端时，先按 `url-research.md` 安装/启用 OpenCLI 或 xiaohongshu-mcp；不安装时再粘贴正文或上传截图。

酒店：
酒店名、地址、入住日期、退房日期、可否寄存行李。也可以上传酒店预订截图。

交通：
航班 / 高铁 / 火车 / 巴士 / 渡轮，包含出发地、到达地、出发时间、到达时间。也可以上传机票、高铁票、火车票、巴士票或渡轮票截图。
```

When URLs are provided, read `url-research.md`. When screenshots are provided, read `screenshot-bookings.md`.

If ordinary web content behind a link is unavailable, ask the user to paste the text or provide screenshots. For Xiaohongshu links, offer backend setup before asking for pasted text. Keep unreadable links as low-confidence source records.

Good pasted materials usually contain:

- place names;
- restaurant or cafe names;
- neighborhoods;
- opening hours;
- reservation notes;
- transport tips;
- avoid notes;
- estimated visit duration.

Good screenshot materials usually show:

- hotel name and address;
- check-in and check-out dates;
- departure and arrival stations or airports;
- departure and arrival times;
- terminal, platform, gate, or station notes;
- baggage, boarding, or security buffer reminders.

Do not store passenger names, full booking references, QR codes, payment details, passport/ID numbers, phone numbers, or email addresses in the generated roadbook.
