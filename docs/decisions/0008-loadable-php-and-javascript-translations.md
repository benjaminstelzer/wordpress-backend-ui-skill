---
format_version: 1
id: ADR-0008
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: skill/i18n
supersedes: ADR-0006
---

# Ladbare PHP- und JavaScript-Uebersetzungen als UI-Invariante

## Decision

Jede vom Skill erzeugte oder gepruefte Plugin-Backend-Oberflaeche ist in PHP und JavaScript internationalisierbar. Alle nutzergerichteten Strings einschliesslich `aria-label`, Screenreader-Text und Alternativtext verwenden WordPress-i18n-APIs mit einer literalen Textdomain, die dem kleingeschriebenen Plugin-Slug mit Bindestrichen entspricht. JavaScript registriert `wp-i18n` als Abhaengigkeit und bindet die bereits registrierte Script-Handle mit `wp_set_script_translations()` und einem expliziten Sprachdateipfad an dieselbe Textdomain.

Der String-Vertrag umfasst vollstaendige Phrasen statt Verkettung, Positionsplatzhalter, Pluralformen, Kontext, unmittelbar vorangestellte `translators:`-Kommentare und kontextgerechtes Escaping. PHP verwendet `wp_date()` und `number_format_i18n()`. JavaScript verwendet `dateI18n` aus `@wordpress/date`; clientseitig angezeigte locale-formatierte Zahlen werden in der Baseline serverseitig mit `number_format_i18n()` geliefert. Eine rein clientseitige Zahlen-, Prozent- oder Waehrungsformatierung ist nur mit separat dokumentierter API, belegter Locale-Zuordnung und eigenem Browsertest zulaessig.

Der reproduzierbare Fixture-Pfad lautet:

1. Quellen werden mit `wp i18n make-pot` in ein POT extrahiert.
2. Eine Test-PO mit dem Dateinamen `<text-domain>-<locale>.po` wird gegen dieses POT gepflegt; sie wird nicht in ein POT konvertiert.
3. Die PO wird mit `wp i18n make-mo` zu `<text-domain>-<locale>.mo` im Plugin-Verzeichnis `languages/` kompiliert.
4. Die Fixture registriert diesen benutzerdefinierten Pfad bei `init` mit `load_plugin_textdomain()`; WordPress 6.7+ laedt das eigentliche Artefakt danach just in time.
5. Dieselbe PO wird mit `wp i18n make-json --no-purge` in JavaScript-JSON ueberfuehrt. Der Golden-Fall legt entweder den dokumentierten Dateinamen `<domain>-<locale>-<handle>.json` fest oder stellt sicher, dass PO-Dateireferenzen auf den registrierten Build-Pfad zeigen, aus dem der MD5-Dateiname berechnet wird; `src/`-Referenzen fuer ein registriertes `build/`-Script sind unzulaessig.
6. Nach reproduzierbarem Site-/Admin-User-Locale-Wechsel beweisen Browser-Assertions mindestens einen wirklich uebersetzten PHP- und React-String.

Layout und Validierung decken Textverdopplung, lange deutsche Beschriftungen, mindestens eine RTL-Sprache und locale-abhaengige Formate ab.

## Problem

POT und PO sind Autorenartefakte. WordPress laedt fuer PHP keine PO-Datei, sondern ein kompiliertes MO- oder `.l10n.php`-Artefakt. Ohne Kompilierung und registrierten Ladepfad kann ein PHP-Browser-Assert nicht bestehen. Ebenso beweist `make-pot` weder eine geladene PHP-Uebersetzung noch korrekte JavaScript-Dateinamen, Script-Handle oder Pfad.

## Drivers

- Der Nutzer verlangt mehrsprachige Plugin-Oberflaechen als feste Eigenschaft.
- WordPress stellt abgestimmte PHP-, JavaScript-, Sprachdatei- und WP-CLI-Vertraege bereit.
- Assistive Strings sind ebenso nutzergerichtet wie sichtbarer Text.
- Uebersetzungen sind nicht vertrauenswuerdig und muessen am Ausgabekontext escaped werden.
- Runtime- und Layoutbeweise muessen den realen WordPress-Ladeweg verwenden.

## Considered alternatives

1. Nur POT-Extraktion pruefen: reproduzierbar, aber kein Runtime-Beweis.
2. Eine PO direkt als PHP-Beweis verwenden: WordPress laedt sie nicht.
3. Browserstrings fest in Testsprachen einbauen: prueft Layout, aber nicht den Uebersetzungsweg.
4. `.l10n.php` statt MO als alleinige Baseline: moeglich, aber MO ist fuer Plugin-Bundles und `load_plugin_textdomain()` der einfachere dokumentierte Fixture-Pfad.

## Consequences

- Der Skill benoetigt konkrete PHP-, JavaScript-, POT/PO/MO/JSON-, Runtime- und Layoutregeln.
- Die Fixture enthaelt eine echte Test-PO, kompiliertes MO und erzeugtes JSON.
- Der Locale-Wechsel fuer Site und Admin-User wird reproduzierbar eingerichtet.
- Beispiele duerfen keine unuebersetzten nutzergerichteten Literale oder variable Textdomains enthalten.

## Confirmation

Die Entscheidung ist umgesetzt, wenn der vorab eingefrorene Golden-Korpus positive und negative PHP-/JavaScript-Faelle abdeckt, POT, MO und JSON reproduzierbar erzeugt werden, `load_plugin_textdomain()` den Plugin-Sprachpfad registriert und Browser-Assertions nach Locale-Wechsel tatsaechlich uebersetzte PHP- und React-Strings sowie robuste deutsche/RTL-Layouts belegen.

## Revisit when

WordPress den empfohlenen MO-/`.l10n.php`-, JavaScript-JSON- oder Sprachpaket-Workflow aendert oder eine dokumentierte clientseitige Zahlenformatierungs-API fuer den Zielpfad bereitstellt.
