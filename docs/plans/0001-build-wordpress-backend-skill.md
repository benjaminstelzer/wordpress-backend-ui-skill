---
format_version: 1
id: PLAN-0001
status: completed
created: 2026-09-03
updated: 2026-09-03
---

# Build a WordPress Backend Skill for consistent plugin interfaces

## Goal

Create a standalone installable agent Skill that first identifies the admin
surface and runtime owner for WordPress 7.0 plugin backends, then enables agents
to design, implement, and audit consistent interfaces using clearly evidenced
rules for components, spacing, vertical flow, user guidance, responsiveness,
and i18n. The Skill uses WordPress APIs, components, default CSS, and actually
available tokens before custom CSS. It may optionally use Scoville UI as a
supplementary UI guardrail but does not depend on it. Its basis is
`docs/audits/wordpress-7-backend-design-system.md`,
`docs/research/source-ledger.md`, and the accepted Decisions.

## Non-goals

- No frontend, block-theme, `theme.json`, or website-layout Skill.
- No claim of a complete official WordPress HIG while the sources do not
  provide one.
- No requirement to introduce experimental WPDS packages into Classic or Core
  Components pages.
- No dependency on Scoville UI or any other Scoville Skill.
- No parallel visual language replacing WordPress buttons, inputs, notices,
  tables, tokens, or admin-shell defaults.
- No GitHub push, tag, release, or other publication without separate
  authorization; the Plan creates only locally testable, publication-ready
  artifacts.
- No version 1 support for Block Editor sidebars or SlotFills, the editor
  canvas, post metaboxes, Dashboard widgets, profile fields, extensions of
  existing Core lists or screens, or UI inside another plugin.
- No plugin-specific product architecture, business logic, or branded
  interface.

## Work items

### W-001 Define the support matrix, runtime owners, and source contract

Status: done
Depends on: []
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010]
Outcome: The Skill has a deterministic two-axis classification for admin surface and runtime owner, an explicit version 1 support matrix, a source contract with fixed fact classes, and a standalone composition contract for Scoville UI.
Acceptance: `docs/research/source-ledger.md` lists URL, ref/SHA or document status, version/package, retrieval date, fact class, and revalidation trigger for every supporting source. `tests/cases/routing.yaml` contains at least twelve frozen positive, negative, and ambiguous cases with expected fields `surface`, `support_status`, `runtime_owner`, `shell_owner`, `spacing_owner`, `experimental_components_policy`, `references`, and `prohibited_recommendations`; all supported and excluded surfaces plus PHP/Core, React/Core Components, bundled WPDS, and Hybrid are represented. Standalone and Scoville UI composition produce the same WordPress-specific decision.
Steps:
1. Convert the ADR-0001 support matrix into triggers and non-triggers.
2. Define the fact classes `Core`, `WPDS`, `WCAG`, and `Skill-Norm`, plus the distinction among documented API, established convention, and observed implementation.
3. Maintain the source ledger with pinned WordPress 7.0 and Gutenberg `wp/7.0` snapshots.
4. Freeze the routing schema and golden cases before drafting the Skill.
5. Define standalone behavior and optional Scoville UI composition as a concern matrix.
Evidence: [`routing.yaml`: 17/17 unique cases and all eight required fields confirmed by contract validator, Live refs and package versions match the ledger, Support source and composition contract frozen]

### W-002 Specify the normative spacing and vertical-flow system

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010]
Outcome: The Skill contains runtime-specific spacing rules, a semantic vertical-flow norm, and a CSS ownership ladder that make two agents choose the same spacing owner and allowed expression for the same structure.
Acceptance: `tests/cases/spacing.yaml` names for each case its relationship, parent owner, runtime, expected token/API/Core default or justified Skill-Norm, and `experimental_components_policy: allow | deny | unknown`. For all three policy values, new generic Core Components groups expect `Flex` with `direction="column"`, `align="stretch"`, `justify="flex-start"`, `wrap={ false }`, `expanded={ true }`, a documented `FlexItem`/`FlexBlock` child role, and gap multiplier `1/2/3/4/6/8/10` for `4/8/12/16/24/32/40px`; `unknown` introduces no new experimental API. Existing experimental subtrees remain their own owner. `tests/cases/css-ownership.yaml` separates required reuse from genuine exceptions and requires an evidenced `Flex` gap before a local stack rule. The reference separates gap, padding, and density; documents the value sequence only as the WPDS gap scale or an explicitly marked Skill-Norm; governs parent ownership, margin reset, nesting, and empty states; and prohibits defining, overriding, or imitating `--wpds-*`. Classic inherits Core rhythm; specialized Core Components own their internal rhythm; generic vertical groups follow ADR-0010; WPDS consumes only provided semantic tokens; exceptions are marked as Skill-Norms.
Steps:
1. Transfer runtime-specific token, experiment-policy, component, and flow ownership from ADR-0010.
2. State the semantic spacing matrix explicitly as a Skill-Norm.
3. Define flow ownership for stack, section, card, field, message, portal, and overlay.
4. Separate Classic Core spacing from plugin-owned component rules.
5. Define the CSS-owner check and evidence-bearing exception format.
6. Freeze spacing and CSS golden cases before Skill examples.
Evidence: [Spacing specification frozen, 28 spacing cases including an error-free 21-case Flex matrix and nine CSS-owner cases checked with `ConvertFrom-Json`]

