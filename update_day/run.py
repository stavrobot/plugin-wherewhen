#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import wherewhen


def handle(params: dict):
    day_id = wherewhen.require(params, "dayId")
    body = wherewhen.select(params, ("startTime", "endTime"))
    if not body:
        raise wherewhen.ToolError("Provide at least one of startTime or endTime.")
    return wherewhen.api_call("PATCH", f"days/{wherewhen.segment(day_id)}/", body=body)


if __name__ == "__main__":
    wherewhen.cli(handle)
