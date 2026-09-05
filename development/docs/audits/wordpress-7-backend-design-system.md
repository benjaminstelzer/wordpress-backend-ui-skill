# Audit: WordPress 7.0 backend design system for plugin interfaces

Status: 2026-09-03

## Audit objective

**Outcome:** A reliable basis for an agent Skill that can design or audit
WordPress 7.0 plugin interfaces in `wp-admin` with consistent spacing,
comprehensible vertical content flow, internationalizable strings, and
responsive behavior without page-wide horizontal overflow.

**Canonical owner:** Official WordPress 7.0 sources own the facts. The planned
Skill owns only the working rules derived from them and labeled as such.
Frontend rules from `theme.json`, block spacing, and theme layout are outside
this audit.

**Risk state:** Normal. The audit changes no WordPress runtime. The material
risk is false authority: an agent could present a derived convention as an
official WordPress rule or double classic Core spacing with a modern stack
system.

**Proof:** Source review of the WordPress 7.0 and Gutenberg `wp/7.0` commits
pinned in `docs/research/source-ledger.md`, plus official WordPress, WP-CLI,
WCAG, and i18n documentation. At this audit stage, no rendered plugin pages or
browser interactions had been tested.

## Summary judgment

WordPress 7.0 has no single, stable, complete Human Interface Guideline for
plugin backends. The Skill must therefore classify two axes separately rather
than merely distinguish Classic from React:

1. **Admin surface:** a plugin-owned page or an embedded/externally owned
   surface; version 1 supports only the plugin-owned pages defined in ADR-0001.
2. **Runtime/component owner:** PHP/Core markup, React with Core
   `@wordpress/components`, bundled experimental WPDS, or Hybrid with an owner
   for each DOM region.

Official sources provide concrete values but no complete semantic rule for
every vertical gap or user-guidance decision. A useful agent Skill must visibly
separate four fixed labels:

- **Core:** documented API, established admin convention, or an observed
  WordPress 7.0 implementation labeled as such.
- **WPDS:** an exact value or contract from an experimental `wp/7.0` package.
- **WCAG:** a normative accessibility requirement.
- **Skill-Norm:** a project-defined mapping that closes gaps and creates
  consistency.

## Source hierarchy

| Rank | Source | Authority for the Skill |
| --- | --- | --- |
| 1 | WordPress 7.0 Core CSS and official Plugin Handbook | Authoritative for classic `wp-admin` and Settings API behavior |
| 2 | Gutenberg branch `wp/7.0` | Authoritative for the examined WPDS tokens and components, but experimental |
| 3 | WordPress Accessibility Coding Standards and WCAG 2.2 AA | Minimum standard for perceivability, operability, understandability, and robustness |
| 4 | Established usability heuristics | Evidence for general user guidance, but not a substitute for WordPress conventions |
| 5 | Derived Skill-Norms | Binding for agent output, but never to be called official WordPress guidance |

The canonical source inventory is in `docs/research/source-ledger.md`. Every
supporting claim there receives a URL, ref/SHA or document status,
version/package, retrieval date, fact class, and revalidation trigger. Observed
Core selectors are not public extension APIs.

## Findings

### F-001: There is no single official backend HIG for plugin pages

**Observation:** The Plugin Handbook describes the Settings API as a route to
visually consistent, future-proof settings pages. Concrete layout values,
however, reside in Core CSS. In parallel, Core-provided React components and
separate experimental WPDS packages exist. React is therefore not synonymous
with WPDS.

**Impact:** An agent searching only for a "WordPress Design Guideline" can
easily mix frontend editor rules, classic `wp-admin`, and experimental WPDS.

**Skill requirement:** Before any design, the agent classifies the admin
surface first and then the runtime/component owner. Version 1 supports
plugin-owned single-site settings/tools pages, workflow/dashboard pages, data
views, and explicit Network Admin pages. Block Editor sidebars/SlotFills, the
editor canvas, post metaboxes, Dashboard widgets, profile fields, extensions of
Core lists, and UI inside another plugin are separately routed or excluded. No
spacing or component recommendation may be made before classification.

