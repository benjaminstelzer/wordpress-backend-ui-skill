---
format_version: 1
id: ADR-0009
status: superseded
created: 2026-09-03
accepted: 2026-09-03
scope: skill/css-ownership
supersedes: ADR-0007
superseded_by: ADR-0010
---

# Decide experimental policy and runtime spacing deterministically

## Decision

For each DOM region, the Skill requires agents to follow this order: existing
WordPress API and semantic Core markup; an existing Core class or WordPress
component with default CSS; a semantic token actually provided in the selected
runtime path; a plugin-owned composition of those primitives; and only as a
final exception, a new narrowly scoped CSS rule.

Semantic `--wpds-*` variables may be consumed only when the selected and loaded
WPDS provider or its stylesheet supplies them. The Skill and plugin code must
neither define, override, nor imitate `--wpds-*`. Primitive WPDS tokens are
implementation details. Classic/Core first inherits Core rhythm.

Routing and spacing oracles contain
`experimental_components_policy: allow | deny | unknown`. Repository evidence
of an experimental component already being used deliberately may justify
`allow`; mere availability does not. For `unknown`, the safe default is `deny`:
the agent introduces no new experimental API, uses exactly one plugin-local
stack composition with a gap marked as a Skill-Norm, and names the missing
opt-in. A question is necessary only when the user explicitly wants to assess
or choose the experimental variant.

In the React/Core Components path, specialized components own their internal
rhythm first. For a generic plugin-owned vertical sibling group, the
Core-provided `__experimentalVStack` owns flow under `allow`. Its numeric
`spacing` prop is the relevant Skill-Norm gap divided by the documented 4 px
grid: `1/2/3/4/6/8/10` for `4/8/12/16/24/32/40px`. Under `deny` or `unknown`,
one plugin-local stack composition owns flow and uses the same gap marked as a
Skill-Norm; individual children receive no parallel outer margins.

An unavoidable isolated plugin gap may use a number marked as a **Skill-Norm**
or a plugin-owned custom property, but must never present it as a WordPress
token.

## Problem

Not every WordPress backend path loads WPDS tokens. At the same time, Core
Components flow remains nondeterministic when the task says nothing about
experimental components. Availability must not silently count as consent.

## Drivers

- The user requires WordPress defaults and as little custom CSS as possible.
- Token availability depends on runtime and provider.
- Two agents should choose the same spacing owner given identical structure and
  evidence.
- New experimental APIs need an evidenced opt-in.

## Considered alternatives

1. Treat `unknown` as `allow`: less custom CSS, but an unevidenced experimental
   opt-in.
2. Always ask under `unknown`: safe, but blocks reversible default cases
   unnecessarily.
3. Permit `Flex`, `VStack`, and custom `gap` equally: flexible, but not
   deterministic.
4. Load WPDS on every plugin page: one provider, but an experimental dependency
   and intervention on classic pages.

## Consequences

- Every routing and spacing case has an explicit experiment-policy value.
- Every recommendation names the runtime, DOM, token, and flow owner.
- Core Components golden cases name the expected component and, where
  applicable, the `spacing` multiplier.
- `unknown` reproducibly selects the local Skill-Norm stack, not a silent
  experimental dependency.

## Confirmation

The Decision is implemented when golden cases cover all three policy values,
produce exactly one owner for identical evidence, introduce no new experimental
API under `unknown`, prohibit unloaded `--wpds-*`, and justify every custom CSS
exception.

## Revisit when

`VStack` is stabilized or replaced, or WordPress provides a stable, globally
documented admin token or layout API.
