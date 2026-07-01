# Screenshot Bookings

Use this reference when the user provides screenshots for hotels, flights, trains, buses, ferries, tickets, or booking confirmations.

Screenshots are treated as user-provided evidence. Extract only the fields needed to build a safe itinerary; do not preserve sensitive identifiers unless the user explicitly asks.

## Privacy Rules

Do not store these in `roadbook.json`:

- passenger full names;
- full booking references or PNRs;
- passport, national ID, student ID, or visa numbers;
- payment card details;
- phone numbers or email addresses;
- loyalty membership numbers;
- QR codes or barcodes.

If a booking reference is useful for the traveler, store only a redacted reminder such as `Booking reference shown in screenshot; check original app`.

## Hotel Fields

Extract:

```json
{
  "name": "Hotel Example",
  "address": "Example Street, Paris",
  "checkIn": "2026-05-20",
  "checkOut": "2026-05-22",
  "notes": "Luggage storage mentioned in screenshot. Full booking reference omitted.",
  "sourceIds": ["shot-hotel-001"],
  "confidence": "high"
}
```

Useful optional fields:

- check-in time;
- check-out time;
- room count;
- breakfast or meal note;
- nearest station;
- luggage storage note;
- cancellation or deposit reminder.

## Transport Fields

Extract:

```json
{
  "type": "flight",
  "from": "Manchester",
  "to": "Paris CDG",
  "departAt": "2026-05-20 08:00",
  "arriveAt": "2026-05-20 10:30",
  "notes": "Terminal shown in screenshot; reserve airport buffer.",
  "sourceIds": ["shot-flight-001"],
  "confidence": "high"
}
```

Supported `type` values:

- `flight`
- `train`
- `bus`
- `coach`
- `ferry`
- `metro`
- `taxi`
- `car`
- `other`

Useful optional fields:

- terminal;
- station;
- platform or gate when visible;
- carrier or train number;
- seat or carriage when the user wants it, preferably redacted if sensitive;
- baggage deadline;
- security or boarding deadline;
- arrival-day or departure-day buffer recommendation.

## Source Records

Create a screenshot source record:

```json
{
  "id": "shot-flight-001",
  "type": "booking-screenshot",
  "platform": "user-screenshot",
  "title": "Flight booking screenshot",
  "url": null,
  "capturedAt": "2026-07-01T12:00:00Z",
  "excerpt": "Flight from Manchester to Paris CDG, 08:00-10:30. Passenger details omitted.",
  "accessStatus": "read",
  "confidence": "high"
}
```

If OCR or visual inspection is unclear, set `confidence` to `low` and ask the user to confirm the field. Do not guess exact dates, times, stations, terminals, or hotel addresses from blurry screenshots.

## Roadbook Rules

- Use screenshot-derived hotel and transport data as hard schedule constraints.
- Keep arrival and departure days lighter when fixed transport exists.
- Add station or airport buffer warnings.
- Reference screenshot sources with `sourceIds`.
- If a booking screenshot conflicts with pasted guide text, prefer the screenshot for fixed times and add a warning.
