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
  "lodging": [
    {
      "name": "Hotel Example",
      "address": "Example Street, Paris",
      "checkIn": "2026-05-20",
      "checkOut": "2026-05-22",
      "notes": "Ask whether luggage can be stored before check-in."
    }
  ],
  "transport": [
    {
      "type": "flight",
      "from": "Manchester",
      "to": "Paris CDG",
      "departAt": "2026-05-20 08:00",
      "arriveAt": "2026-05-20 10:30",
      "notes": "Reserve airport-to-city buffer."
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

