"""Shared TypeSafe System One (Jev) client for narrow, one-question judgments.

Skills hand `judge()` a `state` dict (the text to reason over) and a dict of named
questions; it returns the parsed answers. Code owns control flow, thresholds and
writing results: use Jev only to answer one small question per judgment.

Question helpers:
    noul(instructions)            -> probability question (0..1)
    choice(instructions, labels)  -> label question; labels is {label: criterion}

Key: TYPESAFE_API_KEY from the environment, else a gitignored .env at the
paid-media-analyst-skills root. The key is never printed. Allow egress to
`api.typesafe.ai` in your sandbox network allowlist.

Usage:
    from jev_judge import judge, noul, choice, JevError
    answers = judge({"page_text": text},
                    {"q1": noul("Does `page_text` address X?")})
    answers["q1"]["noul"]   # 0..1

Callers that must degrade gracefully catch JevError (or call `have_key()` first).
"""

import os

import requests

API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
ENV_KEY = "TYPESAFE_API_KEY"
MAX_STATE_CHARS = 40000
TIMEOUT = 60


class JevError(RuntimeError):
    """Missing key, HTTP failure or malformed response. Message never contains the key."""


def _load_dotenv():
    if os.getenv(ENV_KEY):
        return
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                if line.startswith(ENV_KEY + "="):
                    os.environ[ENV_KEY] = line.split("=", 1)[1].strip()
    except OSError:
        pass


def have_key():
    _load_dotenv()
    return bool(os.getenv(ENV_KEY))


def noul(instructions):
    """Probability question: the answer carries a `noul` float in 0..1."""
    return {"type": "noul", "instructions": instructions}


def choice(instructions, labels):
    """Label question: `labels` maps each allowed label to its criterion."""
    return {"type": "choice", "instructions": instructions, "criteria": dict(labels)}


def cap_state(state, max_chars=MAX_STATE_CHARS):
    """Truncate each string value so the whole state stays within `max_chars`."""
    total = sum(len(v) for v in state.values() if isinstance(v, str))
    if total <= max_chars:
        return state
    budget = max_chars // max(1, sum(isinstance(v, str) for v in state.values()))
    return {k: (v[:budget] if isinstance(v, str) else v) for k, v in state.items()}


def judge(state, questions, *, timeout=TIMEOUT):
    """POST `state` + `questions` to System One and return the answers dict.

    Raises JevError on a missing key, network error, non-200 status or bad payload.
    """
    _load_dotenv()
    key = os.getenv(ENV_KEY)
    if not key:
        raise JevError(f"{ENV_KEY} is not set: put it in the environment or a gitignored .env")
    try:
        resp = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {key}"},
            json={"state": cap_state(state), "model": MODEL, "questions": questions},
            timeout=timeout,
        )
    except requests.RequestException as exc:
        raise JevError(f"request failed: {type(exc).__name__}") from None
    if resp.status_code != 200:
        # Status only: the body can echo request headers.
        raise JevError(f"HTTP {resp.status_code} from {API_URL}")
    try:
        return resp.json()["answers"]
    except (ValueError, KeyError):
        raise JevError("response had no `answers`") from None

