# Log

Append-only record of operations on this wiki. Each entry starts with `## [YYYY-MM-DD] <operation> | <target>` so `grep "^## \[" wiki/log.md | tail -5` shows the latest entries.

## [2026-09-30] wiki | bootstrap

- Created the ECMA-402 wiki modelled on Jxck/tc39-llm-wiki.
- Raw sources as submodules: `raw/ecma402` (tc39/ecma402 @ e463f3c, TG2 notes through 2026-09-17), `raw/notes` (tc39/notes @ 53a59ad, plenary through 2026-07), `raw/proposals` (tc39/proposals @ ac9b6b5).
- Tools: `extract_tg2_agenda.py` (new; handles list-style 2017-2019 and heading-style notes), `extract_plenary_agenda.py` (new; ECMA-402 heading filter), `extract_proposals.py` (ECMA-402 only, all stages), `extract_people.py` (adds TG2 attendee lists), `link_people.py`, `link_proposals.py`.
- Generated: TG2 agenda index (106 meetings), plenary ECMA-402 agenda index, proposal stage index (36 proposals).

## [2026-09-30] ingest | Intl.DurationFormat

- Key transitions (plenary): Stage 1 2020-02 (`2020-02/february-6.md`, "Time Duration Format Proposal for Stage 1" — missed by the plenary index and absent from the canonical Meeting Notes column), Stage 2 2020-06 (`2020-06/june-2.md`), Stage 3 2021-10 (`2021-10/oct-25.md`, conditional on the `fractionalDigits` minimum question), Stage 4 2024-12 (`2024-12/december-02.md`); publication 2025. Eleven Stage 3 update / normative-PR plenary slots in between (2022-06 .. 2024-10), plus a Stage 2 redesign update in 2021-08.
- Main issues: separate class vs. NumberFormat/DateTimeFormat/RelativeTimeFormat; the `"digital"` style (naming, always-display defaults, zero minutes, locale separators, grouping separators PR #198); no arithmetic (rounding/truncation/out-of-range units); `fractionalDigits` (Stage 3 condition, default, plenary approved the wrong change in 2023-05 and reverted it in 2023-07); negative durations (sign on first unit per CLDR, PR #176); coupling with Temporal (borrowed AOs/string parsing, RangeError for strings, plural option names, Temporal.Duration limits); `formatToParts` granularity (PR #126).
- Champions: YMD (2020), USA (from 2021); BAN presented most normative PRs 2023-11 .. 2024-10; FYT volunteered in 2019-11 before YMD took it on.
- People generated (24): ABL BAN BSH DE DLM EAO FYT JGT JHD JSW KG LAF LEO PFC RBN RCA RGN SFC SYG USA WH YMD YSZ ZB. Added `JSC` to `extract_people.py` `NON_PERSON` (JavaScriptCore; already in `link_people.py` `AMBIGUOUS`).

## [2026-09-30] wiki | tool fixes from the DurationFormat shake-down

- `extract_plenary_agenda.py`: harvested identifiers also match their spaced form (`Duration ?Format`), so 2020-02 "Time Duration Format Proposal for Stage 1" is now indexed; "Stage N reviewers" lines no longer count as stage signals (281 items).
- `extract_tg2_agenda.py`: every topic line carries its date and the repos/issues it cites (e.g. `[proposal-intl-duration-format#19]`), so issue-titled topics are greppable by proposal repo; reviewer lines excluded from stage signals.
- `extract_people.py` / `link_people.py`: new shared `AMBIGUOUS` set (`JSC`, `MF`) — never detected or linked from bare text, only via hand links / `champions`. `JSC` moved there from `NON_PERSON`; `MF` moved out of `NON_PERSON` so Michael Ficarra can be linked by hand (done on the DurationFormat page). `??` org cells ignored.
- AGENTS.md: real DurationFormat example rows/chart; no H1 rule; `first_seen` / champions / pre-Stage-1 / Stage 3 update row rules; known early-TG2 abbreviation mappings; grep the proposal repo name and spaced names; quote speaker-prefix linking is accepted.

## [2026-09-30] summarise | TG2 2024-10-24 .. 2026-09-17 (24 meetings)

- Summarised the last two years of TG2 calls into `wiki/meetings/<YYYY>/<date>.md` (2026-09-17 written first as the style reference, the other 23 in parallel batches) and listed them in `wiki/meetings/README.md`.
- Ran `extract_people.py` / `link_people.py` / `link_proposals.py`: person pages now link TG2 attendance to these summaries; three topics gained a `- wiki:` bullet to Intl.DurationFormat.
- Stage-relevant TG2 events seen (plenary transitions still to be confirmed per proposal on ingest): DurationFormat Stage 4 support (2024-11-25); Keep Trailing Zeros Stage 1 support (2025-05-08), Stage 2/2.7 support (2025-07-17), Stage 3 approval pending reviews (2026-02-19); Era/MonthCode 2.7 support (2025-07-17), Stage 4 approval pending PRs (2026-02-19); Locale Info Stage 4 support (2025-10-13); Amount Stage 2 support (2025-07-17); Stable Formatting and Sequence Units Stage 2 support (2026-05-19); Unit Format to be marked withdrawn (2026-01-08); EAO cleared for a datetime-options Stage 1 proposal (2026-07-09).
- Data quirks recorded in the summaries: several notes files have a title date differing from the filename (2024-11-25 = "2024-11-21", 2025-10-13 = "2025-10-09", 2026-05-19 = "2026-05-07"; filename date used). Ad-hoc abbreviations normalised (PCO/PRC → PFC, HSI/HSJ/HYS → HJS, DMN → DLM, YSK → YSZ, JNM → JMN, ZBI → ZB).
- Added `MGR` to `extract_people.py` `AMBIGUOUS` (TG2 2025 notes use it for Manish Goregaokar; delegates.txt's MGR is Mira Gross) and the new typo mappings to AGENTS.md.

## [2026-09-30] ingest | Intl Keep Trailing Zeros

- New page `wiki/proposals/intl-keep-trailing-zeros.md` (champion EAO, sole; families: number-format, family page not created).
- Key transitions (plenary): Stage 1 2025-05 (`2025-05/may-28.md`), Stage 2 2025-07 (`2025-07/july-29.md`), Stage 2.7 2025-07 the next day (`2025-07/july-30.md`, after WH's `ToIntlMathematicalValue` block was split off), Stage 3 2026-05 (`2026-05/may-19.md`, with PRs #19/#20 merged). The 2026-03 slot (`2026-03/march-10.md`) was titled "for Stage 3" but no advancement was requested; TG2's Stage 3 approval (2026-02-19) was a recommendation only. Update slot 2025-11 (`november-18.md`): PR #10 / PR #12 supported in principle, issue #11 accepted.
- Main issues: origins in the Decimal trailing-zeros/normalization debate (2023-11 .. 2024-10) and bug-fix-vs-proposal; how string digits interact with digit options (Intl MV record, PR #10 corner cases); rounding keeping trailing zeros (#11) and the `trailingZeroDisplay: "stripToMinimum"` opt-out (#1, #12); values that round to zero (#15, incl. the 2026-03-19 TG2 dispute over what plenary concluded) and integer trailing zeros (#17); `ToIntlMathematicalValue` limits (ecma402 PR #1022) and PluralRules Intl MV (PR #1026); first proposal through W3C i18n review.
- People generated (8 new): CDA CHU CLA HJS JAD JMN NRO SHS. No NON_PERSON/AMBIGUOUS changes needed.
- Summary backlog: 1 meeting added (2024-07-18), 1 existing row updated (2021-04-08). All other cited TG2 meetings (2025-05-08 onward) already have summaries.
- Hand-added `- wiki:` bullets to six issue-titled Keep Trailing Zeros topics in TG2 summaries 2025-11-06 (four), 2026-02-19 ("keep-trailing-zeroes" spelling), 2026-03-19, which `link_proposals.py` cannot match from the heading.
- Fixed `wiki/meetings/2026/2026-05-19.md`: the plenary "two weeks away" from that call (held 2026-05-07) was the 2026-05-19 plenary, not June.

## [2026-09-30] wiki | summary backlog rule; link_proposals matches proposal repos

- AGENTS.md: ingest reads raw notes regardless of summaries and records cited-but-unsummarised TG2 meetings in the `## Summary backlog` of `wiki/meetings/README.md`; `/summarise` removes entries. Seeded the backlog with the 23 unsummarised TG2 meetings cited by Intl.DurationFormat.
- `link_proposals.py`: also adds the `- wiki:` bullet when a topic's `- proposal:` URL points into a page's frontmatter `repo` (issue-titled topics never name their proposal).
