---
format_version: 1
id: ADR-0007
status: superseded
created: 2026-09-03
accepted: 2026-09-03
scope: skill/css-ownership
supersedes: ADR-0005
superseded_by: ADR-0009
---

# Runtime-spezifisches Spacing deterministisch besitzen

## Decision

Der Skill verpflichtet Agenten je DOM-Region auf folgende Reihenfolge: vorhandene WordPress-API und semantisches Core-Markup, vorhandene Core-Klasse oder WordPress-Komponente mit Default-CSS, ein im gewaehlten Runtime-Pfad tatsaechlich bereitgestellter semantischer Token, plugin-eigene Komposition dieser Primitive und erst als letzte Ausnahme eine neue eng gescopte CSS-Regel.

Semantische `--wpds-*`-Variablen duerfen nur konsumiert werden, wenn der ausgewaehlte und geladene WPDS-Provider oder dessen Stylesheet sie bereitstellt. Skill und Plugin-Code duerfen `--wpds-*` weder definieren, ueberschreiben noch nachahmen. Primitive WPDS-Tokens sind Implementierungsdetails. Classic/Core erbt zuerst die Core-Rhythmik.

Im React/Core-Components-Pfad besitzen spezialisierte Komponenten zuerst ihre interne Rhythmik. Fuer eine generische plugin-eigene vertikale Geschwistergruppe ist der Core-bereitgestellte `__experimentalVStack` der Default-Flow-Owner, sofern er im gepinnten `@wordpress/components`-Stand verfuegbar ist und das Projekt experimentelle Komponenten akzeptiert. Seine numerische `spacing`-Prop ist der jeweilige Skill-Norm-Gap geteilt durch das dokumentierte 4-px-Raster: `1/2/3/4/6/8/10` fuer `4/8/12/16/24/32/40px`. Der experimentelle Status wird immer genannt. Verbietet das Projekt experimentelle Komponenten, besitzt eine einzige plugin-lokale Stack-Komposition den Flow und verwendet denselben als Skill-Norm markierten Gap; einzelne Kinder erhalten keine parallelen Aussenabstaende. Der Golden-Fall enthaelt diese Projektbedingung und bestimmt dadurch genau einen Owner.

Eine unvermeidbare isolierte Plugin-Luecke darf eine als **Skill-Norm** markierte Zahl oder eine plugin-eigene Custom Property verwenden, aber niemals als WordPress-Token ausgegeben werden.

## Problem

Nicht jeder WordPress-Backend-Pfad laedt WPDS-Tokens. Zugleich laesst die allgemeine Forderung nach Komponenten-Defaults offen, ob zwei Agenten fuer dieselbe Core-Components-Struktur `__experimentalVStack`, eine andere Layoutkomponente oder eigenes CSS waehlen. Token-Verfuegbarkeit und Flow-Owner muessen daher beide deterministisch sein.

## Drivers

- Der Nutzer verlangt WordPress-Defaults und moeglichst wenig eigenes CSS.
- Token-Verfuegbarkeit ist runtime- und providerabhaengig.
- Zwei Agenten sollen bei identischer Struktur und Projektbedingung denselben Spacing-Owner waehlen.
- Core-, Components- und WPDS-Pfade besitzen unterschiedliche Stabilitaets- und Spacing-Vertraege.

## Considered alternatives

1. `--wpds-*` global fuer alle Pfade definieren: einheitliche Namen, aber erfundene Plattformautoritaet.
2. `Flex`, `VStack` und eigenes `gap` gleichrangig zulassen: flexibel, aber nicht deterministisch.
3. WPDS auf jeder Plugin-Seite laden: einheitlicher Provider, aber experimentelle Abhaengigkeit und unnoetiger Eingriff in Classic-Seiten.
4. Experimentelles `VStack` immer erzwingen: deterministisch, ignoriert aber eine legitime Projektgrenze gegen experimentelle APIs.

## Consequences

- Jede Empfehlung nennt Runtime-, DOM-, Token- und Flow-Owner.
- Core-Components-Golden-Faelle nennen erwartete Komponente, Projektbedingung und `spacing`-Multiplikator.
- Der Skill braucht getrennte Tabellen fuer Core-Beobachtungen, Components-APIs, WPDS-Tokens und Skill-Normen.
- CSS-Ausnahmen muessen die geprueften Owner, den kleinsten Scope und Responsive-/Accessibility-Proof dokumentieren.

## Confirmation

Die Entscheidung ist umgesetzt, wenn Golden-Faelle fuer Classic, Core Components, WPDS und Hybrid jeweils genau einen erwarteten Owner und eine erlaubte Ausdrucksform nennen, Core-Components-Faelle Komponente und Multiplikator pruefen, nicht geladene `--wpds-*` verbieten und jede Custom-CSS-Ausnahme begruenden.

## Revisit when

`VStack` stabilisiert oder ersetzt wird oder WordPress eine stabile, global dokumentierte Admin-Token-/Layout-API bereitstellt.
