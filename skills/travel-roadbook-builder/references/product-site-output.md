# Product Site Output

Use this when rendering or revising the final roadbook page.

The generated page should feel like a traveler-facing product, not an internal planning note:

- first screen: destination, dates, pace, interests, primary action to start the route, and first-stop map action;
- overview: trip workspace copy explaining what the roadbook helps the traveler do now;
- command center: lodging, transport, source evidence, and warnings in one scannable side panel;
- itinerary: day-by-day execution cards with time, stop, duration, map buttons, deadline, fallback, and source confidence;
- evidence: top-level `sourceRecords` shown as auditable source cards;
- deployment: static HTML/CSS only by default, suitable for GitHub Pages or Vercel.

Do not add Supabase unless the user explicitly needs persistent saved trips, accounts, collaboration, analytics, or generated-trip history.