### W-003 Define the responsive layout contract and page archetypes

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010]
Outcome: The Skill can create consistent responsive structures for settings, workflow/dashboard, and data-rich pages that work within the WordPress admin shell without unintended horizontal scrolling and preserve reading and focus order.
Acceptance: The reference defines intrinsic reflow down to `320 CSS px`, the Core boundary at `782px` with checkpoints immediately above at `783px` and below, WordPress mobile controls, WCAG target size, shell padding, `1280px` at `400%` zoom or an equivalent reflow setup, logical properties/RTL, action wrapping, and local Data View scroll containers. Non-exempt page shells satisfy `document.documentElement.scrollWidth <= window.innerWidth` automatically. Settings, workflow/dashboard, and Data View have separate archetypes and no universal width presented as a Core fact.
Steps:
1. Document Core reflow facts separately from derived responsive Skill-Norms.
2. Define width and grid rules for three page archetypes.
3. Describe toolbar, form, card, and Data View reflow for each archetype.
4. Integrate DOM order, keyboard flow, RTL, doubled text, and overflow.
5. Define WCAG 2.2 AA requirements for reflow, focus, contrast, and target size.
6. Freeze viewport, zoom, and content stress cases before implementation.
Evidence: [Three responsive archetypes with 15/15 viewport cases plus 400 percent zoom and RTL stress frozen, Matrix and overflow invariants checked with `ConvertFrom-Json`]

### W-004 Define baseline user guidance, navigation, and state patterns

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010]
Outcome: The Skill leads from the primary user task to clear information hierarchy, predictable actions, understandable forms, and complete feedback and recovery states without introducing a design language foreign to WordPress.
Acceptance: Before W-005, `tests/cases/ui-guidance.yaml` freezes expected navigation, primary action, notice/inline owner, states, recovery, and accessibility invariants for every relevant surface. The reference checks menu placement, page title, `wp-header-end`, header action, navigation, progressive disclosure, heading/group hierarchy, labels/help text, error identification, loading, empty, success, error, disabled, and permission states, recovery, and WCAG 2.2 AA. Classic pages place movable page-wide notices so Core can align them at `.wp-header-end`; field-specific messages remain inline and use `.inline` instead of deprecated `.below-h2`. Every rule is classified as Core, WPDS, WCAG, or Skill-Norm. Custom colors are excluded; an unavoidable color exception needs contrast evidence.
Steps:
1. Convert verified WordPress, WCAG, and usability fundamentals into a prioritized agent checklist.
2. Define navigation and information architecture by page type.
3. Describe action hierarchy, form flow, status feedback, and recovery patterns.
4. Align notice placement and inline messages with Core behavior.
5. Document anti-patterns for decorative containers, multiple primaries, hidden states, and custom controls.
6. Freeze UI guidance and accessibility golden cases before Skill examples.
Evidence: [User-guidance and state contract with ten complete golden cases and eight relevant state types checked with `ConvertFrom-Json`]

