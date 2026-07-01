---
name: travel-roadbook-builder
description: Generate execution-ready travel roadbooks from travel notes, public guide links, Xiaohongshu/web/Notion/Feishu materials, hotel or transport screenshots, booking text, and user preferences. Use when the user wants a structured roadbook.json and static HTML itinerary with source evidence, day-by-day stops, timing buffers, fallback notes, and Amap/Google Maps/Apple Maps links.
---

# Travel Roadbook Builder

## Workflow

Use this skill to build a travel roadbook from pasted materials, readable public URLs, and user-provided booking screenshots. Keep the pipeline stable: do not depend on email access, account imports, or live transport APIs.

1. Collect required trip basics: destination, start date, end date, pace, interests, must-go places, and avoid places.
2. Ask the user for guide notes, public links, hotel screenshots, and transport screenshots. Read `references/input-format.md` for the preferred intake shape.
3. If the user provides URLs, use the installed `agent-reach` skill and read `references/url-research.md`. Run `agent-reach doctor --json` first, then use the active backend. If a Xiaohongshu backend is unavailable, ask for pasted text or screenshots instead of pretending the link was read.
4. If the user provides hotel, flight, train, bus, ferry, or ticket screenshots, read `references/screenshot-bookings.md`, extract only itinerary fields, and omit sensitive identifiers.
5. Extract places, food stops, shopping areas, transport nodes, opening-hour notes, booking reminders, source records, and risks.
6. Apply itinerary rules from `references/itinerary-rules.md`.
7. Generate `roadbook.json` using `references/roadbook-schema.md`.
8. Mark uncertainty using `references/source-quality.md`; do not present unverified opening hours or schedules as certain.
9. Render the roadbook:

```bash
python skills/travel-roadbook-builder/scripts/render_roadbook.py roadbook.json --out docs/generated/my-roadbook.html --css ../assets/roadbook.css
```

10. If the user requests changes, update `roadbook.json` first, then re-render.

## Intake Rules

Read `references/input-format.md` when the user provides raw notes, URLs, screenshots, or asks what to paste.

Only ask blocking questions. Missing travel dates are blocking. Missing hotel details are not blocking, but the generated route should include warnings and avoid tight scheduling.

## Output Rules

- Produce `roadbook.json` before HTML.
- Preserve top-level `sourceRecords` and item-level `sourceIds` when sources are available.
- Include Amap, Google Maps, and Apple Maps search links for each stop.
- Include fallback or skip notes for tight days.
- Use hotel and transport details as constraints, especially on arrival and departure days.
- Keep the final roadbook mobile-readable and execution-focused.
