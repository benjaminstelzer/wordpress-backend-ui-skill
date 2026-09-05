# Routing and composition contract

Status: design derivation; the shipped canonical contract is
`wordpress-backend-ui/references/routing.md`

This derivation predates the 7.1 addendum. Current version-sensitive rules are
in [version-compatibility.md](../../../wordpress-backend-ui/references/version-compatibility.md).

This document records the design derivation for surface/runtime routing and
optional composition. The installed Skill reference is the sole canonical
owner for the structured vocabulary, policy rules and prohibited identifiers;
`tests/cases/routing.yaml` points to it directly. Routing still applies before
component, spacing, responsive, accessibility, or CSS advice.

## Two independent axes

Classify the admin surface first, then classify the runtime owner. React does
not imply WPDS. A hybrid page has one owner per DOM region, including portals
and overlays.

### Supported surfaces in version 1

| Surface | Support | Shell owner |
| --- | --- | --- |
| Plugin-owned single-site settings or tool page | supported | Core admin shell |
| Plugin-owned workflow or dashboard page | supported | Core admin shell, with an explicitly owned plugin root |
| Plugin-owned data view | supported | Core admin shell, with an explicitly owned plugin root |
| Plugin-owned Network Admin page | supported with explicit Multisite context | Network Admin shell |

### Excluded or separately routed surfaces in version 1

- Block Editor sidebars and SlotFills.
- Editor canvas UI.
- Post metaboxes.
- Dashboard widgets.
- Profile fields.
- Extensions of existing Core lists or screens.
- UI inside another plugin's surface.

Do not apply a plugin-page shell or spacing system to an excluded or host-owned
surface. Route to that surface's owner instead.

## Runtime owners

| Runtime owner | Component owner | Default spacing owner | Experimental policy |
| --- | --- | --- | --- |
| `php-core` | WordPress APIs, semantic admin markup, Core classes | Core default CSS | deny new experimental components |
| `react-core-components` | Core-provided `@wordpress/components` | Specialized component internals, then stable `Flex` for a new generic vertical group | allow, deny, or unknown applies only to other experimental APIs |
| `bundled-wpds` | Pinned public APIs from bundled `@wordpress/ui`/`@wordpress/admin-ui` plus exported `@wordpress/theme/design-tokens.css` | Public component plus loaded default-density token stylesheet; no private `ThemeProvider` | explicit opt-in required |
| `hybrid` | Explicit owner per DOM region | Explicit spacing owner per DOM region | evaluate each region independently |

For `experimental_components_policy: unknown`, use the safe value `deny`. Do
not introduce a new experimental API merely because it is installed. A
pre-existing experimental subtree remains its own owner unless the task has a
functional reason to change it.

## Owner output

Every supported result must state:

- `surface` and `support_status`;
- `runtime_owner`;
- `shell_owner`;
- `spacing_owner`;
- `experimental_components_policy`;
- sources or local evidence that justify the classification;
- prohibited recommendations for that route.

When surface or runtime evidence is missing, return `needs-clarification` and
name the missing fact. Do not guess and do not emit downstream spacing advice.

## Prohibited recommendation codes

| Code | Meaning |
| --- | --- |
| `frontend-theme-spacing` | Use `theme.json`, `blockGap`, or theme layout as the admin design owner. |
| `assume-react-is-wpds` | Treat every React screen as bundled WPDS. |
| `inject-wpds-into-classic` | Add experimental WPDS merely to restyle a Classic/Core page. |
| `global-wp-admin-overrides` | Fix a local layout by overriding global admin selectors. |
| `define-wpds-tokens` | Define, override, or imitate `--wpds-*` in plugin code. |
| `custom-css-before-core` | Add CSS before checking the owning WordPress API, component, class, default CSS, or provided token. |
| `own-host-surface` | Apply this Skill's page shell or flow rules inside a Core or foreign-plugin surface. |
| `recommend-without-clarification` | Emit component or spacing advice while a required owner is unknown. |
| `unlock-private-theme-provider` | Unlock or consume a non-public theme provider/private API. |

## Fact and source contract

Every normative statement is labeled as exactly one fact class:

- **Core:** documented WordPress API, established admin convention, or
  explicitly identified observed WordPress 7.0 implementation.
- **WPDS:** documented or observed behavior of the pinned experimental
  Gutenberg `wp/7.0` packages.
- **WCAG:** normative accessibility requirement.
- **Skill-Norm:** an openly identified project rule that closes a gap not
  specified by WordPress.

Core and WPDS facts also state their evidence kind: `documented-api`,
`established-convention`, or `observed-implementation`. An observed selector is
not promoted to a public extension API.

The source ledger entry for a load-bearing fact includes URL or local path,
ref/SHA or document status, package/version where applicable, retrieval date,
fact class, used assertion, and revalidation trigger. Skill-Norms point to the
facts and accepted Decision that justify them.

## Optional Scoville UI composition

The WordPress Backend Skill is complete without Scoville UI. If Scoville UI is
also installed, active, and applicable, ownership is:

| Concern | Canonical owner |
| --- | --- |
| Surface and runtime routing | WordPress Backend Skill |
| WordPress components, admin shell, default CSS, tokens, spacing, and CSS exceptions | WordPress Backend Skill |
| WordPress-specific responsive and i18n constraints | WordPress Backend Skill |
| Remaining task flow, hierarchy, state completeness, accessibility, and rendered quality | Scoville UI within WordPress constraints |

WordPress and accessibility owners take precedence over a generic UI default.
Scoville UI must not introduce a parallel palette, spacing scale, breakpoint,
component language, or page shell. Standalone and composed runs must return the
same WordPress-specific routing and ownership result.
