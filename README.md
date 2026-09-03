# WordPress Backend UI

A WordPress plugin backend should look like it belongs in WordPress. This is
less obvious than it sounds once Classic admin CSS, Core Components and an
experimental design system all appear in the same conversation.

WordPress Backend UI is an Agent Skill for designing, implementing and auditing
plugin-owned `wp-admin` pages against WordPress 7.0. It determines who owns the
surface and each part of the UI before it recommends a component, a gap or a
line of CSS.

The result is a clear vertical flow, responsive layouts, accessible states and
translatable PHP and JavaScript. More importantly, the Skill tries to get there
with WordPress itself. Custom CSS is the exception, not the opening move.

## Why this Skill?

WordPress does not provide one complete, stable backend HIG for every plugin
surface. It provides several real owners instead: the Settings API and Core
admin CSS, `@wordpress/components`, and the newer bundled WPDS path. At the
WordPress 7.0 target, that path remains experimental because it depends on the
experimental `@wordpress/ui` and `@wordpress/theme` packages;
`@wordpress/admin-ui` is only sparsely documented and depends on them.

Ignoring those boundaries creates familiar problems. A Classic form receives a
second spacing system. React is mistaken for WPDS. A plugin defines tokens that
only look official. Mobile fixes shrink gaps while the form itself still does
not reflow.

This Skill makes the missing decisions explicit without pretending WordPress
published rules it did not publish.

## How to use

Invoke the Skill explicitly or ask naturally:

```text
$wordpress-backend-ui Design a responsive settings page for this plugin.
```

```text
Audit this WordPress plugin backend, especially its spacing, states and custom CSS.
```

```text
Use the WordPress Backend UI Skill to implement this React admin page with full i18n support.
```

The Skill first classifies the admin surface and runtime. If the UI belongs to
the editor, a Core screen or another plugin, it routes to that owner instead of
quietly applying a full-page plugin design system where it does not belong.

## Install

Copy the repository's `wordpress-backend-ui/` directory so the final path is:

```text
<skills-dir>/wordpress-backend-ui/SKILL.md
```

The Skill has no runtime dependency on Scoville UI or any other Scoville Skill.

## Requirements

- An Agent Skill-compatible host.
- A WordPress plugin backend. The current contract and fixture target WordPress
  7.0.
- Node 24, npm, Python 3 and WP-CLI only when running the repository's
  development fixture, contract and translation checks.
- PowerShell and an isolated XAMPP setup only when repeating the repository's
  local Single Site and Network Admin runtime checks. The Skill itself needs
  neither XAMPP nor Docker.

Version 1 covers plugin-owned settings, tools, workflows, dashboards, data
views and explicit Network Admin pages. It does not own editor canvas UI,
SlotFills, post metaboxes, Dashboard widgets, profile fields, extensions of
existing Core screens or UI inside another plugin. Those surfaces stay with
their host design system.

## What it enforces

- **Two ownership checks.** The admin surface and the runtime are classified
  separately. React does not automatically mean WPDS.
- **WordPress before plugin CSS.** APIs, semantic markup, Core classes,
  components, default CSS and provided tokens are checked before a local rule.
- **One owner for vertical flow.** The direct parent owns spacing between its
  children. Cards own internal padding. Empty children leave no mystery gap
  behind.
- **A documented spacing scale.** Semantic relationships map to a consistent
  4, 8, 12, 16, 24, 32 and 40 pixel sequence. The mapping is clearly labeled as
  a Skill-Norm where WordPress itself leaves the decision open.
- **Responsive task preservation.** Settings, workflows and data views adapt as
  different page types. The test contract covers the WordPress boundary at 782
  pixels, WCAG reflow at 320 CSS pixels, zoom, long translations and RTL.
- **Complete interface states.** Loading, empty, success, error, disabled and
  permission states keep a visible next step or recovery where one exists.
- **Internationalization as part of the UI.** PHP, JavaScript, accessible text,
  dates, numbers, translation artifacts and localized layout follow one
  testable contract.

The complete behavior contract is in
[`SKILL.md`](wordpress-backend-ui/SKILL.md).

## Optional Scoville UI composition

The Skill works standalone. When Scoville UI is also active, WordPress Backend
UI remains the owner of WordPress components, shell behavior, spacing, tokens,
responsive constraints, i18n and CSS exceptions. Scoville UI can strengthen
the remaining task flow, hierarchy, accessibility and rendered checks inside
those boundaries.

Optional means optional. Installing one Skill should not turn the other into a
missing dependency with better branding.

## Status

Current release: **v1.0.0**.

The source ledger is pinned to WordPress 7.0 and Gutenberg `wp/7.0`. Static
contracts, the Skill package validator, a clean exact-lockfile Node 24 offline
install from the populated npm cache, PHP/JavaScript
runtime translation, Single Site, Network Admin, RTL and responsive browser
checks passed locally against a WordPress 7.0 Single Site and a WordPress 7.0.4
Network Admin. A read-only native XAMPP validator pins and verifies both local
runtimes without making Docker a project requirement. Repository-free
Fresh-Agent checks passed for all eight frozen routing prompts, both standalone
and with optional Scoville UI composition. In both runs the WordPress ownership
fields matched exactly; the Scoville UI run only added checks inside those
boundaries.

## Sources

- [`wordpress-7-backend-design-system.md`](docs/audits/wordpress-7-backend-design-system.md)
  contains the source-backed audit and its derivation boundaries.
- [`source-ledger.md`](docs/research/source-ledger.md) pins Core, Gutenberg,
  WPDS, accessibility and i18n sources with revalidation triggers.
- [`routing.yaml`](tests/cases/routing.yaml),
  [`spacing.yaml`](tests/cases/spacing.yaml), and the remaining files in
  [`tests/cases/`](tests/cases/) define the frozen behavioral oracles.

## License

MIT. See [`LICENSE`](LICENSE).
