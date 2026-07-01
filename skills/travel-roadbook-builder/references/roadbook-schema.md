# Roadbook Schema

Generate a JSON object with this shape:

```json
{
  "trip": {
    "title": "Paris 3-Day Roadbook",
    "destination": "Paris",
    "startDate": "2026-05-20",
    "endDate": "2026-05-22",
    "pace": "standard",
    "interests": ["museum", "food", "city walk"]
  },
  "sourceRecords": [
    {
      "id": "web-001",
      "type": "guide",
      "platform": "web",
      "url": "https://example.com/paris-guide",
      "readerUrl": "https://r.jina.ai/https://example.com/paris-guide",
      "title": "Paris First-Time Guide",
      "author": null,
      "capturedAt": "2026-07-01T12:00:00Z",
      "excerpt": "Short evidence excerpt used for itinerary planning.",
      "accessStatus": "read",
      "confidence": "medium"
    },
    {
      "id": "shot-flight-001",
      "type": "booking-screenshot",
      "platform": "user-screenshot",
      "url": null,
      "title": "Flight booking screenshot",
      "capturedAt": "2026-07-01T12:01:00Z",
      "excerpt": "Flight time and airports visible. Passenger details omitted.",
      "accessStatus": "read",
      "confidence": "high"
    }
  ],
  "lodging": [
    {
      "name": "Hotel Example",
      "address": "Example Street, Paris",
      "checkIn": "2026-05-20",
      "checkOut": "2026-05-22",
      "notes": "Ask whether luggage can be stored before check-in.",
      "sourceIds": ["shot-hotel-001"],
      "confidence": "high"
    }
  ],
  "transport": [
    {
      "type": "flight",
      "from": "Manchester",
      "to": "Paris CDG",
      "departAt": "2026-05-20 08:00",
      "arriveAt": "2026-05-20 10:30",
      "notes": "Reserve airport-to-city buffer.",
      "sourceIds": ["shot-flight-001"],
      "confidence": "high"
    }
  ],
  "days": [
    {
      "date": "2026-05-20",
      "title": "Arrival + City Walk",
      "summary": "Light arrival day.",
      "stops": [
        {
          "time": "14:00",
          "name": "Louvre Museum",
          "type": "museum",
          "description": "Book ticket in advance and reserve 2-3 hours.",
          "durationMinutes": 150,
          "mustGo": true,
          "deadline": "Leave before 17:00 if dinner is fixed.",
          "fallback": "Move Louvre to day 2 if arrival is delayed.",
          "mapQueries": {
            "amap": "Louvre Museum",
            "google": "Louvre Museum Paris",
            "apple": "Louvre Museum Paris"
          },
          "links": [
            {
              "label": "Official site",
              "url": "https://www.louvre.fr/"
            }
          ],
          "source": "pasted guide",
          "sourceIds": ["web-001"],
          "confidence": "medium"
        }
      ]
    }
  ],
  "warnings": [
    "Opening hours and transport schedules should be checked before departure."
  ]
}
```

Required fields:

- `trip.title`
- `trip.destination`
- `days[].date`
- `days[].stops[].name`

When uncertain, keep the stop but set `confidence` to `low` and add a warning or fallback.

Recommended fields:

- `sourceRecords[]`: top-level source registry for readable links, unreadable links, pasted notes, and screenshot evidence.
- `lodging[].sourceIds[]`, `transport[].sourceIds[]`, `days[].stops[].sourceIds[]`: stable references to `sourceRecords[].id`.
- `sourceRecords[].accessStatus`: `read`, `partial`, `unreadable`, or `user-summary`.
- `sourceRecords[].type`: `guide`, `booking-screenshot`, `pasted-note`, `official`, `map`, or `other`.

Keep old single-string `source` fields for human-readable display, but prefer `sourceIds` for traceability.
