#!/usr/bin/env python3
"""
Content-addressed artifact cache for the Superlap pipeline.

Why this exists: resuming a run re-enters the pipeline from the start. Without
a cache, every already-approved stage regenerates — burning tokens and, worse,
possibly producing a *different* artifact than the human approved. Keying on a
hash of everything that shapes the output makes an unchanged stage return
byte-for-byte what it returned before, and makes a changed stage miss honestly.

Usage:
    python cache.py hash <part> [<part> ...]
    python cache.py get <run_id> <stage> <attempt> <input_hash>
    python cache.py put <run_id> <stage> <attempt> <input_hash> <file|->
    python cache.py invalidate <run_id> <stage>
    python cache.py list <run_id>

get exits 0 and prints the artifact on a hit; exits 2 and prints nothing on a
miss, so callers can branch on the exit code.
"""

import hashlib
import json
import os
import sys

CACHE_DIR = os.environ.get("SUPERLAP_CACHE_DIR", "workspace/cache")


def _key(run_id, stage, attempt, input_hash) -> str:
    raw = f"{run_id}:{stage}:{attempt}:{input_hash}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def input_hash(*parts) -> str:
    """Hash everything that determines a stage's output."""
    blob = "||".join("" if p is None else str(p) for p in parts)
    return hashlib.sha256(blob.encode()).hexdigest()[:12]


def _path(run_id, stage, attempt, ihash) -> str:
    return os.path.join(CACHE_DIR, f"{_key(run_id, stage, attempt, ihash)}.json")


def get(run_id, stage, attempt, ihash):
    path = _path(run_id, stage, attempt, ihash)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)["output"]
    return None


def put(run_id, stage, attempt, ihash, output) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = _path(run_id, stage, attempt, ihash)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({
            "run_id": run_id, "stage": stage, "attempt": attempt,
            "input_hash": ihash, "output": output,
        }, fh, indent=2)
    return path


def invalidate(run_id, stage) -> int:
    """Drop every cached artifact for a stage — used on every revision path."""
    if not os.path.isdir(CACHE_DIR):
        return 0
    dropped = 0
    for fn in os.listdir(CACHE_DIR):
        if not fn.endswith(".json"):
            continue
        full = os.path.join(CACHE_DIR, fn)
        try:
            with open(full, encoding="utf-8") as fh:
                rec = json.load(fh)
        except (json.JSONDecodeError, OSError):
            continue
        if rec.get("run_id") == run_id and rec.get("stage") == stage:
            os.remove(full)
            dropped += 1
    return dropped


def entries(run_id) -> list:
    if not os.path.isdir(CACHE_DIR):
        return []
    out = []
    for fn in sorted(os.listdir(CACHE_DIR)):
        if not fn.endswith(".json"):
            continue
        try:
            with open(os.path.join(CACHE_DIR, fn), encoding="utf-8") as fh:
                rec = json.load(fh)
        except (json.JSONDecodeError, OSError):
            continue
        if rec.get("run_id") == run_id:
            out.append({k: rec[k] for k in ("stage", "attempt", "input_hash")})
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    cmd, args = sys.argv[1], sys.argv[2:]

    if cmd == "hash":
        print(input_hash(*args))
        return 0

    if cmd == "get":
        run_id, stage, attempt, ihash = args
        hit = get(run_id, stage, int(attempt), ihash)
        if hit is None:
            return 2
        print(hit)
        return 0

    if cmd == "put":
        run_id, stage, attempt, ihash, src = args
        body = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
        print(put(run_id, stage, int(attempt), ihash, body))
        return 0

    if cmd == "invalidate":
        run_id, stage = args
        print(f"invalidated {invalidate(run_id, stage)} entr(ies) for {stage}")
        return 0

    if cmd == "list":
        for rec in entries(args[0]):
            print(f"{rec['stage']:24} attempt={rec['attempt']} hash={rec['input_hash']}")
        return 0

    print(f"unknown command: {cmd}\n{__doc__}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