### W-007 Specify the internationalization contract for PHP, JavaScript, and layout

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010]
Outcome: Every UI generated or audited by the Skill is extractable and translatable in PHP and JavaScript, safely rendered, and robust to language length, RTL, and locale-dependent formats.
Acceptance: For all user-facing strings including ARIA, screen-reader, and alternative text, the reference requires a literal text domain matching the plugin slug; PHP gettext and escaping functions; `@wordpress/i18n` or `wp-i18n`; a registered script handle before `wp_set_script_translations()` with an explicit language-file path; complete phrases, positional placeholders, plural/context, and immediately preceding `translators:` comments; `wp_date()`/`number_format_i18n()` and `dateI18n` from `@wordpress/date`. In the baseline, locale-formatted numbers displayed client-side are formatted by the server; a JavaScript alternative needs its own source, locale mapping, and browser test. `tests/cases/i18n.yaml` covers positive and negative PHP and JavaScript cases. Sources are extracted with `wp i18n make-pot` into a POT; a test PO maintained against it and named `<slug>-<locale>.po` is compiled with `wp i18n make-mo` to `languages/<slug>-<locale>.mo`, and the plugin language path is registered on `init` with `load_plugin_textdomain()`. The same PO produces the expected JSON file with `wp i18n make-json --no-purge`; the golden case fixes the documented handle filename or build-path/MD5 convention and prohibits `src/` references for a registered `build/` script. After a reproducible site and admin-user locale switch, browser assertions prove at least one genuinely translated PHP and React string. Layout cases with doubled text, long German labels, an RTL language, and locale-dependent numbers/dates lose no information or function.
Steps:
1. State the PHP, JavaScript, text-domain, and script-translation rules from ADR-0008.
2. Document string composition, plural, context, placeholders, translator comments, and escaping with positive and negative examples.
3. Define locale-aware date and number formatting.
4. Define source-to-POT, test PO, PO-to-MO, `load_plugin_textdomain()` on `init`, PO-to-JSON with `--no-purge`, and PHP/React runtime translation as reproducible checks.
5. Freeze i18n golden cases before Skill examples.
6. Feed doubled text, German, and RTL back into the spacing and responsive contracts.
Evidence: [i18n contract and 24 golden cases with positive and negative PHP JavaScript tooling runtime and layout cases checked with `ConvertFrom-Json`]

### W-005 Implement the Skill package with references, tests, examples, and GitHub documentation

