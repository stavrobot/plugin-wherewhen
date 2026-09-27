#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import wherewhen


def handle(params: dict):
    body = wherewhen.select(params, ("name", "startDate", "paddingMin"))
    if not body:
        raise wherewhen.ToolError(
            "Provide at least one of name, startDate or paddingMin."
        )
    return wherewhen.api_call("PATCH", "trip/", body=body)


if __name__ == "__main__":
    wherewhen.cli(handle)
