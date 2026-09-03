# Audit: WordPress-7.0-Backend-Designsystem fuer Plugin-Oberflaechen

Stand: 2026-09-03

## Auditauftrag

**Outcome:** Eine belastbare Grundlage fuer einen Agenten-Skill, der WordPress-7.0-Plugin-Oberflaechen im `wp-admin` mit konsistentem Spacing, nachvollziehbarem Vertical Content Flow, internationalisierbaren Strings und responsive ohne horizontales Ausbrechen entwerfen oder pruefen kann.

**Canonical owner:** Offizielle WordPress-7.0-Quellen besitzen die Tatsachenhoheit. Der geplante Skill besitzt nur die daraus abgeleiteten, als solche gekennzeichneten Arbeitsregeln. Frontend-Regeln aus `theme.json`, Block-Spacing und Theme-Layout sind nicht Teil dieses Audits.

**Risk state:** Normal. Das Audit veraendert keine WordPress-Laufzeit. Das materielle Risiko liegt in falscher Autoritaet: Ein Agent koennte eine abgeleitete Konvention als offizielle WordPress-Regel ausgeben oder klassische Core-Abstaende mit einem modernen Stack-System doppeln.

**Proof:** Quellpruefung der in `docs/research/source-ledger.md` gepinnten WordPress-7.0- und Gutenberg-`wp/7.0`-Commits sowie offizieller WordPress-, WP-CLI-, WCAG- und i18n-Dokumentation. Es wurden noch keine gerenderten Plugin-Seiten oder Browserinteraktionen getestet.

## Kurzurteil

WordPress 7.0 besitzt fuer Plugin-Backends keine einzelne, stabile und vollstaendige Human Interface Guideline. Der Skill darf deshalb nicht nur zwischen Classic und React unterscheiden, sondern muss zwei Achsen getrennt klassifizieren:

1. **Admin-Flaeche:** plugin-eigene Seite oder eingebettete/fremd besessene Oberflaeche; Version 1 unterstuetzt nur die in ADR-0001 festgelegten plugin-eigenen Seiten.
2. **Runtime-/Komponenten-Owner:** PHP/Core-Markup, React mit Core-`@wordpress/components`, gebuendeltes experimentelles WPDS oder hybrid mit Owner je DOM-Region.

Die offiziellen Quellen liefern konkrete Werte, aber keine vollstaendige semantische Regel fuer jeden vertikalen Abstand oder jede Userfuehrung. Ein brauchbarer Agenten-Skill muss deshalb vier feste Kennzeichnungen sichtbar trennen:

- **Core:** dokumentierte API, etablierte Admin-Konvention oder als solche markierte beobachtete WordPress-7.0-Implementierung.
- **WPDS:** exakter Wert oder Vertrag eines experimentellen `wp/7.0`-Pakets.
- **WCAG:** normative Accessibility-Anforderung.
- **Skill-Norm:** projektdefinierte Zuordnung, die Luecken schliesst und Konsistenz erzeugt.

## Quellenhierarchie

| Rang | Quelle | Verbindlichkeit fuer den Skill |
| --- | --- | --- |
| 1 | WordPress-7.0-Core-CSS und offizielles Plugin-Handbuch | Autoritativ fuer klassisches `wp-admin` und Settings-API-Verhalten |
| 2 | Gutenberg-Branch `wp/7.0` | Autoritativ fuer den untersuchten Stand der WPDS-Tokens und Komponenten, aber experimentell |
| 3 | WordPress Accessibility Coding Standards und WCAG 2.2 AA | Mindeststandard fuer Wahrnehmbarkeit, Bedienbarkeit, Verstaendlichkeit und Robustheit |
| 4 | Etablierte Usability-Heuristiken | Evidenz fuer allgemeine Userfuehrung, aber kein Ersatz fuer WordPress-Konventionen |
| 5 | Abgeleitete Skill-Normen | Verbindlich fuer Agentenausgaben, jedoch nie als offizielle WordPress-Vorgabe zu bezeichnen |

Das kanonische Quelleninventar steht in `docs/research/source-ledger.md`. Jede tragende Aussage erhaelt dort URL, Ref/SHA oder Dokumentstatus, Version/Paket, Abrufdatum, Faktklasse und Revalidierungstrigger. Beobachtete Core-Selektoren sind keine oeffentliche Erweiterungs-API.

## Befunde

### F-001: Es gibt keine einzelne offizielle Backend-HIG fuer Plugin-Seiten

**Beobachtung:** Das Plugin-Handbuch beschreibt die Settings API als Weg zu visuell konsistenten, zukunftssicheren Einstellungsseiten. Die konkreten Layoutwerte liegen jedoch im Core-CSS. Parallel existieren Core-bereitgestellte React-Komponenten und separate experimentelle WPDS-Pakete. React ist deshalb kein Synonym fuer WPDS.

**Auswirkung:** Ein Agent, der nur nach einer "WordPress Design Guideline" sucht, vermischt leicht Frontend-Editorregeln, klassisches `wp-admin` und experimentelles WPDS.

**Skill-Anforderung:** Vor jedem Entwurf klassifiziert der Agent zuerst die Admin-Flaeche und danach den Runtime-/Komponenten-Owner. Version 1 unterstuetzt plugin-eigene Single-Site-Settings-/Tool-Seiten, Workflow-/Dashboard-Seiten, Data Views und explizite Network-Admin-Seiten. Block-Editor-Sidebars/SlotFills, Editor-Canvas, Post-Metaboxen, Dashboard-Widgets, Profilfelder, Core-Listen-Erweiterungen und UI innerhalb eines anderen Plugins werden separat geroutet oder ausgeschlossen. Ohne Klassifikation darf er keine Spacing- oder Komponentenempfehlung ausgeben.

