# Wherewhen plugin

A Stavrobot plugin that reads and edits one [Wherewhen](https://www.wherewhen.cc/) trip: its days, stops and unscheduled ideas.

## Requirements

A Wherewhen trip and its agent link. Wherewhen provides the link for the trip; no separate account or API key is needed.

## Installation

Tell Stavrobot to install https://github.com/stavrobot/plugin-wherewhen

## Configuration

- `trip_token` (required): the trip's Wherewhen agent link, or just the token from it. In Wherewhen, open the trip and choose its agent link, then paste the whole URL. The full agent URL and the bare token (the part after `/api/agent/`) are both accepted.

## Tools

- **get_trip** — return the current trip: name, start date, padding, days with their stops, and ideas.
- **update_trip** — change the trip's name, start date or padding.
- **search_places** — search Google Places for candidates to add as real stops.
- **add_day** — append a day to the end of the trip.
- **update_day** — change a day's start or end time.
- **delete_day** — delete a day; its stops move to ideas.
- **add_stop** — add a real place (by `placeId`) or a placeholder (by name) to a day or to ideas.
- **update_stop** — change a stop's name, fixed times, leg mode or notes.
- **delete_stop** — delete a stop.
- **move_stop** — move a stop to another day or to ideas, at an optional index.