Status: cancelled
Depends on: [W-002, W-003, W-004, W-007]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010]
Outcome: An installable Skill directory contains a compact `SKILL.md`, references loaded on demand, frozen golden cases, a WordPress 7.0 fixture, actionable examples, and concise publication-ready GitHub documentation without duplicate authority.
Acceptance: The validator `scripts/quick_validate.py` resolved from the installed `skill-creator` reports `Skill is valid!` for `<skill-root>`; the current local reference is `python "C:\Users\benja\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "<skill-root>"`. The Skill directory name matches the frontmatter `name`; unsupported extra keys are avoided. `SKILL.md` works standalone, routes only relevant references, and describes optional Scoville UI composition. Classic, Core Components, WPDS, and Hybrid examples name the surface and runtime, shell, spacing, and token owners; i18n is implemented in PHP and JavaScript; every custom CSS exception is justified. A root `README.md` follows the voice, directness, and user-focused progression of the local references `Z:\Projekts\AI\ask-claude-for-codex\README.md` and `Z:\Projekts\AI\ask-claude-and-sol-for-codex\README.md`: it begins with a concise statement of problem and benefit, mainly explains what the Skill does for WordPress plugin backends and when to use it, and names WordPress 7.0 focus, the spacing/vertical-flow contract, Core defaults before custom CSS, responsive behavior, accessibility, i18n, standalone use, and optional Scoville UI composition. Technical detail is limited to what is necessary for use, installation, requirements, reliable limits, sources, status, and license; internal architecture, repository tree, reviewer provenance, and unevidenced quality claims remain out. A root `CHANGELOG.md` records publication-relevant user-visible changes with clear categories and observed validation; until a release version is chosen, the entry remains `Unreleased`, and before publication version, date, package metadata, and tag must agree. `package.json` pins `@wordpress/env` to `11.0.1` and all bundled WPDS packages exactly to the ledger versions; the Node major is fixed through `engines` and `.nvmrc`, a lockfile exists, installation uses `npm ci`, and execution uses `npx --no-install wp-env`. `.wp-env.json` tests a real single-site installation; `.wp-env.multisite.json` starts explicitly with `--config=.wp-env.multisite.json` and its own `WP_ENV_PORT`, also pins `core` to `WordPress/WordPress#7.0`, sets `multisite: true`, and tests both Site and Network Admin. Rendered local checks additionally use only the new directory `Z:\xampp_lite_8_5\www\wordpress-backend-skill-test`; existing XAMPP sites remain untouched, and the local Apache, PHP, and MariaDB versions are captured as evidence. Reproducible setup sets site locale first and then admin-user locale, verifies the resulting `determine_locale()` value, and uses the bundled plugin test artifacts; Core language packs may be installed additionally but are not required for the plugin MO proof. The container WP-CLI version used is recorded as evidence. WPDS tests verify a loaded provider/styles and no unresolved `--wpds-*` reference.
Steps:
1. Create the Skill directory and frontmatter-conforming `SKILL.md` with Skill Creator.
2. Split spacing, responsive, user-guidance, i18n, component, and source references according to progressive disclosure.
3. Create Classic, Core Components, WPDS, and Hybrid examples against the golden cases.
4. Integrate standalone and optional Scoville UI composition instructions.
5. Create pinned Node dependencies, lockfile, separate WordPress 7.0 single-site and multisite fixtures, locale setup, and wp-env configurations.
6. Set up a separate local WordPress test installation at `Z:\xampp_lite_8_5\www\wordpress-backend-skill-test` for rendered browser checks without changing existing sites.
7. Create the root `README.md` in Benjamin's voice from the two Ask Skill references and the root `CHANGELOG.md` as a user-visible release record.
8. Run the validator, `npm ci`, `npx --no-install wp-env`, and internal path/link checks.
Evidence: [`wordpress-backend-ui/SKILL.md` and all routed references implemented, ADR-0011 corrected the started WPDS path to public exports only while authored fields remained unchanged, Format 1 preserves started W-005 Decisions and links ADR-0011 here and in still-editable W-006, The heading-to-intro contract missing in review was added transparently during W-005 as the 28th spacing case `wpds-heading-intro` and protected by the contract validator, ADR-0012 baselines the corrected six-file golden corpus by SHA-256 manifest for W-006 instead of claiming an unsaved 27-case prior state, Skill Creator validator reports `Skill is valid!`, Contract validator PHP lint and Scoville Plan validator passed, Node 24.20.0 production build passed, Clean `npm ci` with 1910 packages and `npm ls --depth=0` at exact pins passed, POT PO MO and Jed JSON updated from `build/index.js`, Site locale then admin-user locale set to de_DE and `determine_locale()` observed as de_DE on Single Site and Multisite, WordPress 7.0 Single Site at `Z:\xampp_lite_8_5\www\wordpress-backend-skill-test` and WordPress 7.0.4 Network Admin at `Z:\xampp_lite_8_5\www\wordpress-backend-skill-test-multisite` rendered, Final delayed WPDS fallback Core notice announcement path all viewports German PHP and JavaScript i18n RTL and context-faithful permission recovery passed, Fable and SOL report no High or Medium findings in the final rereview, Review evidence is in `docs/reviews/final-skill-review-2026-09-03.md`, Runtime evidence is in `docs/validation/wordpress-7-runtime-2026-09-03.md`, MIT License is consistent in LICENSE README package.json and CHANGELOG, Both pinned wp-env starts reach `spawn docker ENOENT` because Docker is unavailable, No Docker runtime pass is claimed, User excluded Docker and selected the native XAMPP successor through ADR-0013; W-005 is replaced without reinterpreting its Acceptance]

### W-008 Make Docker-free XAMPP acceptance reproducible

Status: done
Depends on: [W-002, W-003, W-004, W-007]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010, ADR-0013]
Outcome: The complete Skill package has a canonical Docker-free, read-only-verifiable XAMPP acceptance path for an isolated WordPress 7.0 single site and WordPress 7.0.x multisite, without binding the published Skill to XAMPP or Scoville UI.
Acceptance: `fixture/native-xampp.json` fixes relative paths, exact WordPress version, single/multisite mode, active fixture status, `de_DE`, and required build artifacts for both isolated sites. `scripts/validate-xampp-fixtures.ps1` accepts the XAMPP root as a parameter or through `XAMPP_LITE_ROOT`, resolves only paths within that root, and checks read-only PHP, WP-CLI, Apache, MariaDB, both Core versions, site types, active plugin, junctions pointing to `fixture/plugin`, site and admin locale, and build artifacts without outputting credentials. The script passes against `Z:\xampp_lite_8_5`. `package.json`, lockfile, README, fixture documentation, and runtime evidence use this native path as canonical acceptance; `.wp-env.json`, `.wp-env.multisite.json`, `@wordpress/env`, and the `wp-env` script are removed. The Skill Creator validator, contract validator, PHP lint, production build, clean `npm ci`, and `npm ls --depth=0` pass on the final package. POT, PO, MO, and Jed JSON remain reproducible, and already rendered Single Site/Network Admin, responsive, accessibility, i18n, RTL, and WPDS observations are not overstated by the runtime preflight.
Steps:
1. Transfer ADR-0013 into native fixture configuration, validator, and documentation.
2. Remove Docker/wp-env package artifacts and the unnecessary dependency.
3. Run the read-only XAMPP preflight against both existing isolated sites.
4. Repeat build, contract, i18n, PHP, Skill, and dependency checks on the final package.
5. Update runtime evidence and the Plan only with observed results.
Evidence: [Native XAMPP validator passed read-only for WordPress 7.0 Single Site and WordPress 7.0.4 Multisite, PHP 8.5.5 WP-CLI 2.12.0 Apache 2.4.66 and MariaDB 11.4.10 confirmed exactly, Both fixture junctions activation modes and de_DE locale checks passed, Clean Node 24 `npm ci --offline` installed 1667 lockfile packages and `npm ls --depth=0` passed, Production build contract validator PHP lint Skill Creator validator POT MO and Jed JSON passed, Docker configurations direct @wordpress/env dependency and wp-env script removed, Runtime evidence documents the online stall and passing offline clean install without claiming an online pass]

