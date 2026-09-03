---
format_version: 1
id: ADR-0005
status: superseded
created: 2026-09-03
accepted: 2026-09-03
scope: skill/css-ownership
supersedes: ADR-0003
superseded_by: ADR-0007
---

# Bind token and CSS ownership to the runtime owner

## Decision

For each DOM region, the Skill requires agents to follow this order: existing
WordPress API and semantic Core markup; an existing Core class or WordPress
component with default CSS; a semantic token actually provided in the selected
runtime path; a plugin-owned composition of those primitives; and only as a
final exception, a new narrowly scoped CSS rule.

Semantic `--wpds-*` variables may be consumed only when the selected and loaded
WPDS provider or its stylesheet supplies them. The Skill and plugin code must
neither define, override, nor imitate `--wpds-*`. Primitive WPDS tokens are
implementation details. Classic/Core first inherits Core rhythm. React with
`@wordpress/components` first uses component defaults and APIs;
`__experimentalVStack` remains experimental, and its `spacing` is a multiplier
of the 4 px grid. An unavoidable isolated plugin gap may use a number marked as
a **Skill-Norm** or a plugin-owned custom property, but must never present it as
a WordPress token.

## Problem

Not every WordPress backend path loads WPDS tokens. A blanket requirement for
WordPress gap tokens can cause agents to invent nonexistent variables or inject
experimental styles into classic pages.

## Drivers

- The user requires WordPress defaults and as little custom CSS as possible.
- Token availability depends on runtime and provider.
- Core, Components, and WPDS paths have different stability and spacing
  contracts.
- Genuine layout gaps must still be closable in a small, local, and traceable
  way.

## Considered alternatives

1. Define `--wpds-*` globally for every path: consistent names, but fabricated
   and conflict-prone platform authority.
2. Use only raw pixel values: runtime-independent, but fails to use existing
   semantic contracts.
3. Load WPDS on every plugin page: one provider, but an experimental dependency
   and unnecessary intervention on classic pages.

## Consequences

- Every recommendation names the runtime owner, token provider, and CSS owner.
- The Skill needs separate tables for Core observations, Components APIs, WPDS
  tokens, and Skill-Norms.
- CSS exceptions must document the owners checked, smallest scope, and
  responsive/accessibility proof.
- Global `wp-admin` overrides, copied Core CSS blocks, and imitated `--wpds-*`
  variables are prohibited.

## Confirmation

The Decision is implemented when golden cases for Classic, Core Components,
WPDS, and Hybrid each name the expected owner and allowed expression, prohibit
unloaded `--wpds-*` variables, and justify every custom CSS exception.

## Revisit when

WordPress provides a stable, globally documented admin token or layout API.
