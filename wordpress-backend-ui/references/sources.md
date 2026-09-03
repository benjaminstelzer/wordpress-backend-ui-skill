# WordPress 7.0 source contract

Revalidate a source when its trigger applies. Keep documented APIs, observed
implementation, and Skill-Norms distinct.

## Pinned repository state

| Owner | Ref and resolved commit | Target packages | Revalidate |
| --- | --- | --- | --- |
| `WordPress/wordpress-develop` | `7.0` at `90a615f1834824d2583a43bfc698d9c710e5c094` | WordPress 7.0 admin source | Before release, new 7.x target, or branch drift |
| `WordPress/gutenberg` | `wp/7.0` at `28c0dedc4eaf001a24237a1fbba4b0887698b000` | `@wordpress/ui` 0.7.1, `@wordpress/theme` 0.7.1, `@wordpress/admin-ui` 1.8.1, `@wordpress/components` 32.2.1 | Before release, package upgrade, or stability change |
| `WordPress/WordPress` | tag `7.0` at `b16cd68ea199838d8f9daf0ff7e3f35042ba0ad0` | WordPress 7.0 runtime | Before fixture setup or target change |

Retrieved and last revalidated: 2026-09-03.

## Primary owners by fact

| Fact | Primary source |
| --- | --- |
| Classic shell, `.wrap`, heading, and `782px` behavior | pinned `wp-admin/css/common.css` |
| Form-table rhythm, mobile form reflow, and mobile controls | pinned `wp-admin/css/forms.css` |
| Notice relocation and `.inline` behavior | pinned `src/js/_enqueues/admin/common.js` |
| Settings and menu APIs | WordPress Plugin Handbook and Code Reference |
| WPDS gap, padding, density, public exports, and semantic-token policy | pinned `@wordpress/theme` package exports, runtime index, exported design-token CSS, README, and `dimension.json` |
| Experimental bundled UI and `Stack` direction/gap behavior | pinned `@wordpress/ui` README and source |
| Modern `Page` shell | pinned `@wordpress/admin-ui` source |
| Stable `Flex` contract | pinned `@wordpress/components` source and official component reference |
| PHP and JavaScript i18n | WordPress Plugin Handbook, Common APIs, Block Editor Handbook, Code Reference, and WP-CLI i18n commands |
| Accessibility | WordPress Accessibility Coding Standards and WCAG 2.2 |

Official entry points:

- <https://developer.wordpress.org/plugins/settings/settings-api/>
- <https://developer.wordpress.org/plugins/administration-menus/>
- <https://developer.wordpress.org/block-editor/reference-guides/components/>
- <https://developer.wordpress.org/coding-standards/wordpress-coding-standards/accessibility/>
- <https://www.w3.org/TR/WCAG22/>
- <https://developer.wordpress.org/plugins/internationalization/how-to-internationalize-your-plugin/>
- <https://developer.wordpress.org/apis/internationalization/internationalization-guidelines/>
- <https://developer.wordpress.org/block-editor/how-to-guides/internationalization/>

Observed selectors are compatibility evidence, not automatically supported
public extension APIs. When a source changes, update the fact label first, then
re-evaluate the derived Skill-Norm. Never silently preserve a stale number or
experimental contract.
