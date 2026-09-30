# Log

Append-only record of operations on this wiki. Each entry starts with `## [YYYY-MM-DD] <operation> | <target>` so `grep "^## \[" wiki/log.md | tail -5` shows the latest entries.

## [2026-09-30] wiki | bootstrap

- Created the ECMA-402 wiki modelled on Jxck/tc39-llm-wiki.
- Raw sources as submodules: `raw/ecma402` (tc39/ecma402 @ e463f3c, TG2 notes through 2026-09-17), `raw/notes` (tc39/notes @ 53a59ad, plenary through 2026-07), `raw/proposals` (tc39/proposals @ ac9b6b5).
- Tools: `extract_tg2_agenda.py` (new; handles list-style 2017-2019 and heading-style notes), `extract_plenary_agenda.py` (new; ECMA-402 heading filter), `extract_proposals.py` (ECMA-402 only, all stages), `extract_people.py` (adds TG2 attendee lists), `link_people.py`, `link_proposals.py`.
- Generated: TG2 agenda index (106 meetings), plenary ECMA-402 agenda index, proposal stage index (36 proposals).

## [2026-09-30] wiki | tool fixes from the DurationFormat shake-down

- `extract_plenary_agenda.py`: harvested identifiers also match their spaced form (`Duration ?Format`), so 2020-02 "Time Duration Format Proposal for Stage 1" is now indexed; "Stage N reviewers" lines no longer count as stage signals (281 items).
- `extract_tg2_agenda.py`: every topic line carries its date and the repos/issues it cites (e.g. `[proposal-intl-duration-format#19]`), so issue-titled topics are greppable by proposal repo; reviewer lines excluded from stage signals.
- `extract_people.py` / `link_people.py`: new shared `AMBIGUOUS` set (`JSC`, `MF`) — never detected or linked from bare text, only via hand links / `champions`. `JSC` moved there from `NON_PERSON`; `MF` moved out of `NON_PERSON` so Michael Ficarra can be linked by hand (done on the DurationFormat page). `??` org cells ignored.
- AGENTS.md: real DurationFormat example rows/chart; no H1 rule; `first_seen` / champions / pre-Stage-1 / Stage 3 update row rules; known early-TG2 abbreviation mappings; grep the proposal repo name and spaced names; quote speaker-prefix linking is accepted.
