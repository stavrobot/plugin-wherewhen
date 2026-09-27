#!/usr/bin/env -S uv run
# /// script
# dependencies = []
# ///

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import wherewhen


def handle(params: dict):
    link = wherewhen.require(params, "link")
    token = wherewhen.extract_token(link)
    trip = wherewhen.api_call("GET", "trip/", token=token)
    wherewhen.save_token(token)
    return trip


if __name__ == "__main__":
    wherewhen.cli(handle)
