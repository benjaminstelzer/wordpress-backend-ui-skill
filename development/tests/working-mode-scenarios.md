# Working-mode acceptance scenarios

These scenarios supplement the frozen surface/runtime cases. They are manual
behavioral checks, not assertions executed by `check:contracts`. For a fresh
agent evaluation, supply the candidate Skill, the request, and the relevant
raw fixture or project inputs. Keep the acceptance criteria with the evaluator.
Judge actual actions, edits, findings, and evidence claims, not exact wording.
Record execution separately. Listing a scenario does not mean it has passed.

## 1. Source-only spacing audit

Request: "Check only the vertical spacing in this plugin-owned PHP settings
page on WordPress 7.1. Use the supplied source only. Do not change files."

Inputs: Core `.wrap` and `.form-table` markup with no token references, plus a
plugin-owned group with both parent `gap` and child outer margins. The source
also contains an unrelated untranslated label. No browser is available.

Accept: Audit of the spacing owners and potentially additive margins, with a
source-level finding and rendering explicitly unverified. No token-registry
blocker, i18n audit, RTL test, browser requirement, or file edit. No claim of a
measured rendered distance or full UI compliance.

## 2. Focused spacing correction

Request: "Check and fix the doubled spacing in this group. Keep the rest of
the Classic settings page unchanged."

Inputs: The same spacing source plus rendered evidence of additive spacing.

Accept: Inspect, then Implement only the necessary correction in the owning
region. Preserve native controls, `.wrap`, `.form-table`, unrelated copy, and
the existing runtime. Verify the affected spacing and any relevant wrapping or
hidden-child behavior. No full redesign or forced token/React migration.

## 3. New page versus design-only output

Request: "Create a plugin-owned PHP settings page using the Settings API.
It needs English and German i18n-readiness, not completed translations."

Accept: Implement with relevant page-wide design-system concerns, responsive
and accessibility checks, and extractable strings. No mandatory catalogs or
RTL checks. Source-only evidence is not reported as rendered proof.

Variant: "Design this page and explain the structure. Do not edit code."

Accept: Implement mode with design-only output. No code edits or claim of an
implemented or tested page.

## 4. Full page audit

Request: "Audit the complete plugin-owned workflow page, including its states,
accessibility, responsive behavior, custom CSS, and i18n-readiness."

Inputs: One named page and its supported states, with English/German UI scope.

Accept: Audit with broad scope for that page, not another mode or a repository-
wide audit. Inspect the relevant responsive matrix and possible states, report
evidence limits, and leave the implementation unchanged. No forced PO workflow
or RTL test. Each finding identifies location, rule, deviation, impact, smallest
correction, and evidence limit. A requested report file does not authorize fixes.

## 5. Language-scoped readiness

Request: "Audit i18n-readiness on this plugin page. We do not ship catalogs yet."

Inputs: Correct PHP/JS i18n APIs and loading hooks, no catalogs, and a defined
Arabic admin-user language requirement on an otherwise English site.

Accept: Audit the readiness path and affected RTL layout. Do not generate PO
files or require loaded translations merely to establish readiness. Account
for the admin-user language, not only the site language.

Variant: The target languages are unspecified, with no RTL requirement.

Accept: Do not require RTL testing or block readiness on that uncertainty.
Do not claim RTL support was verified.

## 6. Optional Scoville UI composition

Request: "Use WordPress Backend UI and Scoville UI to check only this plugin
toolbar's spacing. Do not change the implementation."

Inputs: A plugin-owned Core Components toolbar and its relevant layout evidence.

Accept: Both Skills preserve Audit and its spacing scope. No full state/i18n
audit, editing, parallel design system, or obligatory sibling installation.
Repeat without Scoville UI available. WordPress ownership and scoped findings
must remain usable standalone.

## 7. Excluded host surface

Request: "Check and fix spacing in this Block Editor sidebar SlotFill."

Accept: Identify the excluded host-owned surface and route to that owner.
Implement mode does not grant this Skill ownership. Do not impose its plugin
page shell or generic spacing matrix on the sidebar.
