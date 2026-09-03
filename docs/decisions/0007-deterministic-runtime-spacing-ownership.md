---
format_version: 1
id: ADR-0007
status: superseded
created: 2026-09-03
accepted: 2026-09-03
scope: skill/css-ownership
supersedes: ADR-0005
superseded_by: ADR-0009
---

# Own runtime-specific spacing deterministically

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

In the React/Core Components path, specialized components own their internal
rhythm first. For a generic plugin-owned vertical sibling group, the
Core-provided `__experimentalVStack` is the default flow owner when it is
available in the pinned `@wordpress/components` version and the project accepts
experimental components. Its numeric `spacing` prop is the relevant Skill-Norm
gap divided by the documented 4 px grid: `1/2/3/4/6/8/10` for
`4/8/12/16/24/32/40px`. Its experimental status is always named. If the project
forbids experimental components, one plugin-local stack composition owns the
flow and uses the same gap marked as a Skill-Norm; individual children receive
no parallel outer margins. The golden case includes this project condition and
therefore determines exactly one owner.

An unavoidable isolated plugin gap may use a number marked as a **Skill-Norm**
or a plugin-owned custom property, but must never present it as a WordPress
token.

## Problem

Not every WordPress backend path loads WPDS tokens. At the same time, the
general requirement to use component defaults leaves open whether two agents
choose `__experimentalVStack`, another layout component, or custom CSS for the
same Core Components structure. Both token availability and flow owner must
therefore be deterministic.

## Drivers

- The user requires WordPress defaults and as little custom CSS as possible.
- Token availability depends on runtime and provider.
- Two agents should choose the same spacing owner for an identical structure
  and project condition.
- Core, Components, and WPDS paths have different stability and spacing
  contracts.

## Considered alternatives

1. Define `--wpds-*` globally for every path: consistent names, but fabricated
   platform authority.
2. Permit `Flex`, `VStack`, and custom `gap` equally: flexible, but not
   deterministic.
3. Load WPDS on every plugin page: one provider, but an experimental dependency
   and unnecessary intervention on classic pages.
4. Always require experimental `VStack`: deterministic, but ignores a legitimate
   project boundary against experimental APIs.

## Consequences

- Every recommendation names the runtime, DOM, token, and flow owner.
- Core Components golden cases name the expected component, project condition,
  and `spacing` multiplier.
- The Skill needs separate tables for Core observations, Components APIs, WPDS
  tokens, and Skill-Norms.
- CSS exceptions must document the owners checked, smallest scope, and
  responsive/accessibility proof.

## Confirmation

The Decision is implemented when golden cases for Classic, Core Components,
WPDS, and Hybrid each name exactly one expected owner and allowed expression;
Core Components cases test the component and multiplier; unloaded `--wpds-*`
variables are prohibited; and every custom CSS exception is justified.

## Revisit when

`VStack` is stabilized or replaced, or WordPress provides a stable, globally
documented admin token or layout API.
