---
format_version: 1
id: ADR-0006
status: superseded
created: 2026-09-03
accepted: 2026-09-03
scope: skill/i18n
supersedes: ADR-0004
superseded_by: ADR-0008
---

# Internationalisierung als runtime-gepruefte UI-Invariante

## Decision

Jede vom Skill erzeugte oder gepruefte Plugin-Backend-Oberflaeche ist in PHP und JavaScript internationalisierbar. Alle nutzergerichteten Strings einschliesslich `aria-label`, Screenreader-Text und Alternativtext verwenden WordPress-i18n-APIs mit einer literalen Textdomain, die dem kleingeschriebenen Plugin-Slug mit Bindestrichen entspricht. JavaScript registriert `wp-i18n` als Abhaengigkeit und bindet die bereits registrierte Script-Handle mit `wp_set_script_translations()` und einem expliziten Sprachdateipfad an dieselbe Textdomain.

Der Vertrag umfasst vollstaendige Phrasen statt String-Verkettung, Positionsplatzhalter, Pluralformen, Kontext, unmittelbar vorangestellte `translators:`-Kommentare, kontextgerechtes Escaping und locale-gerechte Datums-/Zahlenformatierung. PHP verwendet `wp_date()` und `number_format_i18n()`. JavaScript verwendet `dateI18n` aus `@wordpress/date`; clientseitig angezeigte locale-formatierte Zahlen werden in der Baseline serverseitig mit `number_format_i18n()` geliefert. Eine rein clientseitige Zahlen-, Prozent- oder Waehrungsformatierung ist nur mit separat dokumentierter WordPress-/Web-API, belegter Locale-Zuordnung und eigenem Browsertest zulaessig.

Extraktion allein ist kein Beweis. Die Fixture enthaelt eine Test-PO, erzeugt POT und JavaScript-JSON reproduzierbar und beweist nach Locale-Wechsel im Browser jeweils mindestens einen tatsaechlich uebersetzten PHP- und React-String. Layout und Validierung decken Textverdopplung, lange deutsche Beschriftungen, mindestens eine RTL-Sprache und locale-abhaengige Formate ab.

## Problem

`make-pot` beweist nur Extrahierbarkeit. Es beweist weder eine geladene PHP-Uebersetzung noch korrekte JSON-Dateinamen, Script-Handle, Pfad oder die tatsaechliche JavaScript-Uebersetzung im Browser. Nachtraegliche Lokalisierung behebt ausserdem keine dynamisch zusammengesetzten Strings oder Layouts, die bei laengerem beziehungsweise RTL-Text brechen.

## Drivers

- Der Nutzer verlangt mehrsprachige Plugin-Oberflaechen als feste Eigenschaft.
- WordPress stellt abgestimmte PHP-, JavaScript-, Sprachpaket- und WP-CLI-Vertraege bereit.
- Assistive Strings sind ebenso nutzergerichtet wie sichtbarer Text.
- Uebersetzungen sind nicht vertrauenswuerdig und muessen am Ausgabekontext escaped werden.
- Spacing, Reihenfolge, Breiten und Statusmeldungen muessen auch mit expandierendem oder RTL-Text funktionieren.

## Considered alternatives

1. Nur POT-Extraktion pruefen: reproduzierbar, aber kein Runtime-Beweis.
2. Nur PHP internationalisieren: unzureichend fuer React- und hybride Oberflaechen.
3. Browserstrings fest in Testsprachen einbauen: prueft Layout, aber nicht den WordPress-Uebersetzungsweg.
4. Locale-Abbildung fuer JavaScript-Zahlen erfinden: flexibel, aber nicht quellentreu und fehleranfaellig.

## Consequences

- Der Skill benoetigt konkrete PHP-, JavaScript-, PO/POT/JSON-, Runtime- und Layoutregeln.
- Beispiele duerfen keine unuebersetzten nutzergerichteten Literale oder variable Textdomains enthalten.
- Die Fixture benoetigt mindestens eine echte Testuebersetzung und Locale-Wechsel.
- i18n-Stressfaelle werden Teil der Spacing-, Responsive-, Accessibility- und Render-Validierung.

## Confirmation

Die Entscheidung ist umgesetzt, wenn der vorab eingefrorene Golden-Korpus positive und negative PHP-/JavaScript-Faelle abdeckt, `wp i18n make-pot` und `wp i18n make-json` die erwarteten Dateien erzeugen und Browser-Assertions nach Locale-Wechsel tatsaechlich uebersetzte PHP- und React-Strings sowie robuste deutsche/RTL-Layouts belegen.

## Revisit when

WordPress den empfohlenen PHP-/JavaScript-Uebersetzungs-, JSON- oder Sprachpaket-Workflow aendert oder eine dokumentierte clientseitige Zahlenformatierungs-API fuer den Zielpfad bereitstellt.
