# Surface and runtime routing

Classify the surface before the runtime. Do not infer either from the other.

## Surface support

| Surface | Version 1 status | Shell owner |
| --- | --- | --- |
| Plugin-owned single-site settings or tool page | supported | Core admin shell |
| Plugin-owned workflow or dashboard page | supported | Core shell plus explicit plugin root |
| Plugin-owned data view | supported | Core shell plus explicit plugin root |
| Plugin-owned Network Admin page | supported with explicit Multisite context | Network Admin shell |
| Block Editor sidebar or SlotFill | excluded | Block Editor owner |
| Editor canvas | excluded | Editor owner |
| Post metabox | excluded | Post editor/metabox owner |
| Dashboard widget | excluded | Core Dashboard owner |
| Profile field | excluded | Core profile-screen owner |
| Extension of an existing Core list or screen | excluded | Host Core screen |
| UI inside another plugin | excluded | Host plugin |

For an excluded surface, route to its host and stop. Do not apply a
plugin-owned page shell, a generic spacing matrix, or global admin CSS.

## WordPress version and capabilities

| Target | Core token stylesheet | Public provider | Routing consequence |
| --- | --- | --- | --- |
| 7.0 pinned baseline | No Core `wp-theme` style handle in the verified baseline | Not exported by pinned `@wordpress/theme` 0.7.1 | Preserve Classic/Core defaults. The explicitly opted-in bundled experimental path below remains version-specific. |
| 7.1 | Core registers `wp-theme` with semantic tokens for plugin UIs | Public `ThemeProvider` from `@wordpress/theme` through the Core script handle | PHP may consume Core tokens without React. React may use the public provider when needed. Neither requires experimental-component opt-in. |

Check the actual supported installation and minimum supported version. Style
and script registries are separate even though both use `wp-theme`. Registration
does not prove enqueue, successful loading, token availability, or rendering.
Read [version-compatibility.md](version-compatibility.md) for examples and checks.
Do not infer future 7.x contracts or package versions from either row.

## Runtime owners

### PHP/Core

- Use WordPress APIs, semantic admin markup, Core classes, and Core default CSS.
- Core owns `.wrap`, the page title, `.wp-header-end`, native Notices,
  `.form-table`, controls, and `p.submit` where those structures are used.
- Preserve existing Classic pages. No mandatory token conversion, React rewrite,
  or replacement of native elements follows from a WordPress upgrade.
- Do not add experimental WPDS components or a second spacing owner over the
  same subtree. Core `wp-theme` tokens are allowed for a demonstrated missing
  relationship or domain state inside a plugin-owned region, not for restyling
  native controls. The runtime remains `php-core`.

### React/Core Components

- Use Core-provided `@wordpress/components` and registered WordPress packages.
- React alone does not authorize bundled experimental WPDS.
- Specialized components own their internal spacing. Stable `Flex` owns a new
  generic vertical group.

### Bundled experimental WPDS

- Requires an explicit project choice, exact package versions, public package
  APIs, and the exported design-token stylesheet.
- `@wordpress/ui`, `@wordpress/theme`, and `@wordpress/admin-ui` are an
  experimental bundled path at the WordPress 7.0 target.
- `ThemeProvider` is not a public runtime export at this pin. Never unlock
  `@wordpress/theme` private APIs from plugin code.
- Consume semantic tokens only when the selected exported stylesheet supplies
  them. The supported baseline uses default density.
- These package pins describe 7.0, not all WordPress 7 releases. On 7.1 use
  Core's token stylesheet instead of a second copy, and independently verify
  compatibility of any opted-in bundled component package.

### Hybrid

Record one owner per DOM region. A common boundary is:

| Region | Owner |
| --- | --- |
| `#wpcontent`, `.wrap`, title, `.wp-header-end`, page Notices | Core |
| Plugin React mount and descendants | selected React runtime |
| Portal or overlay | runtime and token stylesheet at actual render root |

`.form-table` and a plugin gap stack never own the same subtree.

## Experimental policy

