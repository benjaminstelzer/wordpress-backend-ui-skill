---
format_version: 1
id: ADR-0008
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: skill/i18n
supersedes: ADR-0006
---

# Loadable PHP and JavaScript translations as a UI invariant

## Decision

Every plugin backend interface generated or audited by the Skill is
internationalizable in PHP and JavaScript. All user-facing strings, including
`aria-label`, screen-reader text, and alternative text, use WordPress i18n APIs
with a literal text domain matching the lowercase, hyphenated plugin slug.
JavaScript registers `wp-i18n` as a dependency and binds the already registered
script handle to the same text domain with `wp_set_script_translations()` and an
explicit language-file path.

The string contract covers complete phrases instead of concatenation,
positional placeholders, plural forms, context, immediately preceding
`translators:` comments, and context-appropriate escaping. PHP uses `wp_date()`
and `number_format_i18n()`. JavaScript uses `dateI18n` from `@wordpress/date`;
locale-formatted numbers shown client-side are supplied by the server with
`number_format_i18n()` in the baseline. Pure client-side number, percentage, or
currency formatting is allowed only with a separately documented API,
evidenced locale mapping, and its own browser test.

The reproducible fixture path is:

1. Sources are extracted into a POT with `wp i18n make-pot`.
2. A test PO named `<text-domain>-<locale>.po` is maintained against that POT;
   it is not converted into a POT.
3. The PO is compiled with `wp i18n make-mo` into
   `<text-domain>-<locale>.mo` in the plugin's `languages/` directory.
4. The fixture registers this custom path on `init` with
   `load_plugin_textdomain()`; WordPress 6.7+ then loads the actual artifact
   just in time.
5. The same PO is converted to JavaScript JSON with
   `wp i18n make-json --no-purge`. The golden case either fixes the documented
   filename `<domain>-<locale>-<handle>.json` or ensures PO file references
   point to the registered build path from which the MD5 filename is computed;
   `src/` references for a registered `build/` script are prohibited.
6. After a reproducible site and admin-user locale switch, browser assertions
   prove at least one genuinely translated PHP and React string.

Layout and validation cover doubled text, long German labels, at least one RTL
language, and locale-dependent formats.

## Problem

POT and PO are authoring artifacts. WordPress does not load a PO file for PHP;
it loads a compiled MO or `.l10n.php` artifact. Without compilation and a
registered loading path, a PHP browser assertion cannot pass. Likewise,
`make-pot` proves neither a loaded PHP translation nor correct JavaScript
filenames, script handle, or path.

## Drivers

- The user requires multilingual plugin interfaces as a fixed property.
- WordPress provides coordinated PHP, JavaScript, language-file, and WP-CLI
  contracts.
- Assistive strings are just as user-facing as visible text.
- Translations are untrusted and must be escaped for the output context.
- Runtime and layout evidence must use the real WordPress loading path.

## Considered alternatives

1. Test only POT extraction: reproducible, but not runtime proof.
2. Use a PO directly as PHP proof: WordPress does not load it.
3. Hard-code browser strings in test languages: tests layout, but not the
   translation path.
4. Use `.l10n.php` instead of MO as the only baseline: possible, but MO is the
   simpler documented fixture path for plugin bundles and
   `load_plugin_textdomain()`.

## Consequences

- The Skill needs concrete PHP, JavaScript, POT/PO/MO/JSON, runtime, and layout
  rules.
- The fixture contains a real test PO, compiled MO, and generated JSON.
- The site and admin-user locale switch is established reproducibly.
- Examples must not contain untranslated user-facing literals or variable text
  domains.

## Confirmation

The Decision is implemented when the prefrozen golden corpus covers positive
and negative PHP and JavaScript cases; POT, MO, and JSON are generated
reproducibly; `load_plugin_textdomain()` registers the plugin language path; and
browser assertions after a locale switch demonstrate genuinely translated PHP
and React strings plus robust German and RTL layouts.

## Revisit when

WordPress changes the recommended MO/`.l10n.php`, JavaScript JSON, or
language-pack workflow, or provides a documented client-side number-formatting
API for the target path.
