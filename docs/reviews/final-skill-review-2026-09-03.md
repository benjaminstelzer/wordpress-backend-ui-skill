# Final Skill review — 2026-09-03

## Scope

Fable and SOL reviewed the completed Skill package read-only before the final
test run. The review covered the standalone Skill contract, optional Scoville
UI composition, public WordPress/WPDS APIs, spacing ownership, vertical flow,
responsive behavior, accessibility, PHP/JavaScript i18n, fixture behavior,
validators and GitHub-facing documentation.

## Material findings resolved

- Removed the non-public `ThemeProvider` route and private API assumptions.
  The bundled WPDS route now copies the public
  `@wordpress/theme/design-tokens.css` export unchanged and uses public
  `@wordpress/ui` components at default density.
- Replaced variable JavaScript text domains with the literal plugin domain and
  generated POT, translated PO, MO and path-hashed Jed JSON artifacts from the
  registered `build/index.js` path.
- Added all four runtime modes and all eight required UI states.
- Made the two vertical-flow owners explicit: 32px between major page regions,
  8px between a heading and its own introductory copy, and 16px between related
  form/workflow groups.
- Added current 40px component sizing, a functional dismiss action, associated
  Classic field labels, visible focus for the scroll region, programmatic
  disabled reasons and focusable-but-inactive disabled actions.
- Registered the generated RTL stylesheet and verified that WordPress replaces
  the LTR fixture stylesheet in an RTL admin locale.
- Separated page-level Core Notices from local React state through
  `wbui_notice`, preventing retry/dismiss actions from leaving stale or
  duplicate messages.
- Lifted React state to the fixture root so Empty and Error recovery actually
  controls Data View visibility.
- Made permission recovery context-aware: Network Admin returns to Network
  Admin, not to a site dashboard.
- Made PHP and JavaScript date examples deterministic while retaining both
  `wp_date()` and `dateI18n()` with the WordPress date format.
- Kept `@wordpress/components` Notice as the sole owner of React-state
  announcements. Each Notice now receives a message-only `spokenMessage`;
  recovery controls use the public `actions` prop and are not serialized into
  the announcement. The WPDS Suspense fallback remains a separate status
  region because it is not a Notice.
- Added a build-specific Suspense regression oracle so a stale bundle cannot
  lose the fallback heading referenced by `aria-labelledby`.
- Documented build-before-contract-check order and the Docker limitation.

## Historical publication decision

The first review round observed that Docker was unavailable and the then-pinned
`wp-env` configurations stopped at `spawn docker ENOENT`. ADR-0013 subsequently
replaced that retired path with the native read-only XAMPP contract; the
`wp-env` configurations and dependency no longer exist in the current package.
WordPress 7.0 Single Site and WordPress 7.0.4 Network Admin rendering remains
recorded against the isolated XAMPP installations.

The repository license was subsequently set to MIT and is no longer an open
publication decision.

## Review status

Fable and SOL both returned GO after the final Notice, actions, announcement,
fallback-build and Plan corrections. Neither reported a remaining High or
Medium finding. The result is recorded here rather than used as a public
quality claim in the README.

## Corrected-state closure review

A later pre-closure review covered the Docker-free package and fresh-agent
corpus. It found and triggered these additional canonical fixes:

- ADR-0014 aligns the Network Admin Core-only Hybrid policy with `deny`, adds
  every missing structured routing value and completes editor-canvas/profile-
  field Golden coverage.
- Route-specific prohibited subsets are contract-validated; the shipped
  routing reference is the sole canonical contract owner.
- The repository-free corpus now covers eight prompts. Its new post-metabox
  case first exposed an ambiguous host policy, then passed standalone and with
  optional Scoville UI after the explicit excluded-host matrix was installed.
- The rendered fixture now exercises a wrapping primary/secondary action row.
  Its Core help text exposed a 4.04:1 default contrast; one plugin-scoped color
  exception raised it above 6.5:1 and the tagged axe rerun passed 0/0.
- Stale `@wordpress/env`, hard-coded asset-dependency, internal-selector,
  personal-path and evidence-attribution wording was corrected.

SOL returned GO on this corrected state. Fable's corrected-state pass found one
remaining Medium contradiction in the Hybrid example (`unknown` versus the
canonical `deny`) and three documentation traceability items. The example and
documentation were corrected before the targeted closure rerun.

The targeted SOL rerun returned GO. Four targeted Fable attempts ended at the
provider with HTTP 529 before processing the check (zero input/output tokens),
so no later Fable GO is claimed. The four concrete Fable findings were checked
against the live files by the contract/Skill validators and the SOL rerun; the
provider failure remains an external review-evidence limitation, not a hidden
pass.
