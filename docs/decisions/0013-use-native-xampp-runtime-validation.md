---
format_version: 1
id: ADR-0013
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: validation/runtime
---

# Native XAMPP-Runtimes statt Docker verwenden

## Decision

Die kanonische Runtime-Validierung dieses Projekts verwendet die vorhandene
native XAMPP-Installation fuer eine getrennte WordPress-7.0-Single-Site und
eine WordPress-7.0.x-Multisite. Docker und `wp-env` sind keine Voraussetzung
mehr und werden aus Paket, Lockfile, Skripten und Abnahmeanweisungen entfernt.

Ein versioniertes Fixture-Manifest beschreibt ausschliesslich erwartete
relative Pfade, WordPress-Versionen, Site-Typen, Plugin-Status und Locale. Ein
read-only PowerShell-Validator nimmt den XAMPP-Root explizit entgegen, leitet
daraus PHP, WP-CLI und beide isolierten WordPress-Pfade ab und prueft die
Anforderungen, ohne Zugangsdaten oder bestehende Sites zu veraendern. Die
gerenderten Browserpruefungen laufen gegen dieselben beiden Installationen.

Der XAMPP-Pfad ist Testinfrastruktur des Repositories und keine Abhaengigkeit
des veroeffentlichten Agenten-Skills.

## Problem

Beide gepinnten `wp-env`-Starts enden in dieser Umgebung bei `spawn docker
ENOENT`. Docker ist nicht vorhanden und soll nicht installiert werden. Die
bereits isoliert angelegten XAMPP-Sites decken Single Site und Network Admin
tatsaechlich ab, waren aber noch nicht der reproduzierbare kanonische
Abnahmepfad.

## Drivers

- Die Abnahme muss mit der verfuegbaren lokalen Infrastruktur ausfuehrbar sein.
- Ein fehlender externer Runtime-Dienst darf nicht als bestandener Test gelten.
- Single Site und Network Admin muessen getrennt und wiederholbar pruefbar sein.
- Zugangsdaten und andere XAMPP-Sites bleiben ausserhalb des Repositories und
  der Testausgabe.
- Der publizierte Skill darf weder Docker noch XAMPP zur Laufzeit benoetigen.

## Considered alternatives

1. Docker installieren: wurde ausdruecklich ausgeschlossen und fuegt eine fuer
   das Ergebnis unnoetige Runtime hinzu.
2. `wp-env` als blockierende Pflicht behalten: laesst die lokale Abnahme trotz
   zwei funktionierender WordPress-Installationen dauerhaft unausfuehrbar.
3. Nur eine Single Site pruefen: deckt Network Admin und Multisite-spezifische
   Navigation nicht ab.
4. Die XAMPP-Pruefung nur manuell dokumentieren: liefert keine wiederholbare
   Preflight- und Runtime-Verifikation.

## Consequences

- W-005 bleibt als historisch nicht erfuellter Docker-Pfad erhalten und wird
  durch einen neuen Work Item ersetzt; seine Acceptance wird nicht umgedeutet.
- Das Repository verliert `@wordpress/env` und die beiden `.wp-env`-Dateien.
- Der native Validator ist Windows-/PowerShell-Testtooling; der Skill selbst
  bleibt plattform- und Scoville-UI-unabhaengig.
- Die aktuell beobachteten Runtime-Versionen werden exakt festgehalten. Eine
  Aenderung erfordert eine bewusste Manifest- und Evidenzaktualisierung.
- Browser- und Accessibility-Evidenz bleibt erforderlich; der Preflight allein
  beweist keine gerenderte UI.

## Confirmation

Die Entscheidung ist umgesetzt, wenn das Manifest und der read-only Validator
beide isolierten XAMPP-Sites, ihre exakten WordPress-Versionen, Single-/
Multisite-Modus, aktives Fixture, Plugin-Verknuepfung, Locale und erforderliche
Build-Artefakte pruefen, die Dokumentation nur diesen kanonischen Pfad verlangt
und keine Docker-/`wp-env`-Abhaengigkeit mehr im Paket verbleibt.

## Revisit when

Das Projekt auf eine andere Testmaschine wechselt, XAMPP ersetzt wird, eine
plattformneutrale bereits verfuegbare Runtime dieselbe Abdeckung bietet oder
die WordPress-7-Zielversionen bewusst angehoben werden.
