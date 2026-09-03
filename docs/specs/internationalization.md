# Internationalization contract

Status: frozen for implementation

Internationalization is a string, runtime, and layout invariant. It applies to
visible text, accessible names, screen-reader text, alternative text, notices,
errors, empty states, dates, numbers, and action labels.

Examples below use the fixture slug and literal text domain
`wordpress-backend-skill-fixture`. A real plugin replaces both with its own
lowercase hyphenated slug and uses that same literal domain everywhere.

## PHP strings

- Use WordPress gettext functions with a literal text domain.
- Translate complete phrases. Do not assemble grammar from translated
  fragments.
- Use positional placeholders when translators may reorder values.
- Use `_n()` for plurals and `_x()` when identical source text needs context.
- Put a `translators:` comment immediately before a string with a non-obvious
  placeholder or context.
- Treat translations as untrusted. Escape for the final output context with
  functions such as `esc_html__()`, `esc_attr__()`, `esc_html()`, or
  `wp_kses_post()` as appropriate. Do not make a URL translatable.

```php
/* translators: %1$s: site name, %2$d: number of pending items. */
$message = sprintf(
    __( '%1$s has %2$d pending items.', 'wordpress-backend-skill-fixture' ),
    $site_name,
    $count
);

echo esc_html( $message );
```

## JavaScript strings

- Register `wp-i18n` or declare `@wordpress/i18n` through the build dependency
  metadata. Use the same literal text domain as PHP.
- Use complete phrases, positional placeholders, `_n()`, `_x()`, and immediate
  translator comments by the same rules as PHP.
- Accessible strings are translated too.
- Escape or render through a component contract appropriate to the final DOM
  context. Translation does not make HTML safe.

```js
import { __, sprintf } from '@wordpress/i18n';

/* translators: %s: settings section name. */
const message = sprintf(
    __( 'Settings for %s were saved.', 'wordpress-backend-skill-fixture' ),
    sectionName
);
```

## Runtime loading

Register the custom plugin language path at `init`:

```php
add_action(
    'init',
    static function () {
        load_plugin_textdomain(
            'wordpress-backend-skill-fixture',
            false,
            dirname( plugin_basename( __FILE__ ) ) . '/languages'
        );
    }
);
```

Register the script before attaching translations, then enqueue it:

```php
wp_register_script(
    'wordpress-backend-skill-fixture-app',
    plugins_url( 'build/index.js', __FILE__ ),
    array( 'wp-components', 'wp-date', 'wp-element', 'wp-i18n' ),
    $version,
    true
);

wp_set_script_translations(
    'wordpress-backend-skill-fixture-app',
    'wordpress-backend-skill-fixture',
    plugin_dir_path( __FILE__ ) . 'languages'
);

wp_enqueue_script( 'wordpress-backend-skill-fixture-app' );
```

The handle passed to `wp_set_script_translations()` is the registered handle,
not a source filename.

## Reproducible language artifacts

1. Build JavaScript, then extract PHP and the registered build JavaScript to a
   POT with `wp i18n make-pot --exclude=src`; this prevents a conflicting
   source-path reference.
2. Maintain `languages/wordpress-backend-skill-fixture-de_DE.po` against that
   POT.
3. Compile it with `wp i18n make-mo` to
   `languages/wordpress-backend-skill-fixture-de_DE.mo`.
4. Run `wp i18n make-json --no-purge` against the same PO.
5. PO source references for the registered script use `build/index.js`, not
   `src/index.js`. The generated Jed JSON filename uses the MD5 of the
   registered relative build path unless the documented handle filename form
   is deliberately used.
6. Set the site locale, then set the admin user's locale. Verify
   `determine_locale()` before testing.
7. Prove one translated PHP string and one translated React string in the
   browser. POT extraction alone is not runtime evidence.

The repository fixture keeps POT and PO as authored artifacts and commits its
generated MO and path-hashed Jed JSON. A clean checkout therefore contains the
exact runtime inputs; all artifacts are regenerated after translatable source
or build-path changes.

Core language packs may be installed for realism, but the fixture's bundled MO
and JSON artifacts own the plugin translation proof.

## Dates and numbers

- PHP dates use `wp_date()` and PHP numbers use `number_format_i18n()`.
- JavaScript dates use `dateI18n` from `@wordpress/date` with WordPress date
  settings.
- The baseline supplies client-visible localized numbers from PHP through
  `number_format_i18n()`. A client-only number, percentage, or currency
  formatter requires a separately sourced API, an explicit WordPress-locale to
  formatter-locale mapping, and a browser test. Do not invent a BCP-47 mapping.

## Layout and bidirectionality

- Plan for doubled string length and long German labels.
- Use logical properties and preserve source order in RTL.
- Controls, notices, errors, and actions wrap without clipping or page overflow.
- Do not shorten or fragment a translatable phrase to make layout pass.
- Test at least one RTL locale and locale-specific number and date output.

## Reject

- Variable or mismatched text domains.
- Concatenated translated fragments.
- Unnumbered placeholders when reordering may be required.
- Missing translator comments for non-obvious placeholders.
- Raw translated HTML or attributes without context-aware escaping.
- User-facing literals, including ARIA text, outside i18n functions.
- `wp_set_script_translations()` before script registration or with the wrong
  handle/path.
- PO references to `src/` when WordPress registers a `build/` script.
- POT, PO, hard-coded German, or layout screenshots presented as proof that
  WordPress loaded PHP and JavaScript translations.
