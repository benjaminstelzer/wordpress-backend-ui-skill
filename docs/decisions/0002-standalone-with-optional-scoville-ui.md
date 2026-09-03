---
format_version: 1
id: ADR-0002
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: skill/composition
---

# Standalone-Skill mit optionaler Scoville-UI-Komposition

## Decision

Der WordPress-Backend-Skill ist eigenstaendig und darf nicht von Scoville UI abhaengen. Wenn Scoville UI verfuegbar und fuer dieselbe Aufgabe anwendbar ist, kann es optional komponiert werden. Der WordPress-Skill bleibt dann kanonischer Owner des WordPress-Backend-Designsystems; Scoville UI wendet seine allgemeinen UI-Qualitaetspruefungen innerhalb dieser Grenzen an.

## Problem

Der Skill soll auch in Umgebungen ohne Scoville UI vollstaendig nutzbar sein. Gleichzeitig soll ein Agent bei gemeinsamer Nutzung nicht zwei konkurrierende Designsysteme, Spacing-Skalen oder Komponentenregeln erhalten.

## Drivers

- Der Nutzer hat die Unabhaengigkeit explizit verlangt.
- Scoville UI soll optional nutzbar und kompatibel sein.
- WordPress-spezifische Plattformregeln muessen allgemeinen UI-Defaults vorgehen.
- Doppelte oder widerspruechliche Instruktionen muessen vermieden werden.

## Considered alternatives

1. Harte Abhaengigkeit von Scoville UI: weniger doppelte UI-Grundlagen, aber der Skill waere nicht standalone nutzbar.
2. Keine Komposition: klare Unabhaengigkeit, aber gemeinsame Aufgaben koennten nicht von Scoville-UIs Render-, Accessibility- und Qualitaetspruefung profitieren.
3. Gleichrangige Skills ohne Concern-Ownership: flexibel, aber Konflikte bei Spacing, Breakpoints und Komponentenwahl waeren nicht deterministisch loesbar.

## Consequences

- Der WordPress-Skill muss selbst Mindestregeln fuer Hierarchie, Userfuehrung, States, Responsivitaet und Accessibility enthalten.
- Eine optionale Kompositionssektion definiert Concern-Ownership und Konfliktaufloesung.
- Scoville UI darf keine WordPress-Tokens, Default-CSS oder Komponentenwahl durch eine parallele visuelle Sprache ersetzen.
- Tests muessen Standalone- und Kompositionsfaelle getrennt abdecken.

## Confirmation

Die Entscheidung ist umgesetzt, wenn der fertige Skill ohne Scoville UI vollstaendige WordPress-Backend-Anweisungen liefert und bei gemeinsamer Aktivierung beide Skills anhand einer eindeutigen Ownership-Matrix ohne widerspruechliche Werte arbeiten.

## Revisit when

Scoville UI selbst eine verbindliche, versionsgebundene WordPress-Backend-Spezialisierung als kanonischen Owner integriert oder der Nutzer die Abhaengigkeitsrichtung explizit aendert.
