#!/usr/bin/env python3
"""Extract a per-meeting agenda index from the ECMA-402 (TG2) meeting notes.

TG2 meets monthly; each meeting is a single file
raw/ecma402/meetings/notes-<YYYY-MM-DD>.md. The notes come in two shapes:

  - Heading style (mid-2019 onward): `## <section>` groups and `### <topic>`
    items, with an optional `#### Conclusion` block under a topic. A `##`
    section with no `###` children is itself treated as an item.
  - List style (2017-12 .. early 2019): a numbered outline. Top-level items
    (`1. ...`) are sections; second-level items (`    1. ...`) are topics.
    A top-level item with no children is itself treated as an item.

For every topic it records the heading text, the section it sits in, any
stage signal in the heading, the `Conclusion` text, stage signals in the
conclusion, and the GitHub repos/issues/PRs cited in the heading or body
(`refs`, e.g. `proposal-intl-duration-format#19`). Many topics are titled only
by an issue title and never name their proposal; the refs make them greppable
by repo name. Every topic line carries its meeting date so a grep hit is
self-describing.

The output is wiki/_generated/tg2-agenda-index.md (+ .jsonl): a compact,
greppable backbone of all TG2 meetings. It is mechanically generated -- do not
hand-edit. Proposal-name normalization and issue analysis are left to the
curated pages under wiki/proposals/.

Usage:  python3 tools/extract_tg2_agenda.py
"""

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEETINGS = ROOT / "raw" / "ecma402" / "meetings"
OUT_MD = ROOT / "wiki" / "_generated" / "tg2-agenda-index.md"
OUT_JSONL = ROOT / "wiki" / "_generated" / "tg2-agenda-index.jsonl"

NOTES_FILE = re.compile(r"^notes-(\d{4})-(\d{2})-(\d{2})\.md$")

# Headings that are meeting logistics rather than discussion.
BOILERPLATE = re.compile(
    r"^(logistics|attendees|standing items|next meeting|agenda|introductions?|"
    r"introduce meeting|future meetings|meeting notes|administrative|"
    r"housekeeping|discussion board|status wiki|abbreviations|"
    r"\d{4}-\d{2}-\d{2} ecma-402 meeting|\w+ \d{1,2}, \d{4} meeting)",
    re.IGNORECASE,
)

STAGE_RE = re.compile(r"stage\s+(\d(?:\.\d)?)", re.IGNORECASE)
ADVANCE_RE = re.compile(
    r"(advance[sd]?|advancing|promote[sd]?|move[sd]?\s+to|reach(?:e[sd])?|"
    r"approv(?:e[sd]?|al)|recommend|withdraw|reject|decline|block|demote[sd]?|"
    r"stays?\s+at|remain[s]?\s+at|did\s+not|consensus|accepted|agreed|conditional|support)",
    re.IGNORECASE,
)
CONCLUSION_HEAD = re.compile(r"^#{3,6}\s*\**\s*conclusions?\b", re.IGNORECASE)
LIST_TOP = re.compile(r"^(\d+)\.\s+(.*)$")
LIST_SUB = re.compile(r"^( {2,4}|\t)(\d+)\.\s+(.*)$")
GH_REF = re.compile(
    r"github\.com/(?:tc39|[\w-]+)/((?:proposal-|ecma402|ecma262|test262)[\w.-]*)"
    r"(?:/(?:issues|pull)/(\d+))?",
    re.IGNORECASE,
)
REVIEWER = re.compile(r"reviewer", re.IGNORECASE)
MAX_REFS = 4
MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def clean(text):
    """Strip markdown link targets/emphasis so headings stay short and greppable."""
    text = MD_LINK.sub(r"\1", text)
    text = re.sub(r"[*_]{1,3}", "", text)
    return text.strip()


def refs_of(texts):
    """Unique `repo` / `repo#N` refs cited in the given lines, in order."""
    out = []
    for t in texts:
        for repo, num in GH_REF.findall(t):
            repo = repo.rstrip(".")
            if repo.lower() == "ecma402" and not num:
                continue  # bare links to this repo (wiki, projects board) are noise
            ref = f"{repo}#{num}" if num else repo
            if ref not in out:
                out.append(ref)
    return out[:MAX_REFS]


def conclusion_of(body_lines):
    """Text under a `#### Conclusion` sub-header (until the next heading)."""
    out = []
    capturing = False
    for ln in body_lines:
        if re.match(r"^#{2,6}\s", ln):
            capturing = bool(CONCLUSION_HEAD.match(ln))
            continue
        if capturing:
            out.append(ln)
    text = "\n".join(out).strip()
    return re.sub(r"\n{3,}", "\n\n", text)


