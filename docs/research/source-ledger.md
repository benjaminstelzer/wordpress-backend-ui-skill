# Source Ledger: WordPress-7.0-Backend-Skill

Stand: 2026-09-03

## Zweck und Faktklassen

Das Ledger trennt Quellenstatus und Aussageart. Ein Core-Selektor aus einer gepinnten CSS-Datei ist eine **beobachtete Implementierung**, aber nicht automatisch eine oeffentliche Erweiterungs-API. Die feste Kennzeichnung im Skill lautet:

- **Core:** dokumentierte WordPress-API, etablierte Admin-Konvention oder beobachtete WordPress-7.0-Implementierung.
- **WPDS:** dokumentierter oder beobachteter Vertrag der experimentellen Gutenberg-Pakete am gepinnten `wp/7.0`-Stand.
- **WCAG:** normative Accessibility-Anforderung.
- **Skill-Norm:** eigene, offengelegte Regel zur Schliessung einer nicht offiziell spezifizierten Luecke.

## Gepinnte Repository-Snapshots

| Repository | Ref | Aufgeloester Commit | Paket-/Produktstand | Abruf | Typ | Revalidierung |
| --- | --- | --- | --- | --- | --- | --- |
| [`WordPress/wordpress-develop`](https://github.com/WordPress/wordpress-develop/commit/90a615f1834824d2583a43bfc698d9c710e5c094) | `7.0` | `90a615f1834824d2583a43bfc698d9c710e5c094` | WordPress 7.0 Development Source | 2026-09-03 | Core / beobachtete Implementierung | Vor Skill-Release, bei neuem WordPress-7.x-Ziel oder Branch-Drift |
| [`WordPress/gutenberg`](https://github.com/WordPress/gutenberg/commit/28c0dedc4eaf001a24237a1fbba4b0887698b000) | `wp/7.0` | `28c0dedc4eaf001a24237a1fbba4b0887698b000` | `@wordpress/ui` 0.7.1; `@wordpress/theme` 0.7.1; `@wordpress/admin-ui` 1.8.1; `@wordpress/components` 32.2.1 | 2026-09-03 | WPDS/Components / dokumentierter und beobachteter Paketvertrag | Vor Skill-Release, Paketupgrade oder neuem WordPress-7.x-Ziel |
| [`WordPress/WordPress` Tag 7.0](https://github.com/WordPress/WordPress/tree/b16cd68ea199838d8f9daf0ff7e3f35042ba0ad0) | `7.0` | `b16cd68ea199838d8f9daf0ff7e3f35042ba0ad0` | WordPress-7.0-Runtime der nativen Single-Site-Fixture | 2026-09-03 | Core / Test-Runtime | Vor Fixture-Aufbau und bei geaendertem Runtime-Ziel |

## Core-Admin-Implementierung

| Quelle | Version/Ref | Abruf | Faktklasse | Verwendete Aussage | Revalidierung |
| --- | --- | --- | --- | --- | --- |
| [`common.css`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/common.css) | WP 7.0 / gepinnter SHA | 2026-09-03 | Core / beobachtete Implementierung | `.wrap`, `#wpcontent`, Headings, Admin-Shell, Breakpoint `782px` | Bei Core-CSS-Aenderung; Selektoren nie als oeffentliche API ausgeben |
| [`forms.css`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/forms.css) | WP 7.0 / gepinnter SHA | 2026-09-03 | Core / beobachtete Implementierung | `.form-table`, Control-Hoehen und Mobile-Reflow | Bei Core-CSS-Aenderung; Selektoren nie als oeffentliche API ausgeben |
| [`admin-menu.css`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/admin-menu.css) | WP 7.0 / gepinnter SHA | 2026-09-03 | Core / beobachtete Implementierung | Admin-Menue und Shell-Kontext | Bei Navigations- oder Shell-Aenderung |
| [`common.js`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/js/_enqueues/admin/common.js) | WP 7.0 / gepinnter SHA | 2026-09-03 | Core / beobachtete Implementierung | Verschiebbare `.notice`/`.updated`/`.error` nach `.wp-header-end`; `.inline` bleibt am Ort; `.below-h2` ist veraltet | Bei Notice- oder Header-Aenderung |
| [Settings API](https://developer.wordpress.org/plugins/settings/settings-api/) | laufende offizielle Dokumentation | 2026-09-03 | Core / dokumentierte API | Standardisierte Settings-Formulare und Core-Kompatibilitaet | Vor Release und bei Dokumentationsaenderung |
| [Administration Menus](https://developer.wordpress.org/plugins/administration-menus/) | laufende offizielle Dokumentation | 2026-09-03 | Core / dokumentierte API und Guideline | Untermenue fuer einzelne Options-/Tool-Seiten | Vor Release und bei Dokumentationsaenderung |
| [`network_admin_menu`](https://developer.wordpress.org/reference/hooks/network_admin_menu/) | WordPress Code Reference | 2026-09-03 | Core / dokumentierte API | Plugin-Menues im Network Admin; nur fuer Super Admin in Multisite | Bei WordPress-API-Aenderung |
| [`update_network_option()`](https://developer.wordpress.org/reference/functions/update_network_option/) | WordPress Code Reference | 2026-09-03 | Core / dokumentierte API | Netzwerkweite Optionspersistenz statt Single-Site-Option | Bei WordPress-API-Aenderung |

## Components und experimentelles WPDS

| Quelle | Version/Ref | Abruf | Faktklasse | Verwendete Aussage | Revalidierung |
| --- | --- | --- | --- | --- | --- |
| [`@wordpress/theme` README](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/README.md), [`package.json` exports](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/package.json), [runtime `index.ts`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/src/index.ts) und [`lock-unlock.ts`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/src/lock-unlock.ts) | 0.7.1 / gepinnter SHA | 2026-09-03 | WPDS / dokumentierter experimenteller Vertrag plus beobachtete Exporte | `design-tokens.css` ist oeffentlich exportiert; `ThemeProvider` ist kein oeffentlicher Runtime-Export und `privateApis` sind kein Plugin-Vertrag; semantische `--wpds-*` konsumieren, nicht definieren/ueberschreiben | Bei Paketupgrade, neuem oeffentlichem Provider oder Stabilisierung |
| [`dimension.json`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/tokens/dimension.json) | `@wordpress/theme` 0.7.1 | 2026-09-03 | WPDS / beobachtete Implementierung | Gap-, Padding- und Dichtewerte am WP-7.0-Stand | Bei Paketupgrade; Werte nie auf Classic uebertragen |
| [`@wordpress/ui` README](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/README.md) | 0.7.1 / gepinnter SHA | 2026-09-03 | WPDS / dokumentierter experimenteller Vertrag | Experimentell, gebuendelt, nicht als globales `window.wp` voraussetzen | Bei Paketupgrade oder Stabilisierung |
| [`Stack` Implementierung](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/src/stack/stack.tsx) und [Typen](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/src/stack/types.ts) | `@wordpress/ui` 0.7.1 | 2026-09-03 | WPDS / beobachtete Implementierung | `direction` und `gap` sind optional und besitzen keinen Default; vertikaler Flow setzt beide explizit | Bei Paketupgrade |
| [`@wordpress/admin-ui` README](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/README.md), [`Page` Styles](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/src/page/style.scss), [`PageHeader`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/src/page/header.tsx) | 1.8.1 / gepinnter SHA | 2026-09-03 | WPDS / knapp dokumentiertes Paket, abhaengig von experimentellem `@wordpress/ui`/`@wordpress/theme` | Moderne Page-Shell `16px` block / `24px` inline und Header-Spacing | Bei Paketupgrade; nicht als universelle Core-Shell ausgeben |
| [`@wordpress/components` README](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/README.md) | 32.2.1 / gepinnter SHA | 2026-09-03 | Components / dokumentierter Paketvertrag | Core-bereitgestellte React-Komponenten sind ein eigener Runtime-Pfad | Bei Paketupgrade oder WordPress-Script-API-Aenderung |
| [`Flex`-Typen](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/src/flex/types.ts), [`Flex`-Implementierung](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/src/flex/flex/component.tsx), [offizielle Komponentenreferenz](https://developer.wordpress.org/block-editor/reference-guides/components/flex/) | `@wordpress/components` 32.2.1 / gepinnter SHA | 2026-09-03 | Components / dokumentierter, nicht als experimentell benannter Vertrag plus gepinnte Implementierung | `direction`, `align`, `justify`, `wrap`, `expanded`; `gap` als 4-px-Multiplikator; dokumentierte `FlexItem`-/`FlexBlock`-Kinder | Bei Paketupgrade oder Experimental-/Deprecation-Hinweis |
| [`VStack` README](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/src/v-stack/README.md) | `@wordpress/components` 32.2.1 | 2026-09-03 | Components / dokumentierter experimenteller Vertrag | `__experimentalVStack`; `spacing` als Multiplikator des 4-px-Rasters | Bei Paketupgrade/Stabilisierung |
| [`@wordpress/scripts` dependency extraction](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/dependency-extraction-webpack-plugin/lib/util.js) | `@wordpress/scripts` 32.0.0 lokal gepinnt; Verhalten gegen Gutenberg `wp/7.0` revalidiert | 2026-09-03 | Core Tooling / beobachtete Build-Implementierung | `@wordpress/ui` und `@wordpress/admin-ui` werden gebuendelt; ein JavaScript-Import von `@wordpress/theme` externalisiert zu `wp-theme`, und der CSS-Subpath wurde im JS-Einstieg faelschlich als Script-Abhaengigkeit `wp-theme/design-tokens.css` extrahiert. Die Fixture loest den oeffentlichen CSS-Export deshalb im Build auf, kopiert ihn unveraendert als eigenes Build-Asset und enqueued dieses Stylesheet separat | Bei scripts-/Gutenberg-Upgrade oder Build-Konfigurationsaenderung |
| [Playwright](https://playwright.dev/docs/intro) | `@playwright/test` 1.58.2 exakt gepinnt | 2026-09-03 | Test Tooling / dokumentierte API | Browser- und Viewport-Pruefungen der lokalen Fixture | Vor Browser-Tooling-Upgrade |

## Internationalisierung

| Quelle | Version/Status | Abruf | Faktklasse | Verwendete Aussage | Revalidierung |
| --- | --- | --- | --- | --- | --- |
| [How to Internationalize Your Plugin](https://developer.wordpress.org/plugins/internationalization/how-to-internationalize-your-plugin/) | offizielle Plugin-Handbook-Dokumentation | 2026-09-03 | Core / dokumentierte Guideline | Textdomain entspricht Slug; Literale; gettext, Plural, Kontext, Platzhalter; Sprachpakete | Vor Release und bei Handbook-Aenderung |
| [Internationalization Guidelines](https://developer.wordpress.org/apis/internationalization/internationalization-guidelines/) | offizielle Common-APIs-Dokumentation | 2026-09-03 | Core / dokumentierte Guideline | `translators:`-Kommentare, vollstaendige Phrasen, keine Verkettung, Positionsplatzhalter, Textverdopplung | Vor Release und bei Guideline-Aenderung |
| [Internationalization Security](https://developer.wordpress.org/plugins/internationalization/security/) | offizielle Plugin-Handbook-Dokumentation | 2026-09-03 | Core / Sicherheitsguideline | Uebersetzungen als nicht vertrauenswuerdig behandeln; kontextgerecht escapen; URLs nicht uebersetzbar machen | Vor Release und bei Security-Guideline-Aenderung |
| [JavaScript Internationalization](https://developer.wordpress.org/block-editor/how-to-guides/internationalization/) | offizielle Block-Editor-Dokumentation | 2026-09-03 | Core / dokumentierte API | `@wordpress/i18n`/`wp-i18n`, Script-Handle/-Pfad, PO-zu-JSON-Workflow und geladene JavaScript-Uebersetzungen | Vor Release und bei Script-API-Aenderung |
| [`wp_set_script_translations()`](https://developer.wordpress.org/reference/functions/wp_set_script_translations/) | WordPress Code Reference | 2026-09-03 | Core / dokumentierte API | Erst nach Script-Registrierung; Handle, Domain und optionaler Pfad | Bei WordPress-API-Aenderung |
| [`wp i18n make-pot`](https://developer.wordpress.org/cli/commands/i18n/make-pot/) | offizielle WP-CLI-Dokumentation | 2026-09-03 | Core Tooling / dokumentierte API | Reproduzierbare POT-Extraktion fuer PHP und JavaScript | Vor Release und bei WP-CLI-Upgrade |
| [`wp i18n make-mo`](https://developer.wordpress.org/cli/commands/i18n/make-mo/) | offizielle WP-CLI-Dokumentation | 2026-09-03 | Core Tooling / dokumentierte API | PO zu ladbarem MO kompilieren | Vor Release und bei WP-CLI-Upgrade |
| [`wp i18n make-json`](https://developer.wordpress.org/cli/commands/i18n/make-json/) | offizielle WP-CLI-Dokumentation | 2026-09-03 | Core Tooling / dokumentierte API | PO zu dateibezogenem Jed-JSON; `--no-purge` behaelt die Test-PO unveraendert | Vor Release und bei WP-CLI-Upgrade |
| [`load_plugin_textdomain()`](https://developer.wordpress.org/reference/functions/load_plugin_textdomain/) | WordPress Code Reference; seit 6.7 Just-in-time-Uebergabe | 2026-09-03 | Core / dokumentierte API | Benutzerdefinierten Plugin-Sprachpfad registrieren; Fixture-Aufruf bei `init`; MO-Name `<domain>-<locale>.mo` | Bei WordPress-i18n-Ladeaenderung |
| [`wp_date()`](https://developer.wordpress.org/reference/functions/wp_date/) und [`number_format_i18n()`](https://developer.wordpress.org/reference/functions/number_format_i18n/) | WordPress Code Reference | 2026-09-03 | Core / dokumentierte API | Locale- und WordPress-Zeitzonen-gerechte PHP-Ausgabe | Bei WordPress-API-Aenderung |
| [`@wordpress/date`](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-date/) | offizielle Paketdokumentation | 2026-09-03 | Components / dokumentierte API | `dateI18n` formatiert in Site-Locale und WordPress-Zeitzone | Bei Paketupgrade |

## Accessibility und allgemeine Userfuehrung

| Quelle | Version/Status | Abruf | Faktklasse | Verwendete Aussage | Revalidierung |
| --- | --- | --- | --- | --- | --- |
| [WordPress Accessibility Coding Standards](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/accessibility/) | offizielle WordPress-Dokumentation | 2026-09-03 | WCAG / WordPress-Standard | WCAG 2.2 AA als Mindestziel | Bei Standardaenderung |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | W3C Recommendation | 2026-09-03 | WCAG / normativ | Reflow, Focus, Target Size, Kontrast, Labels, Fehler- und Statusmeldungen | Bei neuer normativer Zielversion |
| [10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) | etablierte Usability-Heuristik | 2026-09-03 | externe Guideline | Statussichtbarkeit, Konsistenz, Fehlervermeidung, Wiedererkennen | Nur bei geaenderter Skill-Norm oder Quelle |

## Optionale Scoville-UI-Komposition

| Quelle | Version/Status | Abruf | Faktklasse | Verwendete Aussage | Revalidierung |
| --- | --- | --- | --- | --- | --- |
| `scoville-ui-anti-ai-slop` Skill | lokaler Snapshot; SHA-256 `95E17C7F1D2430A7E07EDCFCAA20DCF54BDF44A7F7118B2A416B72EC24BCC99B` | 2026-09-03 | optionale lokale Kompositionsquelle | Produkt-/Plattform-Designsystem bleibt Owner; allgemeine UI-Pruefung ergaenzt innerhalb dieser Grenze | Vor Kompositionstest, bei Installation/Update oder fehlendem Skill |

## Revalidierungsregel

Vor Implementierung und vor jedem Release werden mindestens Branch-/Tag-Aufloesung, Paketversionen, experimenteller Status, Token-Namen/-Werte, Notice-Verhalten, i18n-APIs und die WordPress-7.0-Fixture erneut geprueft. Aendert sich eine tragende Quelle, wird zuerst die Faktklasse und danach die abgeleitete Skill-Norm aktualisiert; beobachtete Core-Selektoren werden nie ohne separate Dokumentation zu einer oeffentlichen API hochgestuft.
