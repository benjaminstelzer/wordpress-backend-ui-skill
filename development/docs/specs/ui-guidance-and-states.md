# User guidance, navigation, forms, and states

Status: frozen for implementation

This contract combines WordPress conventions, WCAG 2.2 AA, and openly labeled
Skill-Norms. It does not replace WordPress visual language.

## Start with the task

Before choosing layout or components, state:

- the person's primary task on this page;
- the information needed before the next action;
- the one primary action for the current decision region;
- secondary or progressively disclosed information;
- relevant initial, loading, empty, success, error, disabled, and permission
  states;
- recovery, retry, cancel, undo, or safe return where the behavior supports it.

Spacing communicates these relationships. Do not add cards, panels, color, or
emphasis where no real relationship or interaction boundary exists.

## Navigation and orientation

- Put one small settings or tool page under an existing Core menu such as
  Settings or Tools.
- Use a top-level menu only for a distinct, frequently used, multi-page product
  area. Its child pages need consistent local navigation and a visible current
  item.
- Use exactly one primary page title. Heading levels follow the content
  hierarchy and are not chosen for visual size.
- Preserve the Core admin menu and shell. Breadcrumbs or local navigation do
  not duplicate the global menu.
- Keep page-level actions near the title only when they are understandable
  before the main content. Form submission normally follows the values it
  affects.

For a Classic page use the Core header sequence:

```html
<div class="wrap">
  <h1>...</h1>
  <hr class="wp-header-end">
  <!-- Core moves non-inline page notices here. -->
</div>
```

A Core `page-title-action` may accompany the title. Do not place field errors
in this page-level notice region.

## Actions and safety

- One action is primary for one decision region. Several equally styled primary
  buttons usually mean the task hierarchy is unresolved.
- Name an action by its actual result and use the same object term in action,
  progress, result, and error text.
- Destructive actions name the affected object and consequence. Use confirmation
  when the action is consequential and cannot be easily undone. Prefer undo when
  the product can genuinely restore the state.
- A disabled action is not an explanation. Keep the reason available in nearby
  text and programmatic relationships.
- Loading prevents duplicate submission but does not remove the action context
  or focus without a deliberate focus-management reason.

## Forms

- Every control has a persistent visible label. Placeholder text is not the
  only label or instruction.
- Help text explains format, consequence, or a non-obvious choice. Do not repeat
  the label.
- Requiredness, constraints, and validation timing are communicated before they
  cause avoidable errors.
- Group related controls with a semantic fieldset/legend or owning WordPress
  component. Maintain visible and programmatic association.
- Validate near the field and summarize only when a summary helps users find
  multiple errors. Do not rely on color alone.
- Focus the first invalid control or error summary only when that behavior is
  predictable and does not discard user context.

## Feedback ownership

### Classic

- Use `add_settings_error()` and `settings_errors()` for Settings API results
  where applicable.
- Page-level movable notices use Core Notice markup and remain without `.inline`
  so Core can place them after `.wp-header-end`.
- Field or component messages stay at their source and use `.inline` when Core
  notice styling is appropriate. Do not use the deprecated `.below-h2` alias.

### React

- Use the WordPress `Notice` component for important, persistent, actionable,
  error, warning, or page-level information.
- Use `Snackbar` only for low-priority, short-lived confirmation when the result
  remains discoverable elsewhere. A critical failure or only copy of a result
  is not a Snackbar.
- Use a programmatic status message for asynchronous state changes without
  moving focus unless interaction requirements justify it.

## State contract

| State | Required guidance |
| --- | --- |
| Initial | Primary task, available action, prerequisites, and current values are clear. |
| Loading | Name what is loading or changing, prevent accidental duplicate action, preserve orientation, and expose status programmatically. |
| Partial | Distinguish available results from missing or failed parts, preserve usable results, name the incomplete check, and offer retry or continuation only when it exists. |
| Empty | Explain what is absent and why it matters. Offer one valid next action when available. An empty table shell is not guidance. |
| Success | State what changed. Keep confirmation proportional and persistent enough for its consequence. |
| Error | State the user-relevant problem and an available next action. Keep entered values when safe. Do not promise retry unless retry exists. |
| Disabled | Preserve the reason and requirement for availability. Do not communicate state by opacity alone. |
| Permission | Explain that access is unavailable without exposing sensitive details. Remove or disable impossible actions consistently and provide a safe return. |

Include only states that can occur in the requested flow, but do not omit a
state that implementation introduces.

## Accessibility invariants

- WCAG 2.2 AA is the default floor.
- Keyboard operation, logical focus order, visible and unobscured focus, names,
  roles, values, labels, descriptions, error association, and status
  announcements survive every state.
- Visible control text is contained in the accessible name, preferably at the
  start. Icon-only controls have a purpose-based accessible name.
- Text and non-text contrast use Core/component defaults. A necessary custom
  color requires measured WCAG AA evidence.
- Information is never conveyed only by color, position, shape, or motion.
- Motion respects user preferences and is not required to understand state.
- Pointer targets meet `24 x 24 CSS px` or a documented WCAG exception. Core's
  `40px` mobile input height remains a separate platform convention.

## Anti-patterns

- A top-level menu for one minor settings page.
- Multiple primary actions in one decision region.
- Nested cards used only to create visual depth.
- Hidden help or required action available only on hover.
- A spinner without named status or recovery.
- A generic error without the problem or available next action.
- A disabled control with no reason.
- Snackbar for a critical or non-repeatable result.
- Custom buttons, controls, notices, colors, shadows, or focus treatments when
  WordPress already owns the primitive.
