---
format_version: 1
id: ADR-0013
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: validation/runtime
---

# Use native XAMPP runtimes instead of Docker

## Decision

This project's canonical runtime validation uses the existing native XAMPP
installation for a separate WordPress 7.0 single site and a WordPress 7.0.x
multisite. Docker and `wp-env` are no longer prerequisites and are removed from
the package, lockfile, scripts, and acceptance instructions.

A versioned fixture manifest describes only expected relative paths, WordPress
versions, site types, plugin status, and locale. A read-only PowerShell
validator receives the XAMPP root explicitly, derives PHP, WP-CLI, and both
isolated WordPress paths from it, and checks the requirements without changing
credentials or existing sites. Rendered browser checks run against the same two
installations.

The XAMPP path is repository test infrastructure, not a dependency of the
published agent Skill.

## Problem

Both pinned `wp-env` starts end with `spawn docker ENOENT` in this environment.
Docker is unavailable and should not be installed. The already isolated XAMPP
sites actually cover both Single Site and Network Admin, but were not yet the
reproducible canonical acceptance path.

## Drivers

- Acceptance must be executable with the available local infrastructure.
- A missing external runtime service must not count as a passing test.
- Single Site and Network Admin must be testable separately and repeatedly.
- Credentials and other XAMPP sites remain outside the repository and test
  output.
- The published Skill must require neither Docker nor XAMPP at runtime.

## Considered alternatives

1. Install Docker: explicitly excluded and adds a runtime unnecessary for the
   result.
2. Keep `wp-env` as a blocking requirement: leaves local acceptance permanently
   unexecutable despite two working WordPress installations.
3. Test only one single site: does not cover Network Admin or Multisite-specific
   navigation.
4. Document the XAMPP check only as a manual procedure: provides no repeatable
   preflight and runtime verification.

## Consequences

- W-005 remains as the historical unfulfilled Docker path and is replaced by a
  new Work Item; its Acceptance is not reinterpreted.
- The repository loses `@wordpress/env` and both `.wp-env` files.
- The native validator is Windows/PowerShell test tooling; the Skill itself
  remains platform-independent and independent of Scoville UI.
- Currently observed runtime versions are recorded exactly. A change requires
  a deliberate manifest and evidence update.
- Browser and accessibility evidence remains required; preflight alone does not
  prove rendered UI.

## Confirmation

The Decision is implemented when the manifest and read-only validator check
both isolated XAMPP sites, their exact WordPress versions, single/multisite
mode, active fixture, plugin linkage, locale, and required build artifacts; the
documentation requires only this canonical path; and no Docker or `wp-env`
dependency remains in the package.

## Revisit when

The project moves to another test machine, XAMPP is replaced, an already
available platform-neutral runtime provides the same coverage, or the
WordPress 7 target versions are deliberately raised.
