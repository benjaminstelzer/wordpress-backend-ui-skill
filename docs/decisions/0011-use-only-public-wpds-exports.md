---
format_version: 1
id: ADR-0011
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: skill/wpds-runtime
---

# Nur oeffentliche WPDS-Exporte im Plugin-Runtime-Pfad verwenden

## Decision

Der gebuendelte experimentelle WPDS-Pfad fuer WordPress 7.0 verwendet nur
oeffentliche Paket-Exporte. `@wordpress/ui`-Komponenten werden exakt gepinnt und
gebuendelt. Semantische Default-Tokens kommen aus dem oeffentlich exportierten
CSS-Subpath `@wordpress/theme/design-tokens.css` und muessen am tatsaechlichen
Renderziel geladen sein.

`ThemeProvider` ist am Pin `@wordpress/theme` 0.7.1 kein oeffentlicher
Runtime-Export. Plugin-Code importiert ihn deshalb nicht und entsperrt auch
keine `privateApis`. Eine nicht standardmaessige Dichte wird erst empfohlen,
wenn das Zielpaket dafuer einen oeffentlichen Provider-Vertrag anbietet.

`Stack` setzt fuer vertikalen Flow `direction="column"` und einen semantischen
`gap` explizit, weil beide Props am Pin keinen Default besitzen. Plugin-CSS
definiert, ueberschreibt oder imitiert weiterhin keine `--wpds-*`-Variable.

## Problem

Die erste Fixture und das erste Beispiel importierten `ThemeProvider` direkt
aus `@wordpress/theme`. Der Typ ist im Paket sichtbar, der Runtime-Einstieg
exportiert jedoch nur `privateApis`. Die Anleitung war dadurch nicht baubar und
haette Agenten zu einem privaten WordPress-Vertrag gedrueckt.

## Drivers

- Der Skill darf keine nicht oeffentliche API als Plugin-Vertrag ausgeben.
- Der WPDS-Pfad soll reproduzierbar und gegen die gepinnten Pakete pruefbar
  bleiben.
- Semantische Tokens sollen konsumiert werden, ohne sie in Plugin-CSS
  nachzubauen.
- Experimentelle Nutzung braucht einen ausdruecklichen Opt-in und eine klare
  Upgrade-Grenze.

## Considered alternatives

1. `privateApis` entsperren: technisch moeglich, aber ausdruecklich kein
   Plugin-Vertrag.
2. Einen eigenen Provider nachbauen: erzeugt eine parallele und unbelegte
   WPDS-Laufzeit.
3. WPDS vollstaendig ausschliessen: sicher, aber unnoetig; `Stack` und der
   CSS-Subpath sind oeffentlich exportiert.

## Consequences

- Der Default-Density-Pfad ist testbar; andere Dichten sind auf diesem Pin
  nicht Teil des Skill-Vertrags.
- Build-Evidenz muss zeigen, dass der Token-CSS-Subpath geladen wird und kein
  unaufgeloestes `--wpds-*` verbleibt.
- Bei JavaScript-Imports aus `@wordpress/theme` muss die Externalisierung zu
  `wp-theme` separat beachtet werden; der Baseline-Pfad importiert nur den
  CSS-Subpath.
- Portals und Overlays pruefen Runtime und Token-Styles am wirklichen
  Renderziel.

## Confirmation

Die Entscheidung ist umgesetzt, wenn Beispiele, Golden Cases, Fixture und
Validator keinen direkten oder privaten `ThemeProvider`-Import enthalten,
`Stack` Richtung und Gap explizit setzt und ein gerenderter Test den geladenen
Tokenwert statt nur den numerischen Fallback nachweist.

## Revisit when

`@wordpress/theme` einen oeffentlichen Provider exportiert, Paket-Exports oder
Dependency Extraction sich aendern oder WordPress den WPDS-Pfad stabilisiert.