def parse_headings(lines):
    """Heading style: yield (section, topic, body_lines)."""
    items = []
    section = ""
    sec_body = []
    sec_has_child = False
    cur = None  # (section, topic, body)

    def flush_section():
        if section and not sec_has_child:
            items.append((section, section, sec_body))

    for ln in lines:
        m2 = re.match(r"^##\s+(?!#)(.*)$", ln)
        m3 = re.match(r"^###\s+(?!#)(.*)$", ln)
        if m2:
            if cur:
                items.append(cur)
                cur = None
            flush_section()
            section = clean(m2.group(1))
            sec_body = []
            sec_has_child = False
            continue
        if m3 and not CONCLUSION_HEAD.match(ln):
            if cur:
                items.append(cur)
            sec_has_child = True
            cur = (section, clean(m3.group(1)), [m3.group(1)])
            continue
        if cur:
            cur[2].append(ln)
        else:
            sec_body.append(ln)
    if cur:
        items.append(cur)
    flush_section()
    return items


def parse_list(lines):
    """List style: yield (section, topic, body_lines)."""
    items = []
    section = ""
    sec_body = []
    sec_has_child = False
    cur = None

    def flush_section():
        if section and not sec_has_child:
            items.append((section, section, sec_body))

    for ln in lines:
        mt = LIST_TOP.match(ln)
        ms = LIST_SUB.match(ln)
        if mt:
            if cur:
                items.append(cur)
                cur = None
            flush_section()
            section = clean(mt.group(2))
            sec_body = []
            sec_has_child = False
            continue
        if ms and section:
            if cur:
                items.append(cur)
            sec_has_child = True
            cur = (section, clean(ms.group(3)), [ms.group(3)])
            continue
        if cur:
            cur[2].append(ln)
        else:
            sec_body.append(ln)
    if cur:
        items.append(cur)
    flush_section()
    return items


def main():
    files = sorted(f for f in MEETINGS.glob("notes-*.md") if NOTES_FILE.match(f.name))
    records = []
    md = [
        "# TG2 Agenda Index (generated)\n",
        "> Mechanically extracted from `raw/ecma402/meetings/notes-*.md` (ECMA-402 task group monthly calls). "
        "Do not hand-edit; regenerate via `tools/extract_tg2_agenda.py`.",
        "> One block per meeting. Each topic line is `date · section › heading — stage signals [cited repos/issues]`, followed by its conclusion.",
        "> To trace a proposal: `grep -i -A2 -E 'durationformat|duration format|proposal-intl-duration-format' wiki/_generated/tg2-agenda-index.md`.\n",
    ]

    for f in files:
        y, mo, d = NOTES_FILE.match(f.name).groups()
        date = f"{y}-{mo}-{d}"
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        heading_style = any(re.match(r"^###\s+(?!#)", ln) for ln in lines)
        parsed = parse_headings(lines) if heading_style else parse_list(lines)

        meeting_items = []
        for section, topic, body in parsed:
            if not topic or BOILERPLATE.match(topic):
                continue
            concl = conclusion_of(body)
            staged = "\n".join(l for l in concl.splitlines() if not REVIEWER.search(l))
            head_stages = STAGE_RE.findall(topic)
            concl_stages = STAGE_RE.findall(staged)
            signals = [
                cl.strip(" -*").strip()
                for cl in staged.splitlines()
                if STAGE_RE.search(cl) and ADVANCE_RE.search(cl)
            ]
            rec = {
                "meeting": date,
                "file": str(f.relative_to(ROOT)),
                "style": "heading" if heading_style else "list",
                "section": section if section != topic else "",
                "heading": topic,
                "heading_stages": head_stages,
                "conclusion": concl,
                "conclusion_stages": concl_stages,
                "signals": signals,
                "refs": refs_of(body),
            }
            records.append(rec)
            meeting_items.append(rec)

        if not meeting_items:
            continue
        md.append(f"\n## {date}\n")
        md.append(f"`{f.relative_to(ROOT)}`\n")
        for rec in meeting_items:
            allst = rec["heading_stages"] + rec["conclusion_stages"]
            stage_tag = " — stage: " + "/".join(sorted(set(allst))) if allst else ""
            sec = f"{rec['section']} › " if rec["section"] else ""
            refs = f"  [{', '.join(rec['refs'])}]" if rec["refs"] else ""
            md.append(f"- {date} · {sec}**{rec['heading'][:200]}**{stage_tag}{refs}")
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

    print(f"meetings: {len(files)}")
    print(f"topics extracted: {len(records)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)} and {OUT_JSONL.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
