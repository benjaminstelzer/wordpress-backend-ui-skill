---
format_version: 1
id: PLAN-0001
status: completed
created: 2026-09-03
updated: 2026-09-03
---

# WordPress-Backend-Skill fuer konsistente Plugin-Oberflaechen bauen

## Goal

Einen eigenstaendigen installierbaren Agenten-Skill erstellen, der fuer WordPress-7.0-Plugin-Backends zuerst Admin-Flaeche und Runtime-Owner bestimmt und dann mit eindeutig belegten Komponenten-, Spacing-, Vertical-Flow-, Userfuehrungs-, Responsive- und i18n-Regeln konsistente Oberflaechen entwerfen, implementieren und auditieren laesst. Der Skill verwendet WordPress-APIs, Komponenten, Default-CSS und tatsaechlich verfuegbare Tokens vor eigenem CSS. Er kann Scoville UI optional als ergaenzenden UI-Guardrail nutzen, ist davon aber nicht abhaengig. Grundlage sind `docs/audits/wordpress-7-backend-design-system.md`, `docs/research/source-ledger.md` und die akzeptierten Decisions.

## Non-goals

- Kein Frontend-, Block-Theme-, `theme.json`- oder Website-Layout-Skill.
- Keine Behauptung einer vollstaendigen offiziellen WordPress-HIG, solange die Quellen sie nicht liefern.
- Keine Pflicht, experimentelle WPDS-Pakete in klassischen oder Core-Components-Seiten einzufuehren.
- Keine Abhaengigkeit von Scoville UI oder einem anderen Scoville-Skill.
- Keine parallele visuelle Sprache, die WordPress-Buttons, Inputs, Notices, Tabellen, Tokens oder Admin-Shell-Defaults ersetzt.
- Kein GitHub-Push, Tag, Release oder sonstiges Publishing ohne separate Autorisierung; der Plan stellt nur lokal pruefbare, publikationsreife Artefakte her.
- Keine Version-1-Unterstuetzung fuer Block-Editor-Sidebars/SlotFills, Editor-Canvas, Post-Metaboxen, Dashboard-Widgets, Profilfelder, Erweiterungen bestehender Core-Listen/-Screens oder UI innerhalb eines anderen Plugins.
- Keine plugin-spezifische Produktarchitektur, Geschaeftslogik oder Markenoberflaeche.

## Work items

### W-001 Support-Matrix, Runtime-Owner und Quellenvertrag festlegen

Status: done
Depends on: []
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010]
Outcome: Der Skill besitzt eine deterministische Zweiachsen-Klassifikation fuer Admin-Flaeche und Runtime-Owner, eine explizite Version-1-Support-Matrix, einen Quellenvertrag mit festen Faktklassen sowie einen standalone Kompositionsvertrag fuer Scoville UI.
Acceptance: `docs/research/source-ledger.md` fuehrt fuer jede tragende Quelle URL, Ref/SHA oder Dokumentstatus, Version/Paket, Abrufdatum, Faktklasse und Revalidierungstrigger. `tests/cases/routing.yaml` enthaelt mindestens zwoelf eingefrorene positive, negative und ambige Faelle mit erwarteten Feldern `surface`, `support_status`, `runtime_owner`, `shell_owner`, `spacing_owner`, `experimental_components_policy`, `references` und `prohibited_recommendations`; darunter sind alle unterstuetzten und ausgeschlossenen Flaechen sowie PHP/Core, React/Core Components, gebuendeltes WPDS und Hybrid vertreten. Standalone- und Scoville-UI-Komposition liefern dieselbe WordPress-spezifische Entscheidung.
Steps:
1. Support-Matrix aus ADR-0001 in Trigger und Nicht-Trigger ueberfuehren.
2. Die Faktklassen `Core`, `WPDS`, `WCAG` und `Skill-Norm` sowie die Unterteilung dokumentierte API, etablierte Konvention und beobachtete Implementierung festlegen.
3. Source-Ledger mit gepinnten WordPress-7.0- und Gutenberg-`wp/7.0`-Snapshots pflegen.
4. Routing-Schema und Golden-Faelle vor der Skill-Formulierung einfrieren.
5. Standalone-Verhalten und optionale Scoville-UI-Komposition als Concern-Matrix festlegen.
Evidence: [`routing.yaml`: 17/17 eindeutige Faelle und alle acht Pflichtfelder per Contract-Validator bestaetigt, Live-Refs und Paketversionen entsprechen dem Ledger, Support-/Quellen-/Kompositionsvertrag eingefroren]

