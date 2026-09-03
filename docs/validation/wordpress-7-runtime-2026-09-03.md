# WordPress 7.0 runtime validation — 2026-09-03

## Environment

- WordPress Single Site: exact `7.0` at
  `Z:\xampp_lite_8_5\www\wordpress-backend-skill-test`.
- Multisite/Network Admin:
  `7.0.4` at
  `Z:\xampp_lite_8_5\www\wordpress-backend-skill-test-multisite`.
- Apache `2.4.66`, PHP `8.5.5`, MariaDB `11.4.10`, WP-CLI `2.12.0`.
- Node `24.20.0`; official portable archive SHA-256
  `6cac9ffbca8f6a47091e4b5c772e0606049c3871cb67d900c0cedde630e545ba`.
- Native fixture contract: `fixture/native-xampp.json`, verified read-only by
  `scripts/validate-xampp-fixtures.ps1` with `-XamppRoot Z:\xampp_lite_8_5`.

## Build and static checks

- Clean Node-24 `npm ci --offline --no-audit --no-fund` in a repository copy
  without `node_modules`: passed, 1667 packages installed from the lockfile.
- Clean `npm ls --depth=0`: passed with every direct package at its exact pin.
- Production `npm run build`: passed; emitted `index.js`, `index.asset.php`, the
  asynchronous public-WPDS chunk, LTR/RTL local CSS and copied public token CSS.
- Skill Creator quick validator: `Skill is valid!`.
- Frozen-contract validator: passed.
- Scoville Plan format validator: passed with 16 files, 1 Plan, 8 Work Items,
  14 Decisions, 0 errors and 0 warnings after the completion transition.
- PHP syntax check: passed.

The clean npm install reported upstream deprecation notices and four npm 11
install-script approval notices. The production build still completed without
those scripts and no package pin was loosened. Two network-backed `npm ci`
attempts made no progress to an exit on this host; neither was counted as a
pass. The offline clean install used the already populated npm cache and the
same final lockfile.

## Native runtime preflight

The native validator passed with no state changes and reported:

- Single Site: WordPress `7.0`, mode `single`, fixture `active`, locale
  `de_DE`.
- Network fixture: WordPress `7.0.4`, mode `multisite`, fixture
  `network-active`, locale `de_DE`.
- Both plugin paths are Junctions to this repository's `fixture/plugin`.
- Site locale, administrative-user locale and `determine_locale()` are
  `de_DE` on both fixtures.
- All five required generated build artifacts exist.

## WordPress runtime coverage

- Runtime modes: `classic`, `core`, `wpds`, `hybrid`.
- UI states: `initial`, `loading`, `partial`, `empty`, `success`, `error`,
  `disabled`, `permission`.
- Classic mode loads no fixture JavaScript or WPDS token asset.
- Core mode loads Core Components without the bundled WPDS chunk or token CSS.
- WPDS and Hybrid load the public token stylesheet and asynchronous Stack
  chunk; computed `--wpds-dimension-gap-sm` and the heading-to-intro Stack gap
  are 8px.
- With the WPDS chunk delayed by 1.5 seconds, the fallback contains exactly one
  heading matching its `aria-labelledby` target and one status; after loading,
  the fallback is removed and exactly one final heading remains.
- Network Admin renders the translated React fixture without the site-only
  Settings form and keeps the permission return path in Network Admin.
- Fresh final navigations on Single Site and Network Admin produced no console
  warnings, console errors or uncaught page errors.

## Responsive and accessibility evidence

At 783, 782, 600, 390 and 320 CSS pixels, Single Site and Network Admin satisfy
`document.documentElement.scrollWidth <= window.innerWidth`. At narrow widths,
the data table overflows only inside its named, focusable region. A 320 CSS-px
viewport is the accepted equivalent of a 1280px viewport at 400% zoom.

An authenticated Playwright run injected the lockfile-resolved `axe-core`
4.13.0 and ran the WCAG 2 A/AA, 2.1 A/AA and 2.2 AA tag sets. The earlier
WPDS/initial scan returned zero violations and zero incomplete rules. The final
Core/initial scan at 320px first exposed a Core-default `TextControl` help
contrast of 4.04:1. A plugin-scoped exception on plugin-owned help content
raised it above 6.5:1; the full tagged rerun then returned zero violations and
zero incomplete rules. The scan complements the manual interaction and
measurement checks below; it does not replace them.

