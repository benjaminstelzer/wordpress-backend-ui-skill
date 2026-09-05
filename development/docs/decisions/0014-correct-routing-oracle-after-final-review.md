---
format_version: 1
id: ADR-0014
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: tests/routing-oracle
---

# Correct the Network Admin hybrid to a non-experimental route

## Decision

The golden case `route-network-admin-hybrid` uses
`experimental_components_policy: deny`. Its described React region explicitly
uses Core Components and is therefore no more an unknown or experimental
runtime than the corresponding single-site hybrid.

The canonical routing table also explicitly lists every surface, shell, and
spacing value already used in the frozen routing corpus. For excluded host
surfaces, the policy rule is now deterministic: known Classic/Core PHP hosts
produce `deny`; React or unspecified hosts produce `unknown`.

## Problem

The final read-only review found a contradiction between the normative policy
rule and one golden case, plus six excluded or ambiguous cases whose structured
values were absent from the canonical value table. The seven-case fresh-agent
corpus did not contain this gap.

## Drivers

- The same known Core-only hybrid must produce the same policy.
- Every golden value must be derivable from the installed Skill documentation.
- Excluded interfaces remain with the host and must receive no implicit
  experimental permission.
- A semantic oracle correction must be visibly rebaselined under ADR-0012.

## Considered alternatives

1. Treat Network Admin as `unknown`: contradicts the explicitly named Core
   Components runtime.
2. Remove the missing values from the golden corpus: shrinks the support matrix
   and hides the documentation gap instead of fixing it.
3. Expand only the fresh-agent corpus: leaves the canonical contract
   contradictory.

## Consequences

- `tests/cases/routing.yaml` and its hash are deliberately updated.
- The expanded fresh-agent corpus must be rerun standalone and with optional
  Scoville UI after the correction.
- Other routing, spacing, i18n, responsive, and UI oracles remain unchanged.

## Confirmation

The Decision is implemented when the canonical table covers all routing values,
the Network Admin hybrid produces `deny`, manifest validation passes, and the
expanded fresh-agent corpus passes again in both modes.

## Revisit when

An excluded host is included in version 1, a runtime becomes experimental, or
new structured routing values are added.
