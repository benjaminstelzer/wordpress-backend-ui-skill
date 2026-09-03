# Spacing, vertical flow, and CSS ownership

Choose spacing from the relationship between adjacent children. The mapping is
a **Skill-Norm**, not an official WordPress HIG.

## Semantic gap scale

| Relationship | Gap | WPDS gap if provided | Core Components `Flex` gap |
| --- | ---: | --- | ---: |
| Control to help, status, or error text | 4px | `xs` | `1` |
| Heading to its own introductory body text | 8px | `sm` | `2` |
| Tightly related controls, or icon and label | 8px | `sm` | `2` |
| Elements in one field group | 12px | `md` | `3` |
| Related setting groups | 16px | `lg` | `4` |
| Independent sections | 24px | `xl` | `6` |
| Major page regions | 32px | `2xl` | `8` |
| Exceptional strong separation | 40px | `3xl` | `10` |

The `40px` relationship is exceptional, not a default between ordinary blocks.

## WPDS token facts at Gutenberg `wp/7.0`

These values apply only to the pinned bundled WPDS runtime.

### Gap

| Token | compact | default | comfortable |
| --- | ---: | ---: | ---: |
| `xs` | 4px | 4px | 8px |
| `sm` | 4px | 8px | 12px |
| `md` | 8px | 12px | 16px |
| `lg` | 12px | 16px | 20px |
| `xl` | 20px | 24px | 32px |
| `2xl` | 24px | 32px | 40px |
| `3xl` | 32px | 40px | 48px |

### Padding

| Token | compact | default | comfortable |
| --- | ---: | ---: | ---: |
| `xs` | 4px | 4px | 8px |
| `sm` | 4px | 8px | 12px |
| `md` | 8px | 12px | 16px |
| `lg` | 12px | 16px | 20px |
| `xl` | 16px | 20px | 24px |
| `2xl` | 20px | 24px | 32px |
| `3xl` | 24px | 32px | 40px |

Gap and padding names are not interchangeable. Density is an independent mode,
not a mobile breakpoint.

## Parent ownership

1. The direct parent owns spacing between its direct children.
2. Children do not add the same outer margin when their parent uses `gap`.
3. Nested groups choose the relationship for their own children instead of
   inheriting the parent gap blindly.
4. A card or panel owns internal padding. Its parent owns distance to peers.
5. Hidden, unmounted, or empty children occupy no gap slot.
6. Help, status, and error text stays with the control it explains.
7. Reset heading or paragraph margins only inside the exact plugin-owned gap
   parent that replaces them.
8. Portals and overlays declare the owner at their render destination.

## Runtime expression

### Classic

Core owns native shell and Settings API rhythm. Reuse it. A plugin-owned inner
component may use a Skill-Norm gap only after Core markup, classes, and default
CSS have been checked. Never apply a gap stack over `.wrap`, `.form-table`, or
`p.submit`.

### Core Components

Specialized components own their internals. For a new generic vertical group:

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

Use `FlexItem` for intrinsic content. Use `FlexBlock` only for content intended
to grow into remaining space. Preserve an existing `__experimentalVStack`
subtree unless a functional requirement justifies changing it.

### Bundled WPDS

Bundle the public `@wordpress/ui` API and the exported
`@wordpress/theme/design-tokens.css`, then select the semantic token. At this
pin `ThemeProvider` is not a public runtime export; never unlock
`@wordpress/theme` private APIs from plugin code. `Stack` has neither a default
direction nor a default gap, so set `direction="column"` and the semantic gap
explicitly for vertical flow. The stylesheet supplies the default-density
tokens. Never define, override, or imitate the `--wpds-*` namespace. Primitive
tokens are implementation details.

## CSS ownership ladder

Stop at the first suitable owner:

1. WordPress API and semantic Core markup.
2. Core class or WordPress component with default CSS.
3. Semantic token actually supplied by the runtime.
4. Plugin-owned composition through props, Grid/Flex, `gap`, and logical
   properties.
5. Narrow plugin CSS for a demonstrated gap only.

An exception records the DOM/runtime owner, every WordPress option checked, why
those options fail, why `Flex` fails for a local React stack, the smallest
plugin scope, token or Skill-Norm source, and checks for reflow, RTL, zoom,
focus, text expansion, empty content, and affected states.

Reject global `.wp-admin`, `.wrap`, `.form-table`, or Core-control overrides,
copied Core CSS, custom Core-primitive rebuilds, unloaded WPDS references,
parallel colors/radii/shadows, and undocumented `!important`.
