# Agent Reach Sources Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade Travel Roadbook Builder so it can turn public webpage links and user booking screenshots into source-backed roadbooks.

**Architecture:** Keep the existing static JSON-to-HTML pipeline. Add Agent Reach as the URL acquisition layer, screenshot-derived booking fields as trusted trip constraints, and a small source registry rendered in the roadbook sidebar.

**Tech Stack:** Codex Skill markdown, Python standard library, unittest, static HTML/CSS.

---

### Task 1: Document Agent Reach URL Intake

**Files:**
- Create: `skills/travel-roadbook-builder/references/url-research.md`
- Modify: `skills/travel-roadbook-builder/SKILL.md`
- Modify: `skills/travel-roadbook-builder/references/input-format.md`
- Modify: `skills/travel-roadbook-builder/references/source-quality.md`

- [x] **Step 1: Add URL routing rules**

Create `url-research.md` with Agent Reach commands:

```markdown
# URL Research

Use the installed `agent-reach` skill whenever the user provides travel links.

1. Run `agent-reach doctor --json`.
2. For ordinary webpages, read through Jina Reader:
   `curl -s "https://r.jina.ai/URL"`.
3. For Xiaohongshu links, use the active Agent Reach Xiaohongshu backend when available.
4. If no Xiaohongshu backend is active, ask the user to paste the note text or upload screenshots.
5. Preserve source metadata and mark unreadable links instead of pretending they were read.
```

- [x] **Step 2: Wire the reference into the skill**

Update `SKILL.md` workflow so URL input triggers `url-research.md`.

- [x] **Step 3: Update input and source quality docs**

Add URL lists, access status, and source IDs to the intake and source quality references.

### Task 2: Document Screenshot Booking Intake

**Files:**
- Create: `skills/travel-roadbook-builder/references/screenshot-bookings.md`
- Modify: `skills/travel-roadbook-builder/references/input-format.md`
- Modify: `skills/travel-roadbook-builder/references/roadbook-schema.md`

- [x] **Step 1: Add screenshot extraction rules**

Create `screenshot-bookings.md` with fields for hotel, flight, train, bus, and ferry screenshots. Require redaction of passenger names, full booking references, payment details, phone numbers, emails, and ID/passport numbers.

- [x] **Step 2: Extend the schema**

Add `sourceRecords[]`, `sourceIds[]`, and screenshot-derived `confidence` rules to lodging, transport, and stops.

### Task 3: Add a Deterministic Web Source Fetcher

**Files:**
- Create: `skills/travel-roadbook-builder/scripts/fetch_url_sources.py`
- Create: `tests/test_fetch_url_sources.py`
- Modify: `README.md`

- [x] **Step 1: Write the unit test**

Test that a mocked Jina Reader response becomes a source record with `id`, `platform`, `url`, `readerUrl`, `title`, `capturedAt`, `excerpt`, `accessStatus`, and `confidence`.

- [x] **Step 2: Implement the script**

Use only Python standard library. Accept URLs as CLI arguments or from a newline-delimited file. Return JSON shaped as `{"sources": [...]}`. On fetch failure, keep the URL with `accessStatus: "unreadable"`.

- [x] **Step 3: Document usage**

Add a README example showing how to convert URLs into source records before building a roadbook.

### Task 4: Render Source Evidence

**Files:**
- Modify: `skills/travel-roadbook-builder/scripts/render_roadbook.py`
- Modify: `docs/assets/roadbook.css`
- Modify: `tests/test_renderer.py`
- Modify: `skills/travel-roadbook-builder/examples/paris-roadbook.json`

- [x] **Step 1: Add source rendering**

Render top-level `sourceRecords[]` or `sources[]` in the sidebar. Show title, platform, access status, confidence, and link when present.

- [x] **Step 2: Add source IDs to demo data**

Update the Paris demo with webpage, pasted-guide, flight screenshot, train screenshot, and hotel screenshot records.

- [x] **Step 3: Verify rendering**

Update renderer tests to assert source evidence appears in HTML.

### Task 5: Update Public Demo and Verify

**Files:**
- Modify: `docs/index.html`
- Modify: `docs/generated/paris-demo.html`
- Modify: local installed skill at `/Users/vendredi/.codex/skills/travel-roadbook-builder`

- [x] **Step 1: Regenerate demo**

Run:

```bash
python skills/travel-roadbook-builder/scripts/render_roadbook.py \
  skills/travel-roadbook-builder/examples/paris-roadbook.json \
  --out docs/generated/paris-demo.html \
  --css ../assets/roadbook.css
```

- [x] **Step 2: Run verification**

Run:

```bash
python -m unittest discover -s tests -v
python /Users/vendredi/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/travel-roadbook-builder
```

- [x] **Step 3: Install and push**

Copy the updated skill into `/Users/vendredi/.codex/skills/travel-roadbook-builder`, commit, push, and confirm GitHub Pages updates.