### W-002 Normatives Spacing- und Vertical-Flow-System spezifizieren

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010]
Outcome: Der Skill enthaelt runtime-spezifische Spacing-Regeln, eine semantische Vertical-Flow-Norm und eine CSS-Eigentumsleiter, mit denen zwei Agenten bei gleicher Struktur denselben Spacing-Owner und dieselbe erlaubte Ausdrucksform waehlen.
Acceptance: `tests/cases/spacing.yaml` benennt je Fall Beziehung, Parent-Owner, Runtime, erwarteten Token/API/Core-Default oder die begruendete Skill-Norm sowie `experimental_components_policy: allow | deny | unknown`. Neue generische Core-Components-Gruppen erwarten fuer alle drei Policy-Werte `Flex` mit `direction="column"`, `align="stretch"`, `justify="flex-start"`, `wrap={ false }`, `expanded={ true }`, dokumentierter `FlexItem`-/`FlexBlock`-Kindrolle und dem Gap-Multiplikator `1/2/3/4/6/8/10` fuer `4/8/12/16/24/32/40px`; `unknown` fuehrt keine neue experimentelle API ein. Bestehende experimentelle Teilbaeume bleiben ihr eigener Owner. `tests/cases/css-ownership.yaml` trennt Pflicht-Wiederverwendung von echten Ausnahmen und verlangt vor einer lokalen Stack-Regel eine nachgewiesene `Flex`-Luecke. Die Referenz trennt Gap, Padding und Dichte, dokumentiert die Wertfolge nur als WPDS-Gap-Skala oder ausdruecklich markierte Skill-Norm, regelt Parent-Ownership, Margin-Reset, Nesting und Empty States und verbietet das Definieren, Ueberschreiben oder Nachahmen von `--wpds-*`. Classic erbt Core-Rhythmik; spezialisierte Core Components besitzen ihre interne Rhythmik, generische vertikale Gruppen folgen ADR-0010; WPDS konsumiert nur bereitgestellte semantische Tokens; Ausnahmen sind als Skill-Norm markiert.
Steps:
1. Runtime-spezifische Token-, Experiment-Policy-, Komponenten- und Flow-Ownership aus ADR-0010 ueberfuehren.
2. Die semantische Spacing-Matrix als ausdruecklich eigene Skill-Norm formulieren.
3. Flow-Eigentum fuer Stack, Section, Card, Field, Message, Portal und Overlay definieren.
4. Classic-Core-Abstaende von Plugin-eigenen Komponentenregeln abgrenzen.
5. CSS-Owner-Check und belegpflichtiges Ausnahmeformat festlegen.
6. Spacing- und CSS-Golden-Faelle vor den Skill-Beispielen einfrieren.
Evidence: [Spacing-Spezifikation eingefroren, 28 Spacing-Faelle inklusive fehlerfreier 21-Fall-Flex-Matrix und neun CSS-Owner-Faelle per `ConvertFrom-Json` geprueft]

