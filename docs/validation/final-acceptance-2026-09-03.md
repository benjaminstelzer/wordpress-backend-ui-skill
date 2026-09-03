# Final acceptance — 2026-09-03

## Result

The standalone WordPress Backend UI Skill passed its static, clean-install,
native runtime, rendered UI, accessibility, internationalization and
fresh-agent acceptance gates. Optional Scoville UI composition preserved the
same WordPress ownership decisions and added no dependency or parallel design
system.

## Reproducible checks

- `npm run test:xampp -- -XamppRoot Z:\xampp_lite_8_5`: passed read-only for
  WordPress 7.0 Single Site and WordPress 7.0.4 Multisite/Network Admin, exact
  Apache/PHP/MariaDB/WP-CLI versions, activation, Junction ownership, build
  artifacts and `de_DE` site/admin/runtime locale.
- Clean Node 24 copy without `node_modules`: `npm ci --offline --no-audit
  --no-fund`, `npm ls --depth=0`, production build, contract validation, PHP
  lint, POT/MO/Jed JSON generation and Skill Creator validation passed. Two
  online `npm ci` attempts stalled without an exit and are not counted as
  passes; the accepted clean install used the exact final lockfile and the
  populated local npm cache.
- Frozen agent corpus: the eight prompts and six exact owner fields are pinned
  by `tests/agent-prompts.sha256`. Clean installed Skill copies passed 8/8
  standalone and 8/8 with the source-ledger Scoville UI snapshot. Expected
  prohibited recommendations were required subsets, so applicable additional
  safeguards could not cause a false failure.
- README installation was repeated by copying only `wordpress-backend-ui/` to
  a clean external directory; the Skill Creator validator returned
  `Skill is valid!`. The static contract validator passed its README-link,
  license, package-pin, native-manifest, fixture-source/build and frozen-corpus
  checks. Runtime behavior and public prose claims were checked separately;
  the static validator does not execute XAMPP or fresh agents.

## Rendered evidence

- WordPress modes: Classic, Core Components, bundled WPDS and Hybrid.
- States: initial, loading, partial, empty, success, error, disabled and
  permission.
- Widths: 783, 782, 600, 390 and 320 CSS pixels, with 320 CSS pixels as the
  accepted 1280-at-400%-zoom reflow equivalent.
- Document shells did not overflow; the data table scrolled only in its named,
  focusable local region. Manual checks covered keyboard order, visible focus,
  recovery actions, accessible names and errors, live announcements, minimum
  target size, representative contrast, German expansion and RTL.
- An authenticated `axe-core` 4.13.0 scan of the WordPress 7.0 WPDS fixture for
  WCAG 2 A/AA, 2.1 A/AA and 2.2 AA returned zero violations and zero
  incomplete rules. The final Core/initial run initially found a 4.04:1 Core
  help-text contrast; after a documented plugin-scoped exception, its full
  tagged rerun also returned zero violations and zero incomplete rules. It
  complements rather than replaces the manual checks.
- At 320px, the German primary and secondary workflow actions wrapped into
  separate rows in source order, remained 40px high and caused no document or
  action-row overflow.

Detailed runtime observations are in
`docs/validation/wordpress-7-runtime-2026-09-03.md`. Review findings and their
canonical fixes are in `docs/reviews/final-skill-review-2026-09-03.md`.
Explicit rendered pass/fail assertions and their automation boundary are in
`docs/validation/rendered-checklist-2026-09-03.md`.

## Publication boundary

This record is the local acceptance boundary for release `v1.0.0` under MIT.
Version, date and package metadata are synchronized in the accepted tree.
Remote repository visibility, the release object and the one-tag invariant are
verified separately by the publishing operation and are not inferred from
these local checks.

The corrected-state SOL review returned GO. Fable's completed review found one
Medium and three Low documentation/routing inconsistencies, all corrected and
revalidated. Subsequent targeted Fable confirmation attempts failed at the
provider with HTTP 529 before processing; no final Fable GO is claimed.
