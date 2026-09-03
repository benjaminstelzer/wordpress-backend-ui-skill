---
format_version: 1
id: ADR-0012
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: tests/golden-oracles
---

# Review-korrigierte Golden Oracles neu baselinen

## Decision

Der nach dem finalen Review korrigierte Golden-Korpus ist die reproduzierbare
Baseline fuer W-006. Seine sechs Dateien und SHA-256-Werte stehen in
`tests/cases/MANIFEST.sha256`; der Contract-Validator berechnet jeden Hash neu
und lehnt fehlende, zusaetzliche oder veraenderte Case-Dateien ab.

Der 28. Spacing-Fall `wpds-heading-intro` wurde waehrend W-005 ergaenzt, weil
der Review eine echte Luecke zwischen Spezifikation und Oracle gefunden hatte.
Der historische Vor-W-005-Stand mit 27 Faellen ist deshalb nicht mehr der
fachlich richtige Oracle. W-006 prueft den explizit neu baselinten Stand statt
einen nicht gespeicherten Vorzustand als unveraendert zu behaupten.

## Problem

Der Plan verlangte vor W-005 eingefrorene Oracles, speicherte aber weder Git-
Historie noch Datei-Hashes. Nach der notwendigen Heading-zu-Intro-Korrektur war
der alte Zustand weder richtig noch reproduzierbar. Eine blosse Fallzahl konnte
spaetere stille Aenderungen nicht erkennen.

## Drivers

- Materielle Review-Korrekturen duerfen nicht zugunsten eines Prozessclaims
  verworfen werden.
- W-006 braucht eine reproduzierbare, maschinenpruefbare Baseline.
- Jede spaetere Oracle-Aenderung muss sichtbar und begruendet sein.
- Fallzahl und Inhalt muessen getrennt abgesichert werden.

## Considered alternatives

1. Den 28. Fall entfernen: wuerde die belegte Heading-zu-Intro-Luecke erneut
   oeffnen.
2. Nur die Zahl 28 dokumentieren: erkennt inhaltliche Aenderungen nicht.
3. Einen historischen Stand aus Erinnerung rekonstruieren: waere keine
   belastbare Evidenz.

## Consequences

- Der aktuelle Korpus ist ab diesem Decision-Zeitpunkt eingefroren.
- Eine fachlich notwendige Aenderung braucht eine neue oder ersetzende Decision,
  ein aktualisiertes Manifest und erneut ausgefuehrte betroffene Checks.
- W-006 darf nicht behaupten, der 27-Fall-Stand sei unveraendert geblieben.
- Das Manifest ist Testevidenz, kein Ersatz fuer Fresh-Agent- oder Runtime-
  Validierung.

## Confirmation

Die Entscheidung ist umgesetzt, wenn `MANIFEST.sha256` alle sechs Case-Dateien
genau einmal enthaelt, der Contract-Validator die aktuellen SHA-256-Werte
verifiziert und W-006 ADR-0012 als Decision referenziert.

## Revisit when

Ein Golden Case fachlich geaendert werden muss, neue Case-Dateien hinzukommen
oder eine Versionskontrolle den Baseline-Nachweis uebernimmt.