### W-003 Responsive Layoutvertrag und Seitenarchetypen definieren

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010]
Outcome: Der Skill kann fuer Settings, Workflow-/Dashboard- und datenreiche Seiten eine konsistente responsive Struktur erzeugen, die in der WordPress-Admin-Shell ohne unbeabsichtigtes horizontales Scrollen und mit erhaltener Lese- und Focus-Reihenfolge funktioniert.
Acceptance: Die Referenz definiert intrinsischen Reflow bis `320 CSS px`, die Core-Grenze `782px` mit Pruefpunkten direkt darueber bei `783px` und darunter, WordPress-Mobile-Controls, WCAG-Zielgroesse, Shell-Padding, `1280px` bei `400%` Zoom oder ein gleichwertiges Reflow-Setup, logische Eigenschaften/RTL, Action-Wrapping und lokale Data-View-Scrollcontainer. Fuer nicht ausgenommene Seitenshells gilt automatisiert `document.documentElement.scrollWidth <= window.innerWidth`. Settings, Workflow-/Dashboard und Data View besitzen getrennte Archetypen und keine als Core-Fakt ausgegebene Universalbreite.
Steps:
1. Core-Reflow-Fakten und abgeleitete Responsive-Skill-Normen getrennt dokumentieren.
2. Breiten- und Grid-Regeln fuer drei Seitenarchetypen definieren.
3. Toolbar-, Form-, Card- und Data-View-Reflow je Archetyp beschreiben.
4. DOM-Reihenfolge, Tastaturfluss, RTL, Textverdopplung und Overflow integrieren.
5. WCAG-2.2-AA-Anforderungen fuer Reflow, Focus, Kontrast und Target Size festlegen.
6. Viewport-, Zoom- und Inhaltsstressfaelle vor Implementierung einfrieren.
Evidence: [Drei responsive Archetypen mit 15/15 Viewport-Faellen plus 400-Prozent-Zoom und RTL-Stress eingefroren, Matrix und Overflow-Invarianten per `ConvertFrom-Json` geprueft]

### W-004 Basis-Userfuehrung, Navigation und Zustandsmuster definieren

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010]
Outcome: Der Skill fuehrt von der primaeren Nutzeraufgabe zu klarer Informationshierarchie, vorhersehbaren Aktionen, verstaendlichen Formularen und vollstaendigen Rueckmeldungs-/Recovery-Zustaenden, ohne eine WordPress-fremde Designsprache einzufuehren.
Acceptance: `tests/cases/ui-guidance.yaml` friert vor W-005 fuer jede relevante Flaeche erwartete Navigation, Primaeraktion, Notice-/Inline-Owner, States, Recovery sowie Accessibility-Invarianten ein. Die Referenz prueft Menueplatzierung, Seitentitel, `wp-header-end`, Header-Aktion, Navigation, progressive Offenlegung, Heading-/Gruppenhierarchie, Labels/Help-Text, Fehleridentifikation, Loading, Empty, Success, Error, Disabled und Permission, Recovery sowie WCAG 2.2 AA. Classic-Seiten platzieren seitenweite verschiebbare Notices so, dass Core sie an `.wp-header-end` ausrichten kann; feldbezogene Meldungen bleiben inline und verwenden `.inline` statt des veralteten `.below-h2`. Jede Regel ist als Core/WPDS/WCAG/Skill-Norm klassifiziert. Eigene Farben sind ausgeschlossen; eine unvermeidbare Farbausnahme benoetigt Kontrastnachweis.
Steps:
1. Gepruefte WordPress-, WCAG- und Usability-Grundlagen in eine priorisierte Agenten-Checkliste ueberfuehren.
2. Navigations- und Informationsarchitektur nach Seitentyp definieren.
3. Aktionshierarchie, Form-Flow, Statusfeedback und Recovery-Muster beschreiben.
4. Notice-Platzierung und Inline-Meldungen an Core-Verhalten ausrichten.
5. Dekorative Container-, Mehrfach-Primary-, Hidden-State- und Custom-Control-Anti-Patterns dokumentieren.
6. UI-Guidance- und Accessibility-Golden-Faelle vor den Skill-Beispielen einfrieren.
Evidence: [Userfuehrungs- und Zustandsvertrag mit zehn vollstaendigen Golden-Faellen und acht relevanten Zustandsarten per `ConvertFrom-Json` geprueft]

### W-007 Internationalisierungsvertrag fuer PHP, JavaScript und Layout spezifizieren

