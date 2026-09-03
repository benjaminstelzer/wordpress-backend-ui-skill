---
format_version: 1
id: ADR-0003
status: superseded
created: 2026-09-03
accepted: 2026-09-03
scope: skill/css-ownership
superseded_by: ADR-0005
---

# WordPress-Defaults und Tokens vor eigenem CSS verwenden

## Decision

Der Skill verpflichtet Agenten auf folgende Reihenfolge: vorhandene WordPress-API und semantisches Core-Markup, vorhandene Core-Klasse oder WordPress-Komponente mit Default-CSS, vorhandener WordPress-Token, plugin-eigene Komposition dieser Primitive und erst als letzte Ausnahme eine neue eng gescopte CSS-Regel. Eigene Abstaende verwenden WordPress Gap- oder Padding-Tokens, sofern ein passender Token existiert.

## Problem

Plugin-Backends definieren haeufig eigene Buttons, Inputs, Cards, Abstaende und Responsive-Regeln, obwohl WordPress bereits passende Defaults besitzt. Dadurch entstehen inkonsistente Oberflaechen, doppelte Abstaende, globale Overrides und Wartungsprobleme nach Core-Updates.

## Drivers

- Der Nutzer hat minimale eigene CSS-Definitionen explizit verlangt.
- WordPress-Default-CSS soll die visuelle Baseline bleiben.
- WordPress Gap-Tokens sollen nackte Abstandsangaben ersetzen.
- RTL, Mobile, Focus, Zoom und Core-Updates sollen nicht durch parallele CSS-Systeme geschwaecht werden.
- Echte Layoutluecken muessen weiterhin klein und nachvollziehbar geschlossen werden koennen.

## Considered alternatives

1. Vollstaendig eigenes Plugin-Designsystem: hohe Kontrolle, aber eine parallele Sprache und grosse Wartungsflaeche.
2. Core-CSS ohne jede Ausnahme: maximale Naehe zu WordPress, aber unzureichend fuer echte plugin-spezifische Layoutkompositionen.
3. Freie Mischung von Core und Custom CSS: kurzfristig flexibel, aber ohne deterministische Ownership und schwer auditierbar.

## Consequences

- Der Skill braucht einen verpflichtenden CSS-Owner-Check vor jeder neuen Regel.
- Ausnahmen muessen Owner-Luecke, kleinsten Scope, verwendete Tokens und Responsive-/Accessibility-Proof nennen.
- Globale `wp-admin`-Overrides, kopierte Core-CSS-Bloecke und nackte Werte trotz passendem Token sind unzulaessig.
- Eigene CSS-Dateien bleiben fuer echte Komposition, Layout-Archetypen und klar begrenzte Integrationsluecken moeglich.

## Confirmation

Die Entscheidung ist umgesetzt, wenn Beispiele und Agententests zuerst Core/API/Komponenten auswaehlen, Spacing ueber WordPress-Tokens ausdruecken und jede verbleibende Custom-CSS-Regel den dokumentierten Ausnahmevertrag erfuellt.

## Revisit when

WordPress eine stabilere Admin-Komponenten- oder Layout-API bereitstellt, die heute notwendige Custom-CSS-Ausnahmen ersetzt.
