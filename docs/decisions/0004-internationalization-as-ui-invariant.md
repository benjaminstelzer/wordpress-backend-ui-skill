---
format_version: 1
id: ADR-0004
status: superseded
created: 2026-09-03
accepted: 2026-09-03
scope: skill/i18n
superseded_by: ADR-0006
---

# Internationalisierung als verbindliche UI-Invariante

## Decision

Jede vom Skill erzeugte oder gepruefte Plugin-Backend-Oberflaeche ist in PHP und JavaScript internationalisierbar. Sichtbare Strings verwenden die WordPress-i18n-APIs mit einer literalen Textdomain, die dem kleingeschriebenen Plugin-Slug mit Bindestrichen entspricht. JavaScript registriert `wp-i18n` als Abhaengigkeit und bindet die registrierte Script-Handle mit `wp_set_script_translations()` an dieselbe Textdomain.

Der Vertrag umfasst vollstaendige Phrasen statt String-Verkettung, Positionsplatzhalter, Pluralformen, Kontext, unmittelbar vorangestellte `translators:`-Kommentare, kontextgerechtes Escaping und locale-gerechte Datums- und Zahlenformatierung. Layout und Validierung muessen Textverdopplung, lange deutsche Beschriftungen, mindestens eine RTL-Sprache und locale-abhaengige Formate ohne Informations- oder Funktionsverlust abdecken. Die POT-Extraktion prueft PHP- und JavaScript-Quellen.

## Problem

Nachtraegliche Uebersetzung behebt keine dynamisch zusammengesetzten Strings, falsche Pluralformen, fehlende JavaScript-Sprachdateien oder Layouts, die bei laengeren und rechts-nach-links laufenden Texten brechen. Internationalisierung muss daher den String-, Runtime- und Layoutvertrag von Anfang an bestimmen.

## Drivers

- Der Nutzer verlangt mehrsprachige Plugin-Oberflaechen als feste Eigenschaft.
- WordPress stellt getrennte, aber aufeinander abgestimmte APIs fuer PHP und JavaScript bereit.
- Uebersetzungen sind nicht vertrauenswuerdig und muessen am Ausgabekontext escaped werden.
- Spacing, Reihenfolge, Breiten und Statusmeldungen muessen auch mit expandierendem oder RTL-Text funktionieren.

## Considered alternatives

1. Lokalisierung nach der Implementierung: geringerer Startaufwand, aber nicht verlaesslich nachruestbar.
2. Nur PHP internationalisieren: unzureichend fuer React- und hybride Oberflaechen.
3. Ein externes i18n-System als Standard: schafft eine parallele Infrastruktur und umgeht WordPress-Sprachpakete.

## Consequences

- Der Skill benoetigt konkrete PHP-, JavaScript-, Extraktions- und Layoutregeln.
- Beispiele duerfen keine unuebersetzten sichtbaren Literale oder variable Textdomains enthalten.
- i18n-Stressfaelle werden Teil der Routing-, Spacing-, Responsive- und Render-Validierung.
- Lokalisierte Datums- und Zahlenwerte verwenden WordPress-APIs statt allgemeiner sprachneutraler Formatierung.

## Confirmation

Die Entscheidung ist umgesetzt, wenn der Golden-Korpus positive und negative PHP-/JavaScript-Faelle abdeckt, `wp i18n make-pot` die erwarteten Strings extrahiert und gerenderte Tests mit Textverdopplung, Deutsch und RTL keine abgeschnittenen Inhalte, falsche Reihenfolge oder seitenweiten horizontalen Overflow zeigen.

## Revisit when

WordPress den empfohlenen PHP-/JavaScript-Uebersetzungs- oder Sprachpaket-Workflow aendert.
