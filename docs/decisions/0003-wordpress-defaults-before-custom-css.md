---
format_version: 1
id: ADR-0003
status: superseded
created: 2026-09-03
accepted: 2026-09-03
scope: skill/css-ownership
superseded_by: ADR-0005
---

# Use WordPress defaults and tokens before custom CSS

## Decision

The Skill requires agents to follow this order: existing WordPress API and
semantic Core markup; an existing Core class or WordPress component with
default CSS; an existing WordPress token; a plugin-owned composition of those
primitives; and only as a final exception, a new narrowly scoped CSS rule.
Custom spacing uses WordPress gap or padding tokens whenever a suitable token
exists.

## Problem

Plugin backends often define custom buttons, inputs, cards, spacing, and
responsive rules even though WordPress already provides suitable defaults.
This creates inconsistent interfaces, duplicate spacing, global overrides, and
maintenance problems after Core updates.

## Drivers

- The user explicitly required minimal custom CSS.
- WordPress default CSS should remain the visual baseline.
- WordPress gap tokens should replace raw spacing values.
- RTL, mobile, focus, zoom, and Core updates should not be weakened by parallel
  CSS systems.
- Genuine layout gaps must still be closable in a small, traceable way.

## Considered alternatives

1. A completely custom plugin design system: high control, but a parallel
   language and large maintenance surface.
2. Core CSS without any exception: maximum proximity to WordPress, but
   insufficient for genuine plugin-specific layout compositions.
3. Free mixing of Core and custom CSS: flexible in the short term, but without
   deterministic ownership and difficult to audit.

## Consequences

- The Skill needs a mandatory CSS-owner check before every new rule.
- Exceptions must state the ownership gap, smallest scope, tokens used, and
  responsive/accessibility proof.
- Global `wp-admin` overrides, copied Core CSS blocks, and raw values where a
  suitable token exists are prohibited.
- Custom CSS files remain possible for genuine composition, layout archetypes,
  and clearly bounded integration gaps.

## Confirmation

The Decision is implemented when examples and agent tests choose Core APIs and
components first, express spacing through WordPress tokens, and every remaining
custom CSS rule satisfies the documented exception contract.

## Revisit when

WordPress provides a more stable admin component or layout API that replaces
custom CSS exceptions needed today.
