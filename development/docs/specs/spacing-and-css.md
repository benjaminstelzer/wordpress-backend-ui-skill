# Spacing, vertical flow, and CSS ownership

Status: frozen for implementation

This is the original 7.0 specification. The current 7.1 addendum is
[version-compatibility.md](../../../wordpress-backend-ui/references/version-compatibility.md),
with the shipped [spacing contract](../../../wordpress-backend-ui/references/spacing.md)
owning current guidance.

This specification is normative for the Skill. It separates WordPress facts
from the Skill-Norm that maps semantic relationships to consistent spacing.

## Spacing is a relationship

Choose a gap from the relationship between adjacent children, not from the
component name or viewport. The direct parent owns the gap between its direct
children.

| Relationship | Skill-Norm gap | WPDS semantic gap when loaded | Core Components `Flex` gap |
| --- | ---: | --- | ---: |
| Control to help, status, or error text | 4px | `xs` | `1` |
| Heading to its own introductory body text | 8px | `sm` | `2` |
| Tightly related controls, or icon and label | 8px | `sm` | `2` |
| Elements in one field group | 12px | `md` | `3` |
| Related setting groups | 16px | `lg` | `4` |
| Independent sections | 24px | `xl` | `6` |
| Major page regions | 32px | `2xl` | `8` |
| Exceptional strong separation | 40px | `3xl` | `10` |

This mapping is a **Skill-Norm**, not an official WordPress HIG. In Classic it
selects an existing Core rhythm first. In Core Components it selects a
component API. In bundled WPDS it selects a semantic token supplied by the
loaded exported stylesheet. A numeric fallback remains a named Skill-Norm.

## WPDS gap, padding, and density are different axes

The following values are observed in the pinned Gutenberg `wp/7.0`
`dimension.json`. They are WPDS facts for the bundled experimental runtime,
not values to copy into Classic pages.

### Gap tokens

| Token | compact | default | comfortable |
| --- | ---: | ---: | ---: |
| `xs` | 4px | 4px | 8px |
| `sm` | 4px | 8px | 12px |
| `md` | 8px | 12px | 16px |
| `lg` | 12px | 16px | 20px |
| `xl` | 20px | 24px | 32px |
| `2xl` | 24px | 32px | 40px |
| `3xl` | 32px | 40px | 48px |

### Padding tokens

| Token | compact | default | comfortable |
| --- | ---: | ---: | ---: |
| `xs` | 4px | 4px | 8px |
| `sm` | 4px | 8px | 12px |
| `md` | 8px | 12px | 16px |
| `lg` | 12px | 16px | 20px |
| `xl` | 16px | 20px | 24px |
| `2xl` | 20px | 24px | 32px |
| `3xl` | 24px | 32px | 40px |

Density describes information density. It is not a responsive breakpoint and
must not be changed merely because a viewport is narrow. Gap and padding tokens
with the same name are not interchangeable.

## Runtime expression

### PHP and Classic Core

Core owns `#wpcontent`, `.wrap`, the page title, `.form-table`, native controls,
notices, and `p.submit`. Reuse Settings API markup and Core classes before
adding a plugin layout. Observed WordPress 7.0 values such as `.form-table`
cell padding document the current implementation but are not public extension
APIs.

A plugin-owned inner component may use the semantic Skill-Norm only when Core
does not already own the same relationship. Never put a second gap system over
`.form-table`, `.wrap`, or `p.submit`.

### React with Core Components

Specialized components own their internal rhythm. For a new generic vertical
group use Core-provided `Flex` for `allow`, `deny`, and `unknown` experimental
policies:

```jsx
<Flex
  direction="column"
  align="stretch"
  justify="flex-start"
  wrap={ false }
  expanded={ true }
  gap={ GAP_PX / 4 }
>
  { children }
</Flex>
```

Use `FlexItem` for intrinsic content that should keep its own size. Use
`FlexBlock` only when that child is intended to grow into remaining space. Do
not use child type as decoration. An existing `__experimentalVStack` subtree
retains ownership and is not rewritten merely for stylistic uniformity.

### Bundled experimental WPDS

Bundle and pin the public WPDS package APIs and load the exported
`@wordpress/theme/design-tokens.css`. At the WordPress 7.0 pin,
`ThemeProvider` is not a public runtime export. Plugin code must not unlock the
package's `privateApis`; non-default density therefore has no supported plugin
route on this pin. Do not assume an unloaded `window.wp` global. Plugin code
must never define, override, or imitate `--wpds-*`. `Stack` has no default
direction and no default gap, so vertical flow sets `direction="column"` and
the semantic gap explicitly. The stylesheet supplies default-density tokens.

### Hybrid

Map each DOM region to one runtime and spacing owner. Core commonly owns the
admin shell, title, `.wp-header-end`, and page-level notices. The React root
owns only its descendants. A portal or overlay declares the runtime and token
runtime and token stylesheet present at its actual render destination, not at
its trigger element.

## Flow ownership

| Structure | Owner rule |
| --- | --- |
| Generic stack | Direct parent owns sibling gap. Children have no matching outer margin. |
| Section list | Page or section-list parent owns section gap. Each section owns only its internal flow. |
| Card or panel | Card owns internal padding. Its parent owns distance to adjacent cards or sections. |
| Field | Field/group component owns label, control, help, status, and error relationships. |
| Message | Keep field messages with the field. Page-level notices remain with the shell's notice system. |
| Portal or overlay | The actual rendered root owns flow and must have an explicit runtime and token-style owner. |

Reset heading or paragraph margins only inside the exact plugin-owned parent
whose `gap` replaces them. Do not use a global reset. Nested groups select their
own semantic relationship and do not inherit the parent's gap blindly. Hidden,
unmounted, and empty children occupy no gap slot.

## CSS ownership ladder

Stop at the first owner that can express the requirement:

1. WordPress API and semantic Core admin markup.
2. Existing Core class or WordPress component with its default CSS.
3. Semantic token actually provided by the chosen runtime.
4. Plugin-owned composition of those primitives through component props,
   `gap`, Grid or Flex, and logical properties.
5. New narrowly scoped plugin CSS for a demonstrated gap only.

A CSS exception records:

- the DOM region and its runtime owner;
- the WordPress APIs, classes, components, and tokens checked;
- why they cannot express the required relationship;
- for a local React stack rule, why stable `Flex` cannot express it;
- the smallest plugin-owned selector or component scope;
- whether its value is a provided token or an explicit Skill-Norm;
- checks for reflow, RTL, zoom, focus, content expansion, and relevant states.

Plugin CSS must not target global `.wp-admin`, `.wrap`, `.form-table`, or Core
control selectors to solve a local problem. Do not copy Core CSS, rebuild a
Core primitive for different spacing, create a parallel color/radius/shadow
language, or use `!important` without an unavoidable documented integration
conflict. Custom colors are outside this system unless a product function
requires one and WCAG AA contrast is proved.
