---
format_version: 1
id: ADR-0004
status: superseded
created: 2026-09-03
accepted: 2026-09-03
scope: skill/i18n
superseded_by: ADR-0006
---

# Internationalization as a binding UI invariant

## Decision

Every plugin backend interface generated or audited by the Skill is
internationalizable in PHP and JavaScript. Visible strings use the WordPress
i18n APIs with a literal text domain matching the lowercase, hyphenated plugin
slug. JavaScript registers `wp-i18n` as a dependency and binds the registered
script handle to the same text domain with `wp_set_script_translations()`.

The contract covers complete phrases instead of string concatenation,
positional placeholders, plural forms, context, immediately preceding
`translators:` comments, context-appropriate escaping, and locale-aware date
and number formatting. Layout and validation must cover doubled text, long
German labels, at least one RTL language, and locale-dependent formats without
loss of information or function. POT extraction checks PHP and JavaScript
sources.

## Problem

Translation added later cannot repair dynamically assembled strings, incorrect
plural forms, missing JavaScript language files, or layouts that break with
longer and right-to-left text. Internationalization must therefore define the
string, runtime, and layout contract from the outset.

## Drivers

- The user requires multilingual plugin interfaces as a fixed property.
- WordPress provides separate but coordinated APIs for PHP and JavaScript.
- Translations are untrusted and must be escaped for the output context.
- Spacing, order, widths, and status messages must work with expanding or RTL
  text.

## Considered alternatives

1. Localization after implementation: lower initial effort, but cannot be
   retrofitted reliably.
2. Internationalize only PHP: insufficient for React and hybrid interfaces.
3. Use an external i18n system by default: creates parallel infrastructure and
   bypasses WordPress language packs.

## Consequences

- The Skill needs concrete PHP, JavaScript, extraction, and layout rules.
- Examples must not contain untranslated visible literals or variable text
  domains.
- i18n stress cases become part of routing, spacing, responsive, and rendered
  validation.
- Localized dates and numbers use WordPress APIs instead of generic
  language-neutral formatting.

## Confirmation

The Decision is implemented when the golden corpus covers positive and
negative PHP and JavaScript cases, `wp i18n make-pot` extracts the expected
strings, and rendered tests with doubled text, German, and RTL show no clipped
content, incorrect order, or page-wide horizontal overflow.

## Revisit when

WordPress changes the recommended PHP/JavaScript translation or language-pack
workflow.
