#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote_plus


def text(value: object, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def esc(value: object, default: str = "") -> str:
    return html.escape(text(value, default), quote=True)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "roadbook"


def map_links(stop: dict) -> list[tuple[str, str]]:
    queries = stop.get("mapQueries") or {}
    name = text(stop.get("name"))
    amap = text(queries.get("amap"), name)
    google = text(queries.get("google"), name)
    apple = text(queries.get("apple"), google or name)
    return [
        ("高德", f"https://uri.amap.com/search?keyword={quote_plus(amap)}"),
        ("Google Maps", f"https://www.google.com/maps/search/?api=1&query={quote_plus(google)}"),
        ("Apple Maps", f"https://maps.apple.com/?q={quote_plus(apple)}"),
    ]


def all_stops(data: dict) -> list[dict]:
    stops: list[dict] = []
    for day in data.get("days", []):
        if isinstance(day, dict):
            stops.extend(stop for stop in day.get("stops", []) if isinstance(stop, dict))
    return stops


def first_day_id(data: dict) -> str:
    days = data.get("days", [])
    if not days:
        return "itinerary"
    day = days[0]
    return slugify(text(day.get("date")) + "-" + text(day.get("title"))) if isinstance(day, dict) else "itinerary"


def trip_dates(trip: dict) -> str:
    start = text(trip.get("startDate"))
    end = text(trip.get("endDate"))
    return f"{start} - {end}" if start or end else "Flexible dates"


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    trip = data.get("trip")
    if not isinstance(trip, dict):
        return ["missing trip object"]
    for field in ("title", "destination"):
        if not trip.get(field):
            errors.append(f"missing trip.{field}")
    days = data.get("days")
    if not isinstance(days, list) or not days:
        errors.append("missing days")
        return errors
    for day_index, day in enumerate(days, start=1):
        if not isinstance(day, dict):
            errors.append(f"days[{day_index}] is not an object")
            continue
        if not day.get("date"):
            errors.append(f"days[{day_index}] missing date")
        stops = day.get("stops")
        if not isinstance(stops, list) or not stops:
            errors.append(f"days[{day_index}] missing stops")
            continue
        for stop_index, stop in enumerate(stops, start=1):
            if not isinstance(stop, dict):
                errors.append(f"days[{day_index}].stops[{stop_index}] is not an object")
            elif not stop.get("name"):
                errors.append(f"days[{day_index}].stops[{stop_index}] missing name")
    return errors


def source_records(data: dict) -> list[dict]:
    records = data.get("sourceRecords")
    if records is None:
        records = data.get("sources")
    if not isinstance(records, list):
        return []
    return [record for record in records if isinstance(record, dict)]


def render_list(items: list[dict], kind: str) -> str:
    if not items:
        return ""
    cards = []
    for item in items:
        if kind == "lodging":
            title = esc(item.get("name"), "住宿")
            meta = " / ".join(filter(None, [text(item.get("checkIn")), text(item.get("checkOut"))]))
            body = esc(item.get("address"))
        else:
            title = esc(item.get("type"), "交通")
            meta = " -> ".join(filter(None, [text(item.get("from")), text(item.get("to"))]))
            body = " / ".join(filter(None, [text(item.get("departAt")), text(item.get("arriveAt"))]))
        notes = esc(item.get("notes"))
        cards.append(
            f'<article class="info-card"><h3>{title}</h3><p class="muted">{esc(meta)}</p>'
            f'<p>{body}</p>{f"<p>{notes}</p>" if notes else ""}</article>'
        )
    heading = "住宿" if kind == "lodging" else "交通"
    return f'<section class="info-section"><h2>{heading}</h2><div class="info-grid">{"".join(cards)}</div></section>'


def render_sources(data: dict) -> str:
    records = source_records(data)
    if not records:
        return ""
    cards = []
    for record in records:
        title = esc(record.get("title") or record.get("url") or record.get("id"), "来源")
        platform = esc(record.get("platform"), "source")
        access = esc(record.get("accessStatus"), "unknown")
        confidence = esc(record.get("confidence"), "unknown")
        excerpt = esc(record.get("excerpt"))
        url = esc(record.get("url"))
        source_id = esc(record.get("id"))
        link = f'<a href="{url}" target="_blank" rel="noopener">打开来源</a>' if url else ""
        cards.append(
            '<article class="source-card">'
            f"<h3>{title}</h3>"
            f'<p class="muted">{source_id} · {platform} · {access} · {confidence}</p>'
            f"{f'<p>{excerpt}</p>' if excerpt else ''}"
            f"{link}"
            "</article>"
        )
    return f'<section class="info-section source-section"><h2>资料来源</h2><div class="info-grid">{"".join(cards)}</div></section>'


def render_hero_actions(data: dict) -> str:
    stops = all_stops(data)
    start_link = f'<a class="button primary" href="#{esc(first_day_id(data))}">开始行程</a>'
    if not stops:
        return f'<div class="hero-actions">{start_link}</div>'
    maps = map_links(stops[0])
    map_link = f'<a class="button ghost" href="{esc(maps[1][1])}" target="_blank" rel="noopener">打开第一站地图</a>'
    return f'<div class="hero-actions">{start_link}{map_link}</div>'


def render_metrics(data: dict) -> str:
    trip = data["trip"]
    stops = all_stops(data)
    sources = source_records(data)
    metrics = [
        (esc(trip.get("destination"), "目的地"), "目的地"),
        (f"{len(data.get('days', []))} days", "行程天数"),
        (f"{len(stops)} stops", "路线节点"),
        (f"{len(sources)} sources", "资料证据"),
    ]
    return "".join(f"<div><b>{value}</b><span>{label}</span></div>" for value, label in metrics)


def render_product_intro(data: dict) -> str:
    trip = data["trip"]
    warnings_count = len(data.get("warnings", []))
    return f"""
    <section class="product-intro" id="overview">
      <div>
        <p class="eyebrow">Trip workspace</p>
        <h2>今天只看下一步，不翻长文档</h2>
        <p>这份路书把 {esc(trip.get("destination"))} 的攻略、预订和风险提醒压成一张执行面板：下一站、地图、时间缓冲和来源证据都在同一页。</p>
      </div>
      <div class="status-strip">
        <span>{len(data.get("lodging", []))} 住宿</span>
        <span>{len(data.get("transport", []))} 交通</span>
        <span>{warnings_count} 提醒</span>
      </div>
    </section>
    """


def render_stop(stop: dict) -> str:
    links = "".join(
        f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'
        for label, url in map_links(stop)
    )
    extra_links = ""
    for link in stop.get("links") or []:
        label = esc(link.get("label"), "Link")
        url = esc(link.get("url"))
        if url:
            extra_links += f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'
    deadline = esc(stop.get("deadline"))
    fallback = esc(stop.get("fallback"))
    source = esc(stop.get("source"))
    confidence = esc(stop.get("confidence"))
    duration = stop.get("durationMinutes")
    duration_html = f'<span>{int(duration)} min</span>' if isinstance(duration, int) else ""
    deadline_html = f'\n        <p class="deadline">最晚/提醒：{deadline}</p>' if deadline else ""
    fallback_html = f'\n        <p class="fallback">备选：{fallback}</p>' if fallback else ""
    source_html = f'\n        <p class="source">来源：{source} · 置信度：{confidence}</p>' if source or confidence else ""
    must = '<span class="must">必去</span>' if stop.get("mustGo") else ""
    return f"""
    <article class="stop">
      <div class="time">{esc(stop.get("time"), "flex")}</div>
      <div class="stop-body">
        <div class="stop-title">
          <h3>{esc(stop.get("name"))}</h3>
          <div class="badges">{must}<span>{esc(stop.get("type"), "stop")}</span>{duration_html}</div>
        </div>
        <p>{esc(stop.get("description"))}</p>{deadline_html}{fallback_html}
        <div class="stop-links">{links}{extra_links}</div>{source_html}
      </div>
    </article>
    """.strip()


def render(data: dict, css_path: str) -> str:
    trip = data["trip"]
    interests = ", ".join(text(item) for item in trip.get("interests", []))
    day_nav = "".join(
        f'<a href="#{slugify(text(day.get("date")) + "-" + text(day.get("title")))}">{esc(day.get("date"))}</a>'
        for day in data.get("days", [])
    )
    days_html = ""
    for day in data.get("days", []):
        day_id = slugify(text(day.get("date")) + "-" + text(day.get("title")))
        stops = "".join(render_stop(stop) for stop in day.get("stops", []))
        days_html += f"""
        <section class="day-card" id="{esc(day_id)}">
          <div class="day-head">
            <p>{esc(day.get("date"))}</p>
            <h2>{esc(day.get("title"), "Day")}</h2>
            <span>{esc(day.get("summary"))}</span>
          </div>
          <div class="timeline">{stops}</div>
        </section>
        """
    days_html = days_html.strip()
    warnings = "".join(f"<li>{esc(item)}</li>" for item in data.get("warnings", []))
    warning_section = f'<section class="warnings"><h2>出发前确认</h2><ul>{warnings}</ul></section>' if warnings else ""
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(trip.get("title"))}</title>
  <link rel="stylesheet" href="{esc(css_path)}">
