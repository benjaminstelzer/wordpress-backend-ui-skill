---
format_version: 1
id: ADR-0001
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: skill/ui-paths
---

# Classify admin surface and runtime owner separately

## Decision

The Skill classifies every task on two independent axes: admin surface and
runtime/component owner. The surface determines whether version 1 of the Skill
applies; the runtime owner determines component, CSS, token, and spacing
ownership.

Supported surfaces are plugin-owned single-site settings and tools pages,
workflow and dashboard pages, data views, and plugin-owned Network Admin pages
with explicit Multisite context. Block Editor sidebars and SlotFills, the
editor canvas, post metaboxes, Dashboard widgets, profile fields, extensions of
existing Core lists or screens, and interfaces inside another plugin are routed
separately or excluded.

The runtime owners are:

1. PHP/Core markup with Core default CSS;
2. React with Core-provided `@wordpress/components`;
3. bundled experimental WPDS from `@wordpress/ui`, `@wordpress/theme`, and
   `@wordpress/admin-ui`;
4. hybrid, with an explicit owner for each DOM region, including portals and
   overlays.

The classic path is the stable baseline. Experimental WPDS is a deliberate,
version-bound opt-in. React alone does not mean WPDS. On a typical hybrid page,
Core owns `#wpcontent`, `.wrap`, the page title, `.wp-header-end`, and page-wide
notices; the plugin root owns only its inner subtree. `.form-table` and a
plugin-owned gap stack must not own the same subtree.

## Problem

WordPress 7.0 is not simply a choice between Classic and React. React can use
stable Core components or experimental WPDS packages, and the same plugin page
can contain multiple owners. Without separate surface and runtime
classification, agents make false stability assumptions, create duplicate
spacing, and modify DOM regions owned elsewhere.

## Drivers

- The Skill should work broadly for WordPress plugin backends.
- Spacing and vertical content flow must be unambiguous for agents.
- Official Core facts and project-defined norms must remain distinguishable.
- The result must be responsive and compatible with existing `wp-admin` pages.
- Experimental APIs must not be treated as a stable global runtime.

## Considered alternatives

1. Classic `wp-admin` only: smaller and more stable, but insufficient for React
   plugin interfaces.
2. Equate React with WPDS: a simpler decision tree, but factually wrong because
   `@wordpress/components` and experimental WPDS have different contracts.
3. Support every admin embedding in version 1: broader coverage, but no uniform
   shell or ownership boundary.
4. Modern WPDS only: a more consistent token model, but experimental in
   WordPress 7.0 and not globally available.

## Consequences

- The Skill needs a mandatory two-axis classification and support matrix.
- Examples, spacing rules, and responsive behavior are documented separately
  for each runtime owner.
- Shared Skill-Norms may be applied only to bounded plugin components.
- Portals, overlays, and hybrid boundaries need an owner.
- The source and maintenance surface is larger than for a Classic-only Skill.
- Future stabilization of WPDS may require reassessing the baseline.

## Confirmation

The Decision is implemented when a frozen routing corpus expects `surface`,
`support_status`, `runtime_owner`, `shell_owner`, `spacing_owner`, sources, and
forbidden recommendations for every case, and every case is classified
deterministically.

## Revisit when

`@wordpress/ui`, `@wordpress/theme`, and `@wordpress/admin-ui` are no longer
experimental; WordPress publishes a binding shared admin HIG; or excluded
embedding surfaces should be brought into the Skill's scope.
