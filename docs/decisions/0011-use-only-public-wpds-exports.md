---
format_version: 1
id: ADR-0011
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: skill/wpds-runtime
---

# Use only public WPDS exports in the plugin runtime path

## Decision

The bundled experimental WPDS path for WordPress 7.0 uses only public package
exports. `@wordpress/ui` components are pinned exactly and bundled. Semantic
default tokens come from the publicly exported CSS subpath
`@wordpress/theme/design-tokens.css` and must be loaded at the actual render
target.

At the `@wordpress/theme` 0.7.1 pin, `ThemeProvider` is not a public runtime
export. Plugin code therefore does not import it and does not unlock any
`privateApis`. A non-default density is recommended only when the target package
offers a public provider contract for it.

For vertical flow, `Stack` explicitly sets `direction="column"` and a semantic
`gap`, because neither prop has a default at the pin. Plugin CSS continues to
neither define, override, nor imitate any `--wpds-*` variable.

## Problem

The first fixture and first example imported `ThemeProvider` directly from
`@wordpress/theme`. The type is visible in the package, but the runtime entry
exports only `privateApis`. The guidance was therefore not buildable and would
have directed agents toward a private WordPress contract.

## Drivers

- The Skill must not present a non-public API as a plugin contract.
- The WPDS path should remain reproducible and testable against the pinned
  packages.
- Semantic tokens should be consumed without recreating them in plugin CSS.
- Experimental use needs an explicit opt-in and a clear upgrade boundary.

## Considered alternatives

1. Unlock `privateApis`: technically possible, but explicitly not a plugin
   contract.
2. Recreate a provider: creates a parallel and unevidenced WPDS runtime.
3. Exclude WPDS entirely: safe but unnecessary; `Stack` and the CSS subpath are
   publicly exported.

## Consequences

- The default-density path is testable; other densities are not part of the
  Skill contract at this pin.
- Build evidence must show that the token CSS subpath is loaded and no
  unresolved `--wpds-*` remains.
- JavaScript imports from `@wordpress/theme` require separate attention to
  externalization as `wp-theme`; the baseline path imports only the CSS subpath.
- Portals and overlays check runtime and token styles at the actual render
  target.

## Confirmation

The Decision is implemented when examples, golden cases, fixture, and validator
contain no direct or private `ThemeProvider` import; `Stack` explicitly sets
direction and gap; and a rendered test proves the loaded token value rather
than only the numeric fallback.

## Revisit when

`@wordpress/theme` exports a public provider, package exports or Dependency
Extraction change, or WordPress stabilizes the WPDS path.
