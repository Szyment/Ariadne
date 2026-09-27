# Ariadne project documentation rules (binding)

*Binding document, on a par with `GLOSSARY.md`. It applies to all files in `docs/`, `sessions/`, `hardware/`, `build-log/` and `README.md`.*

*Documents are written in English. The Polish originals of documents written before S-22 are kept in `docs/pl/` for the record; in case of doubt about a frozen document, the Polish text is binding.*

**Exception:** `docs/research/PREZENTACJA_I_PYTANIA_JURY.md`, `REFRAME_KONKURSOWY.md`, `KRYTYKA_NAUKOWA.md`. These are persuasive and review texts, in which rhetoric is the function of the document.

---

## 1. A heading is the name of a thing

No narrative numbering, no assessment, no comment after a colon or a dash.

| Wrong | Right |
|---|---|
| `## Result 2: flight budget per pack, item B1 closed` | `## Item B1 closed` |
| `### The failsafe triggered at 36% remaining capacity` | `### Battery failsafe` |
| `## Operational detail` | `## Source switch` |
| `### Illuminance: readings not comparable` | `### Illuminance` |

A colon is acceptable in a heading when it is part of the name: `# Annex C: wind measurement`, `### A1. Platform 2: specification and cost`. An em dash is not used as a separator in headings.

## 2. A sentence is a fact or a number

Forbidden opening phrases: *it is worth noting*, *it is worth recording*, *note that*, *a caveat*, *the key point is*, *the crux of the matter*, *a remark on*, *this is exactly*, *this is precisely*, *the answer is given by*, *the distinction is*. Intensifiers (*crucially*, *importantly*, *notably*) are not used. Rhetorical contrast ("this is not X, it is Y") is not used. No em-dash asides; use a comma, parentheses or a separate sentence.

| Wrong | Right |
|---|---|
| `A caveat to this number: the aircraft moved by at most 0.58 m, so the discrepancy is of the same order as the reference noise.` | `The aircraft moved by at most 0.58 m. The discrepancy is of the order of the reference noise.` |
| `It is worth adding this indicator to the LUX axis.` | `Indicator added to the LUX axis.` or an item on the list of open points |

A limitation of a result is written as a sentence about the result, not as a separate paragraph about the author's intentions.

## 3. An unfilled field is `[TO BE FILLED IN]`

No explanation in brackets, no hint where to get the data from, no description of why it is missing.

| Wrong | Right |
|---|---|
| `[TO BE FILLED IN: the GM816 shows temperature]` | `[TO BE FILLED IN]` |
| `[TO BE FILLED IN: whether the grass was wet, and whether it differed between flights]` | `[TO BE FILLED IN]` |

## 4. Do not ask for confirmation of data that is in the record

Coordinates, altitude, absolute time, voltages, currents, flight altitudes, number of satellites: all of this is in the log. `[TO BE CONFIRMED]` next to such data means that the log was not checked.

A human fills in only what the autopilot does not measure: wind from the anemometer, illuminance, outside temperatures, surface condition, role assignment, events observed by eye.

## 5. Bold only on result values and parameter names

Not on claims, not on conclusions, not on sentences the author considers important.

## 6. A number without provenance does not enter the document

Every value has a source: log number, instrument name, parameter name, or a calculation with its components given. A value computed from other values gives the formula or the components.

## 7. Failures and errors are recorded the same way as results

No softening, no excuses, no explaining the circumstances. Fact, cause, effect, state.