Status: done
Depends on: [W-001]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010]
Outcome: Jede vom Skill erzeugte oder gepruefte UI ist in PHP und JavaScript extrahierbar, uebersetzbar, sicher ausgebbar und gegen Sprachlaenge, RTL sowie locale-abhaengige Formate robust.
Acceptance: Die Referenz verlangt fuer alle nutzergerichteten Strings einschliesslich ARIA-/Screenreader-/Alternativtext eine literale, dem Plugin-Slug entsprechende Textdomain; PHP-gettext- und Escape-Funktionen; `@wordpress/i18n` bzw. `wp-i18n`; eine registrierte Script-Handle vor `wp_set_script_translations()` mit explizitem Sprachdateipfad; vollstaendige Phrasen, Positionsplatzhalter, Plural/Kontext und unmittelbar vorangestellte `translators:`-Kommentare; `wp_date()`/`number_format_i18n()` sowie `dateI18n` aus `@wordpress/date`. Clientseitig angezeigte locale-formatierte Zahlen kommen in der Baseline serverformatiert; eine JS-Alternative benoetigt eigene Quelle, Locale-Zuordnung und Browsertest. `tests/cases/i18n.yaml` deckt positive und negative PHP-/JS-Faelle ab. Quellen werden mit `wp i18n make-pot` in ein POT extrahiert; eine dagegen gepflegte Test-PO namens `<slug>-<locale>.po` wird mit `wp i18n make-mo` zu `languages/<slug>-<locale>.mo` kompiliert und der Plugin-Sprachpfad bei `init` mit `load_plugin_textdomain()` registriert. Dieselbe PO erzeugt mit `wp i18n make-json --no-purge` die erwartete JSON-Datei; der Golden-Fall fixiert den dokumentierten Handle-Dateinamen oder Build-Pfad/MD5 und verbietet `src/`-Referenzen fuer ein registriertes `build/`-Script. Nach reproduzierbarem Site-/Admin-User-Locale-Wechsel beweisen Browser-Assertions mindestens einen tatsaechlich uebersetzten PHP- und React-String. Layoutfaelle mit Textverdopplung, langen deutschen Labels, einer RTL-Sprache und locale-abhaengigen Zahlen/Datumswerten verlieren keine Information oder Funktion.
Steps:
1. PHP-, JavaScript-, Textdomain- und Script-Translation-Regeln aus ADR-0008 formulieren.
2. String-Komposition, Plural, Kontext, Platzhalter, Translator-Kommentare und Escaping mit positiven/negativen Beispielen dokumentieren.
3. Locale-gerechte Datums- und Zahlenformatierung festlegen.
4. Quellen-zu-POT, Test-PO, PO-zu-MO, `load_plugin_textdomain()` auf `init`, PO-zu-JSON mit `--no-purge` sowie PHP-/React-Runtime-Uebersetzung als reproduzierbare Checks definieren.
5. i18n-Golden-Faelle vor den Skill-Beispielen einfrieren.
6. Textverdopplung, Deutsch und RTL in Spacing-/Responsive-Vertraege rueckkoppeln.
Evidence: [i18n-Vertrag und 24 Golden-Faelle mit positiven und negativen PHP-/JavaScript-, Tooling-, Runtime- und Layoutfaellen per `ConvertFrom-Json` geprueft]

### W-005 Skill-Paket mit Referenzen, Tests, Beispielen und GitHub-Dokumentation implementieren

