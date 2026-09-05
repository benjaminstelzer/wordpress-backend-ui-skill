"""Inspect local WordPress 7.0 and 7.1 Core sources without changing either site."""

import re
import sys
from pathlib import Path


if len(sys.argv) != 3:
    raise SystemExit("usage: test_local_wordpress_compatibility.py WORDPRESS_7_0 WORDPRESS_7_1")


def version(root: Path) -> str:
    text = (root / "wp-includes" / "version.php").read_text(encoding="utf-8")
    match = re.search(r"\$wp_version\s*=\s*'([^']+)'", text)
    if not match:
        raise AssertionError(f"version not found in {root}")
    return match.group(1)


wp70, wp71 = map(Path, sys.argv[1:])
assert re.fullmatch(r"7\.0(?:\.\d+)?", version(wp70)), version(wp70)
assert re.fullmatch(r"7\.1(?:\.\d+)?", version(wp71)), version(wp71)

loader70 = (wp70 / "wp-includes" / "script-loader.php").read_text(encoding="utf-8")
loader71 = (wp71 / "wp-includes" / "script-loader.php").read_text(encoding="utf-8")
assert "'theme'                => array()," not in loader70
assert "'theme'                => array()," in loader71
assert "'components'           => array( 'wp-theme' )," in loader71
assert 'design-tokens$suffix.css' in loader71

tokens = (
    wp71 / "wp-includes" / "css" / "dist" / "theme" / "design-tokens.css"
).read_text(encoding="utf-8")
for declaration in (
    "--wpds-dimension-gap-lg: 16px;",
    "--wpds-dimension-padding-2xl: 24px;",
    "--wpds-color-background-surface-neutral-strong: #fff;",
    "--wpds-color-foreground-content-neutral: #1e1e1e;",
    "--wpds-color-stroke-surface-neutral-weak: #f0f0f0;",
):
    assert declaration in tokens, declaration

theme_js = (wp71 / "wp-includes" / "js" / "dist" / "theme.js").read_text(
    encoding="utf-8"
)
assert re.search(r"__export\(index_exports,\s*\{\s*ThemeProvider:", theme_js)
assert "alternative: \"`ThemeProvider` from `@wordpress/theme`\"" in theme_js
print("VALID: local WordPress 7.0/7.1 registration, token, and public-export boundary")
