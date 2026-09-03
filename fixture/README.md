# WordPress 7.0 acceptance fixture

This fixture is test infrastructure, not a plugin template. It exercises the
four runtime owners and eight UI states required by PLAN-0001 without timers or
network-dependent state changes.

## Build

Use Node 24, Python, a PHP CLI available as `php`, and the lockfile:

```text
npm ci
npm run build
npm run check:contracts
```

`check:contracts` intentionally validates generated fixture assets, so run the
build first in a fresh clone.

The versioned documentation test executes its PHP enqueue example with stubs.
It is not a WordPress runtime or rendering test. For read-only comparison of
existing stable 7.0.x and 7.1.x Core source directories, run:

```text
npm run check:local-wordpress -- "PATH_TO_WORDPRESS_7_0" "PATH_TO_WORDPRESS_7_1"
```

This checks Core registration, token declarations, and the public export. The
7.1 React provider example is source-checked only, not build- or render-tested.
The fixture's frozen dependency graph remains the separate 7.0 baseline.

The build must produce `fixture/plugin/build/index.js`, `index.asset.php`,
`design-tokens.css`, `style-index.css`, and `style-index-rtl.css`. The build
script resolves the public `@wordpress/theme/design-tokens.css` export and
copies that unmodified stylesheet into the plugin build. PHP enqueues it before
the small plugin-owned exception stylesheet. This prevents dependency
extraction from treating the CSS subpath as a script handle.

## Runtime modes

Open the fixture settings page and add one query value:

```text
&wbui_mode=classic
&wbui_mode=core
&wbui_mode=wpds
&wbui_mode=hybrid
```

The default is `hybrid`. The modes isolate PHP/Core, Core Components, the
public bundled WPDS route, and the mixed owner boundary.

## UI states

Add one deterministic state value:

```text
&wbui_state=initial
&wbui_state=loading
&wbui_state=partial
&wbui_state=empty
&wbui_state=success
&wbui_state=error
&wbui_state=disabled
&wbui_state=permission
```

The default is `initial`. Page-level Core notices and React-local feedback are
kept separate so both ownership rules can be checked. Request page-level Core
notices independently; this prevents a local React retry or dismissal from
leaving a stale page notice behind:

```text
&wbui_notice=partial
&wbui_notice=success
&wbui_notice=error
```

## Translation artifacts

After the JavaScript build, use WP-CLI:

```text
npm run i18n:pot
npm run i18n:mo
npm run i18n:json
```

The POT command excludes `src`. The maintained PO therefore references the
registered `build/index.js`, and `make-json --no-purge` retains the PO while it
creates the path-hashed Jed JSON file.

## Native XAMPP runtimes

The canonical runtime check uses two isolated WordPress installations inside a
local XAMPP root. Their relative paths, exact WordPress versions, site modes,
plugin activation and locale are pinned in `fixture/native-xampp.json`.

```powershell
npm run test:xampp -- -XamppRoot Z:\xampp_lite_8_5
```

The command calls `scripts/validate-xampp-fixtures.ps1`. It checks PHP, WP-CLI,
Apache, MariaDB, both WordPress runtimes, the fixture junctions, activation,
locale and required build artifacts. It does not create sites, change options,
read credentials or modify another XAMPP installation. The XAMPP root can also
be provided through `XAMPP_LITE_ROOT`:

```powershell
$env:XAMPP_LITE_ROOT = 'Z:\xampp_lite_8_5'
npm run test:xampp
```

The current manifest expects WordPress 7.0 at
`www/wordpress-backend-skill-test` and WordPress 7.0.4 Multisite at
`www/wordpress-backend-skill-test-multisite`. Each installation links
`wp-content/plugins/wordpress-backend-skill-fixture` to this repository's
`fixture/plugin` directory. Existing XAMPP sites remain outside the test scope.

## Locale setup order

Set the site locale first, then the admin user's locale, and finally verify the
runtime result with that same user. Run these commands through the WP-CLI that
owns the selected fixture, adding its normal `--path` transport as required:

```powershell
wp option update WPLANG de_DE
wp user meta update <admin-user> locale de_DE
wp eval 'echo determine_locale();' --user=<admin-user>
```

The final command must print `de_DE` before the translated browser assertions
are accepted. Core language-pack installation may improve the surrounding
admin translation, but the bundled plugin MO and Jed JSON remain the fixture's
translation proof.

The validator confirms the resulting site locale, administrative user locale
and `determine_locale()` value without printing the selected user's identity.
