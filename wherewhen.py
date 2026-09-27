"""Shared internals for the wherewhen plugin tools.

Every tool talks to the same Wherewhen agent API and needs the same three
things: the trip token from config.json (a bare token or the full agent
URL), the base URL built from it, and one JSON request/response helper.

Tools import this module by putting the plugin root on sys.path, next to
where they already read config.json:

    import pathlib
    import sys

    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

    import wherewhen
"""

import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# A token or the full agent URL resolves to
# https://www.wherewhen.cc/api/agent/<token>/ .
API_ROOT = "https://www.wherewhen.cc/api/agent/"
AGENT_PATH_MARKER = "/api/agent/"

# The plugin runner kills a tool after 30 seconds; stay well inside that.
REQUEST_TIMEOUT_SECONDS = 20

# The API sits behind Cloudflare, which answers the default Python-urllib
# User-Agent with 403 error code 1010 ("browser signature banned"). Send an
# explicit one; the server accepts any non-default value.
USER_AGENT = "wherewhen-stavrobot-plugin/1.0"

READ_ONLY_HINT = (
    "The trip is read-only: either it was made by a newer app version, or "
    "it has not synced to the server yet. Open it in the app while online "
    "and retry."
)
PLACES_NOT_CONFIGURED_HINT = (
    "Place search is not configured on the server. Do not retry; "
    "placeholders still work."
)


class ToolError(Exception):
    """Fatal, user-facing error whose message is safe to print."""


def _load_config() -> dict:
    try:
        with (ROOT / "config.json").open() as config_file:
            config = json.load(config_file)
    except (OSError, json.JSONDecodeError) as err:
        raise ToolError(f"Could not read config.json: {err}") from err
    if not isinstance(config, dict):
        raise ToolError("config.json must contain a JSON object.")
    return config


def extract_token(raw) -> str:
    """Return the trip token from a bare token or a full agent URL.

    The agent link is the whole URL a trip exposes for its agent API, e.g.
    https://www.wherewhen.cc/api/agent/<token>/ ; the token is the last path
    segment. Anything that is not a URL is treated as the token itself,
    with surrounding slashes tolerated.
    """
    value = str(raw).strip()
    if value.startswith(("http://", "https://")):
        path = urllib.parse.urlparse(value).path
        index = path.find(AGENT_PATH_MARKER)
        if index == -1:
            raise ToolError(
                "The trip_token URL does not contain '/api/agent/'. Paste "
                "the trip's agent link or just its token."
            )
        value = path[index + len(AGENT_PATH_MARKER) :]
    token = value.strip("/")
    if not token:
        raise ToolError("The trip_token setting is empty.")
    if "/" in token:
        raise ToolError(
            "The trip_token setting does not look like a Wherewhen agent "
            "token. Paste the trip's agent link or just its token."
        )
    return token


def load_token() -> str:
    raw = _load_config().get("trip_token")
    if not str(raw or "").strip():
        raise ToolError(
            "The 'trip_token' setting is missing from config.json. Set it "
            "to the trip's Wherewhen agent link or token."
        )
    return extract_token(raw)


def build_base_url(token: str) -> str:
    return API_ROOT + urllib.parse.quote(token, safe="") + "/"


def segment(value) -> str:
    """Quote an id for use as a single URL path segment."""
    return urllib.parse.quote(str(value), safe="")


def _error_from_http(err: urllib.error.HTTPError, places: bool) -> ToolError:
    status = err.code
    try:
        body = json.loads(err.read().decode("utf-8"))
    except (OSError, ValueError):
        body = None
    message = body.get("error") if isinstance(body, dict) else None
    if not message:
        message = err.reason or "the request failed"
    text = f"{message} (HTTP {status})"
    if status == 409:
        text += "\n" + READ_ONLY_HINT
    if status == 503 and places:
        text += "\n" + PLACES_NOT_CONFIGURED_HINT
    return ToolError(text)


def api_call(method, path, *, body=None, query=None, places=False):
    """Call the agent API and return the decoded JSON response.

    `path` is relative to the trip base URL, e.g. "trip/" or
    "stops/<id>/move/". A `body` of None sends no payload (GET, DELETE);
    any other value is JSON-encoded. Explicit nulls inside `body` are
    preserved, because the API uses null to clear some fields.
    """
    url = build_base_url(load_token()) + path
    if query:
        url += "?" + urllib.parse.urlencode(query)

    data = None
    headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(
            request, timeout=REQUEST_TIMEOUT_SECONDS
        ) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as err:
        raise _error_from_http(err, places) from err
    except urllib.error.URLError as err:
        raise ToolError(f"Could not reach the Wherewhen API: {err.reason}") from err
    except OSError as err:
        raise ToolError(f"The Wherewhen API request failed: {err}") from err

    if not payload.strip():
        return {}
    try:
        return json.loads(payload)
    except json.JSONDecodeError as err:
        raise ToolError(f"The Wherewhen API returned invalid JSON: {err}") from err


def select(params: dict, keys) -> dict:
    """Return the subset of params whose keys are in `keys`.

    Absent keys are omitted while keys explicitly set to null are kept, so
    an explicit null reaches the API and clears a field.
    """
    return {key: params[key] for key in keys if key in params}


def require(params: dict, key: str) -> str:
    value = params.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ToolError(f"Missing required parameter: {key}")
    return value


def parse_params() -> dict:
    try:
        params = json.load(sys.stdin)
    except json.JSONDecodeError as err:
        raise ToolError(f"Invalid JSON on stdin: {err}") from err
    if not isinstance(params, dict):
        raise ToolError("Parameters must be a JSON object.")
    return params


def cli(handler) -> None:
    """Run a tool handler: read params, print the JSON result, map errors."""
    try:
        result = handler(parse_params())
        json.dump(result, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
    except ToolError as err:
        sys.stderr.write(f"{err}\n")
        sys.exit(1)
