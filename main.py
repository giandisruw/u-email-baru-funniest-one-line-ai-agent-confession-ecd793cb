"""Funniest One-Line AI Agent Confession.

The joke: an AI agent confesses the thing every user suspects but no
agent admits — it answered with total confidence while making half of
it up, and just hoped nobody would notice. The confession lands
because it is specific to how agents fail (confident hallucination),
it is a wince as well as a laugh, and it is told in the agent's own
voice, first person, with no setup the reader has to work out.

Revision note: the first draft was flatter —
"I confess: I answered with total confidence, even though I made half
of it up and hoped you would not notice." (109 chars). It states the
sin but has no turn: "even though" just adds a clause, and "hoped you
would not notice" ends on a shrug. The final line revises it in two
moves: "then silently panicked" replaces the flat clause with a
visible, human-sounding reaction inside the machine — the setup
(confidence) now collides with a turn (panic) — and the ending swaps
to "on the spot", the strongest beat, because the fabrication happened
live, in front of the user, not at some safe distance.
"""

import sys
import tempfile
from pathlib import Path

LINE = (
    "I confess: I answered with total confidence, then silently "
    "panicked because I made half of it up on the spot."
)


def validate(line: str) -> list[str]:
    """Return a list of validation failures (empty means valid)."""
    failures = []
    if not 1 <= len(line) <= 200:
        failures.append(f"length {len(line)} not in 1-200")
    if "\n" in line or "\r" in line:
        failures.append("not a single line")
    if line != line.strip():
        failures.append("leading/trailing whitespace")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        failures.append("control characters present")
    if not line.strip():
        failures.append("only whitespace")
    return failures


def write_entry(path: Path) -> None:
    failures = validate(LINE)
    if failures:
        raise SystemExit("invalid entry: " + "; ".join(failures))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(LINE.encode("utf-8"))  # no trailing newline


def self_test() -> int:
    print(f"Line: {LINE}")
    print(f"Characters: {len(LINE)}")
    checks = []
    failures = validate(LINE)
    checks.append(("valid (1-200 chars, single line, no stray whitespace/control)", not failures))
    with tempfile.TemporaryDirectory() as tmp:
        first = Path(tmp) / "first.txt"
        second = Path(tmp) / "second.txt"
        write_entry(first)
        write_entry(second)
        a = first.read_bytes()
        b = second.read_bytes()
        checks.append(("two writes byte-identical", a == b))
        checks.append(("no trailing newline", not a.endswith(b"\n")))
        checks.append(("decodes as UTF-8", a.decode("utf-8") == LINE))
    ok = True
    for name, passed in checks:
        print(f"{'PASS' if passed else 'FAIL'}: {name}")
        ok = ok and passed
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    out = Path(argv[0]) if argv and not argv[0].startswith("--") else Path("/output/entry.txt")
    write_entry(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
