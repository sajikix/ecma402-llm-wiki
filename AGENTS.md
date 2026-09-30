# ECMA-402 Wiki — Agent Schema

This repository uses the ECMA-402 task group (TG2) meeting notes, the TC39 plenary notes, and the canonical proposal list as raw material for a wiki that an LLM builds and maintains, one that lets you trace **how each ECMA-402 (Intl) proposal changed stage over time, what was debated in TG2 and at plenary, and how it was resolved**. It is modelled on [Jxck/tc39-llm-wiki](https://github.com/Jxck/tc39-llm-wiki); see [llm-wiki.md](llm-wiki.md) for the design rationale.

This file is the wiki's operating schema. A new session should read this first and follow it when doing ingest / query / lint / update / summarise.

## Layers

- **Raw sources** — `raw/` (a set of submodules). **Read-only, immutable**. Never edit. This is the ground-truth material.
  - `raw/ecma402/` (tc39/ecma402) — the ECMA-402 spec source (`spec/*.html`) and **TG2 monthly meeting notes** (`meetings/notes-<YYYY-MM-DD>.md`, 2017-12 onward). **The primary source for design discussion, issues, TG2 approvals of normative PRs, and TG2's recommendations to plenary**.
  - `raw/notes/` (tc39/notes) — verbatim TC39 plenary transcripts. **The primary source for stage transitions** (stage advancement is decided at plenary, not in TG2) and for plenary-level concerns raised by delegates outside TG2. Also the source of `delegates.txt` (abbreviation → full name).
  - `raw/proposals/` (tc39/proposals) — the canonical proposal list. **`raw/proposals/ecma402/`** is the main scope. **The primary source for a proposal's confirmed current stage / status / champion**.
  - **ECMA-262 proposals with a large ECMA-402 surface** (e.g. Amount, Decimal, Temporal) may also get a page when TG2 discusses them substantially. Their canonical entry is in the ECMA-262 tables (`raw/proposals/README.md`, `stage-1-proposals.md`, `finished-proposals.md`, `inactive-proposals.md`); set `ecma: [262]` (or `[262, 402]` if they change ECMA-402 text) and focus the page on the TG2/Intl side while still recording all plenary transitions.
- **The wiki** — `wiki/`. Fully owned by the LLM. It generates/updates proposal pages, family pages, meeting summaries, indexes, and the log.
- **Generated** — `wiki/_generated/`, `wiki/people/`, `wiki/proposals/index.md`. Machine-extracted output from `tools/` scripts. **Do not hand-edit** (regeneration overwrites it).

**Precedence between sources**: which one to trust when they disagree.

- The year/month and direction of **stage transitions** → **`raw/notes`** (plenary) is primary. TG2 notes often say "we will ask for Stage N at the next plenary" or "TG2 supports Stage N" — that is a recommendation, not the transition. Record the transition at the plenary where consensus was reached.
- **Design issues, alternatives considered, and who argued what** → **`raw/ecma402/meetings`** (TG2) is primary; plenary is primary for concerns raised there.
- A proposal's confirmed **current stage (`current_stage` / `status`) and champion** → **`raw/proposals/ecma402`** is primary. If a current stage inferred from notes disagrees, first suspect the notes-side reading and re-trace both.
- `raw/proposals` is a **current snapshot** with no history; the notes tell the history but are weak for confirming the current stage. Cross-check both rather than filling in from just one.
- **Canonical lag**: `raw/proposals` is edited by hand after each plenary and can lag. If a plenary `Conclusion` clearly records a transition that the canonical table doesn't reflect yet (e.g. Stable Formatting and Intl Sequence Units reached Stage 2 at the 2026-05 plenary while `raw/proposals/ecma402` still lists them under Stage 1), use the plenary result for `current_stage` / `status`, add `canonical_stage: <stage in raw/proposals>` to the frontmatter, and say so in the chart note. Remove `canonical_stage` once the canonical table catches up (Lint checks this).
- When TG2 and plenary notes disagree on a fact (e.g. a date or what was agreed), the plenary conclusion wins for stage/consensus; otherwise note the discrepancy on the page rather than silently picking one.

## Directory layout

```
raw/ecma402/meetings/notes-<YYYY-MM-DD>.md   TG2 monthly notes (verbatim)
raw/ecma402/meetings/agenda-<YYYY-MM-DD>.md  TG2 agendas (2017-12 .. 2019 only)
raw/ecma402/spec/*.html                      ECMA-402 spec source (ecmarkup)
raw/notes/meetings/<YYYY-MM>/<month-DD>.md   plenary transcripts
raw/notes/delegates.txt                      abbreviation → full name
raw/proposals/ecma402/README.md              active ECMA-402 proposals (Stage 3 / 2.7 / 2 / 1)
raw/proposals/ecma402/finished-proposals.md  Stage 4 (with Expected Publication Year)
raw/proposals/ecma402/stage-0-proposals.md   Stage 0
raw/proposals/ecma402/inactive-proposals.md  withdrawn / inactive
wiki/
  README.md                 proposal catalog (ingested proposals, families, how to use)
  log.md                    chronological ingest/query/lint/update/summarise log (append-only)
  proposals/<slug>.md       a deep-read page per proposal (history + issues)
  proposals/index.md        stage list of all ECMA-402 proposals (generated from raw/proposals/ecma402. Do not hand-edit)
  families/<family>.md      cross-cutting synthesis (bundles multiple proposals)
  meetings/<YYYY>/<YYYY-MM-DD>.md   TG2 meeting summaries (output of summarise. One file per meeting)
  meetings/README.md        list of summarised TG2 meetings
  people/<ABBR>.md          person reference (generated. filename = abbreviation)
  _generated/
    tg2-agenda-index.md       topic index of all TG2 meetings (grep-able backbone)
    tg2-agenda-index.jsonl    the same, machine-readable
    plenary-agenda-index.md   ECMA-402-related agenda items of all plenaries
    plenary-agenda-index.jsonl
tools/
  extract_tg2_agenda.py     generates tg2-agenda-index (handles both the list-style 2017-2019 notes and the heading-style later notes)
  extract_plenary_agenda.py generates plenary-agenda-index (heading filter: Intl/402/locale/... keywords + API identifiers harvested from raw/proposals/ecma402)
  extract_proposals.py      generates wiki/proposals/index.md from raw/proposals/ecma402 (all stages, Stage 4 with publication year)
  extract_people.py         generates people/ pages for people appearing in proposal/family pages
  link_people.py            links abbreviations in proposal/family/meeting-summary pages to [ABBR](<rel>/people/ABBR.md)
  link_proposals.py         links proposal names in meeting summaries to proposal pages, and ensures the topic-opening meta line (wiki → proposal → slide)
```

## Language convention

- Body text (overview, history, discussion of issues, meeting summaries) is **English**.
- **Proposal names, stage notation, API names, option names, spec terminology, and person abbreviations are kept verbatim**. e.g. `Intl.DurationFormat`, `Stage 2.7`, `roundingIncrement`, `[[LocaleData]]`, `SFC`.
- **When quoting a speaker from the notes, keep the original English as-is**. Summaries and paraphrases are also in English.

## Proposal page format

`wiki/proposals/<slug>.md`. `<slug>` is kebab-case English, prefixed with `intl-` when the proposal is an Intl API (e.g. `intl-durationformat`, `intl-locale-info`, `intl-numberformat-v3`, `intl-keep-trailing-zeros`, `stable-formatting`).

YAML frontmatter at the top (for Obsidian Dataview):

```yaml
---
title: Intl.DurationFormat
slug: intl-durationformat
status: shipped        # stage0 | stage1 | stage2 | stage2.7 | stage3 | shipped | withdrawn | inactive
current_stage: 4       # 0 / 1 / 2 / 2.7 / 3 / 4
ecma: [402]            # affected specs ([402], or [262, 402] for cross-spec proposals)
champions: [YMD, USA]  # abbreviations (see "Champions" below)
first_seen: "2016-01"  # earliest TG2/plenary meeting where the idea itself was raised, even informally (YYYY-MM)
reached_stage4: "2024-12"   # plenary month of Stage 4 (omit if not at Stage 4)
publication: 2025      # Expected Publication Year from finished-proposals.md (omit if not at Stage 4)
repo: https://github.com/tc39/proposal-intl-duration-format
families: [date-time]  # families it belongs to (optional, can be multiple. Corresponds both ways with wiki/families/<family>.md)
tags: [proposal, intl]
---
```

No `# H1` after the frontmatter (the `title` is the page title). Body sections (headings are fixed, in English):

1. `## Overview` — 1-3 paragraphs. What problem the proposal solves and the API shape (a short code example is welcome).
2. `## Stage history` — a chronological table, one row per event. **Both plenary and TG2 events go in the same table**, distinguished by the Venue column:

   | Meeting                                                                              | Venue   | Event                                                        | Stage |
   | ------------------------------------------------------------------------------------ | ------- | ------------------------------------------------------------ | ----- |
   | [2020-01-09](https://github.com/tc39/ecma402/blob/main/meetings/notes-2020-01-09.md) | TG2     | TG2 "Stage 1 consensus"; YMD to present in February          | 0     |
   | [2020-02](https://github.com/tc39/notes/blob/main/meetings/2020-02/february-6.md)    | plenary | Reached Stage 1. `Time Duration Format Proposal for Stage 1` | 0 → 1 |

   The meeting cell links to the **GitHub URL** of the source file (`https://github.com/tc39/notes/blob/main/meetings/<YYYY-MM>/<file>.md` for plenary, `https://github.com/tc39/ecma402/blob/main/meetings/notes-<YYYY-MM-DD>.md` for TG2), so links work on GitHub even without submodules checked out. Plenary rows use `YYYY-MM`, TG2 rows use `YYYY-MM-DD`. The Stage column records a transition as `old → new` (**plenary rows only** — TG2 cannot change stage), or just the current stage for an update-only row (pre-Stage-1 rows use `0`). Keep TG2 rows to the milestones (recommendations to plenary, major design decisions, significant reversals); don't list every TG2 call. Plenary Stage 3 update slots get a row when they carried a normative change or consensus; skip pure "no news" updates. When the notes contradict each other (e.g. a champion's slide misstates an earlier date), trust the plenary conclusion of that meeting and mention the discrepancy in the chart note.

3. Stage-history chart — embed a mermaid `xychart-beta` line chart right below the table. **The x-axis is fixed to 2012-2026** (ECMA-402 1st edition, 2012, through the present), and the y-axis is Stage (0-4). Plot the stage as of the end of each year; a year in which the proposal didn't exist yet is 0. Plot Stage 2.7 as `2.7`. **For a withdrawn proposal, stop the line at the withdrawal year**. Right after the chart, add a `>` note on how to read it (the year/month of each transition). Example:

   ````
   ```mermaid
   xychart-beta
       title "Intl.DurationFormat stage 2012-2026"
       x-axis [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
       y-axis "Stage" 0 --> 4
       line [0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3, 4, 4, 4]
   ```
   ````

   Note: `xychart-beta` requires mermaid 10.3+ and rendering is renderer-dependent. Use ASCII for the title.

4. `## Main issues` — points that became contentious during development. One subheading `### <issue name (English)>` per issue. For each: what was at stake / who raised concerns (abbreviation) / at which meeting (TG2 or plenary) / how it was resolved (or that it's unresolved). Link the GitHub issue/PR number when the notes cite one (e.g. `proposal-intl-duration-format#55`). Quote with `>` (kept in the original English).
   **Champions**: frontmatter `champions` = the canonical champions from `raw/proposals` plus historical champions who have since left (keep them) plus people the notes explicitly show as champions (a self-declaration such as SFC's "I'm champion of the amount proposal", a recognised request to join the champion group, or a plenary Conclusion / Speaker's Summary that calls the presenters "the champions") even if the canonical table doesn't list them yet — say so in the Overview. Presenters, co-authors and spec contributors who are never called champions (e.g. BAN presenting DurationFormat PRs on USA's behalf, JMN on Amount) are mentioned in the text only.

5. `## Related proposals` — cross-links in the form `[Title](other-slug.md)` (a proposal not yet created is written as plain code-formatted text).
6. `## Sources` — a bulleted list of the meeting files referenced, split into `TG2:` and `Plenary:` groups, each as GitHub URLs.

Link convention: **always use standard markdown relative links** within the wiki (no Obsidian `[[wikilink]]` syntax). **Links to raw sources use GitHub URLs** (above), not relative `raw/` paths.

- Between proposals: `[Intl.Locale](intl-locale.md)` (from proposals/), `[Intl.Locale](../proposals/intl-locale.md)` (from families/). A proposal without a page yet is plain code-formatted text (e.g. `` `intl-segmenter` ``) until created.
- Person abbreviations: `[SFC](../people/SFC.md)`. Linking is done by `tools/link_people.py`, not by hand. Frontmatter's `champions` stays as plain abbreviations.

## Family page format

`wiki/families/<family>.md`. A **cross-cutting synthesis page** that bundles a group of related proposals and spec areas. Suggested families for ECMA-402: `number-format` (NumberFormat, PluralRules, trailing zeros, units), `date-time` (DateTimeFormat options, formatRange, DurationFormat, era/monthCode, Temporal integration), `locale` (Intl.Locale, Locale Info, LocaleMatcher, Enumeration, DisplayNames), `text` (Segmenter, Collator, ListFormat), `message-format` (MessageFormat, MessageResource), `stable-formatting` (Stable Formatting, default behaviours). Each proposal's own history/issues stay in `proposals/`; a family page only links to them (don't duplicate stage tables or charts).

YAML frontmatter:

```yaml
---
title: Number formatting
slug: number-format
kind: family
members: [intl-numberformat-v3, intl-keep-trailing-zeros, ...]  # proposal slugs (pages may not exist yet)
tags: [family, number-format]
---
```

Body sections (headings are fixed, in English):

1. `## Overview` — what the members have in common.
2. `## Members` — a table `Proposal | Current stage | One-liner`.
3. `## Cross-cutting themes` — design principles/issues that run through the family (e.g. "options bag conventions", "how much locale data may vary across implementations", ICU/ICU4X/CLDR dependency, the web-compat cost of changing output).
4. `## Related families`.
5. `## Sources` (optional).

**Membership is bidirectional**: keep each family page's `members` in sync with each proposal's frontmatter `families`. `wiki/README.md` has a families section linking to each family.

## Meeting summary format (TG2)

`wiki/meetings/<YYYY>/<YYYY-MM-DD>.md`, one file per TG2 meeting (TG2 calls are single-session).

```yaml
---
title: TG2 meeting 2026-09-17
date: "2026-09-17"
kind: tg2-meeting
source: https://github.com/tc39/ecma402/blob/main/meetings/notes-2026-09-17.md
attendees: [SFC, JMN, MP, YSZ, CDA, EAO]
tags: [meeting, tg2]
---
```

Then a one-paragraph `## Overview` (moderator, main outcomes), followed by one `##` section per discussion topic (the topic's original heading, kept in English):

- Place the opening meta bullet list in **wiki → proposal → slide order** (omit any that don't apply; labels are lowercase): `- wiki: [Title](../../proposals/<slug>.md)`, `- proposal: [name](URL)` / a PR or issue URL, `- slide: [link](URL)`. `tools/link_proposals.py` adds the `wiki:` bullet automatically when the heading names a proposal that has a page, or when the `- proposal:` URL points into a page's `repo` (so issue-titled topics are covered — keep the proposal bullet's URL precise).
- Follow with a **2-5 line** summary in English. Person abbreviations and proposal names may be plain text (the link scripts handle them).
- If there's a `#### Conclusion`, **always include it** (e.g. "TG2 approval", "TG2 supports Stage 2.7").
- Standing items with no real discussion (Standing items, logistics, empty status updates) may be omitted; keep Editors' / Implementers' / MessageFormat WG updates when they carry content.

`wiki/meetings/README.md` lists the summarised meetings (newest first) with a one-line gist each, followed by a `## Summary backlog` table (`| Date | Referenced by |`, oldest first) of TG2 meetings that proposal pages already cite but that have no summary yet.

## Formatting

Markdown / JSON is formatted with **oxfmt** (config `.oxfmtrc.json`, `proseWrap: preserve`, `embeddedLanguageFormatting: off`). Excluded: `raw/**`, `wiki/_generated/**`, `wiki/proposals/index.md`.

- Manual: `pnpm fmt`, check with `pnpm fmt:check`. (This repo uses **pnpm**, not npm.)
- **Enforced automatically**: Claude Code's PostToolUse hook (`.claude/settings.json`) formats any edited .md/.json file immediately, and git's pre-commit hook (`.githooks/pre-commit`) formats staged files and re-stages them.
- Right after cloning: `git submodule update --init`, `pnpm install`, and `git config core.hooksPath .githooks`.

## Workflow

Each operation has a Claude Code slash command (`.claude/commands/`): **`/ingest <proposal>`**, **`/query <question>`**, **`/lint [target]`**, **`/update [submodule]`**, **`/summarise [TG2 meeting date]`**. The commands hold no procedure of their own — they read the matching workflow in this file and execute it (AGENTS.md is the single source of truth).

**Commit convention**: English message with a prefix chosen by what caused the change:

- Caused by an operation → that operation's name: `[ingest]` / `[query]` / `[lint]` / `[update]` / `[summarise]`.
- A wiki-wide change not caused by any operation → `[wiki]` (commands, `tools/`, repo layout, changes to this file).

Skip committing when there's nothing to commit.

### Ingest (bringing in a proposal)

1. Identify the proposal in `wiki/proposals/index.md` (canonical title, champion, repo). Then grep **both** backbones:
   - `grep -i -A2 -E '<name>|<spaced name>|<proposal-repo>' wiki/_generated/tg2-agenda-index.md` — TG2 topics. Each line carries its date and the repos/issues it cites (`[proposal-intl-duration-format#19]`), so **grep the proposal repo name too**: many TG2 topics are titled only by an issue title and never name the proposal.
   - `grep -i -A4 '<name>' wiki/_generated/plenary-agenda-index.md` — plenary items (stage transitions).
   - The canonical tables' "Meeting Notes" column (`grep -i '<name>' raw/proposals/ecma402/*.md` and the link definitions below the table) lists the plenary anchors directly — use it as a checklist.
   - Names shift over time (e.g. "Intl.UnitFormat" → Unified NumberFormat, "Intl Locale Info" / "Intl.Locale info", "Time Duration Format" vs. "Intl.DurationFormat"), and the plenary index filter is heading-based. The canonical Meeting Notes column can also omit early meetings (DurationFormat's Stage 1 at 2020-02 is missing there). When in doubt, `grep -ril -E '<name>|<spaced name>' raw/ecma402/meetings raw/notes/meetings`.
2. Read the matching sections. For plenary, `### Conclusion` / `### Speaker's Summary of Key Points` are key for judging the stage. For TG2, `#### Conclusion`.
3. Create or update the proposal page (format above). Keep quotes in the original English.
   - **Don't settle a champion from delegates.txt alone**. Corroborate with the meeting's presenter and body text.
   - Early TG2 notes (2017-2020) use ad-hoc abbreviations; normalise to the delegates.txt abbreviation in the wiki. Known mappings: `SC` → SFC (Shane Carr; also in plenary 2021-04), `FT` / `YFT` / `FTY` → FYT (Frank Yung-Fong Tang), `USH` → USA (Ujjwal Sharma), `ZBI` → ZB (Zibi Braniecki), `LB` (2020-01-09) → LEO (Leo Balter; delegates.txt's LB is Lee Byron). Recent TG2 typos: `PCO`/`PRC` → PFC, `HSI`/`HSJ`/`HYS` → HJS, `DMN` → DLM, `YSK` → YSZ, `JNM` → JMN, `EAIO` → EAO, `SFO` → SFC, `LFS` → LAF, `FYC` / `FYI` → FYT. Collision: `MGR` in 2025 TG2 notes is Manish Goregaokar, but delegates.txt's MGR is Mira Gross (in `AMBIGUOUS`). Other abbreviations not in delegates.txt (e.g. `MGM`, `KAP`, `ECH`) are kept as written in the notes. Add new mappings here when found.
   - Verify speaker attribution and dates against the original text.
4. **Generate and link people** (always run once the page is written):
   - `python3 tools/extract_people.py` then `python3 tools/link_people.py` then `python3 tools/link_proposals.py`.
   - Acronyms that are never people (`ICU`, `CLDR`, `MF2`, ...) go in `extract_people.py`'s `NON_PERSON`. Real delegate abbreviations that usually mean something else (`JSC` = JavaScriptCore, `MF` = MessageFormat vs. Michael Ficarra) go in its `AMBIGUOUS` (shared with `link_people.py`): they are never detected or linked from bare text, so link the person occurrences by hand (`[MF](../people/MF.md)`) and re-run the scripts.
5. Run `python3 tools/extract_proposals.py` so `wiki/proposals/index.md` links the new page (add to its `ALIASES` if the page title differs from the canonical title).
6. Update the catalog row in `wiki/README.md` (and the family page, if any).
7. **Unsummarised TG2 meetings**: ingest never waits for summaries — read the raw notes directly (the page links to GitHub URLs, so it works without a summary). Then, for every TG2 meeting the page cites that has no `wiki/meetings/<YYYY>/<date>.md` yet, add it to the `## Summary backlog` table in `wiki/meetings/README.md` (or append this proposal's slug to its "Referenced by" cell if already listed). Don't summarise them as part of the ingest.
8. Append an entry to `wiki/log.md` (mention how many meetings were added to the backlog).

### Query (answering a question)

1. Dig in this order: `wiki/README.md` → relevant proposal / family pages → `wiki/proposals/index.md` → the two agenda indexes → `raw/`.
2. Answer with sources (meeting links) attached. For questions about the _current spec text_, read `raw/ecma402/spec/*.html` directly.
3. If the answer contains valuable analysis, **ask the user at the end whether to keep it as a wiki page** (never add it unprompted). If yes, file it back and update `wiki/README.md` / `wiki/log.md`.

### Lint (health check)

**(a) Internal health**

- Contradictions between pages, stale statements, orphan pages, missing cross-links, dangling issues.
- Important proposals in `wiki/proposals/index.md` (especially Stage 2+) without a page yet.
- Bidirectional family consistency (family `members` ↔ proposal `families`).

**(b) Consistency with sources**

- Verify each proposal page's claims against the source notes, **looking to find errors**; fix the wiki treating raw as ground truth. Error-prone spots: stage transition year/month and direction, TG2 recommendation mistaken for a plenary transition, champion identification, early-TG2 abbreviation mismatches, speaker attribution, quote accuracy.
- Cross-check frontmatter `current_stage` / `status` / `champions` / `publication` against `raw/proposals/ecma402/`. Which table a proposal appears in indicates its current stage. `champions` must **cover** the canonical champions; keep historical champions no longer listed (canonical is a snapshot).

After material updates, regenerate: `python3 tools/extract_tg2_agenda.py && python3 tools/extract_plenary_agenda.py && python3 tools/extract_proposals.py && python3 tools/extract_people.py && python3 tools/link_people.py && python3 tools/link_proposals.py`.

### Update (syncing raw sources)

Pull the submodules under `raw/` to latest and show **the diff since the last sync** (= the committed submodule pointers).

1. Note the pointers before syncing: `git submodule status` (call each SHA OLD).
2. Pull: `git -C raw/<sub> checkout main && git -C raw/<sub> pull --ff-only` for each of `ecma402`, `notes`, `proposals` (or `git submodule update --remote`). If `raw/notes` sits on an unmerged PR branch (`pr-<N>`), switch back to main once merged.
3. **Show the diff**: `git -C raw/<sub> log --oneline OLD..HEAD` and `git -C raw/<sub> diff --stat OLD..HEAD`. Highlight especially **new TG2 notes (`raw/ecma402/meetings/notes-*.md`)**, **new plenary meetings that contain ECMA-402 items**, **changes under `raw/proposals/ecma402/`** (stage changes), and **normative changes to `raw/ecma402/spec/`**. If there's no diff, say "up to date" and skip the commit.
4. If a pointer moved, commit (`[update]`), then regenerate all generated files (command in Lint above). Always re-run `extract_proposals.py` if `raw/proposals` moved.
5. Record an entry in `wiki/log.md`. Suggest follow-up `/summarise` for new TG2 meetings and `/ingest` for proposals whose stage changed.

### Summarise (TG2 meeting summaries)

Summarise one TG2 meeting topic-by-topic (distinct from proposal-centric Ingest). Target: a date (`YYYY-MM-DD`), a month (`YYYY-MM`, all TG2 meetings in that month), or unspecified (= the **latest** `raw/ecma402/meetings/notes-*.md`).

1. Read `raw/ecma402/meetings/notes-<date>.md`.
2. Write `wiki/meetings/<YYYY>/<date>.md` in the format above.
3. Add the meeting to `wiki/meetings/README.md`, and remove it from the `## Summary backlog` table if it was listed there. With no target given, `/summarise` may also take the oldest backlog entry instead of the latest meeting when the user asks to "work the backlog".
4. **Generate links**: `python3 tools/extract_people.py && python3 tools/link_people.py && python3 tools/link_proposals.py` (people pages link TG2 attendance to existing summaries).
5. Commit with `[summarise]` and record it in `wiki/log.md`.

Plenary meetings are not summarised as a whole here (that's tc39-llm-wiki's job); their ECMA-402 items are captured via proposal pages and `plenary-agenda-index.md`.

## Person pages (people/)

`wiki/people/<ABBR>.md` is **generated** for abbreviations appearing on proposal and family pages: full name (delegates.txt), affiliation (TG2 attendee lists + plenary attendee tables), champion drafts, pages mentioning them, TG2 meetings attended (linked when summarised), plenary meetings attended.

- Only people who actually appear in the wiki get a page. Early TG2 calls that used ad-hoc abbreviations are not counted in attendance (limitation, not an error).
- `link_people.py` only links abbreviations that have a page, and skips `AMBIGUOUS` tokens (defined in `extract_people.py`). It also links speaker prefixes inside `>` quotes (`> [ZB](../people/ZB.md): ...`); that is the only accepted alteration of a verbatim quote.
- Don't hand-edit; change the script instead.

## Stage list of all proposals (proposals/index.md)

`wiki/proposals/index.md` is **generated by `extract_proposals.py` from `raw/proposals/ecma402/`**. ECMA-402 has only a few dozen proposals, so every stage is listed in full, including all Stage 4 proposals with their Expected Publication Year; rows with a publication year of the current year or later are marked ⏳ (not yet in a ratified edition).

- Ingested ECMA-262 proposals are listed in a trailing "Related ECMA-262 proposals (ingested)" section, taken from the page frontmatter (not from the ECMA-262 tables).
- ES-edition rule: a proposal at Stage 4 and merged by the end-of-March freeze goes into that year's edition, approved at the end-of-June Ecma GA (e.g. ES2026 = ECMA-402 13th edition). The **Expected Publication Year** is the definitive signal of which edition a proposal ships in — except that the canonical table can be optimistic: Intl Era/Month Code reached Stage 4 in 2026-03 and is listed for 2026, but its text rides on the Temporal ECMA-402 PR and missed the ES2026 cut. Record such discrepancies on the page.

## Using the backbones (important)

- `wiki/_generated/tg2-agenda-index.md` — every TG2 topic (106+ meetings). Topics are shown as `section › heading`; the section tells you whether it was a proposal discussion, a normative PR, a status update, etc.
- `wiki/_generated/plenary-agenda-index.md` — only the ECMA-402-related plenary items (heading-filtered, so it can miss items; fall back to `grep -ril`).

These are indexes, not substitutes for reading. Grep them first, then read the original notes.

## ECMA-402 specifics (reference)

- **TG2** (formerly "ECMA-402 task group") meets monthly. It gives "TG2 approval" to normative PRs against ECMA-402 before they go to plenary as needs-consensus PRs, and discusses proposals before stage requests. Moderators/chairs and editors change over time — take them from the notes.
- Stages follow the TC39 process: **Stage 0** / **1** Proposal / **2** Draft / **2.7** (introduced 2023-11) awaiting tests & spec review / **3** Candidate / **4** Finished. Before 2023-11 proposals went directly from 2 to 3.
- Much of ECMA-402's evolution happens through **normative PRs** rather than proposals (e.g. new options on existing constructors). These appear in TG2 notes as `PR #NNN` / `Normative: ...` topics. They are recorded on the relevant proposal or family page when they matter, not as standalone pages (for now).
- Recurring external dependencies: **CLDR** (locale data), **ICU / ICU4X** (implementations), **Unicode MessageFormat 2** (MFWG), **IETF BCP 47**, **IANA tzdb**, **Temporal** (ECMA-262 proposal with large ECMA-402 surface).

## Scope note

The material spans TG2 notes 2017-12 onward (106 meetings as of 2026-09) and plenary notes 2012 onward. Deep reading happens incrementally. Proposals deep-read so far are listed in `wiki/README.md`'s "Ingested proposals" section; the rest are reachable via `wiki/proposals/index.md` and the agenda indexes.
