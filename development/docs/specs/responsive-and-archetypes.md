# Responsive layout and page archetypes

Status: frozen for implementation

This contract is a **Skill-Norm** derived from WordPress 7.0 Core behavior and
WCAG 2.2 AA. WordPress does not define one universal content width for every
plugin page, so the Skill chooses an archetype before choosing a layout.

## Shared invariants

1. Start with intrinsic layout. Allow content, controls, actions, and regions to
   wrap before a breakpoint is needed.
2. Preserve DOM, keyboard, and screen-reader order when visual layout changes.
3. At `<=782px`, respect Core's mobile admin behavior. Stack multi-column forms
   and action groups unless every item remains usable without reordering or
   horizontal page scrolling.
4. At `320 CSS px`, non-exempt content retains information and function in one
   scrolling direction. At `1280px` and `400%` zoom, verify the equivalent
   reflow condition.
5. Typical text inputs and selects follow Core's `40px` mobile control height.
   This is a Core mobile convention. WCAG 2.2 AA separately requires `24 x 24
   CSS px` pointer targets or a documented exception.
6. Use logical properties such as `margin-inline`, `padding-inline`,
   `inline-size`, and `block-size` in unavoidable plugin CSS.
7. Long German labels, doubled strings, RTL, notices, errors, and locale-formatted
   values are normal layout inputs.
8. Primary actions remain visible. Secondary actions wrap or move into an
   accessible labeled menu. Normal form actions never require page-level
   horizontal scrolling.
9. For every non-exempt page shell:

   ```js
   document.documentElement.scrollWidth <= window.innerWidth
   ```

10. A genuinely two-dimensional data view may scroll inside one labeled local
    container. That exception does not permit the document itself to overflow.

## Shell ownership

Classic and hybrid pages inherit `.wrap` and Core shell spacing. Do not add a
second page gutter. A bundled WPDS full-page root starts with the observed
`Page` default of `16px` block and `24px` inline padding. Any reduced inline
padding is an explicit, tested local rule. Density mode is not a mobile switch.

## Archetype A: focused settings or tool page

Use for configuration, diagnostics, and bounded tools whose primary task is
reading or changing one coherent set of values.

- Keep one main content column in source order.
- Classic pages use Settings API and Core form-table reflow. Do not impose a
  plugin page max-width merely to make the form look designed.
- Limit prose only when long explanatory text creates a demonstrated reading
  problem. The local limit is a Skill-Norm and does not constrain controls,
  notices, or the whole admin shell.
- Place a primary save or run action after the values it affects. Header actions
  are for page-level actions that remain understandable before reading the form.
- At `<=782px`, labels and controls stack through Core behavior. Plugin-owned
  inline field actions also stack or wrap without changing source order.

## Archetype B: workflow or dashboard page

Use for a multi-region task, overview, or repeated summary modules.

- Keep page header, primary task region, supporting regions, and recovery/status
  regions as distinct semantic groups.
- Use an owner-provided Grid/Flex primitive. If none exists, a narrowly scoped
  intrinsic grid is a CSS exception, not a new global layout system.
- Columns use content-aware minimums and wrap before they squeeze controls or
  text. Avoid fixed column counts tied only to viewport labels.
- At `<=782px`, default to one visual column unless a small group proves that
  multiple columns preserve readable content, target size, and focus order.
- Cards are used only for real grouping. Their parent owns inter-card gap and
  each card owns only its internal padding.

## Archetype C: data view

Use for tables, lists with many fields, filters, bulk actions, and pagination.

- Use the available admin width. Do not apply the focused-settings measure.
- Keep title, primary action, filters, bulk actions, result status, data region,
  and pagination in source order.
- Toolbars wrap into multiple rows. Labels remain available to assistive
  technology and interactive controls retain accessible names.
- Prefer a deliberate compact list or detail disclosure when it preserves the
  task. If columns must remain two-dimensional, put horizontal scrolling on a
  labeled data container with visible keyboard focus.
- Sticky or clipped controls must not obscure focus. The document shell still
  satisfies the no-overflow invariant.

## Required viewport and content matrix

Check every applicable archetype at `783`, `782`, `600`, `390`, and `320` CSS
pixels. Also check `1280px` at `400%` zoom or an equivalent `320 CSS px` reflow
setup. `600px` and `390px` are Skill-Norm intermediate test widths, not
official universal WordPress breakpoints. Repeat the decisive layouts with:

- doubled text and long German labels;
- one RTL locale;
- validation errors and page notices;
- empty, loading, success, and permission states;
- keyboard-only focus traversal.

Build or source inspection does not prove these conditions. They remain
unverified until the WordPress 7.0 fixture is rendered and operated.
