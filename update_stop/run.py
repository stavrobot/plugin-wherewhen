#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import wherewhen

EDITABLE_KEYS = ("name", "pinnedTime", "pinnedEndTime", "legMode", "notes")


def handle(params: dict):
    stop_id = wherewhen.require(params, "stopId")
    body = wherewhen.select(params, EDITABLE_KEYS)
    if not body:
        raise wherewhen.ToolError(
            "Provide at least one of name, pinnedTime, pinnedEndTime, legMode or notes."
        )
    return wherewhen.api_call(
        "PATCH", f"stops/{wherewhen.segment(stop_id)}/", body=body
    )


if __name__ == "__main__":
    wherewhen.cli(handle)