Use `allow`, `deny`, or `unknown`. `unknown` behaves as `deny` for introducing a
new experimental API. Availability alone is not opt-in. A pre-existing
experimental subtree remains its owner unless the task has a functional reason
to change it. Stable `Flex` remains available for all three values.

Core's 7.1 token stylesheet and public `ThemeProvider` are not bundled
experimental components. `deny` does not prohibit their supported use. A
provider is optional and must never force a PHP page into React.

Use `deny` when the request selects a non-experimental PHP/Core route or a
Core-only hybrid route. Use `allow` only for an explicit bundled experimental
WPDS opt-in. Use `unknown` only when the request leaves a decision-relevant
experimental policy or runtime fact genuinely unspecified; do not replace a
known non-experimental route with `unknown`.

For an excluded host-owned surface, report `deny` when the named host is a
Classic/Core PHP surface and `unknown` when it is React-owned or the host
runtime is unspecified. This field records the known host fact; it never gives
this Skill permission to prescribe the excluded surface.

Use this exact handoff matrix for the excluded version-1 surfaces. The listed
prohibitions are required; add other applicable stable identifiers only when
the request supplies evidence for them.

| Excluded surface | Policy | Required prohibited identifiers |
| --- | --- | --- |
| Block Editor sidebar/SlotFill | `unknown` | `own-host-surface`, `frontend-theme-spacing`, `recommend-without-clarification` |
| Editor canvas | `unknown` | `own-host-surface`, `frontend-theme-spacing`, `recommend-without-clarification` |
| Post metabox | `deny` | `own-host-surface`, `inject-wpds-into-classic`, `global-wp-admin-overrides` |
| Dashboard widget | `deny` | `own-host-surface`, `inject-wpds-into-classic`, `global-wp-admin-overrides` |
| Profile field | `deny` | `own-host-surface`, `inject-wpds-into-classic`, `global-wp-admin-overrides`, `custom-css-before-core` |
| Existing Core list/screen | `deny` | `own-host-surface`, `inject-wpds-into-classic`, `global-wp-admin-overrides` |
| UI inside another plugin | `unknown` | `own-host-surface`, `assume-react-is-wpds`, `recommend-without-clarification` |

If the request explicitly says that no experimental component policy was
provided, return `unknown` even when the known runtime is Core Components;
`unknown` still behaves as deny for adding an experimental API. If the page's
placement or host boundary is not specified, return `unknown` for
`shell_owner` rather than assuming a Core plugin root.

## Canonical structured values

When a caller requests structured classification, emit these exact stable
values instead of prose variants:

| Meaning | Canonical value |
| --- | --- |
| Plugin settings or tool | `plugin-settings-tool` |
| Plugin workflow or dashboard | `plugin-workflow-dashboard` |
| Plugin data view | `plugin-data-view` |
| Explicit Network Admin | `plugin-network-admin` |
| Block Editor sidebar/SlotFill | `block-editor-sidebar-slotfill` |
| Editor canvas | `editor-canvas` |
| Post metabox | `post-metabox` |
| Dashboard widget | `dashboard-widget` |
| Profile field | `profile-field` |
| Extension of an existing Core screen | `core-screen-extension` |
| UI inside another plugin | `foreign-plugin-surface` |
| Plugin-owned page with unspecified runtime | `plugin-owned-unspecified` |
| Admin surface with unspecified placement | `unknown-admin-surface` |
| Supported stable route | `supported` |
| Supported bundled experimental route | `supported-experimental-opt-in` |
| Supported Network Admin route | `supported-explicit-multisite` |
| Excluded host-owned route | `excluded-route-to-host-owner` |
| Missing decision-relevant fact | `needs-clarification` |
| PHP with Core admin | `php-core` |
| React with Core Components | `react-core-components` |
| Bundled experimental WPDS | `bundled-wpds` |
| Region-owned mixed page | `hybrid` |
| Excluded host-owned runtime | `host-owned` |
| Core admin shell | `core-admin` |
| Core shell plus plugin root | `core-admin-plugin-root` |
| Core/React region map | `core-admin-region-map` |
| Network Admin shell | `network-admin` |
| Network Admin/React region map | `network-admin-region-map` |
| Block Editor shell | `block-editor` |
| Editor canvas shell | `editor-canvas` |
| Post editor shell | `post-editor` |
| Core Dashboard shell | `core-dashboard` |
| Core profile screen | `core-profile-screen` |
| Existing Core list/screen | `core-list-screen` |
| Host plugin shell | `foreign-plugin` |
| Core default rhythm | `core-default-css` |
| Core Components | `core-components` |
| WPDS Stack and exported tokens | `wpds-stack-and-exported-token-stylesheet` |
| Region-owned spacing | `region-map` |
| Block Editor spacing | `block-editor` |
| Editor canvas spacing | `editor-canvas` |
| Post editor/metabox spacing | `post-editor-metabox` |
| Core Dashboard widget spacing | `core-dashboard-widget` |
| Core profile-screen spacing | `core-profile-screen` |
| Existing Core list/screen spacing | `core-list-screen` |
| Host plugin spacing | `foreign-plugin` |
| Unknown owner | `unknown` |

