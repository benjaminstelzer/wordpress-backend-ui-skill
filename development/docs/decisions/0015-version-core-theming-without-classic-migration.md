---
format_version: 1
id: ADR-0015
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: skill/version-compatibility
---

# Version Core theming without requiring Classic migration

## Decision

The user selected separate WordPress 7.0 and 7.1 contracts. Core's 7.1
`wp-theme` stylesheet may supply semantic tokens to plugin-owned PHP layouts.
Its public `ThemeProvider` may serve React regions. Neither capability implies
experimental component adoption or a required migration of existing Classic
markup, elements, or default CSS. Existing native owners remain first choice.

## Problem

The original 7.0 package pin lacks a public provider export. Applying that
restriction to all WordPress 7 releases incorrectly rejects supported 7.1
Core APIs. It also conflates token stylesheet ownership with React ownership.

## Drivers

- Preserve existing Classic UI and the smallest necessary CSS change.
- Use public APIs and Core-owned semantic tokens without a duplicate bundle.
- Distinguish source inspection, loading checks, and rendered evidence.
- Keep tested older-version fallback paths explicit.

## Considered alternatives

1. Keep the blanket 7.0 restriction. This rejects documented 7.1 capabilities.
2. Migrate all Classic pages. This changes working UI without a requirement.
3. Version capability checks while preserving owners. This is the user's
   selected direction and requires explicit loading and token verification.

## Consequences

ADR-0011 remains the historical 7.0 pinned-package contract. This addendum
defines the 7.1 path without rewriting the completed Plan or its evidence.
The frozen 7.0 fixture does not become proof of a 7.1 rendered UI. New guidance
and executable enqueue checks cover the version boundary separately.

## Confirmation

Verify public release sources and local Core registration, tokens, and exports.
Run the versioned enqueue examples with and without the style handle and on an
unrelated page. Preserve all frozen contract checks. Before claiming a real
plugin passes, verify loading, computed tokens, accessibility, localization,
and responsive behavior in its actual supported installations.

## Revisit when

Supported Core releases, public exports, token names, or stylesheet ownership
change, or an explicit product requirement calls for a component migration.
