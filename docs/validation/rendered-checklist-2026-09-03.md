# Rendered acceptance checklist — 2026-09-03

## Method and boundary

These are explicit pass/fail assertions from authenticated interactive
Playwright sessions against the isolated native XAMPP fixtures. The repository
does not commit credentials, cookies or session artifacts. A temporary
Single-Site administrator was created only for the final rerun and deleted in
the same command. The read-only XAMPP preflight is reproducible separately; it
does not claim to reproduce browser interaction.

Widths were set in CSS pixels. The 320px case is the accepted equivalent of a
1280px viewport at 400% zoom for WCAG reflow. Modes, states and Network Admin
coverage are detailed in `wordpress-7-runtime-2026-09-03.md`.

## Assertions

| Assertion | Expected | Observed | Result |
| --- | --- | --- | --- |
| Shell reflow at 783, 782, 600, 390 and 320px | `document.documentElement.scrollWidth <= window.innerWidth` | Equal or lower in Single Site and Network Admin | PASS |
| Data table at narrow widths | Overflow stays inside named focusable region | Local region scrolls; document does not | PASS |
| Keyboard order and focus | DOM order, visible in-viewport focus | Controls and data region follow DOM order and remain visible | PASS |
| Keyboard table scroll | Region scrolls without page overflow | `scrollLeft` changed from 0px to 200px | PASS |
| Disabled action | Named, reason-associated, focusable, inactive | `aria-disabled`, valid `aria-describedby`, no activation | PASS |
| Loading/partial/empty/error/success feedback | Message-only programmatic announcement and visible recovery where applicable | WordPress speak regions received message text; controls were excluded | PASS |
| Permission state | Visible programmatic reason and context-correct return | Reason linked; Network Admin returns to Network Admin | PASS |
| Pointer targets at 320px | At least 24x24px or valid exception | Every visible fixture target at least 24x24px; inputs/actions 40px high | PASS |
| Primary/secondary action reflow at 320px | Both labels visible; local and document overflow absent; source order retained | German buttons wrapped to separate rows at y=392.48/440.48px; widths 219.92/149.28px; both 40px high; row 298/298px; document 320/320px | PASS |
| Representative contrast | WCAG AA | Title 13.94:1, body/table 8.8:1, primary action 5.61:1 | PASS |
| Core `TextControl` help contrast | At least 4.5:1 | Initial Core default was 4.04:1; scoped plugin-owned exception changed text to `rgb(80, 87, 94)` and above 6.5:1 | PASS after fix |
| Automated WCAG scan | No violations or incomplete rules for tested fixture state | Core/initial at 320px: 0 violations, 0 incomplete for WCAG 2 A/AA, 2.1 A/AA, 2.2 AA | PASS |
| German expansion and RTL | No information/function loss or document overflow | Long German labels reflowed; Arabic admin loaded RTL CSS and retained local table overflow | PASS |

## CSS-exception record

Core Components rendered the `TextControl` help at `#757575` on the observed
`#f0f0f0` admin canvas, which axe measured at 4.04:1. The fixture therefore
adds one plugin-scoped exception on `.wbui-fixture-help-text` using Core admin
gray `#50575e`. No global selector, component geometry, spacing token or
`--wpds-*` value is changed. The full tagged axe rerun passed after this change.

## Limitations

The assertions are recorded observations, not a committed credential-bearing
end-to-end test suite. The automated scan covers the final Core/initial state;
manual checks cover the remaining modes, states, keyboard behavior, Network
Admin, localization and RTL. Upgrading WordPress, Core Components, the browser
or the fixture requires a new rendered run.
