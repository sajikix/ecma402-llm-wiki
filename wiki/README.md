# ECMA-402 Wiki — Index

A wiki for tracing **how each ECMA-402 (Intl) proposal changed stage, what was debated in TG2 and at plenary, and how it was resolved**, drawn from the TG2 monthly notes (`raw/ecma402/meetings`, 2017-12 onward / 106 meetings), the TC39 plenary notes (`raw/notes`), and the canonical proposal list (`raw/proposals/ecma402`). The operating rules are [AGENTS.md](../AGENTS.md); the design notes are [llm-wiki.md](../llm-wiki.md).

## How to use

- **List every ECMA-402 proposal's current stage** → [proposals/index.md](proposals/index.md) (generated from `raw/proposals/ecma402`; ingested proposals are bold links).
- **Follow one proposal** → the "Ingested proposals" table below. Each page has `## Stage history` (TG2 + plenary timeline and a mermaid chart) and `## Main issues`.
- **Follow a person** → a person link on a proposal page (e.g. `[SFC](people/SFC.md)`) opens a [people/](people/) page.
- **Find what TG2 discussed** → grep [\_generated/tg2-agenda-index.md](_generated/tg2-agenda-index.md) (every topic of every TG2 call), e.g. `grep -i -B1 -A3 'segmenter' wiki/_generated/tg2-agenda-index.md`.
- **Find plenary stage decisions** → grep [\_generated/plenary-agenda-index.md](_generated/plenary-agenda-index.md) (ECMA-402-related plenary items only).
- **Read a TG2 meeting digest** → [meetings/README.md](meetings/README.md).
- **Ingest a new proposal** → `/ingest <name>` (follows "Workflow > Ingest" in AGENTS.md).

## Ingested proposals

| Proposal                                                | Current stage     | Status  | Summary                                                                                                                                                                                                                           |
| ------------------------------------------------------- | ----------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Intl.DurationFormat](proposals/intl-durationformat.md) | Stage 4 (2024-12) | shipped | Locale-aware formatting of compound durations (long/short/narrow/digital, per-unit styles); Stage 3 for three years of implementer-driven fixes (fractionalDigits, negative sign, digital style), decoupled from Temporal; ES2025 |

## Families

(none yet — see AGENTS.md "Family page format" for the suggested families)