**Evidenz:** [Settings API](https://developer.wordpress.org/plugins/settings/settings-api/), [`@wordpress/components`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/README.md), [`@wordpress/admin-ui`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/README.md), [`@wordpress/ui`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/README.md).

### F-002: Das moderne WPDS verwendet ein 4-px-Grundraster

**Beobachtung:** Die WordPress-7.0-Dimension-Tokens definieren primitive Abstaende von `0`, `4`, `8`, `12`, `16`, `20`, `24`, `32`, `40` und `48px`. Die semantische Gap-Skala lautet:

| Gap-Token | Defaultwert |
| --- | ---: |
| `xs` | 4px |
| `sm` | 8px |
| `md` | 12px |
| `lg` | 16px |
| `xl` | 24px |
| `2xl` | 32px |
| `3xl` | 40px |

Die Padding-Skala ist nicht identisch: `xl` ist dort `20px`, `2xl` `24px` und `3xl` `32px`. Die Tokens besitzen zudem Dichtevarianten. Dichte und Responsivitaet sind getrennte Achsen; "compact" ist kein Mobile-Modus.

**Auswirkung:** Eine vereinfachte Liste ohne Tokenart erzeugt Fehler, insbesondere bei `xl` und `2xl`.

**Skill-Anforderung:** Der Skill muss Gap und Padding separat tabellieren. Semantische `--wpds-*`-Tokens duerfen nur konsumiert werden, wenn das gewaehlte WPDS-Paket sie ueber einen oeffentlichen Stylesheet-Export tatsaechlich liefert und dieser am Render-Root geladen ist; Plugin-Code darf sie nicht definieren, ueberschreiben oder nachahmen. Primitive Tokens bleiben intern. Classic/Core und Core Components verwenden zuerst ihre eigenen Defaults/APIs. Eine unvermeidbare plugin-eigene Zahl wird als Skill-Norm und nicht als WordPress-Token gekennzeichnet.

**Evidenz:** [`@wordpress/theme` Vertrag](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/README.md), [`dimension.json` am gepinnten `wp/7.0`-Stand](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/tokens/dimension.json).

### F-003: Die moderne Page-Shell liefert einen konkreten Ausgangspunkt

**Beobachtung:** Die `Page`-Komponente aus `@wordpress/admin-ui` verwendet fuer Header und gepaddeten Inhalt standardmaessig `padding-lg` vertikal und `padding-2xl` horizontal. Im Default entspricht das `16px` vertikal und `24px` horizontal. Der Header nutzt intern `gap="sm"`, also `8px`; der Untertitel besitzt `padding-block-end` mit `padding-xs`, also `4px`.

**Auswirkung:** `16/24px` ist der staerkste quellgestuetzte moderne Page-Shell-Wert. Er ist kein universeller Wert fuer jede verschachtelte Gruppe.

**Skill-Anforderung:** Fuer moderne Vollseiten ist `16px block / 24px inline` der Default. Engere Viewports duerfen das Inline-Padding reduzieren, aber nicht ueber Dichte-Tokens implizit umschalten.

**Evidenz:** [`Page`-Styles](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/src/page/style.scss), [`PageHeader`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/src/page/header.tsx).

### F-004: Vertical Flow ist im modernen Stack nicht automatisch

**Beobachtung:** `@wordpress/ui` stellt einen flexiblen `Stack` bereit. Dessen `direction` und `gap` sind optional und haben keinen Default. `@wordpress/theme` exportiert am WordPress-7.0-Pin zwar `design-tokens.css`, aber keinen oeffentlichen `ThemeProvider` zur Laufzeit; die vorhandenen `privateApis` sind kein Plugin-Vertrag. Der separate `__experimentalVStack` aus `@wordpress/components` ist selbst experimentell; sein `spacing` ist ein Multiplikator des 4-px-Rasters und kein semantischer WPDS-Gap-Name.

**Auswirkung:** Ein Agent muss fuer jede semantische Ebene einen Abstand besitzen. Andernfalls entstehen zufaellige Browser-Margins oder inkonsistente Einzelwerte.

**Skill-Anforderung:** Ein Parent besitzt den Abstand zwischen seinen direkten Kindern. Kinder setzen nicht zusaetzlich denselben Aussenabstand. Standardmargins von Headings und Paragraphen werden in einem gap-gesteuerten Stack neutralisiert. Im React/Core-Components-Pfad besitzen spezialisierte Komponenten ihre interne Rhythmik. Fuer eine neue generische vertikale Plugin-Gruppe besitzt die Core-bereitgestellte `Flex`-Komponente den Flow: `direction="column"`, `align="stretch"`, `justify="flex-start"`, `wrap={ false }`, `expanded={ true }` und `gap` als Skill-Norm geteilt durch vier. Das gilt fuer `allow`, `deny` und `unknown`; die Experiment-Policy verhindert weiterhin neue experimentelle APIs. Im gebuendelten WPDS-Pfad setzt `Stack` `direction="column"` und den semantischen Gap explizit, laedt den oeffentlichen CSS-Subpath und verwendet keine privaten Provider-APIs. Eine plugin-lokale Stack-Regel ist erst nach einer belegten `Flex`-Luecke zulaessig.

**Evidenz:** [`Stack`-Implementierung](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/src/stack/stack.tsx), [`Stack`-Typen](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/src/stack/types.ts), [`Flex`-Typen](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/src/flex/types.ts), [`Flex`-Implementierung](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/src/flex/flex/component.tsx), [`VStack`-README](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/src/v-stack/README.md).

### F-005: Klassisches `wp-admin` besitzt eine eigene Legacy-Rhythmik

**Beobachtung:** Im WordPress-7.0-Core gelten unter anderem:

- `#wpcontent`: `20px` linkes Padding.
- `.wrap`: `10px 20px 0 2px` Margin.
- `.wrap h1`: `0` Margin und `9px 0 4px` Padding.
- `.form-table td`: `15px 10px` Padding.
- `.form-table th`: `20px 10px 20px 0` Padding bei `200px` Breite.
- `.form-table td p`: `4px` oben und `0` unten.
- `p.submit`: `20px` Margin oben und `10px` Padding oben.

**Auswirkung:** Ein modernes 4-px-Stack-System darf nicht pauschal ueber `.wrap`, `.form-table` oder `p.submit` gelegt werden. Das erzeugt doppelte Abstaende und bricht die visuelle Einordnung in den Admin.

**Skill-Anforderung:** Bei nativen Settings-API-Seiten besitzt Core die aeussere und zeilenbezogene Rhythmik. Eigene Gaps gelten nur innerhalb klar abgegrenzter Plugin-Komponenten.

**Evidenz:** [`wp-admin/css/common.css` am gepinnten WordPress-7.0-Stand](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/common.css), [`wp-admin/css/forms.css`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/forms.css).

### F-006: `782px` ist die entscheidende Core-Grenze fuer Form-Reflow

**Beobachtung:** Bei maximal `782px` reduziert Core das linke `#wpcontent`-Padding auf `10px`, setzt `.wrap` links auf `0` und rechts auf `12px`, stellt Form-Tabellenkoepfe und -zellen blockweise dar und setzt typische Formularfelder auf volle Breite. Textfelder und Selects erhalten mindestens `40px` Hoehe; Text und Selects verwenden `16px` Schrift. Die mobile Form-Rhythmik wird auf `10px` oberhalb des Labels sowie `4px 0 6px` im Feldbereich umgestellt.

**Auswirkung:** Responsive Verhalten bedeutet im WordPress-Backend nicht nur kleinere Abstaende. Spalten muessen stapeln, Controls wachsen auf bedienbare Hoehe und die Lesereihenfolge muss erhalten bleiben.

**Skill-Anforderung:** Der Skill muss `782px` als Core-Kompatibilitaetsgrenze behandeln. Plugin-eigene Layouts sollen zuvor intrinsisch umbrechen und duerfen nicht erst bei `782px` auf einen unbrauchbaren Zwischenzustand reagieren.

**Evidenz:** [`common.css`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/common.css), [`forms.css`](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/wp-admin/css/forms.css).

### F-007: Die modernen Pakete sind in WordPress 7.0 noch experimentell

**Beobachtung:** `@wordpress/ui` und `@wordpress/theme` bezeichnen sich als experimentell. `@wordpress/ui` wird nicht ueber das globale `window.wp` bereitgestellt und muss gebuendelt werden. `@wordpress/admin-ui` ist nur knapp dokumentiert. Das ist vom React-Pfad mit Core-bereitgestelltem `@wordpress/components` zu unterscheiden.

**Auswirkung:** Ein Skill darf den modernen Pfad nicht als stabile, ueberall vorhandene Plugin-API behandeln.

**Skill-Anforderung:** WPDS-Beispiele muessen Paketierung, Version-Pinning, Token-Stylesheet und den experimentellen Status nennen. Core-Components-Beispiele verwenden dagegen die von WordPress registrierten Pakete und Komponenten-APIs. Der klassische Pfad bleibt die stabile Baseline.

**Evidenz:** [`@wordpress/ui`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/ui/README.md), [`@wordpress/theme`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/theme/README.md), [`@wordpress/admin-ui`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/admin-ui/README.md), [`@wordpress/components`](https://github.com/WordPress/gutenberg/blob/28c0dedc4eaf001a24237a1fbba4b0887698b000/packages/components/README.md).

### F-008: WordPress definiert keine universelle Inhaltsbreite fuer Plugin-Seiten

**Beobachtung:** Die untersuchten Core- und WPDS-Quellen liefern Shell-Abstaende und Reflow-Verhalten, aber keine universelle maximale Breite fuer Settings, Dashboards und Datentabellen.

**Auswirkung:** Eine einzige feste `max-width` waere eine erfundene WordPress-Regel und fuer datenreiche Seiten ungeeignet.

**Skill-Anforderung:** Der Skill benoetigt Layout-Archetypen statt einer Universalbreite: fokussierte Settings, mehrspaltige Uebersicht und datenreiche Liste/Tabelle. Jede Breitenempfehlung muss als Skill-Norm und nicht als Core-Fakt markiert sein.

### F-009: WordPress-Komponenten und Default-CSS sind vor eigenem CSS zu verwenden

**Beobachtung:** Das Plugin-Handbuch begruendet die Settings API mit visueller Konsistenz, Zukunftssicherheit und weniger eigener Arbeit. `@wordpress/components` stellt gemeinsame React-UI-Elemente bereit. Core bietet zudem native Buttons, Form Controls, Notices, Tabellen und Admin-Shell-Klassen. Welche dieser Optionen zulaessig ist, haengt vom Runtime- und DOM-Owner ab; ein beobachteter Core-Selektor ist nicht automatisch eine oeffentliche Plugin-API.

**Auswirkung:** Eigenes CSS fuer bereits vorhandene WordPress-Primitive schafft eine parallele Designsprache, erhoeht den Wartungsaufwand und kann Core-Updates, RTL, High Contrast, Focus States oder Mobile-Verhalten ueberdecken.

**Skill-Anforderung:** Der Agent muss vor jeder eigenen CSS-Regel den Runtime- und DOM-Owner bestimmen und dann pruefen: dokumentierte Core-API/semantisches Markup, passende vorhandene Komponente oder Default-CSS, tatsaechlich bereitgestellter semantischer Token, eng begrenzte Komposition, erst dann begruendetes Plugin-CSS. Er darf keine Core-Komponente nur zum Zweck anderer Abstaende, Farben, Radien, Schatten oder Control-Hoehen nachbauen.

**Evidenz:** [Settings API](https://developer.wordpress.org/plugins/settings/settings-api/), [`@wordpress/components` Component Reference](https://developer.wordpress.org/block-editor/reference-guides/components/), [Development Platform](https://developer.wordpress.org/block-editor/how-to-guides/platform/).

### F-010: Gute Userfuehrung beginnt mit Aufgabe, Hierarchie und naechster Aktion

**Beobachtung:** Etablierte Usability-Heuristiken fordern sichtbaren Systemstatus, Uebereinstimmung mit der Sprache der Nutzenden, Kontrolle und Rueckweg, Konsistenz mit Plattformstandards, Fehlervermeidung und Wiedererkennen statt Erinnern. Die WordPress-Admin-Roadmap nennt visuelle Klarheit, geringere kognitive Last, bessere Workflows, gute Defaults, Dichte, Usability und Accessibility als Ziele.

**Auswirkung:** Ein reines Spacing-Regelwerk kann formal konsistent und trotzdem schwer benutzbar sein. Abstaende muessen eine reale Informations- und Aufgabenhierarchie sichtbar machen.

**Skill-Anforderung:** Jede Seite benoetigt eine klar benannte Hauptaufgabe, eine erkennbare aktuelle Position, eine priorisierte naechste Aktion, logische Abschnitte, kontextnahe Hilfe und einen sicheren Rueckweg bei mehrstufigen oder destruktiven Aktionen. Dekorative Container ohne neue Beziehung sind zu vermeiden.

**Evidenz:** [Nielsen Norman Group: 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), [WordPress Admin Design](https://make.wordpress.org/core/2023/07/12/admin-design/).

### F-011: Navigation muss der Groesse der Plugin-Aufgabe entsprechen

**Beobachtung:** Das Plugin-Handbuch empfiehlt fuer ein Plugin mit nur einer Optionsseite ein Untermenue unter einem vorhandenen Top-Level-Menue wie Settings oder Tools.

**Auswirkung:** Ein eigenes Top-Level-Menue fuer eine einzelne kleine Seite verlaengert die globale Admin-Navigation und gibt dem Plugin mehr visuelles Gewicht als seiner Aufgabe entspricht.

**Skill-Anforderung:** Der Agent darf eine neue Top-Level-Navigation nur fuer ein eigenstaendiges, mehrseitiges Arbeitsgebiet mit begruendeter primaerer Nutzung empfehlen. Eine einzelne Einstellungs- oder Werkzeugseite nutzt standardmaessig den vorhandenen Core-Kontext.

**Evidenz:** [Plugin Handbook: Administration Menus](https://developer.wordpress.org/plugins/administration-menus/).

### F-012: Zustandsfuehrung und Fehlerbehandlung sind Teil des Designsystems

**Beobachtung:** WordPress bietet fuer klassische Settings `add_settings_error()`, `settings_errors()` und Admin Notices. Core-`common.js` verschiebt `div.updated`, `div.error` und `div.notice`, sofern sie nicht `.inline` tragen, hinter `.wp-header-end`; ersatzweise wird der erste Titel in `.wrap` verwendet. `.below-h2` ist nur ein veralteter Kompatibilitaetsname. Fuer React-Oberflaechen existieren Notice- und Snackbar-Muster; Snackbars sind fuer kurzlebige, niedrig priorisierte Meldungen gedacht, waehrend wichtigere Meldungen als Notice erscheinen sollen. WCAG 2.2 verlangt textliche Fehleridentifikation, sichtbare Labels oder Anweisungen und programmatisch erkennbare Statusmeldungen.

**Auswirkung:** Ohne Zustandsvertrag wissen Nutzende nach Speichern, Laden oder Fehlern nicht, was geschehen ist oder wie sie fortfahren koennen. Ein nur farblicher Zustand oder eine verschwindende kritische Meldung ist unzureichend.

**Skill-Anforderung:** Der Skill muss mindestens Initial-, Loading-, Empty-, Success-, Error-, Disabled- und Permission-State dort definieren, wo sie fuer den Flow auftreten. Classic-Seiten setzen Seitentitel und `.wp-header-end` in Core-kompatibler Reihenfolge. Inline-Fehler bleiben mit `.inline` beim Feld und verwenden nicht `.below-h2`; seitenweite Ergebnisse verwenden verschiebbare Core Notices. Niedrig priorisierte bestaetigende React-Rueckmeldungen duerfen Snackbar verwenden, wenn die Information auch anderswo erreichbar bleibt. Jeder Fehler benennt Problem und naechsten Korrekturschritt, soweit bekannt.

**Evidenz:** [`add_settings_error()`](https://developer.wordpress.org/reference/functions/add_settings_error/), [`common.js` Notice-Verhalten](https://github.com/WordPress/wordpress-develop/blob/90a615f1834824d2583a43bfc698d9c710e5c094/src/js/_enqueues/admin/common.js), [WordPress Notices](https://developer.wordpress.org/block-editor/how-to-guides/notices/), [Snackbar](https://developer.wordpress.org/block-editor/reference-guides/components/snackbar/), [WCAG 2.2 Error Identification](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html), [Labels or Instructions](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html), [Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html).

### F-013: WCAG 2.2 AA ist fuer WordPress-Oberflaechen der Mindeststandard

**Beobachtung:** Die WordPress Accessibility Coding Standards erwarten fuer Code im WordPress-Oekosystem WCAG 2.2 Level AA. Reflow verlangt grundsaetzlich die Nutzung ohne Informations- oder Funktionsverlust bei einer Breite entsprechend `320 CSS px`; zweidimensional notwendige Inhalte wie Datentabellen duerfen eine lokale Ausnahme bilden. WCAG 2.2 AA verlangt ausserdem logische Focus-Reihenfolge, sichtbaren Focus, nicht verdeckten Focus und mindestens `24 x 24 CSS px` grosse Pointer-Ziele oder eine zulaessige Abstandsausnahme.

**Auswirkung:** Responsive Design darf nicht nur bei typischen Telefonbreiten getestet werden. Zoom, Tastatur, Focus, Labels, Statusmeldungen und lokale Scrollcontainer sind Teil derselben Qualitaetsgrenze.

**Skill-Anforderung:** WCAG 2.2 AA ist der Default. Der Skill muss `320px` Reflow, `24px` Mindestziel nach WCAG und die groessere WordPress-Core-Mobile-Hoehe von `40px` korrekt auseinanderhalten. Datentabellen duerfen lokal horizontal scrollen; die gesamte Admin-Seite darf dadurch nicht zweidimensional scrollen.

**Evidenz:** [WordPress Accessibility Coding Standards](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/accessibility/), [WCAG 2.2 Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html), [Focus Order](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html), [Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum).

### F-014: Der Skill muss Scoville UI steuern koennen, aber ohne diese Abhaengigkeit funktionieren

**Beobachtung:** Der Nutzer verlangt einen standalone nutzbaren WordPress-Backend-Skill und optional eine konfliktfreie Komposition mit Scoville UI. ADR-0002 weist dem WordPress-Skill die plattformspezifische Tatsachen- und Regelhoheit zu; allgemeine UI-Pruefungen duerfen nur innerhalb dieser Grenzen ergaenzen.

**Auswirkung:** Bei gemeinsamer Nutzung muss klar sein, welcher Skill welche Entscheidung besitzt. Eine harte Abhaengigkeit wuerde den WordPress-Skill dagegen unnoetig unbrauchbar machen, wenn Scoville UI nicht installiert oder nicht aktiv ist.

**Skill-Anforderung:** Der WordPress-Backend-Skill ist standalone vollstaendig. Wenn Scoville UI ebenfalls aktiv ist, besitzt der WordPress-Skill WordPress-spezifische Komponenten, Defaults, Tokens, Spacing, Admin-Shell und CSS-Ausnahmen. Scoville UI besitzt die verbleibende Aufgabenfuehrung, Hierarchie, Zustandsvollstaendigkeit, Accessibility- und Renderpruefung, ohne die WordPress-Eigentuemer zu ueberschreiben.

### F-015: Internationalisierung ist ein String-, Runtime- und Layoutvertrag

**Beobachtung:** Das Plugin-Handbuch verlangt eine Textdomain, die dem kleingeschriebenen Plugin-Slug mit Bindestrichen entspricht. Nutzergerichtete PHP- und JavaScript-Strings muessen mit WordPress-gettext-Funktionen ausgezeichnet werden; dazu gehoeren auch ARIA-, Screenreader- und Alternativtexte. Die Textdomain muss literal sein. Vollstaendige Phrasen, Pluralformen, Kontext, Positionsplatzhalter und unmittelbar vorangestellte `translators:`-Kommentare erhalten uebersetzbare Grammatik. JavaScript benoetigt `wp-i18n` beziehungsweise `@wordpress/i18n` und `wp_set_script_translations()` nach Registrierung der Script-Handle. Eigene JavaScript-Uebersetzungen benoetigen den dokumentierten PO-zu-JSON- und Handle-/Pfad-Workflow. Uebersetzungen gelten als nicht vertrauenswuerdig und werden am Ausgabekontext escaped. WordPress empfiehlt ausserdem, mit einer Verdopplung der Stringlaenge zu rechnen.

**Auswirkung:** i18n kann nicht nach der UI-Implementierung als reine Sprachdatei ergaenzt werden. Verkettete Strings, variable Domains, fehlende JS-Anbindung, feste Breiten oder Links/Rechts-CSS koennen sonst nicht verlaesslich uebersetzt oder responsive dargestellt werden.

**Skill-Anforderung:** Jede nutzergerichtete UI-Zeichenkette in PHP und JavaScript ist extrahierbar. Der Skill verlangt eine gemeinsame literale Textdomain, vollstaendige Phrasen, Positionsplatzhalter, Plural/Kontext, `translators:`-Kommentare und kontextgerechtes Escaping. Datums- und Zahlenwerte verwenden `wp_date()`, `number_format_i18n()` beziehungsweise `dateI18n` aus `@wordpress/date`. Clientseitige locale-formatierte Zahlen werden in der Baseline serverformatiert; eine JS-Alternative braucht eine eigene Quelle, Locale-Zuordnung und Browserpruefung. Quellen werden mit `wp i18n make-pot` in POT extrahiert; eine dagegen gepflegte Test-PO wird mit `wp i18n make-mo` in ein ladbares MO kompiliert und der Plugin-Sprachpfad bei `init` mit `load_plugin_textdomain()` registriert. `wp i18n make-json --no-purge` erzeugt aus der PO die Test-JSON-Datei. Browser-Assertions beweisen nach reproduzierbarem Locale-Wechsel je einen wirklich uebersetzten PHP- und React-String. Gerenderte Faelle decken Textverdopplung, lange deutsche Labels, mindestens eine RTL-Sprache und locale-abhaengige Formate ab.

**Evidenz:** [How to Internationalize Your Plugin](https://developer.wordpress.org/plugins/internationalization/how-to-internationalize-your-plugin/), [Internationalization Guidelines](https://developer.wordpress.org/apis/internationalization/internationalization-guidelines/), [Internationalization Security](https://developer.wordpress.org/plugins/internationalization/security/), [JavaScript Internationalization](https://developer.wordpress.org/block-editor/how-to-guides/internationalization/), [`wp_set_script_translations()`](https://developer.wordpress.org/reference/functions/wp_set_script_translations/), [`load_plugin_textdomain()`](https://developer.wordpress.org/reference/functions/load_plugin_textdomain/), [`wp i18n make-pot`](https://developer.wordpress.org/cli/commands/i18n/make-pot/), [`wp i18n make-mo`](https://developer.wordpress.org/cli/commands/i18n/make-mo/), [`wp i18n make-json`](https://developer.wordpress.org/cli/commands/i18n/make-json/), [`wp_date()`](https://developer.wordpress.org/reference/functions/wp_date/), [`number_format_i18n()`](https://developer.wordpress.org/reference/functions/number_format_i18n/), [`@wordpress/date`](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-date/).

## Abgeleitete normative Spacing-Matrix

Die folgende Matrix ist eine **Skill-Norm**, keine offizielle WordPress-HIG. Sie schliesst die in F-001 und F-004 festgestellte semantische Luecke. Die Token-Namen duerfen nur im gebuendelten WPDS-Pfad verwendet werden, wenn der oeffentliche Token-Stylesheet geladen ist. Im Classic- oder Core-Components-Pfad steuert dieselbe Beziehung die Auswahl vorhandener Defaults/APIs oder einer ausdruecklich als Skill-Norm markierten lokalen Ausnahme.

| Semantische Beziehung | Gap | WPDS-Gap-Name, falls bereitgestellt | Regel |
| --- | ---: | --- | --- |
| Control zu Help-, Status- oder Error-Text | 4px | `xs` | Engste lesbare Beziehung; keine weitere Child-Margin |
| Heading zu seinem eigenen Einleitungstext | 8px | `sm` | Direkte Beschreibung derselben Region; Heading- und Absatzmargins im Stack neutralisieren |
| Direkt zusammengehoerige Controls oder Icon und Label | 8px | `sm` | Ein gemeinsamer Bedienblock |
| Elemente innerhalb einer Feldgruppe | 12px | `md` | Label, Control-Gruppe und ergaenzende Aktion |
| Zusammengehoerige Einstellungsgruppen | 16px | `lg` | Normaler lokaler Abschnittsrhythmus |
| Eigenstaendige Sektionen | 24px | `xl` | Default zwischen inhaltlich abgeschlossenen Sektionen |
| Grosse Seitenregionen | 32px | `2xl` | Header, Hauptinhalt, gesonderte Nebenregion |
| Sehr starke Trennung | 40px | `3xl` | Ausnahme, nicht Standard zwischen allen Bloecken |

### Flow-Eigentum

1. Der direkte Parent besitzt den Abstand zwischen Geschwistern.
2. Ein Element besitzt keinen Aussenabstand, wenn sein Parent bereits den Flow per `gap` steuert.
3. Verschachtelte Stacks verwenden die semantisch passende Ebene; sie erben den Parent-Gap nicht blind.
4. Visuelle Container wie Card oder Panel steuern Innenpadding, nicht den Abstand zur Nachbarsektion.
5. Ausgeblendete oder leere Elemente duerfen keine Abstandsluecke hinterlassen.
6. Fehler-, Hilfe- und Statusmeldungen bleiben bei dem Control, dessen Zustand sie erklaeren.
7. Im klassischen Settings-API-Pfad gelten diese Regeln nur innerhalb Plugin-eigener Komponenten; Core bleibt Owner der Form-Zeile.
8. In hybriden Seiten besitzt jede DOM-Region genau einen Runtime- und Spacing-Owner; das gilt auch fuer Portale und Overlays.
9. Core besitzt bei der typischen React-in-`.wrap`-Einbettung `#wpcontent`, `.wrap`, Seitentitel, `.wp-header-end` und seitenweite Notices; der Plugin-Root besitzt nur seinen inneren Teilbaum.
10. `.form-table` und ein plugin-eigener Gap-Stack duerfen nicht denselben Teilbaum besitzen.
11. Im Core-Components-Pfad besitzen spezialisierte Komponenten ihre interne Rhythmik. Neue generische vertikale Gruppen verwenden fuer alle Werte von `experimental_components_policy` `Flex` mit `direction="column"`, `align="stretch"`, `justify="flex-start"`, `wrap={ false }`, `expanded={ true }` und `gap` `1/2/3/4/6/8/10`. Bestehende experimentelle Teilbaeume bleiben ihr Owner; neues lokales Stack-CSS benoetigt eine belegte `Flex`-Luecke.

## Abgeleiteter Responsive-Vertrag

Dieser Vertrag ist ebenfalls eine Skill-Norm und muss im Skill als solche gekennzeichnet werden.

1. **Intrinsisch zuerst:** Grid und Flex muessen ohne feste Seitenbreite umbrechen koennen. Lange Labels, lokalisierte Texte und Notices duerfen keine horizontale Seite erzeugen.
2. **Core-Grenze respektieren:** Bei `<=782px` werden mehrspaltige Form- und Aktionslayouts einspaltig, sofern nicht jedes Element nachweislich bedienbar und lesbar bleibt.
3. **Mobile Controls:** Typische Texteingaben und Selects erhalten mindestens die von Core verwendete Hoehe von `40px`; Dichte-Tokens duerfen Touch-Ziele nicht verkleinern.
4. **Shell nicht verdoppeln:** Klassische Seiten uebernehmen `.wrap` und Core-Padding. Moderne Vollseiten beginnen bei `16px` Block- und `24px` Inline-Padding; engeres Inline-Padding muss explizit definiert und getestet sein.
5. **Reading order:** Visuelle Umordnung darf DOM-, Tastatur- und Screenreader-Reihenfolge nicht widersprechen.
6. **Actions:** Primaeraktionen bleiben sichtbar, Nebenaktionen duerfen umbrechen oder in ein eindeutig beschriftetes Menue wechseln. Kein horizontales Scrollen fuer normale Formaktionen.
7. **Data views:** Breite Datentabellen erhalten eine bewusst dokumentierte Small-Screen-Darstellung oder einen lokalen Scrollcontainer; blosses Abschneiden oder horizontales Scrollen der gesamten Seite ist keine responsive Strategie.
8. **Logische Eigenschaften:** Plugin-eigenes CSS verwendet nach Moeglichkeit `margin-inline`, `padding-inline`, `block-size` und `inline-size`, damit RTL und unterschiedliche Admin-Shellbreiten nicht durch Links/Rechts-Annahmen brechen.
9. **Reflow-Untergrenze:** Nicht ausgenommene Inhalte bleiben bei `320 CSS px` und bei entsprechendem Zoom ohne Informations- oder Funktionsverlust in einer Scrollrichtung nutzbar.
10. **i18n-Stress:** Textverdopplung, lange deutsche Labels, eine RTL-Sprache und locale-abhaengige Werte sind regulaere Layoutfaelle, keine spaete Sonderpruefung.
11. **Pruefmatrix:** Die WordPress-7.0-Fixture wird mindestens bei `783`, `782`, `600`, `390` und `320 CSS px` sowie `1280px` bei `400%` Zoom oder gleichwertigem Reflow geprueft. Fuer nicht ausgenommene Seitenshells gilt `document.documentElement.scrollWidth <= window.innerWidth`; notwendiger Tabellen-Overflow bleibt lokal.

## CSS-Eigentums- und Ausnahmevertrag (Skill-Norm)

Der Agent bestimmt zuerst Runtime- und DOM-Owner, arbeitet dann diese Reihenfolge ab und beendet die Suche am ersten geeigneten Owner:

1. Vorhandenes semantisches HTML, WordPress-API und Core-Admin-Markup.
2. Vorhandene Core-Klasse oder WordPress-Komponente mitsamt Default-CSS.
3. Ein semantischer Token, den der geladene oeffentliche Runtime-Stylesheet tatsaechlich bereitstellt.
4. Plugin-eigene Komposition vorhandener Primitive mit `gap`, Grid/Flex und logischen Eigenschaften.
5. Neue, eng gescopte CSS-Regel nur bei nachgewiesener Luecke.

Eine CSS-Ausnahme muss im Agentenergebnis kurz belegen:

- welche WordPress-Option geprueft wurde;
- warum Default-CSS oder Token das konkrete Layout nicht ausdruecken kann;
- welchen kleinsten Plugin-eigenen Scope die Regel besitzt;
- welche Core-/Komponenten-Defaults oder tatsaechlich bereitgestellten Tokens sie weiterhin verwendet;
- wie Reflow, RTL, Focus, Zoom und betroffene Zustände geprueft werden.

Im WPDS-Pfad duerfen semantische `--wpds-*` nur konsumiert werden; Plugin-Code definiert, ueberschreibt oder imitiert diesen Namespace nicht. Primitive WPDS-Tokens sind intern. Classic/Core erbt Core-Rhythmik; React/Core Components verwendet Komponenten-Defaults und APIs. Eine isolierte Plugin-Luecke darf eine plugin-eigene Custom Property oder eine als **Skill-Norm** markierte Zahl verwenden.

Nicht erlaubt sind globale Overrides von `wp-admin`, das Kopieren grosser Core-CSS-Bloecke, nachgeahmte `--wpds-*`, neue nackte Abstandswerte trotz geeignetem Owner, der Nachbau vorhandener Buttons/Inputs/Notices nur fuer eine andere Optik und `!important` ohne dokumentierten unvermeidbaren Integrationskonflikt. Eigene Farben sind grundsaetzlich ausgeschlossen; falls eine echte Produktfunktion eine Ausnahme erfordert, benoetigt sie einen dokumentierten WCAG-AA-Kontrastnachweis.

## Basismodell fuer Userfuehrung (Skill-Norm)

### Aufgaben- und Informationshierarchie

1. Die Seite benennt in genau einem primaeren Titel, wo sich die Person befindet.
2. Ein kurzer Kontext erklaert nur, was vor der ersten Entscheidung noetig ist.
3. Die primaere Aufgabe und ihre naechste Aktion sind ohne Scroll-Suche erkennbar, soweit der Seitentyp das erlaubt.
4. Abschnitte folgen der Aufgabenreihenfolge statt interner Daten- oder Code-Struktur.
5. Verwandte Controls stehen naeher beieinander als unabhaengige Gruppen; die normative Spacing-Matrix macht diese Beziehung sichtbar.
6. Fortgeschrittene oder seltene Einstellungen duerfen progressiv offengelegt werden, bleiben aber auffindbar und behalten ihren Zustand.

### Aktionen und Sicherheit

1. Eine Region besitzt hoechstens eine visuell primaere Aktion.
2. Sekundaere Aktionen konkurrieren nicht gleich stark; destruktive Aktionen sind semantisch und raeumlich getrennt.
3. Mehrstufige oder destruktive Flows zeigen Konsequenz, Rueckweg und gegebenenfalls Wiederherstellung oder Bestaetigung.
4. Lade- und Speicherzustand verhindern unbeabsichtigte Doppelaktionen, ohne Status oder Focus verschwinden zu lassen.

### Formulare

1. Jedes Eingabefeld besitzt ein dauerhaft sichtbares, programmatisch verknuepftes Label.
2. Help-Text erklaert Format, Folge oder Grenze vor der Fehleingabe und steht in der engsten `4px`-Beziehung zum Control; im WPDS-Pfad entspricht das bereitgestelltem `xs`, im Classic-Pfad bleibt Core Owner der `.description`-Rhythmik.
3. Validierung erhaelt eingegebene Werte, kennzeichnet das konkrete Feld und beschreibt den Fehler in Text.
4. Nach einem fehlgeschlagenen Submit fuehrt ein Summary oder Focus-Management zur ersten sinnvollen Korrekturstelle, ohne eine verwirrende Focus-Reihenfolge zu erzeugen.
5. Abhaengige Controls zeigen Ursache und Zustand; blosses Deaktivieren ohne Erklaerung ist zu vermeiden.

### Systemzustand und Orientierung

1. Jede gestartete Aktion liefert zeitnah Rueckmeldung.
2. Loading, Empty, Success, Error, Disabled und Permission werden nur dort vorgesehen, wo der reale Flow sie kennt, dann aber vollstaendig.
3. Seitenweite Meldungen verwenden WordPress Notices; feldbezogene Meldungen bleiben inline; Snackbars sind nur fuer niedrig priorisierte, nicht exklusive Information.
4. Ein Zustandswechsel wird nie ausschliesslich durch Farbe, Position oder kurzlebige Animation vermittelt.
5. Struktur bleibt ueber Zustandswechsel stabil genug, dass Nutzer die Orientierung behalten.

## Internationalisierungsvertrag

1. Die Textdomain ist ein literaler String, entspricht dem Plugin-Slug, ist kleingeschrieben und verwendet Bindestriche statt Unterstrichen oder Leerzeichen.
2. Jede nutzergerichtete PHP-Zeichenkette einschliesslich ARIA-/Screenreader-/Alternativtext verwendet die passende WordPress-gettext-Funktion; Ausgabe wird am HTML-, Attribut- oder sonstigen Zielkontext escaped.
3. Jede nutzergerichtete JavaScript-Zeichenkette verwendet `@wordpress/i18n` beziehungsweise die registrierte `wp-i18n`-Abhaengigkeit. `wp_set_script_translations()` wird erst nach Registrierung der Script-Handle mit derselben Textdomain und explizitem Sprachdateipfad aufgerufen.
4. Vollstaendige Phrasen werden uebersetzt; String-Verkettung und uebersetzte Satzfragmente sind unzulaessig. Mehrere Werte verwenden nummerierte Positionsplatzhalter, damit Uebersetzungen ihre Reihenfolge aendern koennen.
5. Pluralformen verwenden `_n()`/`_nx()` beziehungsweise die JavaScript-Pendants; mehrdeutige Begriffe erhalten Kontext mit `_x()`/`_nx()`.
6. Nicht offensichtliche Platzhalter oder Bedeutungen erhalten einen unmittelbar vor der gettext-Anweisung stehenden, kleingeschriebenen `translators:`-Kommentar.
7. URLs, Markup und variable Daten werden nicht als frei uebersetzbarer Bestandteil eingebettet, wenn sichere Platzhalter oder getrenntes Markup den Fall ausdruecken.
8. PHP formatiert Datum/Zeit und Zahlen mit WordPress-locale-APIs wie `wp_date()` und `number_format_i18n()`; JavaScript verwendet fuer lokalisierte Datumswerte `dateI18n` aus `@wordpress/date`. Locale-formatierte Client-Zahlen kommen in der Baseline serverformatiert; eine JS-Alternative benoetigt eine separat belegte Locale-Zuordnung und Browserpruefung.
9. Nach dem JavaScript-Build extrahiert `wp i18n make-pot . languages/<slug>.pot --domain=<slug> --exclude=src` PHP und den registrierten Build-Pfad in ein POT. Eine Test-PO namens `<slug>-<locale>.po` wird dagegen gepflegt, mit `wp i18n make-mo` zu `languages/<slug>-<locale>.mo` kompiliert und der Plugin-Sprachpfad bei `init` ueber `load_plugin_textdomain()` registriert.
10. Dieselbe PO wird mit `wp i18n make-json --no-purge` in JSON ueberfuehrt. Der Golden-Fall fixiert entweder `<domain>-<locale>-<handle>.json` oder korrekte PO-Dateireferenzen zum registrierten Build-Pfad fuer den MD5-Namen; `src/`-Referenzen bei registriertem `build/`-Script sind unzulaessig.
11. Nach reproduzierbarem Site-/Admin-User-Locale-Wechsel beweisen Browser-Assertions mindestens einen tatsaechlich uebersetzten PHP- und React-String. Fest eingebaute Teststrings gelten nicht als Runtime-Beweis.
12. Textverdopplung, lange deutsche Labels, mindestens eine RTL-Sprache und locale-abhaengige Zahlen/Datumswerte sind Teil der Spacing-, Responsive- und Render-Validierung.

## Kompositionsvertrag mit Scoville UI

- Der WordPress-Backend-Skill hat keine technische oder instruktionale Laufzeitabhaengigkeit von Scoville UI.
- Ist nur der WordPress-Skill aktiv, muss er UI-Pfad, Plattform-Owner, Spacing, Responsive Flow, Basis-Userfuehrung, States und Accessibility selbst ausreichend abdecken.
- Sind beide Skills aktiv, ist der WordPress-Skill der kanonische Owner fuer WordPress-Backend-Designsystem, Default-CSS, Komponentenwahl, Tokens, Spacing und CSS-Ausnahmen.
- Scoville UI darf die offene, produktbezogene UI-Qualitaet verbessern, aber keine parallelen Pixelwerte, Breakpoints, Komponenten oder visuelle Sprache einfuehren.
- Scoville UI kann gerenderte Hierarchie, Aufgabenfluss, Zustände, Accessibility und Responsivitaet pruefen; bei Konflikten gilt der hoehere WordPress-/Accessibility-Owner.
- Der WordPress-Skill muss ohne installierten, geladenen oder anwendbaren Scoville-UI-Skill dieselbe plattformspezifische Entscheidung liefern.

## Agenten-Anti-Patterns

- Frontend-`theme.json`, `blockGap` oder Theme-Spacing als Backend-Quelle verwenden.
- Abgeleitete Skill-Normen als "offizielle WordPress-Vorgabe" ausgeben.
- Gap- und Padding-Tokens wegen gleicher Namen gleichsetzen.
- `compact` automatisch mit Mobile gleichsetzen.
- React automatisch mit experimentellem WPDS gleichsetzen.
- Eine fehlende Projekt-Policy als stillen Opt-in fuer neue experimentelle Komponenten behandeln.
- Bei `deny` oder `unknown` eine vorhandene nicht-experimentelle Core-Komponente ueberspringen und direkt eigenes Stack-CSS schreiben.
- `--wpds-*` auf einer Seite definieren, ueberschreiben oder nachahmen, auf der der oeffentliche Token-Stylesheet sie nicht liefert.
- `.form-table` zusaetzlich mit einem globalen Stack-Gap versehen.
- Einzelnen Kindern willkuerliche `margin-bottom`-Werte geben, obwohl der Parent den Flow steuern kann.
- Eine feste Universalbreite fuer Settings, Dashboards und Tabellen verwenden.
- Responsive nur als kleinere Abstaende behandeln, ohne Reflow, Control-Groesse und Reading Order zu pruefen.
- Experimentelle Pakete als global vorhandene `window.wp`-API voraussetzen.
- Vorhandene WordPress-Buttons, Inputs, Notices oder Tabellen visuell neu implementieren, obwohl Core oder `@wordpress/components` den Fall abdeckt.
- Globales Plugin-CSS gegen `.wp-admin`, `.wrap`, `.form-table` oder Core-Control-Klassen richten, um ein lokales Layoutproblem zu loesen.
- Mehrere gleich starke Primaeraktionen, dekorative Card-Verschachtelung oder versteckte Statuswechsel als Ersatz fuer klare Userfuehrung einsetzen.
- Nutzergerichtete Strings verketten, eine variable Textdomain verwenden, JavaScript-Uebersetzungen nicht an die Script-Handle binden oder uebersetzte Ausgabe ungeprueft als vertrauenswuerdig behandeln.
- Nur POT-Extraktion oder fest eingebaute deutsche/RTL-Teststrings als Beweis fuer geladene PHP-/JavaScript-Uebersetzungen ausgeben.
- Eine WordPress-Locale ohne belegte Regel in ein JavaScript-BCP-47-Locale umformen.
- Feste Breiten oder Links/Rechts-Eigenschaften verwenden, die lange Uebersetzungen oder RTL brechen.

## Erforderliche Bestandteile des geplanten Skills

1. Klare Trigger und Ausschluesse fuer WordPress-Plugin-Backend statt Frontend/Block-Theme.
2. Zweiachsen-Klassifikation fuer Admin-Flaeche und Runtime-Owner mit Support-Matrix.
3. Quellenledger mit Ref/SHA, Paketversion, Abrufdatum, Supportstatus, Revalidierungstrigger und Kennzeichnung `Core`, `WPDS`, `WCAG` oder `Skill-Norm`.
4. Getrennte Tabellen fuer Gap, Padding und Dichte.
5. Normative Vertical-Flow-Matrix und Flow-Eigentumsregeln.
6. CSS-Eigentumsleiter mit Default-CSS-first-Regel und strengem Ausnahmeformat.
7. Page-Shell-, Settings-, Section-, Card-, Toolbar-, Form- und Data-View-Muster.
8. Basisregeln fuer Navigation, Aufgabenhierarchie, Aktionen, Formulare, States, Feedback und Recovery.
9. Responsive Vertrag einschliesslich `782px`, `320px` Reflow, intrinsischem Layout, RTL und lokalem Data-View-Overflow.
10. Beispiele fuer PHP/Core, React/Core Components, gebuendeltes WPDS und Hybrid mit Owner je DOM-Region.
11. Anti-Patterns und Entscheidungsbaum fuer gemischte Seiten, Portale und Overlays.
12. Standalone-Vertrag und optionale Komposition mit Scoville UI ohne Abhaengigkeit.
13. Verbindlicher PHP-/JavaScript-i18n-Vertrag einschliesslich Textdomain, PO/POT/JSON, Runtime-Uebersetzung, Escaping, Plural/Kontext, locale-Formaten, Textverdopplung und RTL.
14. Vor der Skill-Formulierung eingefrorene Routing-, Experiment-Policy-, Spacing-, CSS-Ownership-, UI-Guidance-/Accessibility- und i18n-Golden-Faelle.
15. Reproduzierbare getrennte WordPress-7.0-Single-Site- und WordPress-7.0.x-Multisite-Fixtures mit exakt gepinnten npm-Paketen, Lockfile, `npm ci`, nativem XAMPP-Manifest samt read-only Validator, geladenem oeffentlichem WPDS-Token-Stylesheet und Network-Admin-Fall.
16. Repository-freier Fresh-Agent-Smoke-Test sowie gerenderte Validierungsrubrik fuer `783/782/600/390/320px`, Zoom, Tastatur, nicht verdeckten Focus, Target Size, Kontrast, Labels, Fehler-/Statussemantik und lokalisierte Inhalte.

## Auditgrenzen

- Keine Live- oder Screenshot-Pruefung einer konkreten Plugin-Seite.
- Keine vollstaendige Farb-, Typografie-, Icon- oder Navigationsspezifikation. Core-/WPDS-Farben bleiben Owner; WCAG-AA-Kontrast bleibt trotzdem Pflicht.
- Keine Aussage, dass experimentelle WPDS-Pakete in einer spaeteren WordPress-7.x-Version unveraendert bleiben.
- Keine universelle Empfehlung fuer Content-Max-Width, Tabellenersatz oder Navigationsarchitektur ohne konkreten Seitentyp.
- Der Audit prueft Quellen und leitet einen Skill-Vertrag ab; er ist noch nicht der Skill selbst.

## Auditfazit

Die Quellen reichen aus, um einen konsistenten Skill zu bauen, wenn der Skill Admin-Flaeche und Runtime-Owner getrennt routet und seine eigene normative Schicht offenlegt. Die wichtigste Invariante lautet: **Core besitzt Legacy-Shell und native Form-Rhythmik; ein Plugin besitzt nur seine abgegrenzten DOM-Regionen; jeder Flow hat genau einen Parent-Owner; WPDS-Tokens existieren nur, wenn ihr oeffentlicher Stylesheet am Render-Root geladen ist.** Responsive und mehrsprachige Konsistenz entsteht aus intrinsischem Reflow, der Core-Grenze von `782px`, logischen Eigenschaften und getesteter Textexpansion/RTL, nicht aus pauschal kleineren Abstaenden.
