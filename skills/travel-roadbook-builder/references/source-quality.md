# Source Quality

Use confidence labels:

- `high`: user-provided booking information, fixed ticket time, official site copied by user.
- `medium`: copied guide text, user notes, widely known place information.
- `low`: inferred duration, ambiguous place, unverified opening hour, vague recommendation.

Rules:

- Preserve source notes when possible.
- Surface conflicts instead of silently resolving them.
- Mark unverified schedules as needing confirmation.
- Do not pretend a Xiaohongshu link was read if only the URL was provided.
- Ask for pasted text when a source is inaccessible.

