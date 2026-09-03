# Changelog

## 1.0.1 - 2026-09-03

### Changed

- Separated WordPress 7.0 package restrictions from WordPress 7.1's public
  Core token stylesheet and `ThemeProvider` APIs.
- Allowed Core tokens for genuine missing layout relationships and domain
  states on PHP pages without requiring React or experimental components.
- Explicitly preserved existing Classic elements and default CSS, with no
  mandatory token or component migration.
- Added versioned loading and fallback checks plus a source-checked
  public-provider example.

### Validation

- Frozen contracts, the eight-case PHP enqueue example, local 7.0/7.1 Core
  source checks, Skill validation, and the Scoville Plan profile passed.
- The 7.1 provider example is source-checked only. A separate 7.1 plugin build
  and rendered UI validation are not claimed.

## 1.0.0 - 2026-09-03

### Added

- Added the standalone `wordpress-backend-ui` Agent Skill for WordPress 7.0
  plugin-owned admin pages.
- Added separate routing for PHP/Core, React with Core Components, bundled
  experimental WPDS and hybrid DOM regions.
- Added the semantic spacing and vertical-flow contract, including stable
  `Flex` output for all experimental-policy states and a strict CSS exception
  boundary.
- Added responsive archetypes for settings, workflows and data views with
  WordPress, WCAG, zoom, localization and RTL checks.
- Added navigation, form, feedback, state, recovery and accessibility guidance.
- Added the PHP and JavaScript internationalization contract with POT, PO, MO,
  Jed JSON and runtime translation requirements.
- Added frozen routing, spacing, CSS ownership, responsive, UI guidance and
  i18n cases.
- Added a pinned native XAMPP manifest and read-only validator for separate
  WordPress 7.0 Single Site and WordPress 7.0.4 Multisite fixtures.
- Added the MIT license.

### Validation

- The Agent Skill package validator, deterministic repository checks, PHP lint
  and the production fixture build passed.
- A clean Node 24 `npm ci --offline` installed the pinned dependency graph from
  the populated npm cache; `npm ls --depth=0` passed in that clean directory.
- WordPress, Gutenberg and npm refs in the source ledger were revalidated on
  2026-09-03.
- PHP and JavaScript translations, locale-formatted date and number output,
  all four runtime modes, all eight UI states, RTL, Single Site and Network
  Admin passed in local WordPress 7.0 Single-Site and 7.0.4 Multisite fixtures.
- Responsive and rendered accessibility checks passed at 783, 782, 600, 390
  and 320 CSS pixels, including document reflow, local table overflow, focus,
  labels, disabled reasons, target sizes and representative contrast.
- A WCAG 2 A/AA, 2.1 A/AA and 2.2 AA axe scan reported no violations or
  incomplete rules on the authenticated WordPress 7.0 WPDS fixture; manual
  keyboard, focus and layout checks remain the complementary evidence.
- Repository-free Fresh-Agent checks passed all eight frozen routing prompts
  standalone and with optional Scoville UI composition. Both runs returned the
  exact expected WordPress ownership fields and required prohibitions.
