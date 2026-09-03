---
format_version: 1
id: ADR-0006
status: superseded
created: 2026-09-03
accepted: 2026-09-03
scope: skill/i18n
supersedes: ADR-0004
superseded_by: ADR-0008
---

# Internationalization as a runtime-proven UI invariant

## Decision

Every plugin backend interface generated or audited by the Skill is
internationalizable in PHP and JavaScript. All user-facing strings, including
`aria-label`, screen-reader text, and alternative text, use WordPress i18n APIs
with a literal text domain matching the lowercase, hyphenated plugin slug.
JavaScript registers `wp-i18n` as a dependency and binds the already registered
script handle to the same text domain with `wp_set_script_translations()` and an
explicit language-file path.

The contract covers complete phrases instead of string concatenation,
positional placeholders, plural forms, context, immediately preceding
`translators:` comments, context-appropriate escaping, and locale-aware date
and number formatting. PHP uses `wp_date()` and `number_format_i18n()`.
JavaScript uses `dateI18n` from `@wordpress/date`; locale-formatted numbers shown
client-side are supplied by the server with `number_format_i18n()` in the
baseline. Pure client-side number, percentage, or currency formatting is
allowed only with a separately documented WordPress or Web API, evidenced
locale mapping, and its own browser test.

Extraction alone is not proof. The fixture includes a test PO, generates POT
and JavaScript JSON reproducibly, and proves at least one actually translated
PHP and React string in the browser after switching locale. Layout and
validation cover doubled text, long German labels, at least one RTL language,
and locale-dependent formats.

## Problem

`make-pot` proves only extractability. It proves neither a loaded PHP
translation nor correct JSON filenames, script handle, path, or an actual
JavaScript translation in the browser. Localization added later also cannot
repair dynamically assembled strings or layouts that break with longer or RTL
text.

## Drivers

- The user requires multilingual plugin interfaces as a fixed property.
- WordPress provides coordinated PHP, JavaScript, language-pack, and WP-CLI
  contracts.
- Assistive strings are just as user-facing as visible text.
- Translations are untrusted and must be escaped for the output context.
- Spacing, order, widths, and status messages must work with expanding or RTL
  text.

## Considered alternatives

1. Test only POT extraction: reproducible, but not runtime proof.
2. Internationalize only PHP: insufficient for React and hybrid interfaces.
3. Hard-code browser strings in test languages: tests layout, but not the
   WordPress translation path.
4. Invent locale mapping for JavaScript numbers: flexible, but not source-faithful
   and prone to error.

## Consequences

- The Skill needs concrete PHP, JavaScript, PO/POT/JSON, runtime, and layout
  rules.
- Examples must not contain untranslated user-facing literals or variable text
  domains.
- The fixture needs at least one real test translation and locale switch.
- i18n stress cases become part of spacing, responsive, accessibility, and
  rendered validation.

## Confirmation

The Decision is implemented when the prefrozen golden corpus covers positive
and negative PHP and JavaScript cases, `wp i18n make-pot` and
`wp i18n make-json` produce the expected files, and browser assertions after a
locale switch demonstrate actually translated PHP and React strings plus robust
German and RTL layouts.

## Revisit when

WordPress changes the recommended PHP/JavaScript translation, JSON, or
language-pack workflow, or provides a documented client-side number-formatting
API for the target path.
