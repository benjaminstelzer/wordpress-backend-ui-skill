---
format_version: 1
id: ADR-0009
status: superseded
created: 2026-09-03
accepted: 2026-09-03
scope: skill/css-ownership
supersedes: ADR-0007
superseded_by: ADR-0010
---

# Experiment-Policy und Runtime-Spacing deterministisch entscheiden

## Decision

Der Skill verpflichtet Agenten je DOM-Region auf folgende Reihenfolge: vorhandene WordPress-API und semantisches Core-Markup, vorhandene Core-Klasse oder WordPress-Komponente mit Default-CSS, ein im gewaehlten Runtime-Pfad tatsaechlich bereitgestellter semantischer Token, plugin-eigene Komposition dieser Primitive und erst als letzte Ausnahme eine neue eng gescopte CSS-Regel.

Semantische `--wpds-*`-Variablen duerfen nur konsumiert werden, wenn der ausgewaehlte und geladene WPDS-Provider oder dessen Stylesheet sie bereitstellt. Skill und Plugin-Code duerfen `--wpds-*` weder definieren, ueberschreiben noch nachahmen. Primitive WPDS-Tokens sind Implementierungsdetails. Classic/Core erbt zuerst die Core-Rhythmik.

Routing- und Spacing-Oracles enthalten `experimental_components_policy: allow | deny | unknown`. Repository-Evidenz fuer eine bereits bewusst verwendete experimentelle Komponente darf `allow` begruenden; die blosse Verfuegbarkeit tut es nicht. Bei `unknown` gilt der sichere Default `deny`: Der Agent fuehrt keine neue experimentelle API ein, verwendet genau eine plugin-lokale Stack-Komposition mit als Skill-Norm markiertem Gap und nennt den fehlenden Opt-in. Eine Rueckfrage ist nur noetig, wenn der Nutzer ausdruecklich die experimentelle Variante bewerten oder waehlen will.

Im React/Core-Components-Pfad besitzen spezialisierte Komponenten zuerst ihre interne Rhythmik. Fuer eine generische plugin-eigene vertikale Geschwistergruppe ist bei `allow` der Core-bereitgestellte `__experimentalVStack` der Flow-Owner. Seine numerische `spacing`-Prop ist der jeweilige Skill-Norm-Gap geteilt durch das dokumentierte 4-px-Raster: `1/2/3/4/6/8/10` fuer `4/8/12/16/24/32/40px`. Bei `deny` oder `unknown` besitzt eine einzige plugin-lokale Stack-Komposition den Flow und verwendet denselben als Skill-Norm markierten Gap; einzelne Kinder erhalten keine parallelen Aussenabstaende.

Eine unvermeidbare isolierte Plugin-Luecke darf eine als **Skill-Norm** markierte Zahl oder eine plugin-eigene Custom Property verwenden, aber niemals als WordPress-Token ausgegeben werden.

## Problem

Nicht jeder WordPress-Backend-Pfad laedt WPDS-Tokens. Zugleich bleibt der Core-Components-Flow nondeterministisch, wenn die Aufgabe keine Aussage zu experimentellen Komponenten enthaelt. Verfuegbarkeit darf nicht stillschweigend als Zustimmung gelten.

## Drivers

- Der Nutzer verlangt WordPress-Defaults und moeglichst wenig eigenes CSS.
- Token-Verfuegbarkeit ist runtime- und providerabhaengig.
- Zwei Agenten sollen bei identischer Struktur und Evidenz denselben Spacing-Owner waehlen.
- Neue experimentelle APIs benoetigen einen nachweisbaren Opt-in.

## Considered alternatives

1. `unknown` als `allow` behandeln: weniger eigenes CSS, aber unbelegter Experiment-Opt-in.
2. Bei `unknown` immer nachfragen: sicher, aber blockiert reversible Standardfaelle unnoetig.
3. `Flex`, `VStack` und eigenes `gap` gleichrangig zulassen: flexibel, aber nicht deterministisch.
4. WPDS auf jeder Plugin-Seite laden: einheitlicher Provider, aber experimentelle Abhaengigkeit und Eingriff in Classic-Seiten.

## Consequences

- Jeder Routing-/Spacing-Fall besitzt einen expliziten Experiment-Policy-Wert.
- Jede Empfehlung nennt Runtime-, DOM-, Token- und Flow-Owner.
- Core-Components-Golden-Faelle nennen erwartete Komponente und gegebenenfalls `spacing`-Multiplikator.
- `unknown` fuehrt reproduzierbar zum lokalen Skill-Norm-Stack und nicht zu einer stillen experimentellen Abhaengigkeit.

## Confirmation

Die Entscheidung ist umgesetzt, wenn Golden-Faelle alle drei Policy-Werte abdecken, bei identischer Evidenz genau einen Owner ergeben, `unknown` keine neue experimentelle API einfuehrt, nicht geladene `--wpds-*` verbieten und jede Custom-CSS-Ausnahme begruenden.

## Revisit when

`VStack` stabilisiert oder ersetzt wird oder WordPress eine stabile, global dokumentierte Admin-Token-/Layout-API bereitstellt.
