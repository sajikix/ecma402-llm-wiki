#!/usr/bin/env python3
"""Extract the ECMA-402-related agenda items from the TC39 plenary notes.

Stage advancement for ECMA-402 proposals is decided at the TC39 plenary
(raw/notes); TG2 only discusses and recommends. This walks every plenary day
file under raw/notes/meetings/<YYYY-MM>/, keeps the level-2 agenda items
(`## ...`) whose heading is ECMA-402-related, and records:
  - the heading text
  - stage signals in the heading (e.g. "for Stage 2.7")
  - the `### Conclusion` / `### Summary` block text
  - stage signals found in the conclusion (e.g. "advances to stage 4")

"ECMA-402-related" = the heading matches STATIC_KEYWORDS, or names one of the
API identifiers harvested from the canonical ECMA-402 proposal tables under
raw/proposals/ecma402/ (e.g. `Intl.DurationFormat` -> "DurationFormat").

Output: wiki/_generated/plenary-agenda-index.md (+ .jsonl). Mechanically
generated -- do not hand-edit.

Usage:  python3 tools/extract_plenary_agenda.py
"""

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEETINGS = ROOT / "raw" / "notes" / "meetings"
PROP402 = ROOT / "raw" / "proposals" / "ecma402"
OUT_MD = ROOT / "wiki" / "_generated" / "plenary-agenda-index.md"
OUT_JSONL = ROOT / "wiki" / "_generated" / "plenary-agenda-index.jsonl"

# Always-relevant words in a plenary heading.
STATIC_KEYWORDS = [
    r"intl", r"ecma[- ]?402", r"\b402\b", r"i18n", r"internationali[sz]",
    r"\btg ?2\b", r"locale", r"tolocale\w*", r"collat", r"plural",
    r"messageformat", r"cldr", r"\bicu\b", r"time ?zone",
    r"calendar", r"stable formatting", r"\bera\b", r"month ?code",
    r"\bamount\b", r"\bmeasure\b",  # Amount (formerly Measure), ECMA-262 with Intl surface
]

# Identifiers from proposal titles that are too generic to match on their own.
GENERIC = {
    "Intl", "Proposal", "Proposals", "API", "Option", "Options", "Unicode",
    "JavaScript", "Format", "Extend", "More", "Smart", "Keep",
}

# "Stage 3 reviewers: ..." names a future stage, not a transition.
REVIEWER = re.compile(r"reviewer", re.IGNORECASE)
STAGE_RE = re.compile(r"stage\s+(\d(?:\.\d)?)", re.IGNORECASE)
ADVANCE_RE = re.compile(
    r"(advance[sd]?|advancing|promote[sd]?|move[sd]?\s+to|reach(?:e[sd])?|"
    r"approv(?:e[sd]?|al)|withdraw|reject|decline|block|demote[sd]?|stays?\s+at|"
    r"remain[s]?\s+at|did\s+not|consensus|accepted|agreed|conditional)",
    re.IGNORECASE,
)


def harvest_identifiers():
    """API-ish identifiers from ECMA-402 proposal titles (DurationFormat, ...)."""
    idents = set()
    for f in PROP402.glob("*.md"):
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.startswith("| ["):
                continue
            m = re.match(r"^\|\s*\[([^\]]+)\]", line)
            if not m:
                continue
            title = m.group(1).replace("`", "")
            for tok in re.findall(r"(?:Intl\.)?([A-Z][a-z]+(?:[A-Z][a-z]+)+|[a-z]+[A-Z]\w+)", title):
                if tok not in GENERIC and len(tok) >= 6:
                    idents.add(tok)
    return idents


def parse_day(text):
    sections = []
    cur_head, cur_body = None, []
    for ln in text.splitlines():
        m = re.match(r"^##\s+(?!#)(.*)$", ln)
        if m:
            if cur_head is not None:
                sections.append((cur_head, cur_body))
            cur_head, cur_body = m.group(1).strip(), []
        elif cur_head is not None:
            cur_body.append(ln)
    if cur_head is not None:
        sections.append((cur_head, cur_body))
    return sections


def extract_conclusion(body_lines):
    out = []
    capturing = False
    for ln in body_lines:
        if re.match(r"^###\s+", ln):
            capturing = bool(
                re.search(r"conclusion|summary", ln, re.IGNORECASE)
                and not re.search(r"speaker", ln, re.IGNORECASE)
            )
            continue
        if capturing:
            out.append(ln)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out).strip())


def main():
    idents = harvest_identifiers()
    # "DurationFormat" also matches "Duration Format" (e.g. the 2020-02
    # "Time Duration Format Proposal for Stage 1" heading).
    spaced = [r"\s?".join(re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])", i)) for i in sorted(idents)]
    relevant = re.compile("|".join(STATIC_KEYWORDS + spaced), re.IGNORECASE)
    meetings = sorted(
        d for d in MEETINGS.iterdir() if d.is_dir() and re.match(r"\d{4}-\d{2}", d.name)
    )
    records = []
    md = [
        "# Plenary Agenda Index — ECMA-402 items (generated)\n",
        "> Mechanically extracted from `raw/notes` (TC39 plenary). Only agenda items whose heading looks ECMA-402-related are kept "
        "(keyword + identifiers harvested from `raw/proposals/ecma402/`). Do not hand-edit; regenerate via `tools/extract_plenary_agenda.py`.",
        "> Stage transitions are decided here; TG2 discussion lives in `tg2-agenda-index.md`.",
        "> The filter is heading-based and can miss items (e.g. a 402 topic under a generic heading) — fall back to `grep -ril` over `raw/notes/meetings` when tracing.",
        "> To trace a proposal: `grep -i -A4 'durationformat' wiki/_generated/plenary-agenda-index.md`.\n",
    ]
    n_meetings = 0
    for mdir in meetings:
        ym = mdir.name
        items = []
        for f in sorted(mdir.glob("*.md")):
            if f.name in ("toc.md", "README.md"):
                continue
            for head, body in parse_day(f.read_text(encoding="utf-8", errors="replace")):
                if not relevant.search(head):
                    continue
                concl = extract_conclusion(body)
                staged = "\n".join(l for l in concl.splitlines() if not REVIEWER.search(l))
                signals = [
                    cl.strip(" -*").strip()
                    for cl in staged.splitlines()
                    if STAGE_RE.search(cl) and ADVANCE_RE.search(cl)
                ]
                rec = {
                    "meeting": ym,
                    "file": str(f.relative_to(ROOT)),
                    "heading": head,
                    "heading_stages": STAGE_RE.findall(head),
                    "conclusion": concl,
                    "conclusion_stages": STAGE_RE.findall(staged),
                    "signals": signals,
                }
                records.append(rec)
                items.append(rec)
        if not items:
            continue
        n_meetings += 1
        md.append(f"\n## {ym}\n")
        for rec in items:
            allst = rec["heading_stages"] + rec["conclusion_stages"]
            stage_tag = " — stage: " + "/".join(sorted(set(allst))) if allst else ""
            md.append(f"- **{rec['heading']}**{stage_tag}  `{rec['file']}`")
            if rec["signals"]:
                for s in rec["signals"]:
                    md.append(f"  - → {s[:200]}")
            elif rec["conclusion"]:
                first = rec["conclusion"].splitlines()[0].strip(" -*").strip()
                if first:
                    md.append(f"  - {first[:200]}")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    with OUT_JSONL.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"identifiers harvested: {len(idents)}")
    print(f"meetings with 402 items: {n_meetings} / {len(meetings)}")
    print(f"agenda items extracted: {len(records)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)} and {OUT_JSONL.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
