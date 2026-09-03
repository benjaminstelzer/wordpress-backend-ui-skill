---
name: wordpress-backend-ui
description: Design, implement, or audit WordPress 7 plugin-owned wp-admin pages with platform-aligned components, spacing, vertical flow, responsive behavior, accessibility, and PHP/JavaScript internationalization. Use for plugin settings, tools, workflows, dashboards, data views, and explicit Network Admin pages. Do not use for site frontends, themes, the editor canvas, SlotFills, metaboxes, Dashboard widgets, profile fields, Core-screen extensions, or UI owned by another plugin.
---

# WordPress Backend UI

Build plugin administration interfaces that belong in WordPress instead of
placing a second design system inside `wp-admin`.

This Skill is complete on its own. It may compose with Scoville UI, but never
requires it.

## Classify before designing

Read [routing.md](references/routing.md) first. Classify two independent axes:

1. the admin surface and whether version 1 supports it;
2. the runtime and component owner for each DOM region.

React does not imply WPDS. A page can be Classic, Core Components, bundled
experimental WPDS, or hybrid. For hybrid pages, classify portals and overlays
at their actual render destination.

If the surface is excluded, name its host owner and do not apply this Skill's
plugin-page shell or spacing rules. If a required owner is unknown, ask for the
missing fact before recommending components, tokens, spacing, or CSS.

## Follow the owning WordPress layer

For each region, stop at the first layer that can express the requirement:

1. WordPress API and semantic Core admin markup.
2. Existing Core class or WordPress component with its default CSS.
3. Semantic token actually supplied by the selected runtime.
4. Plugin-owned composition of those primitives.
5. New narrowly scoped plugin CSS for a demonstrated gap only.

Never rebuild a WordPress button, control, Notice, table, shell, color system,
focus treatment, radius, or shadow merely to change its appearance. Never
define, override, or imitate `--wpds-*`. Do not load experimental WPDS merely
to restyle a Classic or Core-Components page.

## Load only the relevant contract

- Before choosing gaps, margins, padding, stacks, cards, fields, portals, or
  custom CSS, read [spacing.md](references/spacing.md).
- For page shells, columns, toolbars, data views, narrow widths, zoom, RTL, or
  content expansion, read [responsive.md](references/responsive.md).
- For navigation, hierarchy, actions, forms, Notices, loading, empty, success,
  error, disabled, permission, or recovery states, read
  [ui-guidance.md](references/ui-guidance.md).
- Before implementing or auditing user-facing PHP or JavaScript, accessible
  text, dates, numbers, or localized layout, read
  [internationalization.md](references/internationalization.md).
- For code-shaped output, read [examples.md](references/examples.md) after the
  applicable contracts. Examples demonstrate ownership and are not templates
  to copy across runtimes.
- Before asserting that a rule is official, updating the WordPress target, or
  changing a token/package contract, read [sources.md](references/sources.md)
  and revalidate its trigger.

## Preserve the vertical-flow invariant

The direct parent owns spacing between direct children. Children do not add the
same outer margin. Cards own internal padding, while their parent owns the gap
between cards. Hidden or empty children leave no gap slot.

In Core Components, specialized components own their internal rhythm. A new
generic vertical group uses stable `Flex` with `direction="column"`,
`align="stretch"`, `justify="flex-start"`, `wrap={ false }`,
`expanded={ true }`, and the Skill-Norm gap divided by four. This remains the
default when experimental policy is `allow`, `deny`, or `unknown`.

## Keep every UI translatable

All visible and assistive strings use WordPress i18n APIs with one literal text
domain matching the plugin slug. Use complete phrases, positional placeholders,
plural and context APIs, translator comments, and context-aware escaping. Bind
registered JavaScript handles with `wp_set_script_translations()`. Treat German
text expansion, RTL, and locale-formatted values as normal responsive inputs.

## Accessibility and proof

Use WCAG 2.2 AA as the default floor. Preserve labels, names, roles, values,
relationships, keyboard behavior, focus order, visible and unobscured focus,
error association, status announcements, zoom, contrast, and target size.

Source or build inspection does not prove rendering. State which behavior was
rendered and operated, which was only inspected, and what remains unverified.

## Result contract

For a design, implementation, or audit, make the decision traceable:

- surface, support status, runtime, shell, spacing owner, and experimental
  policy;
- WordPress APIs, components, classes, defaults, and provided tokens reused;
- semantic relationship and its spacing expression;
- page archetype, responsive transformations, relevant states, and recovery;
- PHP/JavaScript i18n path and localized-layout checks;
- any CSS exception with checked owners, demonstrated gap, smallest scope, and
  reflow, RTL, zoom, focus, content, and state checks;
- rendered, source-only, and unverified evidence kept separate.

When the caller requests structured classification, use the canonical field
values and prohibited-recommendation identifiers from `routing.md`; do not
replace them with prose synonyms.

Label facts as **Core**, **WPDS**, **WCAG**, or **Skill-Norm**. Never describe
the Skill-Norm as an official WordPress HIG.

## Optional Scoville UI composition

When Scoville UI is installed, active, and applicable, this Skill remains owner
of WordPress surfaces, components, shell, defaults, tokens, spacing, responsive
constraints, i18n, and CSS exceptions. Scoville UI may strengthen remaining
task flow, hierarchy, state completeness, accessibility, and rendered quality
inside those boundaries. It must not introduce a parallel component language,
spacing scale, breakpoint, palette, or page shell.
