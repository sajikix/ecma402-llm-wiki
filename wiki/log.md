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

## [2026-09-30] ingest | Stable Formatting

- New page `wiki/proposals/stable-formatting.md` (champion EAO, sole; families: stable-formatting, family page not created).
- Key transitions (plenary): Stage 1 2023-09 (`2023-09/september-27.md`), Stage 2 2026-05 (`2026-05/may-20.md`; Stage 2.7 reviewers RGN, DLM). The 2025-02 update (`2025-02/february-19.md`) settled the `zxx` direction and let PR #18 be merged; no stage change. Canonical lag: `raw/proposals/ecma402` still lists Stage 1, so the page records `canonical_stage: 1`.
- Origin: TG2 2023-06-01 (misuse of localized strings after the NNBSP breakage); presented at TG2 2023-09-07 as "Define the behavior and properties of the “und” root locale" (`eemeli/proposal-intl-root-locale`) and renamed Stable Formatting there. The spin-off Default Behaviours for some Intl APIs (`und` root locale for Collator/Segmenter/case mapping) reached Stage 1 at the same 2026-05 session.
- Main issues: general locale vs. purpose-built APIs (#17); trigger `null`/`und`/`zxx`/`Intl.STABLE` (PR #21); `und` as root vs. host default (ecma402#885, PR #956); stable vs. locale-independent for Collator/Segmenter/case mapping (PR #24); ECMA-402 vs. CLDR ownership of the data; per-API output (SI prefixes, short unit identifiers, DisplayNames holes, DurationFormat "P" strings vs. composed output PR #23, RelativeTimeFormat, `Intl.Locale` iso8601 PR #22); shifting motivation (misuse → testing → determinism).
- Summary backlog: 5 meetings added (2023-06-01, 2023-09-07, 2023-12-14, 2024-02-22, 2024-08-22), 1 existing row updated (2023-11-16).

## [2026-09-30] ingest | Intl Sequence Units

- Key transitions (plenary): Stage 1 and Stage 2 in the same 2026-05 slot (`2026-05/may-20.md`, "Intl Sequence Units for Stage 1 or 2"; conclusion "Consensus for Stage 1." + "Consensus for Stage 2 with the object-based design"; EAO and DLM Stage 2.7 reviewers). `raw/proposals/ecma402` still lists it under Stage 1 → `canonical_stage: 1`. 2026-07 (`2026-07/july-22.md`, "Duration units in Amount and Intl Sequence Units") was discussion only.
- Prehistory: ecma402#398 "Sequence unit formatting" (TG2 2020-07-09); part of Smart Unit Preferences and Measure (Stage 1 2024-10) until Amount dropped compound units (2025-07); WH's person-height "feet-and-inches" objection to Amount (2026-03) led SFC to split it out (TG2 2026-03-19, 2026-04-16).
- Main issues: in scope for Intl / NumberFormat vs Amount.toLocaleString; scalar vs structured input (#1) → array (#16, TG2 2026-09-17); missing/extra/out-of-range/negative values (#2 #4 #5 #6); sanctioned unit groups and order (#7 #9); integer larger units (#3) and throwing on significant digits (#14); zero-valued components (#11); time units (#8, unresolved after 2026-07 plenary) and arcminute/arcsecond (#13).
- Champion: SFC.
- Summary backlog: 6 TG2 meetings added (2018-03-16, 2020-07-09, 2020-09-10, 2024-05-23, 2024-08-22, 2024-09-26).

## [2026-09-30] ingest | Amount

- Created `wiki/proposals/amount.md`: an ECMA-262 proposal with a large ECMA-402 surface (`ecma: [262]`, `families: [number-format]`), repo tc39/proposal-amount (formerly proposal-measure).
- Stage transitions from plenary conclusions: Stage 1 2024-10 (`october-10.md`, item titled "Measure object stage 0"); renamed Measure → Amount at 2025-07 without advancing (`july-29.md`); Stage 2 2026-05 (`may-20.md`, reviewers WH and JHD). Stage 2 slots in 2025-07, 2025-09 and 2026-03 did not advance.
- Champions: BAN (canonical) plus EAO (asked to be recognised, 2025-02) and SFC ("I'm champion of the amount proposal", 2025-09) per the notes; JMN is a contributor, mentioned in text (new champions rule in AGENTS.md).
- Main issues: scope (conversion removed, then restored), type vs. protocol (Intl Unit Protocol split out), Decimal split and precision (Intl Keep Trailing Zeros), rounding and representation, non-finite values and ToIntlMathematicalValue limits, conversion math (double rounding; led to Math.fma), Intl integration (public fields, currency as unit, null no-unit), mixed units and array-valued `.value`, time units (unresolved), naming and V8 concerns, rationals.
- Summary backlog: 2024-08-22 added; `amount` appended to 2024-07-18 and 2024-09-26.

## [2026-09-30] wiki | canonical-lag, ECMA-262 and champion rules; index fixes

- AGENTS.md: canonical-lag rule (`canonical_stage` frontmatter when a plenary transition isn't in `raw/proposals` yet; Stable Formatting and Intl Sequence Units), ECMA-262 proposals with a large Intl surface may get pages (Amount), champions include people the notes explicitly show as champions; new typo mappings `EAIO` → EAO, `SFO` → SFC.
- `extract_proposals.py`: trailing "Related ECMA-262 proposals (ingested)" section. `extract_plenary_agenda.py`: `amount` / `measure` keywords; conclusion lines with "consensus"/"accepted"/"agreed" now count as stage signals (the 2026-05 Sequence Units Stage 2 bullet was hidden). Same signal fix in `extract_tg2_agenda.py`.

## [2026-09-30] summarise | TG2 backlog, newest 10 (2023-09-07 .. 2024-09-26)

- Summarised the 10 newest Summary backlog entries (2023-09-07, 2023-10-12, 2023-11-16, 2023-12-14, 2024-02-22, 2024-04-25, 2024-05-23, 2024-07-18, 2024-08-22, 2024-09-26) into `wiki/meetings/<YYYY>/`, added them to `wiki/meetings/README.md` and removed them from the backlog (22 entries left).
- Stage-relevant TG2 events: Stable Formatting (then "root locale") judged ready for Stage 1 (2023-09-07); TG2 recommends a TG5 study before `Intl.MessageFormat` advances (2024-08-22); Smart Units pivots to a Measure type (2024-08-22); numerics-with-precision announced at Stage 0 and DurationFormat Stage 4 check deferred to October (2024-09-26); ECMA-402 11th edition approved, BAN to become co-editor (2024-07-18).
- Quirks: `notes-2023-11-16.md` is headed "2022-11-16"; typos normalised (`LFS` → LAF, `HSI` → HJS, `PCO` → PFC, `SFO` → SFC, `YSK` → YSZ). Unlisted speakers added to frontmatter `attendees` (JGT in 2023-10-12 and 2024-04-25; BAN in 2025-08-14, fixing the earlier batch). The 2024-05-23 Accept-Language topic links `Tanych/accept-language#10` exactly as the notes give it.
- `LFS` added to AGENTS.md mappings and `extract_people.py` alias exclusions.

## [2026-09-30] summarise | TG2 backlog entries cited by two pages (2020-09-10, 2021-04-08)

- Summarised 2020-09-10 (cited by intl-durationformat, intl-sequence-units) and 2021-04-08 (cited by intl-durationformat, intl-keep-trailing-zeros); moved them from the backlog to the meetings list (20 backlog entries left).
- TG2 events: Intl.DisplayNames Stage 4 consensus (2020-09-10); Intl Locale Info and DisplayNames v2 Stage 3 support, Extend TimeZoneName Stage 2 support with `shortOffset`/`longOffset`, NumberFormat V3 rounding options settled (2021-04-08).
- Cross-check: the citing pages match the notes; clarified on intl-keep-trailing-zeros that the 2021-04-08 notes spell the option value "stringIfInteger". SFC speaks but is unlisted in 2021-04-08 (added to attendees).

## [2026-09-30] ingest | Intl Era/Month Code

- Created `wiki/proposals/intl-era-month-code.md` (canonical "Intl Era and MonthCode Proposal"; champions FYT, BAN, plus SFC ("taken up the mantle", 2025-04) and USA, PFC (the 2025-07 plenary Conclusion calls them "the champions")).
- Stage history: Stage 1 2022-11 (`dec-01.md`), Stage 2 2023-01 (`feb-01.md`), Stage 2.7 2025-07 (`july-30.md`, conditional on an ECMA-402 editor), Stage 3 2026-01 (`january-20.md`), Stage 4 2026-03 (`march-10.md`); the 2025-11 "for Stage 3" slot did not advance. Stalled 2023-24 until implementers revived it in 2025-03.
- Main issues from TG2 2025-26: era-code authority and naming (CE/BCE, ROC, Japanese pre-Meiji and 6 Meiji), epoch years, the Hijri fallback (`islamic` → `islamic-tbla`, `islamic-rgsa` ignored), the closed calendar list, the PR #69 arithmetic scope and its "editorial" mislabel, `overflow: "reject"` for missing leap months, reference years and the safe date range.
- Publication note: canonical gives 2026, but the text was folded into the Temporal ECMA-402 PR (ecma402#1044), and the editors said it was not in the ES2026 cut (TG2 2026-04-16, 2026-05-07).
- Summary backlog: 2 meetings added (2022-06-16, 2022-10-06); slug appended to 2022-05-19 and 2023-01-12.

## [2026-09-30] ingest | Intl Locale Info

- Created `wiki/proposals/intl-locale-info.md` (`families: [locale]`). Precursor `Intl.resolveLocaleInfo` in "Abstract Locale Operations" (plenary 2015-11, 2016-01) sets `first_seen: "2015-11"`.
- Stage transitions from plenary conclusions: Stage 1 2020-09 (`sept-23.md`), Stage 2 2021-01 without `unitInfo` (`jan-26.md`), Stage 3 2021-04 (`apr-20.md`), Stage 4 2025-11 (`november-18.md`, with PR #92); ES2026. The planned 2022-11 Stage 4 slot became an update; the 2023-11 plenary raised but did not decide a return to Stage 2.
- Champion: FYT (sole). SFC (presenter 2025-02/05) and ABL (Anba; spec issues, PR #92) appear in the text only.
- Main issues: measurement-system scope; preference lists and `-u-` keywords, list ordering; non-contiguous `weekend`; getters → `get` methods and shipped-getter web compat; `firstDayOfWeek` / `-u-fw`; calendar/region influence on week info with follow-ups ecma402 #1051/#1097/#1059; text direction; time zones; `minimalDays` removal; fallback behaviour (PR #92) and post-Stage-4 PRs #1072/#1074/#1086.
- Summary backlog: 9 TG2 meetings added; `intl-locale-info` appended to 4 existing entries.

## [2026-09-30] wiki | champion rule wording; new typo mappings

- AGENTS.md: a plenary Conclusion / Speaker's Summary that calls the presenters "the champions" counts as explicitly showing them as champions; `FYC` / `FYI` → FYT added to the typo mappings (and to `extract_people.py` exclusions); ES-edition note that Intl Era/Month Code reached Stage 4 in 2026-03 but missed the ES2026 cut like Temporal.
- `extract_people.py`: person detection now skips code spans and hyphenated tokens (`"ja-JP"` had produced a page for JP = John Pampuch) and treats `BCE` (era code vs. Ben Coe) as `AMBIGUOUS`; removed the three auto-links to BCE.

## [2026-09-30] summarise | TG2 backlog, next 10 (2022-08-04 .. 2023-06-29)

- Summarised 2022-08-04, 2022-09-01, 2022-10-06, 2022-11-03, 2022-12-08, 2023-01-12, 2023-04-06, 2023-05-04, 2023-06-01, 2023-06-29; moved them from the backlog to the meetings list.
- TG2 events: Intl Enumeration cleared for Stage 4 (2022-10-06); `proposal-intl-temporal` renamed to Intl Era and Month Codes (2022-10-06); Intl.MessageResource split out for Stage 1 (2022-10-06); Era Display decoupled from Temporal (2022-11-03); DurationFormat to ask for Stage 4 (2023-01-12); Intl.ZonedDateTimeFormat Stage 1 support (2023-04-06); time zone canonicalization toward Stage 2/3 with an FYT objection (2023-05-04, 2023-06-29).
- Cross-checks against citing pages: fixed intl-durationformat (issue #55 came up at 2022-11-03, not 2022-08-04) and intl-locale-info (the 2023-05-04 notes don't credit ABL with #68; FYT brought it). Title-date quirk: `notes-2023-01-12.md` is headed 2023-01-13. The 2023-05-04 notes give a malformed URL `github.com/tc39/issues/574` (kept verbatim).
- New typo mappings `SFA` → SFC, `DM` → DLM, `AB` → ABL.

## [2026-10-01] ingest | Intl Unit Protocol

- Added `wiki/proposals/intl-unit-protocol.md` (canonical "explore associating a unit with a number", champion SFC, families: number-format).
- Stage 1 at the 2025-11 plenary (`november-18.md`), Stage 2 at the 2026-03 plenary (`march-11.md`, RGN and ACE as Stage 2.7 reviewers); canonical table still lists Stage 1, so `canonical_stage: 1`.
- Prehistory traced through Amount: TG2 2024-07-18 (EAO's NumberFormat input protocol), plenary 2025-02 (KG protocol-only), 2025-07/2025-09 (no internal-slot reads, TG3).
- Main issues: protocol vs built-in type, public fields vs internal slots, shape and naming (object bag, `number`→`value`, `currency`→`unit`), conflicting units (#3, conversion gated on Amount), currency as unit (`cup`/`CUP`), web-compat sniffing and `null` no-unit (#5), array-valued `value` for sequence units (proposal-amount#118), loss of constructor-time data preloading.
- Summary backlog: no additions (all 7 cited TG2 meetings are summarised).

## [2026-10-01] ingest | Smart Unit Preferences in Intl.NumberFormat

- Created `wiki/proposals/smart-unit-preferences.md` (`families: [number-format]`). First mention: SFC at the 2020-02 plenary (`february-6.md`), so `first_seen: "2020-02"`.
- Stage transitions from plenary conclusions: Stage 1 2020-06 (`june-4.md`); no later transition. The 2024-06 (`june-12.md`) and 2024-10 (`october-10.md`) slots were BAN's updates.
- Champion: YMD (canonical). BAN (2024 revival, fork repo) and HUG appear in the text only. YMD's separate `Units Conversion` proposal (Stage 1 2022-03, `mar-30.md`) is recorded on the page; it is missing from every raw/proposals/ecma402 table.
- Effectively dormant: no own agenda item after 2024-10. Its parts live on in Amount (`convertTo` + ECMA-402 locale/usage, TG2 2026-02-19), Intl Sequence Units and Intl Unit Protocol.
- Main issues: black box vs building blocks; unit conversion and Intl misuse, then the move to Measure/Amount; user preferences, fingerprinting and the `en-US` problem; which usages; measurement system from Locale Info; mixed units.
- Summary backlog: 5 meetings added, `smart-unit-preferences` appended to the rest of 8 cited unsummarised meetings.

## [2026-10-01] wiki | unit-proposal cross-links and aliases

- Replaced plain-code references to `intl-unit-protocol` / `smart-unit-preferences` (and the wrong slug `intl-smart-unit-preferences` on intl-locale-info) with links on amount, intl-keep-trailing-zeros, intl-sequence-units and intl-locale-info; corrected amount's protocol-sniffing wording (a plain `Get` of `value` and `unit`, no presence check, per TG2 2026-08-06).
- `extract_proposals.py` alias for "explore associating a unit with a number"; `link_proposals.py` aliases "Unit Protocol", "Smart Unit Preferences", "Smart Units"; AGENTS.md: `EOA` → EAO, `repo:` keeps the canonical URL even after a move to the tc39 org.

## [2026-10-01] summarise | entire Summary backlog (24 meetings, 2017-12-15 .. 2024-03-28)

- Summarised every remaining backlog entry (2017-12-15, 2018-03-16, 2019-07-11, 2019-11-14, 2020-01-09, 2020-01-30, 2020-02-27, 2020-06-11, 2020-07-09, 2020-08-13, 2020-12-04, 2021-01-14, 2021-02-11, 2021-06-03, 2021-09-09, 2021-10-07, 2021-11-04, 2022-01-13, 2022-03-17, 2022-04-21, 2022-05-19, 2022-06-16, 2023-03-09, 2024-03-28); the Summary backlog is now empty. The list-style 2017-12 and 2018-03 notes use the outline items as headings.
- TG2 events seen: ListFormat/RelativeTimeFormat toward Stage 3 (2017-12-15); UnitFormat folded into unified NumberFormat (2018-03-16); DurationFormat pitched (2019-11-14) and TG2 "Stage 1 consensus" (2020-01-09); ListFormat and dateStyle/timeStyle Stage 4 support (2020-06-11); Locale Info and DisplayNames V2 Stage 1 support (2020-08-13); eraDisplay and LocaleMatcher Stage 1 support (2020-12-04); DisplayNames V2 / Locale Info Stage 2 and Extend TimeZoneName Stage 1 support (2021-01-14); Segmenter can proceed to Stage 4 (2021-10-07); Segmenter V2 Stage 2 pushback (2022-01-13); Units Conversion Stage 1 support (2022-03-17); EAO steps back from MessageFormat (2024-03-28).
- Cross-check fixes on proposal pages: intl-locale-info (#33 order debate was SFC vs ZB; no ABL remark in the notes), intl-durationformat (`digital` was a poll result, not a settled vote; JHD "noticed" rather than "objected" to the Temporal dependency). Removed an inferred `proposal-intl-numberformat-v3#21` URL from the 2021-02-11 summary.
- Title-date quirks: 2020-12-04 headed "December 12", 2024-03-28 headed "2023-03-28". Many early ad-hoc abbreviations added to AGENTS.md and the `extract_people.py` exclusions; `JH` (Jack Horton vs. delegates.txt Jafar Husain) added to `AMBIGUOUS`.
- Unlinked an ad-hoc `MM` (= MCM) in the 2019-07-11 Overview mapping list that `link_people.py` had linked to Mark S. Miller.

## [2026-10-01] ingest | Intl.MessageFormat

- Added `wiki/proposals/intl-messageformat.md` (Stage 1 since the 2022-03 plenary `mar-30.md`; no Stage 2 request ever made; last plenary item 2024-06 `june-11.md`).
- Champions `[EAO, DLM, USA]`: DLM as a historical co-champion ("championed by me and by Dan Minor", 2022-03 plenary; TG2 2022-01-13); USA joined as co-champion per the 2024-04 plenary conclusion; EAO announced stepping back at TG2 2024-03-28 but stayed on. Canonical lists EAO only.
- Covers the 2018-2019 move of the syntax to the Unicode MFWG, the 2022 MessageResource split, the 2024-02 plenary DSL-stability debate and the "dozen organizations" bar, the rejected data-model-only PR #47, the TG2 2024-08-22 TG5-study recommendation, MF2 milestones, onError/error handling, API shape, and MF2 function options diverging from ECMA-402.
- New abbreviation notes: `KGN` → KG; `EA` (Eemeli Aro) and `AH` (Axel Hecht) collide with delegates.txt in 2019 TG2 notes and are now `AMBIGUOUS`.
- Summary backlog: 6 TG2 meetings added (2018-08-16, 2019-06-13, 2021-07-01, 2022-02-10, 2023-02-09, 2024-01-18).

## [2026-10-01] summarise | Summary backlog from Intl.MessageFormat (6 meetings)

- Summarised 2018-08-16, 2019-06-13, 2021-07-01, 2022-02-10, 2023-02-09, 2024-01-18; the Summary backlog is empty again (76 TG2 meetings summarised).
- TG2 events: Unified NumberFormat #11/#9 settled (2018-08-16); MessageFormat landscape survey and the move toward Unicode MessageFormat 2.0 (2019-06-13); NumberFormat v3 Stage 3 approval and Enumeration to proceed to Stage 3 (2021-07-01); Intl.MessageFormat TG2 "consensus for Stage 1" (2022-02-10); EAO turns a MessageFormat Stage 2 request into an update (2024-01-18).
- Cross-check: softened intl-messageformat's "ZB's counter-proposal won" (2019-06-13 records only agreement, no formal conclusion). New mapping `SG` → SGN.
- Unlinked ad-hoc `MM` (= MCM) in 2019-06-13 that `link_people.py` had linked to Mark S. Miller.

## [2026-10-01] ingest | eraDisplay option for Intl.DateTimeFormat

- Added `wiki/proposals/intl-eradisplay.md` (champions SFC, LAF; families: date-time).
- Stage 1 at the 2021-01 plenary (`jan-27.md`; TG2 recommended on 2020-12-04), Stage 2 at the 2022-11 plenary (`nov-29.md`; reviewers EAO, DLM). No Stage 2.7 request yet; matches the canonical table.
- Main issues: era-only scope (#7), value set and `auto` default, runtime pattern selection via internal slots (#4), decoupling from Temporal, CLDR-driven cutoffs instead of the current date (#9), year precision / `yearStyle` naming (#10), Julian/Gregorian reckoning, champion bandwidth.
- Summary backlog: 2 TG2 meetings added (2020-11-05, 2024-06-20).

## [2026-10-01] ingest | Default Behaviours for some Intl APIs

- Added `wiki/proposals/intl-default-behaviours.md` (Stage 1 at the 2026-05 plenary `may-20.md`, presented right after Stable Formatting's Stage 2; no later plenary or TG2 item through 2026-09-17). Champion `[EAO]`, matching canonical; `first_seen` 2023-09.
- Covers the prehistory inside Stable Formatting and ecma402: #885 ("und" as root or host default), case-mapping locale resolution #896 / #956, the 2025-02 plenary split of root behaviour from `zxx` stability, and PR #24 at TG2 2026-05-07 (file `notes-2026-05-19.md`), where TG2 approved the spin-off.
- Main issues: what "und" means today; the identifier ("und" vs "root" / Symbol / `zxx`, SFC's web-compat concern); locale-independent vs stable; case mapping; what "untailored" means for Segmenter.
- Summary backlog: no additions (all 9 cited TG2 meetings are summarised).

## [2026-10-01] wiki | eraDisplay / Default Behaviours cross-links and summary fixes

- Linked the new pages from stable-formatting and intl-era-month-code; `link_proposals.py` aliases "eraDisplay", "Era Display", "Default Behaviours".
- Summary wording fixes found during these ingests: 2025-02-06 (`["und","tr"]` fallback was SFC's answer accepted by RGN, not a group agreement), 2026-05-19 (SFC's and RGN's actual stability points), 2026-03-19 (eraDisplay cutoffs were SFC's proposed conclusion, not an agreed direction).
- `BE` (Buddhist Era vs. Brendan Eich) added to `AMBIGUOUS`; removed the auto-links on intl-eradisplay.

## [2026-10-02] summarise | Summary backlog from eraDisplay (2 meetings)

- Summarised 2020-11-05 (scope guidelines #442, default time zone #507, first eraDisplay #426 discussion) and 2024-06-20 (CLDR-driven eraDisplay #9, "sub-era"); the Summary backlog is empty again (78 TG2 meetings summarised). Both match intl-eradisplay.

## [2026-11-03] update | raw/ecma402, raw/notes

- `raw/ecma402`: e463f3c → 3691634 (9 commits). New TG2 notes `notes-2026-10-08.md` (Amount duration units #139, Sequence Units #19, Unit Protocol #6/#7/#8, toTitleCase #294, cyclic year #816). Spec: merged normative PR #1095 (`%TypedArray%.prototype.toLocaleString`) and editorial PRs #1048, #1050, #1063, #1079, #1087, #1096, #1106.
- `raw/notes`: already up to date on main (latest plenary 2026-07). The 2026-09 plenary (116th) minutes are still an open PR (tc39/notes#424).
- Regenerated the TG2 agenda index (1359 topics) and people pages. Follow-ups: `/summarise 2026-10-08`; revisit Amount, Intl Sequence Units and Intl Unit Protocol with the new TG2 discussion.
