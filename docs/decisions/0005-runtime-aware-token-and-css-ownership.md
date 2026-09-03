---
format_version: 1
id: ADR-0005
status: superseded
created: 2026-09-03
accepted: 2026-09-03
scope: skill/css-ownership
supersedes: ADR-0003
superseded_by: ADR-0007
---

# Token- und CSS-Ownership an den Runtime-Owner binden

## Decision

Der Skill verpflichtet Agenten je DOM-Region auf folgende Reihenfolge: vorhandene WordPress-API und semantisches Core-Markup, vorhandene Core-Klasse oder WordPress-Komponente mit Default-CSS, ein im gewaehlten Runtime-Pfad tatsaechlich bereitgestellter semantischer Token, plugin-eigene Komposition dieser Primitive und erst als letzte Ausnahme eine neue eng gescopte CSS-Regel.

Semantische `--wpds-*`-Variablen duerfen nur konsumiert werden, wenn der ausgewaehlte und geladene WPDS-Provider oder dessen Stylesheet sie bereitstellt. Der Skill und Plugin-Code duerfen `--wpds-*` weder definieren, ueberschreiben noch nachahmen. Primitive WPDS-Tokens sind Implementierungsdetails. Classic/Core erbt zuerst die Core-Rhythmik. React mit `@wordpress/components` verwendet zuerst Komponenten-Defaults und APIs; `__experimentalVStack` bleibt experimentell und sein `spacing` ist ein Multiplikator des 4-px-Rasters. Eine unvermeidbare isolierte Plugin-Luecke darf eine als **Skill-Norm** markierte Zahl oder eine plugin-eigene Custom Property verwenden, aber niemals als WordPress-Token ausgeben.

## Problem

Nicht jeder WordPress-Backend-Pfad laedt WPDS-Tokens. Die pauschale Forderung nach WordPress-Gap-Tokens kann Agenten dazu bringen, nicht vorhandene Variablen zu erfinden oder experimentelle Styles in klassische Seiten einzuschleusen.

## Drivers

- Der Nutzer verlangt WordPress-Defaults und moeglichst wenig eigenes CSS.
- Token-Verfuegbarkeit ist runtime- und providerabhaengig.
- Core-, Components- und WPDS-Pfade besitzen unterschiedliche Stabilitaets- und Spacing-Vertraege.
- Echte Layoutluecken muessen weiterhin klein, lokal und nachvollziehbar geschlossen werden koennen.

## Considered alternatives

1. `--wpds-*` global fuer alle Pfade definieren: einheitliche Namen, aber erfundene und konflikttraechtige Plattformautoritaet.
2. Nur nackte Pixelwerte verwenden: runtime-unabhaengig, aber keine Nutzung vorhandener semantischer Vertrage.
3. WPDS auf jeder Plugin-Seite laden: einheitlicher Provider, aber experimentelle Abhaengigkeit und unnoetiger Eingriff in Classic-Seiten.

## Consequences

- Jede Empfehlung nennt Runtime-Owner, Token-Provider und CSS-Owner.
- Der Skill braucht getrennte Tabellen fuer Core-Beobachtungen, Components-APIs, WPDS-Tokens und Skill-Normen.
- CSS-Ausnahmen muessen die geprueften Owner, den kleinsten Scope und Responsive-/Accessibility-Proof dokumentieren.
- Globale `wp-admin`-Overrides, kopierte Core-CSS-Bloecke und nachgeahmte `--wpds-*`-Variablen sind unzulaessig.

## Confirmation

Die Entscheidung ist umgesetzt, wenn Golden-Faelle fuer Classic, Core Components, WPDS und Hybrid jeweils den erwarteten Owner und die erlaubte Ausdrucksform nennen, nicht geladene `--wpds-*`-Variablen verbieten und jede Custom-CSS-Ausnahme begruenden.

## Revisit when

WordPress eine stabile, global dokumentierte Admin-Token- oder Layout-API bereitstellt.