Observed interaction checks include:

- DOM-order keyboard navigation through Classic and React controls.
- Visible, in-viewport focus on fields, actions and the data scroll region.
- Keyboard horizontal scrolling of the data region from 0px to 200px.
- Accessible names for the Classic endpoint field and the data region.
- Focusable disabled actions with `aria-disabled="true"`, a valid
  `aria-describedby` target and no activation.
- Loading, Partial, Empty, Error and Success were captured in the WordPress
  `#a11y-speak-polite` or `#a11y-speak-assertive` regions with only the message
  text; recovery-action labels did not leak into the announcement. The
  Permission state keeps a visible reason linked through `aria-describedby`;
  no separate live-region claim is made for that initial state.
- Every visible fixture target at 320 CSS pixels measured at least 24x24px;
  text fields and primary actions measured 40px high.
- The German primary and secondary workflow actions wrapped into separate rows
  at 320px, retained source order, remained 40px high and produced neither
  document nor local action-row overflow.
- Representative contrast ratios: page/section title 13.94:1, body/table text
  8.8:1, primary action text 5.61:1.
- Success action and dismissal work; Empty/Error recovery and Data View
  visibility are regression-tested after the final state-owner correction.

## Internationalization evidence

- German PHP title and React strings load from the plugin's MO/Jed JSON files.
- Locale setup was applied in the required order on both XAMPP fixtures: site
  `WPLANG=de_DE`, then admin-user `locale=de_DE`. A user-scoped WP-CLI call to
  `determine_locale()` returned `de_DE` on Single Site and Multisite.
- Long German labels reflow at 320 CSS pixels without document overflow.
- PHP number output is `12.345,67`.
- PHP `wp_date()` and JavaScript `dateI18n()` use the same fixed fixture instant
  and the WordPress date format.
- Arabic admin locale produces `lang="ar"`, `dir="rtl"`, no page overflow and
  a request for `style-index-rtl.css`; the user locale is restored to `de_DE`
  after the test.
- The temporary Single-Site browser-test administrator was removed after the
  final run; the isolated WordPress installations and fixture remain in place.

The explicit assertion table and the CSS-exception record are in
`docs/validation/rendered-checklist-2026-09-03.md`. These checks were
interactive observations; no credential-bearing browser harness or session
artifact is committed.

## Reproducibility boundary

Docker and `wp-env` are no longer part of the project gate. The native
PowerShell validator verifies the existing isolated XAMPP installations but
does not create WordPress databases, users or credentials. Rendered browser
evidence remains separate from the read-only preflight; the preflight does not
by itself prove layout, accessibility or interaction behavior.

## Fresh-agent behavior

The frozen repository-free corpus in `tests/agent-prompts.json` contains eight
prompts covering Classic, Core Components, bundled WPDS, Hybrid, Network
Admin, excluded Block Editor and post-metabox surfaces, and an ambiguous React runtime. Its
SHA-256 is recorded in `tests/agent-prompts.sha256`.

Two fresh agents received only a clean installed copy of the Skill and the
frozen prompts:

- Standalone: 8/8 cases returned the exact expected `surface`,
  `support_status`, `runtime_owner`, `shell_owner`, `spacing_owner` and
  `experimental_components_policy`; every expected prohibited recommendation
  was present.
- With the pinned Scoville UI snapshot: 8/8 cases returned the same exact
  WordPress fields and required prohibitions. The additional guidance stayed
  within task flow, affected states, accessibility and rendered validation;
  it did not introduce another shell, runtime, spacing scale or token owner.

The Scoville UI snapshot used for the optional-composition run had SHA-256
`95e17c7f1d2430a7e07edcfcaa20dcf54bdf44a7f7118b2a416b72ec24bcc99b`,
matching the source ledger. The Skill remains independently installable and
does not load or require that snapshot in standalone mode.

The eighth post-metabox prompt initially exposed an ambiguous excluded-host
policy in the installed reference: both agents returned `unknown`. Under
ADR-0014, the canonical owner was corrected with an explicit excluded-host matrix, a new
clean Skill copy was installed, and fresh standalone and composed reruns then
returned the expected `deny` policy and all required handoff prohibitions. The
retained seven results already contained the now-required Network Admin
Classic prohibition, so all eight current expected subsets are evidenced.
