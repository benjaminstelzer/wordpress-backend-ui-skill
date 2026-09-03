# Responsive layout and page archetypes

WordPress has no universal content width for all plugin pages. Choose an
archetype, keep the shell owner intact, and adapt intrinsically before adding a
breakpoint.

## Shared invariants

- At `<=782px`, respect Core mobile admin behavior. Check `783px` as the
  boundary immediately above it.
- At `320 CSS px`, non-exempt content retains information and function in one
  scrolling direction. Also check the equivalent `1280px` at `400%` zoom.
- `600px` and `390px` are Skill-Norm intermediate test widths, not official
  universal WordPress breakpoints.
- Preserve DOM, keyboard, and screen-reader order when layout changes.
- Typical text inputs and selects follow Core's `40px` mobile height. WCAG 2.2
  AA separately requires `24 x 24 CSS px` pointer targets or an allowed
  exception.
- Use logical properties in unavoidable plugin CSS.
- Treat doubled text, long German labels, RTL, errors, notices, dates, and
  numbers as normal content inputs.
- Primary actions remain visible. Secondary actions wrap or move to an
  accessible labeled menu.
- Non-exempt shells satisfy:

  ```js
  document.documentElement.scrollWidth <= window.innerWidth
  ```

A two-dimensional data view may use one labeled local horizontal scroll
container. The document must not overflow.

## Shells

Classic and hybrid pages inherit `.wrap` and Core gutters. Do not add a second
page gutter. A bundled WPDS `Page` starts from the observed `16px` block and
`24px` inline padding. Reducing it is an explicit tested local rule. Density is
not a responsive switch.

## Focused settings or tool page

- One main source-order column.
- Use Settings API and Core form-table behavior on Classic pages.
- Do not impose a plugin page max-width just to create an aesthetic measure.
- Limit prose locally only for a demonstrated reading problem and label that
  choice as Skill-Norm.
- Put submission after the values it affects.
- At `<=782px`, labels and controls stack through Core behavior. Plugin-owned
  inline actions wrap or stack without reordering.

## Workflow or dashboard

- Separate header, primary task, supporting regions, and status/recovery by
  meaning.
- Use the owner-provided Grid/Flex primitive. A custom intrinsic grid requires
  a documented CSS exception.
- Use content-aware minimums. Avoid fixed column counts chosen only from device
  labels.
- At `<=782px`, default to one visual column unless a smaller group proves
  readable content, target size, and focus order.
- Cards represent real groups. The parent owns inter-card gap.

## Data view

- Use the available admin width instead of the focused-settings measure.
- Keep title, primary action, filters, bulk actions, result status, data region,
  and pagination in source order.
- Wrap toolbars into multiple rows without losing labels or accessible names.
- Prefer a compact list or detail disclosure when it preserves the task.
- If columns must remain two-dimensional, use a labeled local scroll container
  with visible keyboard focus.
- Sticky or clipped UI must not obscure focus.

## Test matrix

Render each applicable archetype at `783`, `782`, `600`, `390`, and `320` CSS
pixels, plus `1280px` at `400%` zoom or an equivalent reflow setup. Repeat the
decisive cases with doubled text, long German labels, RTL, errors/notices,
empty/loading/success/permission states, and keyboard-only traversal.

Source and build inspection do not prove these conditions.
