#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import wherewhen


def handle(params: dict):
    query = wherewhen.require(params, "q")
    return wherewhen.api_call("GET", "places/", query={"q": query}, places=True)


if __name__ == "__main__":
    wherewhen.cli(handle)