**Evidence:** [Settings API](https://developer.wordpress.org/plugins/settings/settings-api/), [`@wordpress/components`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/README.md), [`@wordpress/admin-ui`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/README.md), [`@wordpress/ui`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/README.md).

### F-002: Modern WPDS uses a 4 px base grid

**Observation:** The WordPress 7.0 dimension tokens define primitive spacing of
`0`, `4`, `8`, `12`, `16`, `20`, `24`, `32`, `40`, and `48px`. The semantic
gap scale is:

| Gap token | Default value |
| --- | ---: |
| `xs` | 4px |
| `sm` | 8px |
| `md` | 12px |
| `lg` | 16px |
| `xl` | 24px |
| `2xl` | 32px |
| `3xl` | 40px |

The padding scale is not identical: there, `xl` is `20px`, `2xl` is `24px`,
and `3xl` is `32px`. Tokens also have density variants. Density and
responsiveness are separate axes; "compact" is not a mobile mode.

**Impact:** A simplified list without token type produces errors, especially
for `xl` and `2xl`.

**Skill requirement:** The Skill must tabulate gap and padding separately.
Semantic `--wpds-*` tokens may be consumed only when the selected WPDS package
actually supplies them through a public stylesheet export loaded at the render
root; plugin code must not define, override, or imitate them. Primitive tokens
remain internal. Classic/Core and Core Components first use their own defaults
and APIs. An unavoidable plugin-owned number is labeled as a Skill-Norm, not a
WordPress token.

**Evidence:** [`@wordpress/theme` contract](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/README.md), [`dimension.json` at the pinned `wp/7.0` state](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/tokens/dimension.json).

### F-003: The modern Page shell provides a concrete starting point

**Observation:** By default, the `Page` component from `@wordpress/admin-ui`
uses `padding-lg` vertically and `padding-2xl` horizontally for the header and
padded content. At default density, that is `16px` vertically and `24px`
horizontally. Internally, the header uses `gap="sm"`, or `8px`; the subtitle has
`padding-block-end` with `padding-xs`, or `4px`.

**Impact:** `16/24px` is the strongest source-supported modern Page-shell value.
It is not a universal value for every nested group.

**Skill requirement:** For modern full pages, `16px block / 24px inline` is the
default. Narrow viewports may reduce inline padding, but must not switch it
implicitly through density tokens.

**Evidence:** [`Page` styles](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/src/page/style.scss), [`PageHeader`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/src/page/header.tsx).

### F-004: Vertical flow is not automatic in the modern Stack

**Observation:** `@wordpress/ui` supplies a flexible `Stack`. Its `direction`
and `gap` are optional and have no default. At the WordPress 7.0 pin,
`@wordpress/theme` exports `design-tokens.css` but no public runtime
`ThemeProvider`; the available `privateApis` are not a plugin contract. The
separate `__experimentalVStack` from `@wordpress/components` is itself
experimental; its `spacing` is a multiplier of the 4 px grid, not a semantic
WPDS gap name.

**Impact:** An agent must own spacing at every semantic level. Otherwise,
incidental browser margins or inconsistent one-off values emerge.

**Skill requirement:** A parent owns spacing between its direct children.
Children do not add the same outer spacing. Default heading and paragraph
margins are neutralized inside a gap-controlled stack. In the React/Core
Components path, specialized components own their internal rhythm. For a new
generic vertical plugin group, the Core-provided `Flex` component owns flow:
`direction="column"`, `align="stretch"`, `justify="flex-start"`,
`wrap={ false }`, `expanded={ true }`, and `gap` equal to the Skill-Norm divided
by four. This applies to `allow`, `deny`, and `unknown`; the experiment policy
still prevents new experimental APIs. In the bundled WPDS path, `Stack`
explicitly sets `direction="column"` and the semantic gap, loads the public CSS
subpath, and uses no private provider API. A plugin-local stack rule is allowed
only after an evidenced `Flex` gap.

**Evidence:** [`Stack` implementation](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/src/stack/stack.tsx), [`Stack` types](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/src/stack/types.ts), [`Flex` types](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/src/flex/types.ts), [`Flex` implementation](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/src/flex/flex/component.tsx), [`VStack` README](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/src/v-stack/README.md).

### F-005: Classic `wp-admin` has its own legacy rhythm

**Observation:** WordPress 7.0 Core includes, among other values:

- `#wpcontent`: `20px` left padding.
- `.wrap`: `10px 20px 0 2px` margin.
- `.wrap h1`: `0` margin and `9px 0 4px` padding.
- `.form-table td`: `15px 10px` padding.
- `.form-table th`: `20px 10px 20px 0` padding at `200px` width.
- `.form-table td p`: `4px` top and `0` bottom margin.
- `p.submit`: `20px` top margin and `10px` top padding.

**Impact:** A modern 4 px stack system must not be applied indiscriminately to
`.wrap`, `.form-table`, or `p.submit`. That creates duplicate spacing and breaks
visual integration with the admin.

**Skill requirement:** On native Settings API pages, Core owns outer and
row-level rhythm. Custom gaps apply only inside clearly bounded plugin
components.

**Evidence:** [`wp-admin/css/common.css` at the pinned WordPress 7.0 state](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/common.css), [`wp-admin/css/forms.css`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/forms.css).

### F-006: `782px` is the decisive Core boundary for form reflow

**Observation:** At a maximum of `782px`, Core reduces left `#wpcontent`
padding to `10px`, sets `.wrap` to `0` left and `12px` right margin, displays
form-table headings and cells as blocks, and makes typical form fields full
width. Text fields and selects receive at least `40px` height; text and selects
use a `16px` font. Mobile form rhythm changes to `10px` above the label and
`4px 0 6px` in the field area.

**Impact:** Responsive WordPress backend behavior is not merely smaller
spacing. Columns must stack, controls must grow to an operable height, and
reading order must be preserved.

**Skill requirement:** The Skill treats `782px` as a Core compatibility
boundary. Plugin-owned layouts should reflow intrinsically before that and must
not wait until `782px` to escape an unusable intermediate state.

**Evidence:** [`common.css`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/common.css), [`forms.css`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/forms.css).

### F-007: The modern packages remain experimental in WordPress 7.0

**Observation:** `@wordpress/ui` and `@wordpress/theme` describe themselves as
experimental. `@wordpress/ui` is not provided through global `window.wp` and
must be bundled. `@wordpress/admin-ui` has only minimal documentation. This is
distinct from the React path using Core-provided `@wordpress/components`.

**Impact:** A Skill must not treat the modern path as a stable, universally
available plugin API.

**Skill requirement:** WPDS examples must name bundling, version pins, the
token stylesheet, and experimental status. Core Components examples instead
use packages registered by WordPress and component APIs. The classic path
remains the stable baseline.

**Evidence:** [`@wordpress/ui`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/README.md), [`@wordpress/theme`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/README.md), [`@wordpress/admin-ui`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/README.md), [`@wordpress/components`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/README.md).

### F-008: WordPress defines no universal content width for plugin pages

**Observation:** The examined Core and WPDS sources provide shell spacing and
reflow behavior, but no universal maximum width for settings, dashboards, and
data tables.

**Impact:** One fixed `max-width` would be an invented WordPress rule and would
be unsuitable for data-rich pages.

**Skill requirement:** The Skill needs layout archetypes rather than a
universal width: focused settings, a multi-column overview, and a data-rich
list/table. Every width recommendation must be marked as a Skill-Norm, not a
Core fact.

### F-009: Use WordPress components and default CSS before custom CSS

**Observation:** The Plugin Handbook justifies the Settings API with visual
consistency, future-proofing, and less custom work. `@wordpress/components`
provides shared React UI elements. Core also provides native buttons, form
controls, notices, tables, and admin-shell classes. Which options are allowed
depends on runtime and DOM owner; an observed Core selector is not
automatically a public plugin API.

**Impact:** Custom CSS for existing WordPress primitives creates a parallel
design language, raises maintenance cost, and can hide Core updates, RTL, high
contrast, focus states, or mobile behavior.

**Skill requirement:** Before every custom CSS rule, the agent identifies
runtime and DOM owner and then checks: documented Core API/semantic markup;
suitable existing component or default CSS; an actually provided semantic
token; narrowly bounded composition; and only then justified plugin CSS. It
must not recreate a Core component merely to change spacing, colors, radii,
shadows, or control heights.

**Evidence:** [Settings API](https://developer.wordpress.org/plugins/settings/settings-api/), [`@wordpress/components` Component Reference](https://developer.wordpress.org/block-editor/reference-guides/components/), [Development Platform](https://developer.wordpress.org/block-editor/how-to-guides/platform/).

### F-010: Good user guidance starts with task, hierarchy, and next action

**Observation:** Established usability heuristics call for visible system
status, alignment with users' language, control and a way back, consistency
with platform standards, error prevention, and recognition rather than recall.
The WordPress admin roadmap names visual clarity, lower cognitive load, better
workflows, good defaults, density, usability, and accessibility as goals.

**Impact:** A pure spacing system can be formally consistent but still hard to
use. Spacing must reveal a real information and task hierarchy.

**Skill requirement:** Every page needs a clearly named primary task, a
recognizable current location, a prioritized next action, logical sections,
contextual help, and a safe path back in multi-step or destructive actions.
Decorative containers without a new relationship should be avoided.

**Evidence:** [Nielsen Norman Group: 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), [WordPress Admin Design](https://make.wordpress.org/core/2023/07/12/admin-design/).

### F-011: Navigation must fit the size of the plugin task

**Observation:** For a plugin with only one options page, the Plugin Handbook
recommends a submenu under an existing top-level menu such as Settings or
Tools.

**Impact:** A separate top-level menu for one small page lengthens global admin
navigation and gives the plugin more visual weight than its task warrants.

**Skill requirement:** The agent may recommend new top-level navigation only
for a standalone, multi-page area with justified primary use. A single settings
or tools page uses the existing Core context by default.

**Evidence:** [Plugin Handbook: Administration Menus](https://developer.wordpress.org/plugins/administration-menus/).

### F-012: State guidance and error handling are part of the design system

**Observation:** For classic settings, WordPress provides
`add_settings_error()`, `settings_errors()`, and admin notices. Core
`common.js` moves `div.updated`, `div.error`, and `div.notice` after
`.wp-header-end` unless they carry `.inline`; otherwise it uses the first title
in `.wrap`. `.below-h2` is only a deprecated compatibility name. React
interfaces have notice and snackbar patterns; snackbars are for short-lived,
low-priority messages, while more important messages should be notices. WCAG
2.2 requires textual error identification, visible labels or instructions, and
programmatically determinable status messages.

**Impact:** Without a state contract, users do not know what happened after
saving, loading, or an error, or how to continue. A color-only state or a
critical message that disappears is insufficient.

**Skill requirement:** Where the flow uses them, the Skill defines at least
initial, loading, empty, success, error, disabled, and permission states.
Classic pages place the page title and `.wp-header-end` in Core-compatible
order. Inline errors remain with the field using `.inline`, not `.below-h2`;
page-wide results use movable Core notices. Low-priority confirming React
feedback may use a snackbar when the information remains available elsewhere.
Every error names the problem and the next corrective step where known.

**Evidence:** [`add_settings_error()`](https://developer.wordpress.org/reference/functions/add_settings_error/), [`common.js` notice behavior](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/js/_enqueues/admin/common.js), [WordPress Notices](https://developer.wordpress.org/block-editor/how-to-guides/notices/), [Snackbar](https://developer.wordpress.org/block-editor/reference-guides/components/snackbar/), [WCAG 2.2 Error Identification](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html), [Labels or Instructions](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html), [Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html).

### F-013: WCAG 2.2 AA is the minimum standard for WordPress interfaces

**Observation:** WordPress Accessibility Coding Standards expect WCAG 2.2
Level AA for code in the WordPress ecosystem. Reflow generally requires use
without loss of information or function at a width equivalent to `320 CSS px`;
content requiring two dimensions, such as data tables, may use a local
exception. WCAG 2.2 AA also requires logical focus order, visible focus,
unobscured focus, and pointer targets at least `24 x 24 CSS px` or a permitted
spacing exception.

**Impact:** Responsive design cannot be tested only at common phone widths.
Zoom, keyboard, focus, labels, status messages, and local scroll containers are
part of the same quality boundary.

**Skill requirement:** WCAG 2.2 AA is the default. The Skill must distinguish
`320px` reflow, the WCAG `24px` minimum target, and the larger WordPress Core
mobile height of `40px`. Data tables may scroll horizontally in a local
container; the entire admin page must not thereby become two-dimensionally
scrollable.

**Evidence:** [WordPress Accessibility Coding Standards](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/accessibility/), [WCAG 2.2 Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), [Focus Order](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html), [Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum).

### F-014: The Skill must be able to direct Scoville UI but work without that dependency

**Observation:** The user requires a standalone WordPress Backend Skill and
optional conflict-free composition with Scoville UI. ADR-0002 gives the
WordPress Skill platform-specific factual and rule authority; general UI checks
may supplement it only within those boundaries.

**Impact:** When both are used, decision ownership must be clear. A hard
dependency would make the WordPress Skill needlessly unusable when Scoville UI
is not installed or active.

**Skill requirement:** The WordPress Backend Skill is complete standalone. When
Scoville UI is also active, the WordPress Skill owns WordPress-specific
components, defaults, tokens, spacing, the admin shell, and CSS exceptions.
Scoville UI owns remaining task guidance, hierarchy, state completeness,
accessibility, and rendered validation without overriding WordPress owners.

### F-015: Internationalization is a string, runtime, and layout contract

**Observation:** The Plugin Handbook requires a text domain matching the
lowercase, hyphenated plugin slug. User-facing PHP and JavaScript strings must
be marked with WordPress gettext functions, including ARIA, screen-reader, and
alternative text. The text domain must be literal. Complete phrases, plural
forms, context, positional placeholders, and immediately preceding
`translators:` comments preserve translatable grammar. JavaScript needs
`wp-i18n` or `@wordpress/i18n` and `wp_set_script_translations()` after script
handle registration. Custom JavaScript translations need the documented
PO-to-JSON and handle/path workflow. Translations are untrusted and escaped for
the output context. WordPress also recommends planning for doubled string
length.

**Impact:** i18n cannot be added after UI implementation as only a language
file. Concatenated strings, variable domains, missing JavaScript binding, fixed
widths, or left/right CSS may otherwise be impossible to translate or render
responsively and reliably.

**Skill requirement:** Every user-facing UI string in PHP and JavaScript is
extractable. The Skill requires one shared literal text domain, complete
phrases, positional placeholders, plural/context, `translators:` comments, and
context-appropriate escaping. Date and number values use `wp_date()`,
`number_format_i18n()`, or `dateI18n` from `@wordpress/date`. Client-side
locale-formatted numbers are formatted by the server in the baseline; a
JavaScript alternative needs its own source, locale mapping, and browser test.
Sources are extracted into POT with `wp i18n make-pot`; a test PO maintained
against it is compiled into loadable MO with `wp i18n make-mo`, and the plugin
language path is registered on `init` with `load_plugin_textdomain()`.
`wp i18n make-json --no-purge` creates the test JSON from the PO. Browser
assertions prove one genuinely translated PHP and React string after a
reproducible locale switch. Rendered cases cover doubled text, long German
labels, at least one RTL language, and locale-dependent formats.

**Evidence:** [How to Internationalize Your Plugin](https://developer.wordpress.org/plugins/internationalization/how-to-internationalize-your-plugin/), [Internationalization Guidelines](https://developer.wordpress.org/apis/internationalization/internationalization-guidelines/), [Internationalization Security](https://developer.wordpress.org/plugins/internationalization/security/), [JavaScript Internationalization](https://developer.wordpress.org/block-editor/how-to-guides/internationalization/), [`wp_set_script_translations()`](https://developer.wordpress.org/reference/functions/wp_set_script_translations/), [`load_plugin_textdomain()`](https://developer.wordpress.org/reference/functions/load_plugin_textdomain/), [`wp i18n make-pot`](https://developer.wordpress.org/cli/commands/i18n/make-pot/), [`wp i18n make-mo`](https://developer.wordpress.org/cli/commands/i18n/make-mo/), [`wp i18n make-json`](https://developer.wordpress.org/cli/commands/i18n/make-json/), [`wp_date()`](https://developer.wordpress.org/reference/functions/wp_date/), [`number_format_i18n()`](https://developer.wordpress.org/reference/functions/number_format_i18n/), [`@wordpress/date`](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-date/).

## Derived normative spacing matrix

The following matrix is a **Skill-Norm**, not an official WordPress HIG. It
closes the semantic gap identified in F-001 and F-004. Token names may be used
only in the bundled WPDS path when the public token stylesheet is loaded. In the
Classic or Core Components path, the same relationship guides selection of
existing defaults/APIs or a local exception explicitly marked as a Skill-Norm.

| Semantic relationship | Gap | WPDS gap name, if provided | Rule |
| --- | ---: | --- | --- |
| Control to help, status, or error text | 4px | `xs` | Tightest readable relationship; no additional child margin |
| Heading to its own introductory text | 8px | `sm` | Direct description of the same region; neutralize heading and paragraph margins in the stack |
| Directly related controls or icon and label | 8px | `sm` | One shared interaction block |
| Elements within a field group | 12px | `md` | Label, control group, and supplementary action |
| Related settings groups | 16px | `lg` | Normal local section rhythm |
| Independent sections | 24px | `xl` | Default between semantically complete sections |
| Large page regions | 32px | `2xl` | Header, main content, separate secondary region |
| Very strong separation | 40px | `3xl` | Exception, not the default between every block |

### Flow ownership

1. The direct parent owns spacing between siblings.
2. An element has no outer spacing when its parent already controls flow with
   `gap`.
3. Nested stacks use the semantically appropriate level; they do not blindly
   inherit the parent gap.
4. Visual containers such as a card or panel control internal padding, not the
   gap to an adjacent section.
5. Hidden or empty elements must leave no spacing hole.
6. Error, help, and status messages remain with the control whose state they
   explain.
7. In the classic Settings API path, these rules apply only inside plugin-owned
   components; Core remains owner of the form row.
8. On hybrid pages, every DOM region has exactly one runtime and spacing owner;
   this includes portals and overlays.
9. In a typical React-in-`.wrap` embedding, Core owns `#wpcontent`, `.wrap`, the
   page title, `.wp-header-end`, and page-wide notices; the plugin root owns only
   its inner subtree.
10. `.form-table` and a plugin-owned gap stack must not own the same subtree.
11. In the Core Components path, specialized components own their internal
    rhythm. For every `experimental_components_policy` value, new generic
    vertical groups use `Flex` with `direction="column"`, `align="stretch"`,
    `justify="flex-start"`, `wrap={ false }`, `expanded={ true }`, and `gap`
    `1/2/3/4/6/8/10`. Existing experimental subtrees remain their own owner;
    new local stack CSS needs an evidenced `Flex` gap.

## Derived responsive contract

This contract is also a Skill-Norm and must be labeled as such in the Skill.

1. **Intrinsic first:** Grid and Flex must reflow without a fixed page width.
   Long labels, localized text, and notices must not create page-wide
   horizontal overflow.
2. **Respect the Core boundary:** At `<=782px`, multi-column form and action
   layouts become single-column unless every element demonstrably remains
   operable and readable.
3. **Mobile controls:** Typical text inputs and selects receive at least the
   `40px` height used by Core; density tokens must not shrink touch targets.
4. **Do not double the shell:** Classic pages inherit `.wrap` and Core padding.
   Modern full pages start with `16px` block and `24px` inline padding; narrower
   inline padding must be explicitly defined and tested.
5. **Reading order:** Visual reordering must not conflict with DOM, keyboard, or
   screen-reader order.
6. **Actions:** Primary actions remain visible; secondary actions may wrap or
   move into an unambiguously labeled menu. Normal form actions must not require
   horizontal scrolling.
7. **Data views:** Wide data tables receive a deliberately documented small-screen
   presentation or a local scroll container; clipping or horizontal scrolling
   of the entire page is not a responsive strategy.
8. **Logical properties:** Plugin-owned CSS uses `margin-inline`,
   `padding-inline`, `block-size`, and `inline-size` where possible so RTL and
   different admin-shell widths do not break through left/right assumptions.
9. **Reflow floor:** Non-exempt content remains usable in one scroll direction
   at `320 CSS px` and corresponding zoom without loss of information or
   function.
10. **i18n stress:** Doubled text, long German labels, an RTL language, and
    locale-dependent values are regular layout cases, not late special tests.
11. **Test matrix:** Test the WordPress 7.0 fixture at least at `783`, `782`,
    `600`, `390`, and `320 CSS px`, plus `1280px` at `400%` zoom or equivalent
    reflow. Non-exempt page shells satisfy
    `document.documentElement.scrollWidth <= window.innerWidth`; required table
    overflow remains local.

## CSS ownership and exception contract (Skill-Norm)

The agent first identifies runtime and DOM owner, then follows this sequence and
stops at the first suitable owner:

1. Existing semantic HTML, WordPress API, and Core admin markup.
2. Existing Core class or WordPress component with its default CSS.
3. A semantic token actually provided by the loaded public runtime stylesheet.
4. Plugin-owned composition of existing primitives using `gap`, Grid/Flex, and
   logical properties.
5. A new narrowly scoped CSS rule only for a demonstrated gap.

A CSS exception must briefly establish in the agent output:

- which WordPress option was checked;
- why default CSS or a token cannot express the specific layout;
- the smallest plugin-owned scope of the rule;
- which Core/component defaults or actually provided tokens it still uses;
- how reflow, RTL, focus, zoom, and affected states are tested.

In the WPDS path, semantic `--wpds-*` may only be consumed; plugin code does not
define, override, or imitate that namespace. Primitive WPDS tokens are internal.
Classic/Core inherits Core rhythm; React/Core Components uses component
defaults and APIs. An isolated plugin gap may use a plugin-owned custom property
or a number marked as a **Skill-Norm**.

Prohibited practices include global `wp-admin` overrides, copying large Core
CSS blocks, imitated `--wpds-*`, new raw spacing values despite a suitable
owner, rebuilding existing buttons/inputs/notices only for different styling,
and `!important` without a documented unavoidable integration conflict. Custom
colors are excluded by default; if a genuine product function requires an
exception, it needs documented WCAG AA contrast evidence.

## Baseline user-guidance model (Skill-Norm)

### Task and information hierarchy

1. Exactly one primary title tells the person where they are.
2. Short context explains only what is needed before the first decision.
3. The primary task and next action are recognizable without searching by
   scrolling where the page type allows.
4. Sections follow task order rather than internal data or code structure.
5. Related controls are closer than independent groups; the normative spacing
   matrix makes the relationship visible.
6. Advanced or rare settings may be progressively disclosed but remain
   discoverable and retain their state.

### Actions and safety

1. A region has at most one visually primary action.
2. Secondary actions do not compete at equal strength; destructive actions are
   semantically and spatially separated.
3. Multi-step or destructive flows show the consequence, a way back, and where
   applicable recovery or confirmation.
4. Loading and saving state prevents unintended duplicate actions without
   making status or focus disappear.

### Forms

1. Every input has a persistently visible, programmatically associated label.
2. Help text explains format, consequence, or limits before an error and has
   the tightest `4px` relationship to the control; in WPDS this corresponds to
   provided `xs`, while in Classic Core owns `.description` rhythm.
3. Validation preserves entered values, identifies the specific field, and
   describes the error in text.
4. After a failed submit, a summary or focus management leads to the first
   meaningful correction point without creating a confusing focus order.
5. Dependent controls show cause and state; avoid disabling without explanation.

### System state and orientation

1. Every started action provides timely feedback.
2. Loading, empty, success, error, disabled, and permission states are defined
   only where the real flow has them, but completely when they occur.
3. Page-wide messages use WordPress notices; field-specific messages remain
   inline; snackbars are only for low-priority, non-exclusive information.
4. A state change is never conveyed only through color, position, or brief
   animation.
5. Structure remains stable enough across state changes for users to keep their
   orientation.

## Internationalization contract

1. The text domain is a literal string matching the lowercase, hyphenated
   plugin slug.
2. Every user-facing PHP string, including ARIA, screen-reader, and alternative
   text, uses the appropriate WordPress gettext function; output is escaped for
   its HTML, attribute, or other target context.
3. Every user-facing JavaScript string uses `@wordpress/i18n` or the registered
   `wp-i18n` dependency. `wp_set_script_translations()` is called only after
   script-handle registration with the same text domain and an explicit
   language-file path.
4. Complete phrases are translated; string concatenation and translated
   sentence fragments are prohibited. Multiple values use numbered positional
   placeholders so translations can reorder them.
5. Plural forms use `_n()`/`_nx()` or JavaScript counterparts; ambiguous terms
   receive context with `_x()`/`_nx()`.
6. Non-obvious placeholders or meanings receive a lowercase `translators:`
   comment immediately before the gettext statement.
7. URLs, markup, and variable data are not embedded as freely translatable
   content when safe placeholders or separate markup can express the case.
8. PHP formats date/time and numbers with WordPress locale APIs such as
   `wp_date()` and `number_format_i18n()`; JavaScript uses `dateI18n` from
   `@wordpress/date` for localized dates. Locale-formatted client numbers are
   server-formatted in the baseline; a JavaScript alternative needs separately
   evidenced locale mapping and a browser test.
9. After the JavaScript build,
   `wp i18n make-pot . languages/<slug>.pot --domain=<slug> --exclude=src`
   extracts PHP and the registered build path into a POT. A test PO named
   `<slug>-<locale>.po` is maintained against it, compiled with
   `wp i18n make-mo` into `languages/<slug>-<locale>.mo`, and the plugin
   language path is registered on `init` through `load_plugin_textdomain()`.
10. The same PO is converted to JSON with `wp i18n make-json --no-purge`. The
    golden case fixes either `<domain>-<locale>-<handle>.json` or correct PO
    file references to the registered build path for the MD5 name; `src/`
    references are prohibited when the registered script is under `build/`.
11. After a reproducible site and admin-user locale switch, browser assertions
    prove at least one genuinely translated PHP and React string. Hard-coded
    test strings are not runtime proof.
12. Doubled text, long German labels, at least one RTL language, and
    locale-dependent numbers/dates are part of spacing, responsive, and
    rendered validation.

## Composition contract with Scoville UI

- The WordPress Backend Skill has no technical or instructional runtime
  dependency on Scoville UI.
- When only the WordPress Skill is active, it must sufficiently cover the UI
  path, platform owner, spacing, responsive flow, baseline user guidance,
  states, and accessibility itself.
- When both Skills are active, the WordPress Skill is canonical owner for the
  WordPress backend design system, default CSS, component choice, tokens,
  spacing, and CSS exceptions.
- Scoville UI may improve open product-specific UI quality, but must introduce
  no parallel pixel values, breakpoints, components, or visual language.
- Scoville UI may audit rendered hierarchy, task flow, states, accessibility,
  and responsiveness; on conflict, the higher WordPress/accessibility owner
  prevails.
- Without an installed, loaded, or applicable Scoville UI Skill, the WordPress
  Skill must produce the same platform-specific decision.

## Agent anti-patterns

- Use frontend `theme.json`, `blockGap`, or theme spacing as a backend source.
- Present derived Skill-Norms as "official WordPress guidance."
- Equate gap and padding tokens because their names match.
- Automatically equate `compact` with mobile.
- Automatically equate React with experimental WPDS.
- Treat a missing project policy as silent opt-in to new experimental components.
- Under `deny` or `unknown`, skip an existing non-experimental Core component
  and write custom stack CSS directly.
- Define, override, or imitate `--wpds-*` on a page where the public token
  stylesheet does not supply it.
- Add a global stack gap to `.form-table`.
- Give individual children arbitrary `margin-bottom` values when the parent can
  own flow.
- Use one fixed universal width for settings, dashboards, and tables.
- Treat responsive design only as smaller spacing without testing reflow,
  control size, and reading order.
- Assume experimental packages are globally available through `window.wp`.
- Reimplement existing WordPress buttons, inputs, notices, or tables visually
  when Core or `@wordpress/components` covers the case.
- Target `.wp-admin`, `.wrap`, `.form-table`, or Core control classes with
  global plugin CSS to solve a local layout problem.
- Use multiple equally strong primary actions, decorative card nesting, or
  hidden state changes instead of clear user guidance.
- Concatenate user-facing strings, use a variable text domain, fail to bind
  JavaScript translations to the script handle, or treat translated output as
  trusted without checking.
- Present only POT extraction or hard-coded German/RTL test strings as proof of
  loaded PHP/JavaScript translations.
- Transform a WordPress locale into a JavaScript BCP 47 locale without an
  evidenced rule.
- Use fixed widths or left/right properties that break long translations or RTL.

## Required parts of the planned Skill

1. Clear triggers and exclusions for WordPress plugin backend rather than
   frontend/block theme.
2. Two-axis classification for admin surface and runtime owner with a support
   matrix.
3. Source ledger with ref/SHA, package version, retrieval date, support status,
   revalidation trigger, and `Core`, `WPDS`, `WCAG`, or `Skill-Norm` labels.
4. Separate tables for gap, padding, and density.
5. Normative vertical-flow matrix and flow-ownership rules.
6. CSS ownership ladder with a default-CSS-first rule and strict exception
   format.
7. Page shell, settings, section, card, toolbar, form, and Data View patterns.
8. Baseline rules for navigation, task hierarchy, actions, forms, states,
   feedback, and recovery.
9. Responsive contract including `782px`, `320px` reflow, intrinsic layout,
   RTL, and local Data View overflow.
10. Examples for PHP/Core, React/Core Components, bundled WPDS, and Hybrid with
    an owner for each DOM region.
11. Anti-patterns and a decision tree for mixed pages, portals, and overlays.
12. Standalone contract and optional composition with Scoville UI without a
    dependency.
13. Binding PHP/JavaScript i18n contract including text domain, PO/POT/JSON,
    runtime translation, escaping, plural/context, locale formats, doubled
    text, and RTL.
14. Routing, experiment-policy, spacing, CSS-ownership, UI-guidance/accessibility,
    and i18n golden cases frozen before Skill wording.
15. Reproducible separate WordPress 7.0 single-site and WordPress 7.0.x
    multisite fixtures with exactly pinned npm packages, lockfile, `npm ci`, a
    native XAMPP manifest and read-only validator, loaded public WPDS token
    stylesheet, and a Network Admin case.
16. Repository-free fresh-agent smoke test and rendered validation rubric for
    `783/782/600/390/320px`, zoom, keyboard, unobscured focus, target size,
    contrast, labels, error/status semantics, and localized content.

## Audit limits

- No live or screenshot review of a concrete plugin page.
- No complete color, typography, icon, or navigation specification. Core/WPDS
  colors remain the owner; WCAG AA contrast remains mandatory.
- No claim that experimental WPDS packages remain unchanged in a later
  WordPress 7.x version.
- No universal recommendation for content max width, table replacement, or
  navigation architecture without a concrete page type.
- The audit reviews sources and derives a Skill contract; it is not the Skill
  itself.

## Audit conclusion

The sources are sufficient to build a consistent Skill when the Skill routes
admin surface and runtime owner separately and discloses its own normative
layer. The central invariant is: **Core owns the legacy shell and native form
rhythm; a plugin owns only its bounded DOM regions; every flow has exactly one
parent owner; WPDS tokens exist only when their public stylesheet is loaded at
the render root.** Responsive multilingual consistency comes from intrinsic
reflow, the Core boundary at `782px`, logical properties, and tested text
expansion/RTL, not blanket reductions in spacing.
