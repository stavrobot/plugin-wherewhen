---
id: rep-djreo
status: closed
deps: []
links: []
created: 2026-09-27T11:05:00Z
type: feature
priority: 2
assignee: Stavros Korokithakis
---
# Implement wherewhen Stavrobot plugin

Objective: create a Stavrobot plugin (per coder/PLUGIN.md in skorokithakis/stavrobot) that reads and edits one Wherewhen trip through the Wherewhen agent API at https://www.wherewhen.cc/api/agent/<token>/ .

Scope (repo root):
- manifest.json: name 'wherewhen'; description written for the assistant, including the API rules it needs (days have no stored date and cannot be reordered; 'ideas' as dayId for unscheduled stops; placeholders cannot be the first stop of a day; pinnedTime/pinnedEndTime are HH:mm local, up to 47:59, null clears; legMode auto|walk|drive|cycle|other; notes max 2000 chars; add a real place by search_places then add_stop with placeId). summary under 80 chars. config: trip_token (required).
- Shared module at root (e.g. wherewhen.py): load ../config.json, build base URL, do the HTTP call with stdlib urllib, JSON in/out. trip_token accepts either the bare token or the full agent URL; extract the token from the URL.
- One tool dir per operation: get_trip, update_trip (name, startDate, paddingMin), search_places (q), add_day (startTime, endTime), update_day, delete_day, add_stop (dayId, placeId or name, index, pinnedTime, pinnedEndTime, legMode, notes), update_stop, delete_stop, move_stop (dayId, index). Only send parameters the caller gave, but allow explicit null where the API uses null to clear.
- Tools output the API JSON (writes return the full updated trip).
- Errors: on non-2xx, write the API 'error' message plus status to stderr, exit non-zero. For 409 add: trip is read-only, open it in the app while online and retry. For 503 on places: place search is not configured on the server, do not retry; placeholders still work.
- README.md in the PLUGIN.md order; install line: Tell Stavrobot to install https://github.com/stavrobot/plugin-wherewhen . Explain where to get the token (the agent link from Wherewhen; the full URL is fine).
- LICENSE: full AGPLv3 text. .gitignore: config.json, __pycache__, *.pyc.
- All scripts executable, uv run shebang, no third-party deps.

Non-goals: multiple trips per install; trip create/delete/share; schedule/travel-time computation; tests in repo; CI.

Caveats:
- Never commit config.json or the token. Do not put the token in any tracked file.
- Do not commit PLUGIN.md (do not add it to the repo at all).
- Test each tool live against the user's sample trip 'Greece' (token supplied out of band; put it in a local config.json). Restore the trip afterwards to its original state: 3 days, 10 stops, ideas empty, paddingMin 10, name Greece, startDate 2026-08-11. Report anything you could not restore.
- Do not commit or push in this task.


## Notes

**2026-09-27T11:28:33Z**

ready for implementation
