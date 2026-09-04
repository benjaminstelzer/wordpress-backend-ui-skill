# WordPress Backend UI

A plugin backend should feel like WordPress before it starts looking like
another product.

WordPress Backend UI is an Agent Skill for designing, implementing and auditing
plugin-owned `wp-admin` interfaces against WordPress 7.0 and 7.1. It gives an
agent a clear contract for surface ownership, vertical flow, spacing,
responsive behavior, accessibility, interface states and internationalization.

The Skill does not add another UI framework. It tells the agent when WordPress
APIs, Core Components, default CSS or provided design tokens already own the
decision, and when a small local CSS exception is actually justified.

## Why this Skill?

WordPress does not have one complete, stable backend design system for every
plugin surface. Classic admin CSS, Core Components, Core's 7.1 token stylesheet
and bundled experimental components coexist, but they do not have the same
runtime, support status or spacing owner.

Without those boundaries, agents tend to mix systems. A Classic form gets a
second spacing scale, React is mistaken for WPDS, custom tokens start looking
official, and a mobile fix changes gaps without fixing the layout itself.

This Skill makes the ownership decisions explicit. The interface can still be
custom where the task requires it, but WordPress remains the starting point.

## How to use

Invoke the Skill explicitly or ask naturally:

```text
$wordpress-backend-ui Design a responsive settings page for this plugin.
```

```text
Audit this WordPress plugin backend, especially its spacing, states and custom CSS.
```

```text
Check only the spacing and vertical flow on this settings page. Do not change files.
```

```text
Use WordPress Backend UI to implement this React admin page with full i18n support.
```

The request selects one of two modes. **Implement** creates or changes the
requested UI. **Audit** inspects and reports without changing it. You can limit
an audit to spacing, responsiveness, accessibility or another concern. A full
UI audit uses the same mode with a broader scope. "Check and fix" permits
corrections within the stated scope, not an unrelated redesign.

The Skill checks whether the interface is really a plugin-owned admin
surface. Editor UI, Core screens, post metaboxes and interfaces owned by another
plugin stay with their host design system.

## Install

The repository contains one installable Agent Skill directory. Usually, let
Codex install it with this prompt:

```text
Install this Agent Skill from GitHub and make it available for all my projects:
https://github.com/benjaminstelzer/wordpress-backend-ui-skill/tree/main/wordpress-backend-ui
```

For a manual installation, copy the repository's `wordpress-backend-ui/`
directory so the final path is:

```text
<skills-dir>/wordpress-backend-ui/SKILL.md
```

The Skill works standalone.

## What it enforces

- **Surface ownership before styling.** The agent first determines whether the
  plugin owns the page or must follow another WordPress surface.
- **Runtime ownership before components.** Classic admin UI, Core Components
  and bundled WPDS are separate implementation paths. React alone decides
  nothing.
- **WordPress before custom CSS.** APIs, semantic markup, Core classes,
  components, default CSS and provided tokens come before a local rule.
- **No forced Classic migration.** A working PHP page keeps its native elements
  and default CSS. WordPress 7.1 tokens are optional tools for missing plugin
  layout relationships, not a reason to rebuild the page in React.
- **One owner for vertical flow.** The direct parent controls the space between
  its children. Components keep responsibility for their internal padding.
- **A consistent spacing contract.** Semantic relationships map to a documented
  4, 8, 12, 16, 24, 32 and 40 pixel sequence where WordPress leaves the choice
  open.
- **Responsive task preservation.** Settings, workflows and data views reflow
  according to their purpose instead of receiving one generic mobile layout.
- **Complete and accessible states.** Loading, empty, success, error, disabled
  and permission states keep their meaning, focus behavior and available next
  step.
- **Internationalization as part of the layout.** PHP, JavaScript, accessible
  text, dates, numbers and text expansion belong to the UI contract. RTL checks
  are required only when a supported or explicitly planned UI language uses RTL.
  The requirement is readiness for later translations, not a mandatory PO
  workflow or completed translations.

The complete contract is in [`SKILL.md`](wordpress-backend-ui/SKILL.md).

## How it works

### Mode and scope

Both modes use the same WordPress design-system rules. The difference is the
work requested and the evidence needed. A spacing check follows spacing owners,
Core defaults and relevant layout changes. It does not automatically become a
translation project or a complete UI audit. Findings explain the location,
rule, observed problem, impact and smallest correction. Source inspection and
rendered proof remain separate.

### Surface and runtime

The Skill classifies the admin surface first, then selects the supported
runtime path. This keeps host-owned interfaces with their host and prevents an
experimental component package from quietly becoming the design system for an
entire plugin.

### Spacing and CSS

Vertical flow belongs to the nearest layout parent. The Skill maps intended
relationships to WordPress component gaps or available design tokens before it
allows custom CSS. A local CSS exception must solve a concrete layout problem,
stay at the smallest useful scope and survive responsive, zoom and text-expansion
checks. RTL checks apply only when the language scope requires them.

### Responsive UI and i18n

Responsive behavior starts with the task, not a breakpoint. Forms reflow,
actions wrap, data views contain their overflow, and text remains usable at 320
CSS pixels and 400 percent zoom. The Skill requires extractable strings and
the loading structure needed for later translations. Catalog generation and
translation delivery stay optional. When delivery is part of the task, test
actual loading too, because an extractable string is not automatically a
loaded translation.

## Optional Scoville UI composition

WordPress Backend UI remains the owner of WordPress surfaces, components,
spacing, tokens, responsive constraints, internationalization and CSS
exceptions. When
[Scoville UI](https://github.com/benjaminstelzer/scoville-ui-anti-ai-slop) is
also active, it can strengthen task flow, hierarchy, accessibility and rendered
validation inside those boundaries. It preserves the selected mode and scope.

Optional means optional. Installing one Skill does not turn the other into a
missing dependency.

## Status

Current release: **v1.1.1**.

The contract, installable Skill and production fixture were validated against a
WordPress 7.0 Single Site and a WordPress 7.0.4 Network Admin installation.
Responsive behavior, RTL and PHP and JavaScript translations were exercised in
the local XAMPP fixtures. The repository also contains frozen routing, spacing,
CSS ownership, UI state and internationalization cases. WordPress 7.1 Core
source and the local 7.1 installation were inspected for `wp-theme` style
registration, required tokens and the public `ThemeProvider` export. That
source inspection is not a rendered 7.1 UI test.

## Sources

- [`wordpress-7-backend-design-system.md`](docs/audits/wordpress-7-backend-design-system.md)
  contains the source-backed audit and its derivation boundaries.
- [`source-ledger.md`](docs/research/source-ledger.md) pins the relevant
  WordPress, Gutenberg, accessibility and internationalization sources.
- [`tests/cases/`](tests/cases/) contains the frozen behavioral contracts.

## License

MIT - see [`LICENSE`](LICENSE).
