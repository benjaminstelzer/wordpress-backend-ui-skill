---
format_version: 1
id: ADR-0002
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: skill/composition
---

# Standalone Skill with optional Scoville UI composition

## Decision

The WordPress Backend Skill is standalone and must not depend on Scoville UI.
When Scoville UI is available and applies to the same task, it may optionally be
composed with this Skill. The WordPress Skill remains the canonical owner of the
WordPress backend design system; Scoville UI applies its general UI quality
checks within those boundaries.

## Problem

The Skill must remain fully usable in environments without Scoville UI. At the
same time, an agent using both Skills must not receive two competing design
systems, spacing scales, or component rules.

## Drivers

- The user explicitly required independence.
- Scoville UI should be optional and compatible.
- WordPress-specific platform rules must take precedence over general UI
  defaults.
- Duplicate or contradictory instructions must be avoided.

## Considered alternatives

1. Hard dependency on Scoville UI: fewer duplicated UI fundamentals, but the
   Skill would not work standalone.
2. No composition: clear independence, but shared tasks could not benefit from
   Scoville UI's rendering, accessibility, and quality checks.
3. Peer Skills without concern ownership: flexible, but conflicts over spacing,
   breakpoints, and component choice would not be resolved deterministically.

## Consequences

- The WordPress Skill must itself contain minimum rules for hierarchy, user
  guidance, states, responsiveness, and accessibility.
- An optional composition section defines concern ownership and conflict
  resolution.
- Scoville UI must not replace WordPress tokens, default CSS, or component
  choices with a parallel visual language.
- Tests must cover standalone and composition cases separately.

## Confirmation

The Decision is implemented when the completed Skill provides complete
WordPress backend guidance without Scoville UI and, when both are active, the
two Skills work from an unambiguous ownership matrix without contradictory
values.

## Revisit when

Scoville UI itself integrates a binding, version-bound WordPress backend
specialization as canonical owner, or the user explicitly changes the
dependency direction.