</head>
<body>
  <nav class="topnav product-nav">
    <a class="brand" href="../index.html">Roadbook</a>
    <div class="nav-links"><a href="#overview">总览</a>{day_nav}<a href="#sources">来源</a></div>
  </nav>
  <header class="hero product-hero">
    <div class="hero-copy">
      <p class="eyebrow">AI Travel Roadbook</p>
      <h1>{esc(trip.get("title"))}</h1>
      <p class="hero-subtitle">{esc(trip.get("destination"))} · {esc(trip_dates(trip))} · {esc(trip.get("pace"), "standard")}</p>
      <p>{esc(interests)}</p>
      {render_hero_actions(data)}
    </div>
    <div class="hero-metrics">{render_metrics(data)}</div>
  </header>
  <main class="layout product-layout">
    <aside class="side-panel">
      <div class="summary command-center">{render_metrics(data)}</div>
      {render_list(data.get("lodging", []), "lodging")}
      {render_list(data.get("transport", []), "transport")}
      <div id="sources">{render_sources(data)}</div>
      {warning_section}
    </aside>
    <section class="days">{render_product_intro(data)}{days_html}</section>
  </main>
  <footer class="site-footer">Generated as a static product roadbook. Verify live schedules before departure.</footer>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render roadbook.json to static HTML.")
    parser.add_argument("json_path", help="Path to roadbook.json")
    parser.add_argument("--out", required=True, help="Output HTML path")
    parser.add_argument("--css", default="../assets/roadbook.css", help="CSS path written into generated HTML")
    args = parser.parse_args()

    json_path = Path(args.json_path)
    data = json.loads(json_path.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 2
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(data, args.css), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
