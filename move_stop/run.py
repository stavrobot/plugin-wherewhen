#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import wherewhen


def handle(params: dict):
    stop_id = wherewhen.require(params, "stopId")
    day_id = wherewhen.require(params, "dayId")
    body = {"dayId": day_id}
    if "index" in params:
        body["index"] = params["index"]
    return wherewhen.api_call(
        "POST", f"stops/{wherewhen.segment(stop_id)}/move/", body=body
    )


if __name__ == "__main__":
    wherewhen.cli(handle)