Status: cancelled
Depends on: [W-002, W-003, W-004, W-007]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010]
Outcome: Ein installierbares Skill-Verzeichnis enthaelt eine kompakte `SKILL.md`, bedarfsgerecht geladene Referenzen, eingefrorene Golden-Faelle, eine WordPress-7.0-Fixture, umsetzbare Beispiele und knappe publikationsreife GitHub-Dokumentation ohne doppelte Autoritaet.
Acceptance: Der aus dem installierten `skill-creator` aufgeloeste Validator `scripts/quick_validate.py` meldet fuer `<skill-root>` `Skill is valid!`; die aktuelle lokale Referenz ist `python "C:\Users\benja\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "<skill-root>"`. Der Skill-Ordnername entspricht dem Frontmatter-`name`; nicht vom Validator unterstuetzte Zusatzkeys werden vermieden. `SKILL.md` funktioniert standalone, routet nur relevante Referenzen und beschreibt optionale Scoville-UI-Komposition. Classic-, Core-Components-, WPDS- und Hybrid-Beispiele benennen Flaeche, Runtime-, Shell-, Spacing- und Token-Owner; i18n ist in PHP und JavaScript umgesetzt; jede Custom-CSS-Ausnahme ist begruendet. Ein Root-`README.md` folgt in Stimme, Direktheit und nutzerorientierter Dramaturgie den lokalen Referenzen `Z:\Projekts\AI\ask-claude-for-codex\README.md` und `Z:\Projekts\AI\ask-claude-and-sol-for-codex\README.md`: Es beginnt mit einer knappen Aussage zum Problem und Nutzen, erklaert vor allem, was der Skill fuer WordPress-Plugin-Backends leistet und wann er eingesetzt wird, und nennt WordPress-7.0-Fokus, Spacing-/Vertical-Flow-Vertrag, Core-Defaults-vor-Custom-CSS, Responsive-Verhalten, Accessibility, i18n, standalone Nutzung und optionale Scoville-UI-Komposition. Technische Details bleiben auf die fuer Nutzung, Installation, Anforderungen, belastbare Grenzen, Quellen, Status und Lizenz noetigen Angaben beschraenkt; interne Architektur, Repository-Baum, Reviewer-Provenienz und unbelegte Qualitaetsbehauptungen bleiben draussen. Ein Root-`CHANGELOG.md` dokumentiert publikationsrelevante nutzersichtbare Aenderungen mit klaren Kategorien und beobachteter Validation; bis eine Release-Version entschieden ist, bleibt der Eintrag `Unreleased`, vor einer Veroeffentlichung muessen Version, Datum, Paketmetadaten und Tag uebereinstimmen. `package.json` pinnt `@wordpress/env` auf `11.0.1` und alle gebuendelten WPDS-Pakete exakt auf die im Ledger genannten Versionen; Node-Major ist ueber `engines` und `.nvmrc` festgelegt, ein Lockfile ist vorhanden, Installation erfolgt mit `npm ci`, Ausfuehrung mit `npx --no-install wp-env`. `.wp-env.json` prueft eine echte Single-Site-Installation; `.wp-env.multisite.json` wird explizit mit `--config=.wp-env.multisite.json` und eigenem `WP_ENV_PORT` gestartet, pinnt ebenfalls `core` auf `WordPress/WordPress#7.0`, setzt `multisite: true` und prueft Site sowie Network Admin. Fuer gerenderte lokale Pruefungen wird zusaetzlich ausschliesslich das neue Verzeichnis `Z:\xampp_lite_8_5\www\wordpress-backend-skill-test` verwendet; bestehende XAMPP-Sites bleiben unberuehrt und die lokale Apache-, PHP- und MariaDB-Version wird als Evidenz erfasst. Ein reproduzierbares Setup setzt zuerst Site-Locale und danach Admin-User-Locale, prueft den resultierenden Wert von `determine_locale()` und nutzt die gebuendelten Plugin-Testartefakte; Core-Sprachpakete koennen ergaenzend installiert werden, sind fuer den Plugin-MO-Beweis aber nicht erforderlich. Die verwendete Container-WP-CLI-Version wird als Evidenz protokolliert. WPDS-Tests pruefen geladenen Provider/Styles und keine unaufgeloeste `--wpds-*`-Referenz.
Steps:
1. Skill-Verzeichnis und frontmatter-konforme `SKILL.md` mit dem Skill-Creator anlegen.
2. Spacing-, Responsive-, Userfuehrungs-, i18n-, Komponenten- und Quellenreferenzen nach Progressive Disclosure aufteilen.
3. Classic-, Core-Components-, WPDS- und Hybrid-Beispiele gegen die Golden-Faelle erstellen.
4. Standalone- und optionale Scoville-UI-Kompositionsanweisungen integrieren.
5. Gepinnte Node-Abhaengigkeiten, Lockfile, getrennte WordPress-7.0-Single-Site-/Multisite-Fixtures, Locale-Setup und wp-env-Konfigurationen anlegen.
6. Eine separate lokale WordPress-Testinstallation unter `Z:\xampp_lite_8_5\www\wordpress-backend-skill-test` fuer gerenderte Browserpruefungen einrichten, ohne vorhandene Sites zu veraendern.
7. Root-`README.md` in Benjamins Stimme anhand der beiden Ask-Skill-Referenzen und Root-`CHANGELOG.md` als nutzersichtbares Release-Protokoll erstellen.
8. Validator, `npm ci`, `npx --no-install wp-env` und interne Pfad-/Linkpruefung ausfuehren.
Evidence: [`wordpress-backend-ui/SKILL.md` und alle gerouteten Referenzen implementiert, ADR-0011 korrigiert den gestarteten WPDS-Pfad auf ausschliesslich oeffentliche Exporte bei unveraenderten authored fields, Format 1 haelt gestartete W-005-Entscheidungen unveraendert und verknuepft ADR-0011 hier sowie im noch editierbaren W-006, Der im Review fehlende Heading-zu-Intro-Vertrag wurde waehrend W-005 transparent als 28. Spacing-Fall `wpds-heading-intro` ergaenzt und durch den Contract-Validator abgesichert, ADR-0012 baselint den korrigierten sechs Dateien umfassenden Golden-Korpus per SHA-256-Manifest fuer W-006 statt einen nicht gespeicherten 27-Fall-Vorzustand zu behaupten, Skill-Creator-Validator meldet `Skill is valid!`, Contract-Validator PHP-Lint und Scoville-Plan-Validator bestanden, Node 24.20.0 Production-Build bestanden, Sauberer `npm ci` mit 1910 Paketen und `npm ls --depth=0` bei exakten Pins bestanden, POT PO MO und Jed-JSON aus `build/index.js` aktualisiert, Site-Locale danach Admin-User-Locale auf de_DE gesetzt und `determine_locale()` auf Single Site und Multisite als de_DE beobachtet, WordPress 7.0 Single Site unter `Z:\xampp_lite_8_5\www\wordpress-backend-skill-test` und WordPress 7.0.4 Network Admin unter `Z:\xampp_lite_8_5\www\wordpress-backend-skill-test-multisite` gerendert, Finaler verzogerter WPDS-Fallback Core-Notice-Ansagepfad alle Viewports deutsche PHP-JS-i18n RTL und kontexttreue Permission-Recovery bestanden, Fable und SOL melden im finalen Re-Review keine High- oder Medium-Befunde, Review-Evidenz liegt in `docs/reviews/final-skill-review-2026-09-03.md`, Runtime-Evidenz liegt in `docs/validation/wordpress-7-runtime-2026-09-03.md`, MIT-Lizenz in LICENSE README package.json und CHANGELOG konsistent eingetragen, Beide gepinnten wp-env-Starts erreichen wegen fehlendem Docker `spawn docker ENOENT`, Kein Docker-Runtime-Pass wird behauptet, Nutzer hat Docker ausgeschlossen und mit ADR-0013 den nativen XAMPP-Nachfolger gewaehlt; W-005 wird ohne Umdeutung seiner Acceptance ersetzt]

