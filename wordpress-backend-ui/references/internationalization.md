# PHP, JavaScript, and layout internationalization

Use one literal text domain equal to the lowercase hyphenated plugin slug. Apply
the contract to visible text, ARIA labels, screen-reader text, alternative text,
notices, errors, empty states, dates, and numbers.

## PHP

- Use WordPress gettext functions with the literal domain.
- Translate complete phrases instead of concatenating translated fragments.
- Use positional placeholders, `_n()` for plurals, and `_x()` for context.
- Put `translators:` comments immediately before non-obvious placeholders.
- Treat translations as untrusted and escape for the final output context.
- Keep URLs and structural markup outside translatable strings unless a safe
  documented markup pattern requires otherwise.

```php
/* translators: %1$s: site name, %2$d: pending item count. */
$message = sprintf(
    __( '%1$s has %2$d pending items.', 'plugin-slug' ),
    $site_name,
    $count
);

echo esc_html( $message );
```

## JavaScript

- Use `@wordpress/i18n` or the registered `wp-i18n` dependency.
- Use the same literal domain, complete phrases, positional placeholders,
  plural/context APIs, and immediate translator comments.
- Translate accessible text too.
- Rendering through React does not make translated HTML safe.

```js
import { __, sprintf } from '@wordpress/i18n';

/* translators: %s: settings section name. */
const message = sprintf(
    __( 'Settings for %s were saved.', 'plugin-slug' ),
    sectionName
);
```

## Load translations

Register a custom language path at `init` when the plugin bundles translations:

```php
add_action( 'init', static function () {
    load_plugin_textdomain(
        'plugin-slug',
        false,
        dirname( plugin_basename( __FILE__ ) ) . '/languages'
    );
} );
```

Register the JavaScript handle first, attach translations to that exact handle
and literal domain with an explicit language path, then enqueue:

```php
$asset = require plugin_dir_path( __FILE__ ) . 'build/index.asset.php';

wp_register_script(
    'plugin-slug-app',
    plugins_url( 'build/index.js', __FILE__ ),
    $asset['dependencies'],
    $asset['version'],
    true
);

wp_set_script_translations(
    'plugin-slug-app',
    'plugin-slug',
    plugin_dir_path( __FILE__ ) . 'languages'
);

wp_enqueue_script( 'plugin-slug-app' );
```

The build-generated dependency list is authoritative. This prevents missing
runtime handles such as `react` or `react-jsx-runtime` when the build emits
them.

## Reproducible artifact chain

1. After the JavaScript build, `wp i18n make-pot` extracts PHP and the
   registered build JavaScript to POT. Exclude `src` so the PO cannot acquire a
   source-path reference that disagrees with the registered script path.
2. Maintain `<domain>-<locale>.po` against the POT.
3. `wp i18n make-mo` creates `<domain>-<locale>.mo` in `languages/`.
4. `wp i18n make-json --no-purge` creates Jed JSON from the same PO.
5. PO source references use the registered `build/index.js`, not `src/index.js`.
   The generated filename uses the MD5 of the registered relative build path
   unless the documented handle filename form is deliberately used.
6. Set site locale, then admin-user locale, and verify `determine_locale()`.
7. Assert one genuinely translated PHP string and one translated React string
   in a browser.

The acceptance fixture keeps POT and PO as authored artifacts and commits its
generated MO and path-hashed Jed JSON so a clean checkout contains the exact
runtime proof inputs. Regenerate all four after translatable source or build
path changes.

POT extraction, a PO file, or hard-coded translated text does not prove runtime
loading.

## Dates and numbers

- PHP uses `wp_date()` and `number_format_i18n()`.
- JavaScript dates use `dateI18n` from `@wordpress/date`.
- The baseline passes PHP-formatted numbers to client UI. A client-only number,
  currency, or percentage formatter requires an authoritative API, explicit
  locale mapping, and a browser test. Do not derive BCP-47 by replacing `_`
  with `-` without a source-backed contract.

## Layout

Test doubled strings, long German labels, one RTL locale, and locale-dependent
dates and numbers. Use logical properties, allow controls and actions to wrap,
and preserve information, function, and source order. Fix presentation instead
of shortening or fragmenting translatable copy.

Reject variable domains, concatenated grammar, missing placeholder comments,
unescaped output, untranslated accessible text, wrong handle order, `src/`
references for a registered `build/` script, and translation artifacts claimed
as runtime proof without browser assertions.