### W-006 Validate agent behavior and rendered results

Status: done
Depends on: [W-008]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010, ADR-0011, ADR-0012, ADR-0013]
Outcome: The completed Skill is tested through golden cases, a fresh-agent run, and rendered WordPress 7.0 plugin backends against incorrect owners, inconsistent spacing, unnecessary custom CSS, i18n failures, poor user guidance, and responsive defects.
Acceptance: Documented tests cover standalone use without Scoville UI, optional composition, all four runtime owners, unclear and excluded surfaces, Single Site and Network Admin, notice placement, long and doubled German labels, RTL, working PHP and JavaScript runtime translation, locale formats, all relevant states, action wrapping, CSS exceptions, and Data View reflow. Rendered checks run at `783`, `782`, `600`, `390`, and `320` CSS pixels and at `1280px` with `400%` zoom or equivalent. Explicit pass/fail assertions test focus order, visible and unobscured focus, keyboard operation, `24x24px` pointer targets or permitted exceptions, WCAG AA contrast, accessible names and labels, textual error identification, and programmatic status messages; an automated scan is supplemented by manual keyboard/focus testing. Non-exempt page shells satisfy `document.documentElement.scrollWidth <= window.innerWidth`; tables scroll locally only. A clean-install/fresh-agent smoke test runs in a clean working directory without repository context and with only the installed Skill; the frozen prompts must produce the expected owners and `prohibited_recommendations` and, in the Classic case without a loaded WPDS runtime, recommend no `--wpds-*`. The same corpus is then repeated separately with the Scoville UI version recorded in the ledger. README installation and usage instructions are executed from a clean working directory; all public claims are checked against observed Skill behavior, relative links and GitHub Markdown must work, and the changelog may name only changes actually implemented and validated. Before any later separately authorized publication, README, changelog, package version, date, and release metadata must be consistent. All material defects found are corrected at the canonical owner and affected checks pass again.
Steps:
1. Verify the golden oracles rebaselined after review under ADR-0012 against `tests/cases/MANIFEST.sha256` and prove they remain unchanged since that baseline.
2. Run the native XAMPP validator against the manifested single-site and multisite fixtures and confirm reproducible site and admin-user locale setup.
3. Run fresh-agent cases outside the repository first standalone and then with the recorded Scoville UI version.
4. Check source fidelity, routing, component selection, i18n, CSS owner, and spacing outputs deterministically.
5. Render and operate the local XAMPP site and reproducible fixtures under every viewport, zoom, RTL, language, and input condition.
6. Follow the README from a clean working directory, verify public claims and links against artifacts, and check changelog and release metadata for consistency.
7. Correct defects at the canonical owner and repeat targeted and full checks.
8. Record observed evidence and complete the Plan only then.
Evidence: [ADR-0014 corrects and baselines the routing policy; manifest and contract validator pass, Eight current prompts pass repository-free 8/8 standalone and 8/8 with optional Scoville UI, Native XAMPP acceptance passes for WordPress 7.0 Single Site and 7.0.4 Multisite with de_DE, Rendered checklist passes at 783 782 600 390 and 320px including local table and action wrapping, Final Core axe rerun passes after a documented local contrast exception with 0 Violations and 0 Incomplete, Clean snapshot build i18n PHP lint Skill and Plan validators pass, SOL reports GO in the corrected final review; every actual Fable finding is fixed, targeted Fable confirmation ended provider-side with 529 and is not claimed as GO]
