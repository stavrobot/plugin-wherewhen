#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import wherewhen


def handle(params: dict):
    body = wherewhen.select(params, ("startTime", "endTime"))
    return wherewhen.api_call("POST", "days/", body=body)


if __name__ == "__main__":
    wherewhen.cli(handle)
