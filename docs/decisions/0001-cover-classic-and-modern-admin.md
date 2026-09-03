---
format_version: 1
id: ADR-0001
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: skill/ui-paths
---

# Admin-Flaeche und Runtime-Owner getrennt klassifizieren

## Decision

Der Skill klassifiziert jede Aufgabe auf zwei unabhaengigen Achsen: Admin-Flaeche und Runtime-/Komponenten-Owner. Die Flaeche bestimmt, ob der Skill in Version 1 zustaendig ist; der Runtime-Owner bestimmt Komponenten, CSS, Tokens und Spacing-Verantwortung.

Unterstuetzt werden plugin-eigene Single-Site-Settings-/Tool-Seiten, Workflow-/Dashboard-Seiten, Data Views sowie plugin-eigene Network-Admin-Seiten mit explizitem Multisite-Kontext. Separat geroutet oder ausgeschlossen werden Block-Editor-Sidebars und SlotFills, Editor-Canvas, Post-Metaboxen, Dashboard-Widgets, Profilfelder, Erweiterungen bestehender Core-Listen/-Screens und Oberflaechen innerhalb eines anderen Plugins.

Die Runtime-Owner sind:

1. PHP/Core-Markup mit Core-Default-CSS;
2. React mit Core-bereitgestelltem `@wordpress/components`;
3. gebuendeltes experimentelles WPDS aus `@wordpress/ui`, `@wordpress/theme` und `@wordpress/admin-ui`;
4. hybrid mit explizitem Owner je DOM-Region einschliesslich Portalen und Overlays.

Der klassische Pfad ist die stabile Baseline. Experimentelles WPDS ist ein bewusster, versionsgebundener Opt-in. React allein bedeutet nicht WPDS. Bei einer typischen hybriden Seite besitzt Core `#wpcontent`, `.wrap`, den Seitentitel, `.wp-header-end` und seitenweite Notices; der Plugin-Root besitzt nur seinen inneren Teilbaum. `.form-table` und ein plugin-eigener Gap-Stack duerfen nicht denselben Teilbaum besitzen.

## Problem

WordPress 7.0 besitzt nicht bloss die Wahl Classic oder React. React kann stabile Core-Komponenten oder experimentelle WPDS-Pakete verwenden, und dieselbe Plugin-Seite kann mehrere Owner enthalten. Ohne getrennte Flaechen- und Runtime-Klassifikation entstehen falsche Stabilitaetsannahmen, doppelte Abstaende und Eingriffe in fremd besessene DOM-Regionen.

## Drivers

- Der Skill soll fuer WordPress-Plugin-Backends allgemein einsetzbar sein.
- Spacing und Vertical Content Flow muessen fuer Agenten eindeutig sein.
- Offizielle Core-Fakten und projektdefinierte Normen muessen unterscheidbar bleiben.
- Das Ergebnis muss responsive und mit bestehenden `wp-admin`-Seiten kompatibel sein.
- Experimentelle APIs duerfen nicht als stabile globale Runtime behandelt werden.

## Considered alternatives

1. Nur klassisches `wp-admin`: stabiler und kleiner, aber unzureichend fuer React-Plugin-Oberflaechen.
2. React mit WPDS gleichsetzen: einfacher Entscheidungsbaum, aber sachlich falsch, weil `@wordpress/components` und experimentelles WPDS unterschiedliche Vertraege besitzen.
3. Alle Admin-Einbettungen in Version 1 unterstuetzen: groessere Abdeckung, aber keine einheitliche Shell- oder Ownership-Grenze.
4. Nur modernes WPDS: konsistenteres Token-Modell, aber fuer WordPress 7.0 experimentell und nicht global verfuegbar.

## Consequences

- Der Skill benoetigt eine verpflichtende Zweiachsen-Klassifikation und eine Support-Matrix.
- Beispiele, Spacing-Regeln und Responsive-Verhalten werden je Runtime-Owner getrennt dokumentiert.
- Gemeinsame Skill-Normen duerfen nur auf abgegrenzte Plugin-Komponenten angewendet werden.
- Portale, Overlays und Hybrid-Grenzen benoetigen einen Owner.
- Die Quellen- und Wartungsflaeche ist groesser als bei einem Classic-only-Skill.
- Eine spaetere Stabilisierung von WPDS kann eine Neubewertung der Baseline erfordern.

## Confirmation

Die Entscheidung ist umgesetzt, wenn ein eingefrorener Routing-Korpus fuer jeden Fall `surface`, `support_status`, `runtime_owner`, `shell_owner`, `spacing_owner`, Quellen und verbotene Empfehlungen erwartet und alle Faelle deterministisch klassifiziert werden.

## Revisit when

`@wordpress/ui`, `@wordpress/theme` und `@wordpress/admin-ui` nicht mehr experimentell sind, WordPress eine verbindliche gemeinsame Admin-HIG veroeffentlicht oder ausgeschlossene Einbettungsflaechen in den Skill-Scope aufgenommen werden sollen.
