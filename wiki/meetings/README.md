# TG2 meeting summaries

Topic-by-topic digests of ECMA-402 task group (TG2) monthly calls, produced by `/summarise`. Newest first. Source notes: [tc39/ecma402 meetings/](https://github.com/tc39/ecma402/tree/main/meetings).

| Date                             | Gist                                                                                                                                                                                       |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [2026-09-17](2026/2026-09-17.md) | TG2 approves #1074, #1097 and #1095; Sequence Units: throw on significant-digit rounding, array input; EAO proposed as third editor; #434 deprioritised.                                   |
| [2026-08-06](2026/2026-08-06.md) | #1078 merged; Amount, Sequence Units and Unit Protocol converge on an array-valued `.value`; `Accept-Language` locale data; Stage 2 proposal reviews.                                      |
| [2026-07-09](2026/2026-07-09.md) | TG2 approves #1086; Sequence Units zero and unit-table decisions; time units go to TG1; EAO cleared for a Stage 1 datetime-options proposal.                                               |
| [2026-06-11](2026/2026-06-11.md) | TG2 approves #1074, #1072 and #1051; region overrides (#1059) should become a proposal; temperature checks on PersonNameFormat and `identityFallback`.                                     |
| [2026-05-19](2026/2026-05-19.md) | Stable Formatting gets TG2 support for Stage 2 (`und` spun off); Sequence Units Stage 2 support with caveats; Anba's PRs deferred.                                                         |
| [2026-04-16](2026/2026-04-16.md) | No formal conclusions: unit protocol fallback deferred to Amount Stage 2, `-and-` sequence units via NumberFormat, titlecase sent to CSS/web platform, Firefox ICU4X.                      |
| [2026-03-19](2026/2026-03-19.md) | Design discussions without decisions: keep-trailing-zeros #15, unit protocol fallback, sequence units, unit-usage criteria, EraDisplay year style and cutoffs.                             |
| [2026-02-19](2026/2026-02-19.md) | Keep Trailing Zeros approved for Stage 3, Era/Month Code for Stage 4; IntlMV limits PR proceeds; Amount rework and Unit Protocol design discussed.                                         |
| [2026-01-08](2026/2026-01-08.md) | TG2 recommends CLDR keep `-`/`:` and `h23` for `iso8601`; `tols` and Era/MonthCode #99 approved; energy unit choices discussed; Unit Format withdrawn.                                     |
| [2025-12-04](2025/2025-12-04.md) | `iso8601` `DateTimeFormat` calendar debate (referred to CLDR); calendar list made a closed set; `islamic-rgsa` dropped; `DisplayNames` editorial-vs-normative discussion.                  |
| [2025-11-06](2025/2025-11-06.md) | #1032 `PluralRules` `compactDisplay` approved for TG1; keep-trailing-zeros questions deferred to plenary; energy units (`kilowatt-hour`) steered toward a Stage 1 proposal.                |
| [2025-10-13](2025/2025-10-13.md) | Intl Locale Info cleared for Stage 4; Era/MonthCode alias, Buddhist, Japanese and Hijri decisions; safe-date-range debate left open.                                                       |
| [2025-09-11](2025/2025-09-11.md) | PRs #1026 and #1022 approved; `overflow: "reject"` made strict for lunisolar leap months; Standard Measures (`en-ZZ`) and #978 discussed without decision.                                 |
| [2025-08-14](2025/2025-08-14.md) | PluralRules `[[CompactDisplay]]` approved; W3C i18n review becomes a stage requirement; `h24` aliased to `h23`; PRs #958/#957 closed; calendar-arithmetic PR #69 undecided.                |
| [2025-07-17](2025/2025-07-17.md) | Support for Era/MonthCode (2.7), Keep Trailing Zeros and Amount (Stage 2); Segments iterator `name` PR approved; PR #958 to be closed.                                                     |
| [2025-06-12](2025/2025-06-12.md) | Era/MonthCode calendar-alias, arithmetic and epoch decisions; Hijri `islamic` fallback debate without decision; TG1 text-direction addendum accepted.                                      |
| [2025-05-08](2025/2025-05-08.md) | Support for Keep Trailing Zeros (Stage 1); #780 locale-set note; #956 made a draft; `getVariants` to TG1 as a PR; text direction stops falling back to LTR.                                |
| [2025-04-03](2025/2025-04-03.md) | Era/Month Codes era-code decisions (`CE`/`BCE`, ISO year for Chinese); Hijri fallback conclusion proposed; `PluralRules` `notation` (#989) to TG1.                                         |
| [2025-03-06](2025/2025-03-06.md) | `DurationFormat` editorial PR (#972) headed for merge; Temporal shipping, unshipping `islamic`/`islamic-rgsa` (#971), Era/Month Codes stalled; `getVariants` (#960) motivation questioned. |
| [2025-02-06](2025/2025-02-06.md) | Case-mapping locale resolution (#956) and Stable Formatting null/`zxx` locale debated without decision; `era`/`timeZoneName` PR (#957) to be split; `minimalDays` to be dropped.           |
| [2025-01-16](2025/2025-01-16.md) | RGN to PR case-mapping locale resolution (#896); option-read-order plan (#747); minimalDays likely dropped; currency display naming; Decimal+Measure unification.                          |
| [2024-12-19](2024/2024-12-19.md) | #929 numbering systems go to TG1; LocaleInfo issues (fallback, minimalDays) to be fixed; "und" semantics and 5-8-letter language subtags discussed.                                        |
| [2024-11-25](2024/2024-11-25.md) | TG2 supports DurationFormat Stage 4 and a currency-symbol Stage 1 proposal; era-display century option, variants getter, DisplayNames slicing debated.                                     |
| [2024-10-24](2024/2024-10-24.md) | Discussion only: Segmenter locale resolution (#895), 2025 planning (MF2, Measure, RBNF, data loading), test262 guidelines for locale-sensitive tests.                                      |

## Summary backlog

TG2 meetings already cited by proposal pages but not yet summarised (oldest first). `/summarise <date>` removes an entry; `/ingest` adds them (AGENTS.md "Workflow > Ingest" step 7).

| Date                                                                                 | Referenced by                                    |
| ------------------------------------------------------------------------------------ | ------------------------------------------------ |
| [2017-12-15](https://github.com/tc39/ecma402/blob/main/meetings/notes-2017-12-15.md) | intl-durationformat                              |
| [2018-03-16](https://github.com/tc39/ecma402/blob/main/meetings/notes-2018-03-16.md) | intl-sequence-units                              |
| [2019-11-14](https://github.com/tc39/ecma402/blob/main/meetings/notes-2019-11-14.md) | intl-durationformat                              |
| [2020-01-09](https://github.com/tc39/ecma402/blob/main/meetings/notes-2020-01-09.md) | intl-durationformat                              |
| [2020-01-30](https://github.com/tc39/ecma402/blob/main/meetings/notes-2020-01-30.md) | intl-durationformat                              |
| [2020-07-09](https://github.com/tc39/ecma402/blob/main/meetings/notes-2020-07-09.md) | intl-sequence-units                              |
| [2020-09-10](https://github.com/tc39/ecma402/blob/main/meetings/notes-2020-09-10.md) | intl-durationformat, intl-sequence-units         |
| [2021-01-14](https://github.com/tc39/ecma402/blob/main/meetings/notes-2021-01-14.md) | intl-durationformat                              |
| [2021-02-11](https://github.com/tc39/ecma402/blob/main/meetings/notes-2021-02-11.md) | intl-durationformat                              |
| [2021-04-08](https://github.com/tc39/ecma402/blob/main/meetings/notes-2021-04-08.md) | intl-durationformat, intl-keep-trailing-zeros    |
| [2021-06-03](https://github.com/tc39/ecma402/blob/main/meetings/notes-2021-06-03.md) | intl-durationformat                              |
| [2021-10-07](https://github.com/tc39/ecma402/blob/main/meetings/notes-2021-10-07.md) | intl-durationformat                              |
| [2022-01-13](https://github.com/tc39/ecma402/blob/main/meetings/notes-2022-01-13.md) | intl-durationformat                              |
| [2022-05-19](https://github.com/tc39/ecma402/blob/main/meetings/notes-2022-05-19.md) | intl-durationformat                              |
| [2022-08-04](https://github.com/tc39/ecma402/blob/main/meetings/notes-2022-08-04.md) | intl-durationformat                              |
| [2022-09-01](https://github.com/tc39/ecma402/blob/main/meetings/notes-2022-09-01.md) | intl-durationformat                              |
| [2022-11-03](https://github.com/tc39/ecma402/blob/main/meetings/notes-2022-11-03.md) | intl-durationformat                              |
| [2022-12-08](https://github.com/tc39/ecma402/blob/main/meetings/notes-2022-12-08.md) | intl-durationformat                              |
| [2023-01-12](https://github.com/tc39/ecma402/blob/main/meetings/notes-2023-01-12.md) | intl-durationformat                              |
| [2023-04-06](https://github.com/tc39/ecma402/blob/main/meetings/notes-2023-04-06.md) | intl-durationformat                              |
| [2023-06-01](https://github.com/tc39/ecma402/blob/main/meetings/notes-2023-06-01.md) | stable-formatting                                |
| [2023-06-29](https://github.com/tc39/ecma402/blob/main/meetings/notes-2023-06-29.md) | intl-durationformat                              |
| [2023-09-07](https://github.com/tc39/ecma402/blob/main/meetings/notes-2023-09-07.md) | stable-formatting                                |
| [2023-10-12](https://github.com/tc39/ecma402/blob/main/meetings/notes-2023-10-12.md) | intl-durationformat                              |
| [2023-11-16](https://github.com/tc39/ecma402/blob/main/meetings/notes-2023-11-16.md) | intl-durationformat, stable-formatting           |
| [2023-12-14](https://github.com/tc39/ecma402/blob/main/meetings/notes-2023-12-14.md) | stable-formatting                                |
| [2024-02-22](https://github.com/tc39/ecma402/blob/main/meetings/notes-2024-02-22.md) | stable-formatting                                |
| [2024-04-25](https://github.com/tc39/ecma402/blob/main/meetings/notes-2024-04-25.md) | intl-durationformat                              |
| [2024-05-23](https://github.com/tc39/ecma402/blob/main/meetings/notes-2024-05-23.md) | intl-sequence-units                              |
| [2024-07-18](https://github.com/tc39/ecma402/blob/main/meetings/notes-2024-07-18.md) | intl-keep-trailing-zeros, amount                 |
| [2024-08-22](https://github.com/tc39/ecma402/blob/main/meetings/notes-2024-08-22.md) | intl-sequence-units, stable-formatting, amount   |
| [2024-09-26](https://github.com/tc39/ecma402/blob/main/meetings/notes-2024-09-26.md) | intl-durationformat, intl-sequence-units, amount |
