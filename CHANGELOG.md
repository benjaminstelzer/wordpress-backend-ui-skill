# Changelog

## v1.1.4 - 2026-09-08

- Put WordPress Core spacing precedence before the fallback scale so existing
  native spacing does not receive a second value.
- Compare heading-to-content spacing with section transitions and trace
  unexplained differences to their layout owner.
- Check heading colour, size, and weight through computed styles and the winning
  CSS declarations while preserving the distinction between page and section
  headings.

## v1.1.0 - 2026-09-04

- Added separate Implement and Audit modes. Audit remains read-only unless the
  user requests corrections.
- Scope reference selection, responsive checks, and result reporting to the
  requested work.
- Require RTL checks only when a supported or planned language uses RTL.

## v1.0.2 - 2026-09-03

- Require internationalization readiness without forcing catalog generation,
  completed translations, or a PO workflow.
- Apply POT, PO, MO, Jed JSON, and translated-runtime checks only when
  translation delivery is part of the request.

## v1.0.1 - 2026-09-03

- Separated WordPress 7.0 package restrictions from WordPress 7.1 Core token
  styles and `ThemeProvider` APIs.
- Allowed Core tokens for genuine missing relationships and domain states on
  PHP pages without forcing React or experimental components.
- Preserved existing Classic elements and default CSS without mandatory token
  or component migration.
- Added version-aware loading and fallback checks.

## v1.0.0 - 2026-09-03

- Added implementation and audit guidance for WordPress 7 plugin-owned admin
  pages across PHP/Core, React with Core Components, bundled experimental WPDS,
  and hybrid DOM regions.
- Added spacing, vertical-flow, responsive, accessibility, feedback, recovery,
  and internationalization contracts for Single Site and Network Admin.
- Added explicit boundaries for CSS exceptions and optional Scoville UI
  composition.
