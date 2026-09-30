#!/usr/bin/env python3
"""Generate per-person reference pages for delegates referenced in the wiki.

Scope: only people whose abbreviation actually appears in a curated proposal
page (`wiki/proposals/*.md`) or family page (`wiki/families/*.md`). The set
grows automatically as more pages are added -- just re-run this script.

For each referenced abbreviation it collects:
  - full name         (raw/notes/delegates.txt, fallback: attendee lists)
  - organization(s)   (TG2 attendee lists + plenary attendee tables)
  - champion drafts   (proposals whose frontmatter `champions` lists the abbr)
  - mentioned on      (proposal/family pages whose body references the abbr)
  - TG2 meetings      (raw/ecma402/meetings/notes-<date>.md attendee lists;
                       linked to wiki/meetings/<YYYY>/<date>.md when a
                       summary exists)
  - plenary meetings  (raw/notes/meetings/<YYYY-MM>/ attendee tables)

Caveat: early TG2 notes (2017-2020) sometimes use ad-hoc abbreviations that
differ from delegates.txt (e.g. SC for Shane Carr, later SFC). Attendance is
keyed by the abbreviation as written, so those early calls are not counted.

Output: wiki/people/<ABBR>.md. These files are GENERATED -- do not hand-edit;
re-run instead.

Usage:  python3 tools/extract_people.py
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
NOTES = ROOT / "raw" / "notes"
PLENARY = NOTES / "meetings"
TG2 = ROOT / "raw" / "ecma402" / "meetings"
DELEGATES = NOTES / "delegates.txt"
PROPOSALS = ROOT / "wiki" / "proposals"
FAMILIES = ROOT / "wiki" / "families"
WIKI_MEETINGS = ROOT / "wiki" / "meetings"
OUT_DIR = ROOT / "wiki" / "people"

ABBR_TOKEN = re.compile(r"[A-Z][A-Z0-9]{1,4}")
REF_TOKEN = re.compile(r"(?<![A-Za-z0-9_#@.\[\]])([A-Z][A-Z0-9]{1,4})(?![A-Za-z0-9_])")
WIKILINK = re.compile(r"\[\[([A-Z][A-Z0-9]{1,4})(?:\|[^\]]*)?\]\]")
PEOPLE_LINK = re.compile(r"/people/([A-Z][A-Z0-9]{1,4})\.md")
TG2_FILE = re.compile(r"^notes-(\d{4}-\d{2}-\d{2})\.md$")
PAREN_ABBR = re.compile(r"\(([A-Z][A-Z0-9]{1,4})\)")

# Acronyms that collide with delegate abbreviations but are common nouns in
# prose (e.g. "API surface", "ICU data"). Never treat these as person refs.
NON_PERSON = {
    "API", "JS", "JSON", "CSS", "HTML", "IDL", "RFC", "GC", "DOM", "URL",
    "UTC", "ISO", "TG", "TG1", "TG2", "ES", "IO", "OS", "UI", "ID", "ECMA",
    "IETF", "CLDR", "ICU", "ICU4X", "ICU4C", "ICU4J", "MF2", "MFWG",
    "UTS", "UTR", "BCP", "BCP47", "IANA", "TZ", "TZDB", "W3C", "MDN", "NFC",
    "NFD", "WG", "WHATWG", "CSP", "PR", "PRS", "TC", "TC39", "CLI", "AO",
    "JIT", "TS", "VM", "BTW", "LDML", "UCD", "CJK", "RTL", "LTR",
    # Ad-hoc / mistyped TG2 abbreviations that pages normalise (AGENTS.md
    # "Known mappings") and may cite in parentheses; never person pages.
    "SC", "FT", "YFT", "FTY", "USH", "ZBI", "PCO", "PRC", "HSI", "HSJ",
    "HYS", "DMN", "YSK", "JNM", "EAIO", "SFO", "LFS",
}

# Real delegate abbreviations that usually mean something else in prose. They
# are never picked up from bare text; a page is generated only when the abbr
# is linked by hand ([MF](../people/MF.md)) or listed in `champions`.
# link_people.py imports this set and never auto-links these tokens.
AMBIGUOUS = {
    "JSC",  # JavaScriptCore, rarely J. S. Choi
    "MF",   # MessageFormat, or Michael Ficarra
    "MGR",  # TG2 2025 notes: Manish Goregaokar; delegates.txt: Mira Gross
}


def load_delegates():
    """abbr -> full name, from 'Full Name (ABBR)' lines."""
    out = {}
    if not DELEGATES.exists():
        return out
    for line in DELEGATES.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^(.*?)\s*\(([A-Z][A-Za-z0-9?]{0,5})\)\s*$", line.strip())
        if m:
            out[m.group(2)] = m.group(1).strip()
    return out


def entry(data, abbr):
    return data.setdefault(
        abbr, {"orgs": set(), "plenary": set(), "tg2": set(), "names": set()}
    )


def scan_plenary(data):
    """Plenary attendee tables: | Name | ABBR | Org |."""
    for mdir in sorted(PLENARY.iterdir()):
        if not (mdir.is_dir() and re.match(r"\d{4}-\d{2}", mdir.name)):
            continue
        for f in mdir.glob("*.md"):
            if f.name in ("toc.md", "README.md"):
                continue
            for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
                if not line.startswith("|"):
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) < 2:
                    continue
                name, abbr = cells[0], cells[1]
                org = cells[2] if len(cells) >= 3 else ""
                if not ABBR_TOKEN.fullmatch(abbr):
                    continue
                d = entry(data, abbr)
                d["plenary"].add(mdir.name)
                if org and not set(org) <= set("-:? "):
                    d["orgs"].add(org)
                if name and not set(name) <= set("-: "):
                    d["names"].add(name)


def parse_tg2_attendee(line):
    """'- Shane Carr - Google i18n (SFC), Moderator' -> (abbr, name, org)."""
    body = line.strip().lstrip("-* ").strip()
    m = PAREN_ABBR.search(body)
    if not m:
        return None
    abbr = m.group(1)
    before = body[: m.start()].strip(" -,")
    after = body[m.end():].strip(" -,")
    if " - " in before:
        name, org = before.split(" - ", 1)
    else:
        name, org = before, after.split(",")[0] if after else ""
    org = re.sub(r"\s*github\.com/\S+", "", org).strip(" -,")
    return abbr, name.strip(), org.strip()


def scan_tg2(data):
    """TG2 attendee bullet lists under an 'Attendees' heading/line."""
    for f in sorted(TG2.glob("notes-*.md")):
        m = TG2_FILE.match(f.name)
        if not m:
            continue
        date = m.group(1)
        capturing = False
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if re.search(r"attendees", line, re.IGNORECASE) and not line.lstrip().startswith(("-", "*")):
                capturing = True
                continue
            if not capturing:
                continue
            if line.startswith("#") or re.match(r"^\d+\.\s", line):
                break
            if not line.lstrip().startswith(("-", "*")):
                continue
            parsed = parse_tg2_attendee(line)
            if not parsed:
                continue
            abbr, name, org = parsed
            d = entry(data, abbr)
            d["tg2"].add(date)
            if org:
                d["orgs"].add(org)
            if name:
                d["names"].add(name)


def parse_frontmatter(text):
    fm = {"title": None, "slug": None, "champions": []}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                m = re.match(r"^(\w+):\s*(.*)$", line)
                if not m:
                    continue
                k, v = m.group(1), m.group(2).strip()
                if k in ("title", "slug"):
                    fm[k] = v
                elif k == "champions":
                    fm["champions"] = [x.strip() for x in v.strip("[]").split(",") if x.strip()]
            return fm, text[end + 4:]
    return fm, text


def refs_in(text, roster, champions=()):
    tokens = set(REF_TOKEN.findall(text)) - AMBIGUOUS
    tokens |= set(WIKILINK.findall(text)) | set(PEOPLE_LINK.findall(text)) | set(champions)
    return (tokens & roster) - NON_PERSON


def summary_path(date):
    """wiki/meetings/<YYYY>/<date>.md if a TG2 summary exists, else None."""
    p = WIKI_MEETINGS / date[:4] / f"{date}.md"
    return p if p.exists() else None


def main():
    delegates = load_delegates()
    attendance = {}
    scan_plenary(attendance)
    scan_tg2(attendance)
    roster = set(delegates) | set(attendance)

    proposals = []  # (slug, title, champions, refs)
    referenced = set()
    for pf in sorted(PROPOSALS.glob("*.md")):
        if pf.name == "index.md":
            continue
        text = pf.read_text(encoding="utf-8", errors="replace")
        fm, _ = parse_frontmatter(text)
        tokens = refs_in(text, roster, fm["champions"])
        proposals.append((fm["slug"] or pf.stem, fm["title"] or pf.stem, set(fm["champions"]), tokens))
        referenced |= tokens

    families = []
    if FAMILIES.is_dir():
        for ff in sorted(FAMILIES.glob("*.md")):
            text = ff.read_text(encoding="utf-8", errors="replace")
            fm, _ = parse_frontmatter(text)
            tokens = refs_in(text, roster)
            families.append((fm["slug"] or ff.stem, fm["title"] or ff.stem, tokens))
            referenced |= tokens

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.md"):
        old.unlink()
    if not referenced:
        print("no referenced delegates found in wiki/proposals/ or wiki/families/")
        return

    empty = {"orgs": set(), "plenary": set(), "tg2": set(), "names": set()}
    for abbr in sorted(referenced):
        att = attendance.get(abbr, empty)
        name = delegates.get(abbr) or (max(att["names"], key=len) if att["names"] else "(unknown)")
        orgs = sorted(att["orgs"])
        tg2 = sorted(att["tg2"])
        plenary = sorted(att["plenary"])
        champ_of = [(s, t) for (s, t, ch, _r) in proposals if abbr in ch]
        appears_in = [(s, t) for (s, t, _c, ref) in proposals if abbr in ref]
        fam_in = [(s, t) for (s, t, ref) in families if abbr in ref]

        L = [
            "---",
            f"abbr: {abbr}",
            f"name: {name}",
            f"orgs: [{', '.join(orgs)}]",
            f"tg2_meetings_attended: {len(tg2)}",
            f"plenary_meetings_attended: {len(plenary)}",
            "tags: [person]",
            "---",
            "",
            f"# {abbr} — {name}",
            "",
            f"- **Full name**: {name}",
            f"- **Affiliation**: {' / '.join(orgs) if orgs else '(not identifiable from attendee lists)'}",
        ]
        if champ_of:
            L.append("- **Champion drafts**: " + ", ".join(f"[{t}](../proposals/{s}.md)" for s, t in champ_of))
        else:
            L.append("- **Champion drafts**: (none among curated pages)")
        if appears_in:
            L.append("- **Mentioned on proposal pages**: " + ", ".join(f"[{t}](../proposals/{s}.md)" for s, t in appears_in))
        if fam_in:
            L.append("- **Mentioned on family pages**: " + ", ".join(f"[{t}](../families/{s}.md)" for s, t in fam_in))
        L.append(f"- **TG2 meetings attended**: {len(tg2)}")
        L.append(f"- **Plenary meetings attended**: {len(plenary)}")
        L.append("")
        if tg2:
            L += ["## TG2 meetings attended", ""]
            for date in reversed(tg2):
                L.append(f"- [{date}](../meetings/{date[:4]}/{date}.md)" if summary_path(date) else f"- {date}")
            L.append("")
        if plenary:
            L += ["## Plenary meetings attended", "", ", ".join(reversed(plenary)), ""]
        L.append(
            "> Generated by `tools/extract_people.py`. Full name from `raw/notes/delegates.txt`; affiliation and "
            "attendance from TG2 attendee lists (`raw/ecma402/meetings`) and plenary attendee tables (`raw/notes`). "
            "Champion drafts are cross-referenced from proposal frontmatter `champions`. Do not edit by hand; regenerate."
        )
        L.append("")
        (OUT_DIR / f"{abbr}.md").write_text("\n".join(L), encoding="utf-8")

    print(f"roster size: {len(roster)}  referenced: {len(referenced)}")
    print(f"wrote {len(referenced)} person pages to {OUT_DIR.relative_to(ROOT)}/")
    print("referenced:", " ".join(sorted(referenced)))


if __name__ == "__main__":
    main()