### W-008 Docker-freie XAMPP-Abnahme reproduzierbar machen

Status: done
Depends on: [W-002, W-003, W-004, W-007]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010, ADR-0013]
Outcome: Das vollstaendige Skill-Paket besitzt einen kanonischen Docker-freien, read-only pruefbaren XAMPP-Abnahmepfad fuer eine isolierte WordPress-7.0-Single-Site und eine WordPress-7.0.x-Multisite, ohne den publizierten Skill an XAMPP oder Scoville UI zu binden.
Acceptance: `fixture/native-xampp.json` fixiert fuer beide isolierten Sites relative Pfade, exakte WordPress-Version, Single-/Multisite-Modus, aktiven Fixture-Status, `de_DE` und erforderliche Build-Artefakte. `scripts/validate-xampp-fixtures.ps1` akzeptiert den XAMPP-Root als Parameter oder ueber `XAMPP_LITE_ROOT`, loest nur Pfade innerhalb dieses Roots auf und prueft read-only PHP, WP-CLI, Apache, MariaDB, beide Core-Versionen, Site-Typen, aktives Plugin, die auf `fixture/plugin` gerichteten Junctions, Site- und Admin-Locale sowie Build-Artefakte, ohne Zugangsdaten auszugeben. Das Skript besteht gegen `Z:\xampp_lite_8_5`. `package.json`, Lockfile, README, Fixture-Dokumentation und Runtime-Evidenz verwenden diesen nativen Pfad als kanonische Abnahme; `.wp-env.json`, `.wp-env.multisite.json`, `@wordpress/env` und das `wp-env`-Skript sind entfernt. Der Skill-Creator-Validator, Contract-Validator, PHP-Lint, Production-Build, sauberes `npm ci` und `npm ls --depth=0` bestehen auf dem finalen Paket. POT, PO, MO und Jed-JSON bleiben reproduzierbar und die bereits gerenderten Single-Site-/Network-Admin-, Responsive-, Accessibility-, i18n-, RTL- und WPDS-Beobachtungen werden durch den Runtime-Preflight nicht ueberbeansprucht.
Steps:
1. ADR-0013 in native Fixture-Konfiguration, Validator und Dokumentation ueberfuehren.
2. Docker-/wp-env-Paketartefakte und die unnoetige Abhaengigkeit entfernen.
3. Den read-only XAMPP-Preflight gegen beide vorhandenen isolierten Sites ausfuehren.
4. Build-, Contract-, i18n-, PHP-, Skill- und Dependency-Checks auf dem finalen Paket wiederholen.
5. Runtime-Evidenz und Plan nur mit beobachteten Ergebnissen aktualisieren.
Evidence: [Native XAMPP-Validator bestand read-only fuer WordPress 7.0 Single Site und WordPress 7.0.4 Multisite, PHP 8.5.5 WP-CLI 2.12.0 Apache 2.4.66 und MariaDB 11.4.10 wurden exakt bestaetigt, Beide Fixture-Junctions Aktivierungsarten und de_DE-Locale-Pruefungen bestanden, Sauberes Node-24 `npm ci --offline` installierte 1667 Lockfile-Pakete und `npm ls --depth=0` bestand, Production-Build Contract-Validator PHP-Lint Skill-Creator-Validator POT MO und Jed-JSON bestanden, Docker-Konfigurationen direkte @wordpress/env-Abhaengigkeit und wp-env-Skript sind entfernt, Runtime-Evidenz dokumentiert Online-Stillstand und den bestandenen Offline-Clean-Install ohne einen Online-Pass zu behaupten]

