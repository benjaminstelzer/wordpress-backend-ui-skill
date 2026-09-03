---
format_version: 1
id: ADR-0010
status: accepted
created: 2026-09-03
accepted: 2026-09-03
scope: skill/css-ownership
supersedes: ADR-0009
---

# Nicht-experimentelle Core-Komponenten vor experimentellem oder eigenem Spacing

## Decision

Der Skill verpflichtet Agenten je DOM-Region auf folgende Reihenfolge: vorhandene WordPress-API und semantisches Core-Markup, vorhandene Core-Klasse oder WordPress-Komponente mit Default-CSS, ein im gewaehlten Runtime-Pfad tatsaechlich bereitgestellter semantischer Token, plugin-eigene Komposition dieser Primitive und erst als letzte Ausnahme eine neue eng gescopte CSS-Regel.

Semantische `--wpds-*`-Variablen duerfen nur konsumiert werden, wenn der ausgewaehlte und geladene WPDS-Provider oder dessen Stylesheet sie bereitstellt. Skill und Plugin-Code duerfen `--wpds-*` weder definieren, ueberschreiben noch nachahmen. Primitive WPDS-Tokens sind Implementierungsdetails. Classic/Core erbt zuerst die Core-Rhythmik.

Im React/Core-Components-Pfad besitzen spezialisierte Komponenten zuerst ihre interne Rhythmik. Fuer eine neue generische plugin-eigene vertikale Geschwistergruppe ist die Core-bereitgestellte, nicht als experimentell benannte `Flex`-Komponente der Default-Flow-Owner. Der Skill setzt `direction="column"`, `align="stretch"`, `justify="flex-start"`, `wrap={ false }` und `expanded={ true }` explizit. Die numerische `gap`-Prop ist der jeweilige Skill-Norm-Gap geteilt durch das dokumentierte 4-px-Raster: `1/2/3/4/6/8/10` fuer `4/8/12/16/24/32/40px`. Dokumentierte `FlexItem`-/`FlexBlock`-Kinder werden nach ihrer Groessenrolle verwendet. Eine plugin-lokale Stack-Regel ist erst zulaessig, wenn `Flex` den belegten Layoutbedarf nicht ausdruecken kann.

Routing- und Spacing-Oracles enthalten weiterhin `experimental_components_policy: allow | deny | unknown`. Sie steuert nur die Einfuehrung anderer experimenteller Komponenten, nicht den stabilen `Flex`-Flow. Repository-Evidenz fuer eine bewusst verwendete experimentelle Komponente darf `allow` begruenden; die blosse Verfuegbarkeit tut es nicht. Bei `unknown` gilt der sichere Default `deny`: keine neue experimentelle API. Ein bestehender `__experimentalVStack`-Teilbaum bleibt sein eigener Owner und wird nicht allein zur Stilbereinigung umgebaut; neue generische Gruppen verwenden `Flex`.

Eine unvermeidbare isolierte Plugin-Luecke darf eine als **Skill-Norm** markierte Zahl oder eine plugin-eigene Custom Property verwenden, aber niemals als WordPress-Token ausgegeben werden.

## Problem

Ein sicherer Default gegen experimentelle APIs darf nicht dazu fuehren, dass der Skill eine vorhandene Core-Komponente ueberspringt und eigenes CSS erzeugt. `Flex` kann am gepinnten `@wordpress/components`-Stand einen vertikalen Flow und das 4-px-Gap-Raster ohne experimentellen Exportnamen ausdruecken.

## Drivers

- Der Nutzer verlangt WordPress-Defaults und moeglichst wenig eigenes CSS.
- Zwei Agenten sollen bei identischer Struktur denselben Spacing-Owner und dieselben Ausrichtungswerte waehlen.
- Token-Verfuegbarkeit ist runtime- und providerabhaengig.
- Neue experimentelle APIs benoetigen einen nachweisbaren Opt-in, stabile vorhandene Komponenten nicht.

## Considered alternatives

1. Bei `unknown` direkt eigenes CSS verwenden: sicher gegen Experimente, aber verletzt die Owner-Leiter.
2. `__experimentalVStack` als Default: weniger Props, aber unbelegter Experiment-Opt-in.
3. `Flex` ohne explizite Ausrichtung verwenden: nutzt Core, aber die Defaults `center` und `space-between` sind fuer normalen Vertical Flow ungeeignet und nicht deterministisch zur Skill-Norm.
4. WPDS auf jeder Plugin-Seite laden: einheitlicher Provider, aber experimentelle Abhaengigkeit und Eingriff in Classic-Seiten.

## Consequences

- Neue generische Core-Components-Stacks verwenden `Flex` vor lokalem CSS, unabhaengig von der Experiment-Policy.
- Golden-Faelle pruefen `direction`, `align`, `justify`, `wrap`, `expanded`, Gap-Multiplikator und Kindrolle.
- `unknown` fuehrt reproduzierbar zu keiner neuen experimentellen API, aber ebenso wenig automatisch zu Custom CSS.
- Bestehende experimentelle Teilbaeume werden nicht ohne funktionalen Grund refaktoriert.

## Confirmation

Die Entscheidung ist umgesetzt, wenn Golden-Faelle alle drei Experiment-Policy-Werte abdecken, neue generische Core-Components-Gruppen jeweils `Flex` mit den festgelegten Props und Multiplikatoren waehlen, bestehende experimentelle Owner respektieren, nicht geladene `--wpds-*` verbieten und jede verbleibende Custom-CSS-Ausnahme eine nachgewiesene `Flex`-Luecke belegt.

## Revisit when

`Flex` seinen oeffentlichen Vertrag oder das 4-px-Raster aendert, `VStack` stabilisiert wird oder WordPress eine stabilere semantische Vertical-Stack-Komponente bereitstellt.
