#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import wherewhen


def handle(params: dict):
    return wherewhen.api_call("GET", "trip/")


if __name__ == "__main__":
    wherewhen.cli(handle)
