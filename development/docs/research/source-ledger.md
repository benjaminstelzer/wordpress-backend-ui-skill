# Source Ledger: WordPress 7.0 and 7.1 Backend Skill

Status: 2026-09-03

## Purpose and fact classes

The ledger separates source status from claim type. A Core selector from a
pinned CSS file is an **observed implementation**, but not automatically a
public extension API. The fixed labels in the Skill are:

- **Core:** documented WordPress API, established admin convention, or observed
  implementation with its WordPress version named.
- **WPDS:** documented or observed token or component contract with its provider
  and WordPress/package version named. This label is not an experimental-status
  claim by itself.
- **WCAG:** normative accessibility requirement.
- **Skill-Norm:** a disclosed project rule that closes a gap not officially
  specified.

## Pinned repository snapshots

| Repository | Ref | Resolved commit | Package/product state | Retrieved | Type | Revalidation |
| --- | --- | --- | --- | --- | --- | --- |
| [`WordPress/wordpress-develop`](https://github.com/WordPress/wordpress-develop/commit/90a615f1834824d2583a43bfc698d9c710e5c094) | `7.0` | `90a615f1834824d2583a43bfc698d9c710e5c094` | WordPress 7.0 Development Source | 2026-09-03 | Core / observed implementation | Before a Skill release, a new WordPress 7.x target, or branch drift |
| [`WordPress/gutenberg`](https://github.com/WordPress/gutenberg/commit/28c0dedc4eaf001a24237a1fbba4b0887698b000) | `wp/7.0` | `28c0dedc4eaf001a24237a1fbba4b0887698b000` | `@wordpress/ui` 0.7.1; `@wordpress/theme` 0.7.1; `@wordpress/admin-ui` 1.8.1; `@wordpress/components` 32.2.1 | 2026-09-03 | WPDS/Components / documented and observed package contract | Before a Skill release, package upgrade, or new WordPress 7.x target |
| [`WordPress/WordPress` tag 7.0](https://github.com/WordPress/WordPress/tree/b16cd68ea199838d8f9daf0ff7e3f35042ba0ad0) | `7.0` | `b16cd68ea199838d8f9daf0ff7e3f35042ba0ad0` | WordPress 7.0 runtime of the native single-site fixture | 2026-09-03 | Core / test runtime | Before fixture setup and when the runtime target changes |
| [`WordPress/WordPress` tag 7.1](https://github.com/WordPress/WordPress/tree/b998fef9238af183f9523b3df71618e6e57498b6) | `7.1` | `b998fef9238af183f9523b3df71618e6e57498b6` | Stable WordPress 7.1 runtime and Core token registration | 2026-09-03 | Core / public capability plus observed implementation | Before release or target change |
| [`@wordpress/theme` 1.0.0 publication](https://github.com/WordPress/gutenberg/commit/7fe6fa42d4cf9cdd084223e3150f796567914f87) | `1.0.0` | `7fe6fa42d4cf9cdd084223e3150f796567914f87` | WordPress 7.1 theme package contract | 2026-09-03 | WPDS / public export plus observed implementation | Before release or package/target change |

The 7.0 rows remain the frozen fixture and bundled-package contract. They are
not generalized to all WordPress 7 releases.

## WordPress 7.1 Core theming

| Source | Version/ref | Retrieved | Fact class | Claim used | Revalidation |
| --- | --- | --- | --- | --- | --- |
| [Design system theming in WordPress 7.1](https://make.wordpress.org/core/2026/07/31/design-system-theming-in-wordpress-7-1/) | WordPress 7.1 Dev Note | 2026-09-03 | Core / official release guidance | Core registers `wp-theme` as a style for plugin admin UIs; direct semantic-token use is allowed for plugin-specific CSS; the separate script provides public `ThemeProvider` | On Core guidance or target change |
| [`script-loader.php`](https://github.com/WordPress/WordPress/blob/b998fef9238af183f9523b3df71618e6e57498b6/wp-includes/script-loader.php) | WordPress 7.1 stable tag / pinned SHA | 2026-09-03 | Core / observed implementation | `wp-theme` design-token style registration and `wp-components` style dependency | On Core source change |
| [`@wordpress/theme` runtime entry](https://github.com/WordPress/gutenberg/blob/7fe6fa42d4cf9cdd084223e3150f796567914f87/packages/theme/src/index.ts) and [README](https://github.com/WordPress/gutenberg/blob/7fe6fa42d4cf9cdd084223e3150f796567914f87/packages/theme/README.md) | 1.0.0 / pinned SHA | 2026-09-03 | WPDS / public export | `ThemeProvider` is public in 7.1; documented props and wrapper limits are pinned; private APIs remain forbidden | On package or Core target change |
| [Current package reference](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-theme/) | Living official documentation | 2026-09-03 | WPDS / official current guidance | Inside WordPress, use Core's stylesheet rather than bundling a second token copy; stylesheet and provider have separate roles | Before applying current props to a pinned release |

The inspected local WordPress 7.1 source agrees on the style registration,
semantic token declarations and public JavaScript export. That inspection does
not prove actual enqueue, computed CSS, accessibility or responsive rendering
on a customer plugin page.

## Core admin implementation

| Source | Version/ref | Retrieved | Fact class | Claim used | Revalidation |
| --- | --- | --- | --- | --- | --- |
| [`common.css`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/common.css) | WP 7.0 / pinned SHA | 2026-09-03 | Core / observed implementation | `.wrap`, `#wpcontent`, headings, admin shell, `782px` breakpoint | On Core CSS change; never present selectors as public APIs |
| [`forms.css`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/forms.css) | WP 7.0 / pinned SHA | 2026-09-03 | Core / observed implementation | `.form-table`, control heights, and mobile reflow | On Core CSS change; never present selectors as public APIs |
| [`admin-menu.css`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/admin-menu.css) | WP 7.0 / pinned SHA | 2026-09-03 | Core / observed implementation | Admin menu and shell context | On navigation or shell change |
| [`common.js`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/js/_enqueues/admin/common.js) | WP 7.0 / pinned SHA | 2026-09-03 | Core / observed implementation | Moves `.notice`/`.updated`/`.error` after `.wp-header-end`; `.inline` remains in place; `.below-h2` is deprecated | On notice or header change |
| [Settings API](https://developer.wordpress.org/plugins/settings/settings-api/) | Living official documentation | 2026-09-03 | Core / documented API | Standardized settings forms and Core compatibility | Before release and when documentation changes |
| [Administration Menus](https://developer.wordpress.org/plugins/administration-menus/) | Living official documentation | 2026-09-03 | Core / documented API and guideline | Submenu for a single options/tools page | Before release and when documentation changes |
| [`network_admin_menu`](https://developer.wordpress.org/reference/hooks/network_admin_menu/) | WordPress Code Reference | 2026-09-03 | Core / documented API | Plugin menus in Network Admin; Super Admin only in Multisite | On WordPress API change |
| [`update_network_option()`](https://developer.wordpress.org/reference/functions/update_network_option/) | WordPress Code Reference | 2026-09-03 | Core / documented API | Network-wide option persistence instead of a single-site option | On WordPress API change |

## Components and experimental WPDS

| Source | Version/ref | Retrieved | Fact class | Claim used | Revalidation |
| --- | --- | --- | --- | --- | --- |
| [`@wordpress/theme` README](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/README.md), [`package.json` exports](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/package.json), [runtime `index.ts`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/src/index.ts), and [`lock-unlock.ts`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/src/lock-unlock.ts) | 0.7.1 / pinned SHA | 2026-09-03 | WPDS / documented experimental contract plus observed exports | `design-tokens.css` is publicly exported; `ThemeProvider` is not a public runtime export and `privateApis` are not a plugin contract; consume semantic `--wpds-*`, do not define or override them | On package upgrade, a new public provider, or stabilization |
| [`dimension.json`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/tokens/dimension.json) | `@wordpress/theme` 0.7.1 | 2026-09-03 | WPDS / observed implementation | Gap, padding, and density values at the WP 7.0 state | On package upgrade; never transfer values to Classic |
| [`@wordpress/ui` README](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/README.md) | 0.7.1 / pinned SHA | 2026-09-03 | WPDS / documented experimental contract | Experimental, bundled, not assumed as a global `window.wp` | On package upgrade or stabilization |
| [`Stack` implementation](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/src/stack/stack.tsx) and [types](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/src/stack/types.ts) | `@wordpress/ui` 0.7.1 | 2026-09-03 | WPDS / observed implementation | `direction` and `gap` are optional and have no default; vertical flow sets both explicitly | On package upgrade |
| [`@wordpress/admin-ui` README](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/README.md), [`Page` styles](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/src/page/style.scss), [`PageHeader`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/src/page/header.tsx) | 1.8.1 / pinned SHA | 2026-09-03 | WPDS / minimally documented package dependent on experimental `@wordpress/ui`/`@wordpress/theme` | Modern Page shell uses `16px` block / `24px` inline and header spacing | On package upgrade; do not present as a universal Core shell |
| [`@wordpress/components` README](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/README.md) | 32.2.1 / pinned SHA | 2026-09-03 | Components / documented package contract | Core-provided React components are a separate runtime path | On package upgrade or WordPress Script API change |
| [`Flex` types](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/src/flex/types.ts), [`Flex` implementation](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/src/flex/flex/component.tsx), [official component reference](https://developer.wordpress.org/block-editor/reference-guides/components/flex/) | `@wordpress/components` 32.2.1 / pinned SHA | 2026-09-03 | Components / documented contract not named experimental plus pinned implementation | `direction`, `align`, `justify`, `wrap`, `expanded`; `gap` as a 4 px multiplier; documented `FlexItem`/`FlexBlock` children | On package upgrade or experimental/deprecation notice |
| [`VStack` README](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/src/v-stack/README.md) | `@wordpress/components` 32.2.1 | 2026-09-03 | Components / documented experimental contract | `__experimentalVStack`; `spacing` as a multiplier of the 4 px grid | On package upgrade or stabilization |
| [`@wordpress/scripts` dependency extraction](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/dependency-extraction-webpack-plugin/lib/util.js) | `@wordpress/scripts` 32.0.0 pinned locally; behavior revalidated against Gutenberg `wp/7.0` | 2026-09-03 | Core Tooling / observed build implementation | `@wordpress/ui` and `@wordpress/admin-ui` are bundled; a JavaScript import of `@wordpress/theme` is externalized to `wp-theme`, and the CSS subpath in the JavaScript entry was incorrectly extracted as the script dependency `wp-theme/design-tokens.css`. The fixture therefore resolves the public CSS export during the build, copies it unchanged as its own build asset, and enqueues that stylesheet separately | On scripts/Gutenberg upgrade or build-configuration change |
| [Playwright](https://playwright.dev/docs/intro) | `@playwright/test` 1.58.2 pinned exactly | 2026-09-03 | Test Tooling / documented API | Browser and viewport checks of the local fixture | Before browser-tooling upgrade |

## Internationalization

| Source | Version/status | Retrieved | Fact class | Claim used | Revalidation |
| --- | --- | --- | --- | --- | --- |
| [How to Internationalize Your Plugin](https://developer.wordpress.org/plugins/internationalization/how-to-internationalize-your-plugin/) | Official Plugin Handbook documentation | 2026-09-03 | Core / documented guideline | Text domain matches slug; literals; gettext, plural, context, placeholders; language packs | Before release and when the Handbook changes |
| [Internationalization Guidelines](https://developer.wordpress.org/apis/internationalization/internationalization-guidelines/) | Official Common APIs documentation | 2026-09-03 | Core / documented guideline | `translators:` comments, complete phrases, no concatenation, positional placeholders, doubled text | Before release and when the guideline changes |
| [Internationalization Security](https://developer.wordpress.org/plugins/internationalization/security/) | Official Plugin Handbook documentation | 2026-09-03 | Core / security guideline | Treat translations as untrusted; escape for context; do not make URLs translatable | Before release and when the security guideline changes |
| [JavaScript Internationalization](https://developer.wordpress.org/block-editor/how-to-guides/internationalization/) | Official Block Editor documentation | 2026-09-03 | Core / documented API | `@wordpress/i18n`/`wp-i18n`, script handle/path, PO-to-JSON workflow, and loaded JavaScript translations | Before release and on Script API change |
| [`wp_set_script_translations()`](https://developer.wordpress.org/reference/functions/wp_set_script_translations/) | WordPress Code Reference | 2026-09-03 | Core / documented API | Only after script registration; handle, domain, and optional path | On WordPress API change |
| [`wp i18n make-pot`](https://developer.wordpress.org/cli/commands/i18n/make-pot/) | Official WP-CLI documentation | 2026-09-03 | Core Tooling / documented API | Reproducible POT extraction for PHP and JavaScript | Before release and on WP-CLI upgrade |
| [`wp i18n make-mo`](https://developer.wordpress.org/cli/commands/i18n/make-mo/) | Official WP-CLI documentation | 2026-09-03 | Core Tooling / documented API | Compile PO into loadable MO | Before release and on WP-CLI upgrade |
| [`wp i18n make-json`](https://developer.wordpress.org/cli/commands/i18n/make-json/) | Official WP-CLI documentation | 2026-09-03 | Core Tooling / documented API | Convert PO to file-specific Jed JSON; `--no-purge` preserves the test PO | Before release and on WP-CLI upgrade |
| [`load_plugin_textdomain()`](https://developer.wordpress.org/reference/functions/load_plugin_textdomain/) | WordPress Code Reference; just-in-time delegation since 6.7 | 2026-09-03 | Core / documented API | Register a custom plugin language path; fixture call on `init`; MO name `<domain>-<locale>.mo` | On WordPress i18n-loading change |
| [`wp_date()`](https://developer.wordpress.org/reference/functions/wp_date/) and [`number_format_i18n()`](https://developer.wordpress.org/reference/functions/number_format_i18n/) | WordPress Code Reference | 2026-09-03 | Core / documented API | Locale-aware and WordPress-timezone-aware PHP output | On WordPress API change |
| [`@wordpress/date`](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-date/) | Official package documentation | 2026-09-03 | Components / documented API | `dateI18n` formats in the site locale and WordPress timezone | On package upgrade |

## Accessibility and general user guidance

| Source | Version/status | Retrieved | Fact class | Claim used | Revalidation |
| --- | --- | --- | --- | --- | --- |
| [WordPress Accessibility Coding Standards](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/accessibility/) | Official WordPress documentation | 2026-09-03 | WCAG / WordPress standard | WCAG 2.2 AA as the minimum target | On standard change |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | W3C Recommendation | 2026-09-03 | WCAG / normative | Reflow, focus, target size, contrast, labels, error and status messages | On a new normative target version |
| [10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | Established usability heuristic | 2026-09-03 | External guideline | Status visibility, consistency, error prevention, recognition | Only when the Skill-Norm or source changes |

## Optional Scoville UI composition

| Source | Version/status | Retrieved | Fact class | Claim used | Revalidation |
| --- | --- | --- | --- | --- | --- |
| `scoville-ui-anti-ai-slop` Skill | Local snapshot; SHA-256 `95E17C7F1D2430A7E07EDCFCAA20DCF54BDF44A7F7118B2A416B72EC24BCC99B` | 2026-09-03 | Optional local composition source | Product/platform design system remains the owner; general UI review supplements it within that boundary | Before a composition test, on installation/update, or when the Skill is missing |

## Revalidation rule

Before implementation and every release, recheck at minimum branch/tag
resolution, package versions, experimental status, token names and values,
notice behavior, i18n APIs, the WordPress 7.0 fixture, and the applicable 7.1
Core capability. When a supporting
source changes, update the fact class first and then the derived Skill-Norm;
observed Core selectors are never promoted to public APIs without separate
documentation.