### W-006 Agentenverhalten und gerenderte Ergebnisse validieren

Status: done
Depends on: [W-008]
Blocked by: []
Decisions: [ADR-0001, ADR-0002, ADR-0008, ADR-0010, ADR-0011, ADR-0012, ADR-0013]
Outcome: Der fertige Skill ist durch Golden-Faelle, einen frischen Agentenlauf und gerenderte WordPress-7.0-Plugin-Backends gegen falsche Owner, inkonsistentes Spacing, unnoetiges Custom CSS, i18n-Ausfaelle, schlechte Userfuehrung und Responsive-Fehler geprueft.
Acceptance: Dokumentierte Tests decken standalone ohne Scoville UI, optionale Komposition, alle vier Runtime-Owner, unklare/ausgeschlossene Flaechen, Single Site und Network Admin, Notice-Platzierung, lange/verdoppelte deutsche Labels, RTL, funktionierende PHP-/JS-Runtime-Uebersetzung, locale-Formate, alle relevanten States, Action-Wrapping, CSS-Ausnahmen und Data-View-Reflow ab. Gerenderte Pruefungen laufen bei `783`, `782`, `600`, `390` und `320` CSS-Pixeln sowie `1280px` bei `400%` Zoom oder gleichwertig. Explizite Pass-/Fail-Assertions pruefen Focus-Reihenfolge, sichtbaren und nicht verdeckten Focus, Tastaturbedienung, `24x24px` Pointer-Ziele oder zulaessige Ausnahmen, WCAG-AA-Kontrast, Accessible Names/Labels, textliche Fehleridentifikation und programmatische Statusmeldungen; ein automatischer Scan wird durch manuelle Tastatur-/Focus-Pruefung ergaenzt. Nicht ausgenommene Seitenshells erfuellen `document.documentElement.scrollWidth <= window.innerWidth`; Tabellen scrollen nur lokal. Ein Clean-Install-/Fresh-Agent-Smoke-Test laeuft in einem sauberen Arbeitsverzeichnis ohne Repository-Kontext und nur mit installiertem Skill; die eingefrorenen Prompts muessen die erwarteten Owner und `prohibited_recommendations` liefern und im Classic-Fall ohne geladene WPDS-Runtime kein `--wpds-*` empfehlen. Danach wird derselbe Korpus separat mit der im Ledger erfassten Scoville-UI-Version wiederholt. README-Installations- und Nutzungsangaben werden aus einem sauberen Arbeitsverzeichnis ausgefuehrt; alle oeffentlichen Aussagen werden gegen das beobachtete Skill-Verhalten geprueft, relative Links und GitHub-Markdown muessen funktionieren, und der Changelog darf nur tatsaechlich implementierte sowie validierte Aenderungen nennen. Vor einer spaeter separat autorisierten Veroeffentlichung muessen README, Changelog, Paketversion, Datum und Release-Metadaten konsistent sein. Alle gefundenen materiellen Fehler sind am kanonischen Owner korrigiert und die betroffenen Checks erneut bestanden.
Steps:
1. Die nach dem Review gemaess ADR-0012 neu baselinten Golden-Oracles gegen `tests/cases/MANIFEST.sha256` verifizieren und ihren seit dieser Baseline unveraenderten Stand nachweisen.
2. Den nativen XAMPP-Validator gegen die manifestierten Single-Site- und Multisite-Fixtures ausfuehren und das reproduzierbare Site-/Admin-User-Locale-Setup bestaetigen.
3. Frische Agentenfaelle ausserhalb des Repositories zuerst standalone und danach mit der erfassten Scoville-UI-Version ausfuehren.
4. Source-Fidelity, Routing, Komponentenwahl, i18n, CSS-Owner und Spacing-Ausgaben deterministisch pruefen.
5. Die lokale XAMPP-Site und die reproduzierbaren Fixtures bei allen Viewports, Zoom-, RTL-, Sprach- und Eingabebedingungen rendern und bedienen.
6. README aus einem sauberen Arbeitsverzeichnis nachvollziehen, oeffentliche Aussagen und Links gegen Artefakte pruefen sowie Changelog und Release-Metadaten auf Konsistenz kontrollieren.
7. Fehler am kanonischen Owner korrigieren und gezielte sowie volle Checks wiederholen.
8. Beobachtete Evidenz eintragen und den Plan erst dann abschliessen.
Evidence: [ADR-0014 korrigiert und baselint die Routing-Policy; Manifest und Contract-Validator bestehen, Acht aktuelle Prompts bestehen repository-frei 8/8 standalone und 8/8 mit optionalem Scoville UI, Native XAMPP-Abnahme besteht fuer WordPress 7.0 Single Site und 7.0.4 Multisite mit de_DE, Gerenderte Checkliste besteht bei 783 782 600 390 und 320px inklusive lokalem Tabellen- und Action-Wrapping, Finaler Core-Axe-Rerun besteht nach dokumentierter lokaler Kontrastausnahme mit 0 Violations und 0 Incomplete, Clean-Snapshot-Build i18n PHP-Lint Skill- und Plan-Validator bestehen, SOL meldet im korrigierten Abschlussreview GO; alle tatsaechlichen Fable-Befunde sind behoben, gezielte Fable-Bestaetigung endete providerseitig 529 und wird nicht als GO behauptet]
