---
format_version: 1
id: ADR-0014
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: tests/routing-oracle
---

# Network-Admin-Hybrid als nicht-experimentelle Route korrigieren

## Decision

Der Golden Case `route-network-admin-hybrid` verwendet
`experimental_components_policy: deny`. Seine beschriebene React-Region nutzt
ausdruecklich Core Components und ist damit wie der entsprechende Single-Site-
Hybrid keine unbekannte oder experimentelle Runtime.

Die kanonische Routing-Tabelle fuehrt ausserdem alle bereits im eingefrorenen
Routing-Korpus verwendeten Surface-, Shell- und Spacing-Werte explizit auf.
Fuer ausgeschlossene Host-Flaechen ist die Policy-Regel nun deterministisch:
bekannte Classic/Core-PHP-Hosts ergeben `deny`, React- oder nicht spezifizierte
Hosts `unknown`.

## Problem

Der finale Read-only-Review fand einen Widerspruch zwischen der normativen
Policy-Regel und einem Golden Case sowie sechs ausgeschlossene/ambige Cases,
deren strukturierte Werte nicht in der kanonischen Wertetabelle standen. Der
siebenfaellige Fresh-Agent-Korpus enthielt diese Luecke nicht.

## Drivers

- Derselbe bekannte Core-only-Hybrid muss dieselbe Policy liefern.
- Jeder Golden-Wert muss aus der installierten Skill-Dokumentation ableitbar
  sein.
- Ausgeschlossene Oberflaechen bleiben beim Host und duerfen keine implizite
  Experimentfreigabe erhalten.
- Eine fachliche Oracle-Korrektur muss nach ADR-0012 sichtbar neu baselint
  werden.

## Considered alternatives

1. Network Admin als `unknown` behandeln: widerspricht der ausdruecklich
   genannten Core-Components-Runtime.
2. Die fehlenden Werte aus dem Golden-Korpus entfernen: verringert die
   Support-Matrix und verdeckt statt behebt die Dokumentationsluecke.
3. Nur den Fresh-Agent-Korpus erweitern: laesst den kanonischen Vertrag
   widerspruechlich.

## Consequences

- `tests/cases/routing.yaml` und sein Hash werden bewusst aktualisiert.
- Der erweiterte Fresh-Agent-Korpus muss nach der Korrektur erneut standalone
  und mit optionalem Scoville UI laufen.
- Andere Routing-, Spacing-, i18n-, responsive und UI-Oracles bleiben
  unveraendert.

## Confirmation

Die Entscheidung ist umgesetzt, wenn die kanonische Tabelle alle Routing-
Werte abdeckt, der Network-Admin-Hybrid `deny` liefert, die Manifestpruefung
besteht und der erweiterte Fresh-Agent-Korpus in beiden Modi erneut besteht.

## Revisit when

Ein ausgeschlossener Host in Version 1 aufgenommen wird, eine Runtime
experimentell wird oder neue strukturierte Routing-Werte hinzukommen.
