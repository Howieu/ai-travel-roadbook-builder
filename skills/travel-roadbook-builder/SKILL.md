---
name: travel-roadbook-builder
description: Generate execution-ready travel roadbooks from pasted travel notes, hotel bookings, flight/train/coach details, and user preferences. Use when the user wants to turn Xiaohongshu/web/Notion/Feishu travel materials or booking text into a structured roadbook.json and a static HTML itinerary with day-by-day stops, timing buffers, fallback notes, and Amap/Google Maps/Apple Maps links.
---

# Travel Roadbook Builder

## Workflow

Use this skill to build a travel roadbook from pasted materials. Keep V0 stable: do not depend on scraping, logins, email access, or live transport APIs.

1. Collect required trip basics: destination, start date, end date, pace, interests, must-go places, and avoid places.
2. Ask the user to paste guide notes, hotel details, and transport details. If a link cannot be read, ask for pasted text.
3. Extract places, food stops, shopping areas, transport nodes, opening-hour notes, booking reminders, and risks.
4. Apply itinerary rules from `references/itinerary-rules.md`.
5. Generate `roadbook.json` using `references/roadbook-schema.md`.
6. Mark uncertainty using `references/source-quality.md`; do not present unverified opening hours or schedules as certain.
7. Render the roadbook:

```bash
python skills/travel-roadbook-builder/scripts/render_roadbook.py roadbook.json --out docs/generated/my-roadbook.html --css ../assets/roadbook.css
```

8. If the user requests changes, update `roadbook.json` first, then re-render.

## Intake Rules

Read `references/input-format.md` when the user provides raw notes or asks what to paste.

Only ask blocking questions. Missing travel dates are blocking. Missing hotel details are not blocking, but the generated route should include warnings and avoid tight scheduling.

## Output Rules

- Produce `roadbook.json` before HTML.
- Include Amap, Google Maps, and Apple Maps search links for each stop.
- Include fallback or skip notes for tight days.
- Use hotel and transport details as constraints, especially on arrival and departure days.
- Keep the final roadbook mobile-readable and execution-focused.

