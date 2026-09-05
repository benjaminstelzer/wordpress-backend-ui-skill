---
format_version: 1
id: ADR-0010
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: skill/css-ownership
supersedes: ADR-0009
---

# Use non-experimental Core components before experimental or custom spacing

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
rhythm first. For a new generic plugin-owned vertical sibling group, the
Core-provided `Flex` component, whose name is not experimental, is the default
flow owner. The Skill explicitly sets `direction="column"`, `align="stretch"`,
`justify="flex-start"`, `wrap={ false }`, and `expanded={ true }`. The numeric
`gap` prop is the relevant Skill-Norm gap divided by the documented 4 px grid:
`1/2/3/4/6/8/10` for `4/8/12/16/24/32/40px`. Documented `FlexItem` and
`FlexBlock` children are used according to their sizing role. A plugin-local
stack rule is allowed only when `Flex` cannot express the evidenced layout need.

Routing and spacing oracles continue to contain
`experimental_components_policy: allow | deny | unknown`. It controls only the
introduction of other experimental components, not stable `Flex` flow.
Repository evidence of a deliberately used experimental component may justify
`allow`; mere availability does not. For `unknown`, the safe default is `deny`:
no new experimental API. An existing `__experimentalVStack` subtree remains
its own owner and is not refactored merely for style cleanup; new generic groups
use `Flex`.

An unavoidable isolated plugin gap may use a number marked as a **Skill-Norm**
or a plugin-owned custom property, but must never present it as a WordPress
token.

## Problem

A safe default against experimental APIs must not cause the Skill to skip an
existing Core component and generate custom CSS. In the pinned
`@wordpress/components` version, `Flex` can express vertical flow and the 4 px
gap grid without an experimental export name.

## Drivers

- The user requires WordPress defaults and as little custom CSS as possible.
- Two agents should choose the same spacing owner and alignment values for an
  identical structure.
- Token availability depends on runtime and provider.
- New experimental APIs need an evidenced opt-in; stable existing components do
  not.

## Considered alternatives

1. Use custom CSS directly under `unknown`: safe from experiments, but violates
   the ownership ladder.
2. Use `__experimentalVStack` by default: fewer props, but an unevidenced
   experimental opt-in.
3. Use `Flex` without explicit alignment: uses Core, but the defaults `center`
   and `space-between` are unsuitable for ordinary vertical flow and not
   deterministic with the Skill-Norm.
4. Load WPDS on every plugin page: one provider, but an experimental dependency
   and intervention on classic pages.

## Consequences

- New generic Core Components stacks use `Flex` before local CSS, regardless of
  experiment policy.
- Golden cases test `direction`, `align`, `justify`, `wrap`, `expanded`, the gap
  multiplier, and child role.
- `unknown` reproducibly introduces no new experimental API, but also does not
  automatically lead to custom CSS.
- Existing experimental subtrees are not refactored without a functional
  reason.

## Confirmation

The Decision is implemented when golden cases cover all three experiment-policy
values; every new generic Core Components group selects `Flex` with the fixed
props and multipliers; existing experimental owners are respected; unloaded
`--wpds-*` variables are prohibited; and every remaining custom CSS exception
demonstrates a real `Flex` gap.

## Revisit when

`Flex` changes its public contract or 4 px grid, `VStack` is stabilized, or
WordPress provides a more stable semantic vertical-stack component.
