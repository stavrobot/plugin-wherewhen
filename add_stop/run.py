#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import wherewhen

OPTIONAL_KEYS = (
    "placeId",
    "name",
    "index",
    "pinnedTime",
    "pinnedEndTime",
    "legMode",
    "notes",
)


def handle(params: dict):
    wherewhen.require(params, "dayId")
    if (
        not str(params.get("placeId") or "").strip()
        and not str(params.get("name") or "").strip()
    ):
        raise wherewhen.ToolError(
            "Provide either placeId (from search_places) or name for the stop."
        )
    body = wherewhen.select(params, ("dayId",) + OPTIONAL_KEYS)
    return wherewhen.api_call("POST", "stops/", body=body)


if __name__ == "__main__":
    wherewhen.cli(handle)