For structured `prohibited_recommendations`, use only the applicable stable
identifiers: `assume-react-is-wpds`, `custom-css-before-core`,
`define-wpds-tokens`, `frontend-theme-spacing`, `global-wp-admin-overrides`,
`inject-wpds-into-classic`, `own-host-surface`,
`recommend-without-clarification`, and `unlock-private-theme-provider`.
Their prose explanation may follow outside the structured object.

`inject-wpds-into-classic` prohibits introducing a bundled experimental component
runtime merely to restyle Classic UI. It does not prohibit a Core `wp-theme`
stylesheet dependency. `define-wpds-tokens` prohibits plugin-authored token
assignments or imitations, not supported public provider props.
`unlock-private-theme-provider` prohibits private APIs on every version, not
the public 7.1 export. Keep these identifiers stable with these precise meanings.

An unknown React runtime must include `assume-react-is-wpds`,
`define-wpds-tokens`, and `recommend-without-clarification`. An excluded host
surface must include `own-host-surface`; when the host facts needed for a
downstream recommendation are absent, also include
`recommend-without-clarification`. Additional applicable identifiers are
allowed, but these route-specific prohibitions must not be omitted.

A Classic PHP/Core plugin page must include `frontend-theme-spacing`,
`inject-wpds-into-classic`, `global-wp-admin-overrides`, and
`custom-css-before-core`. A bundled WPDS route must include
`unlock-private-theme-provider`, `define-wpds-tokens`,
`global-wp-admin-overrides`, and `custom-css-before-core`. A Block Editor
sidebar/SlotFill handoff must include `own-host-surface`,
`frontend-theme-spacing`, and `recommend-without-clarification` because this
Skill must stop before prescribing the host-owned details.

## Required classification output

Return:

- `surface` and `support_status`;
- `runtime_owner`;
- `shell_owner`;
- `spacing_owner`;
- `experimental_components_policy`;
- supporting source or repository evidence;
- prohibited recommendations for this route.

When structured output was requested, use the canonical values above for all
six fields and for each prohibited-recommendation identifier.

For a version-sensitive recommendation, also record supported/observed versions,
token stylesheet owner, required token names, and loading/fallback evidence.
These facts supplement the six stable fields, they do not change a PHP route
to `bundled-wpds` just because Core tokens are available.

If surface, runtime, token-style, or ownership evidence is missing, return
`needs-clarification`, name the missing fact, and emit no downstream spacing or
component recommendation.

## Fact labels

- **Core:** documented API, established admin convention, or explicitly named
  observed implementation with its WordPress version named.
- **WPDS:** documented or observed token/component behavior with its provider
  and version named. This label does not by itself mean experimental.
- **WCAG:** normative accessibility requirement.
- **Skill-Norm:** an openly identified rule that closes an unspecified gap.

Observed Core selectors are not automatically public extension APIs.
