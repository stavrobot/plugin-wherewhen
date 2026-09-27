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
    return wherewhen.api_call("DELETE", f"stops/{wherewhen.segment(stop_id)}/")


if __name__ == "__main__":
    wherewhen.cli(handle)
