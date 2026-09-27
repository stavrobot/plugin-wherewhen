---
id: rep-puuzd
status: closed
deps: []
links: []
created: 2026-09-27T16:09:46Z
type: feature
priority: 2
assignee: Stavros Korokithakis
---
# Add switch_trip tool and shorten plugin description

Objective: let the bot move the plugin to another Wherewhen trip with a dedicated tool, so it does not fall back to calling the Wherewhen agent API directly. Owner rule: always switch the plugin's token when working on a trip; never use the raw API.

Scope:
- New tool dir switch_trip/ (manifest.json + run.py, same pattern as get_trip). One required string parameter 'link': the trip's agent link or bare token.
- Behaviour: extract the token (reuse extract_token), GET trip/ with that token. If the fetch fails, save nothing and return the error. If it works, write the token into ../config.json as trip_token and return the trip JSON.
- Config write: read the whole config.json, change only trip_token, keep every other key (including 'permissions', which the runner owns), write to a temp file in the same dir and os.replace it. Store the bare token.
- wherewhen.py: api_call currently always uses load_token(); let it accept an explicit token (small change, no refactor beyond that).
- switch_trip tool description (use verbatim): "Switch the plugin to another Wherewhen trip. Pass the trip's agent link or token. Use this instead of calling the Wherewhen API directly. The link grants write access to the trip, so do not repeat it. Returns the new trip."
- Root manifest.json: set description to exactly "A plugin for the trip management app Wherewhen." Keep all other fields unchanged.
- README.md: add switch_trip to the tool list; one sentence under Configuration that the plugin works on one trip at a time and switch_trip changes it.
- Commit on main and push to origin (no force push). config.json must stay untracked; no real token in any file.

Non-goals: multi-trip support (per-call token, token list); a separate state file; changes to other tools; tests infrastructure.

Caveat: never read the real config.json on this machine; it holds secrets. Test the config write against a temp copy with dummy values.

## Acceptance Criteria

switch_trip with an invalid link leaves config.json unchanged. With a valid link, trip_token is replaced and other keys are preserved.


## Notes

**2026-09-27T16:09:49Z**

ready for implementation
