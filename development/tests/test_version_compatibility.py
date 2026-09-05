"""Execute the documented PHP enqueue example against both version branches."""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


root = Path(__file__).resolve().parents[1]
reference = root.parent / "wordpress-backend-ui" / "references" / "version-compatibility.md"
markdown = reference.read_text(encoding="utf-8")
match = re.search(r"```php\n(.*?)\n```", markdown, re.DOTALL)
if not match:
    raise SystemExit("FAIL: documented PHP example not found")

example = match.group(1)
php = shutil.which("php")
if not php:
    raise SystemExit("FAIL: php executable not found")

stub = r"""<?php
$registered = false;
$version = '7.0';
$calls = array();
function wp_style_is( $handle, $state ) { global $registered; return $registered; }
function wp_get_wp_version() { global $version; return $version; }
function plugins_url( $path, $file ) { return $path; }
function wp_enqueue_style( ...$args ) { global $calls; $calls[] = array( 'enqueue', $args ); }
function wp_add_inline_style( ...$args ) { global $calls; $calls[] = array( 'inline', $args ); }
function add_action( ...$args ) {}
"""
checks = r"""
function run_case( $core_version, $has_tokens, $hook ) {
    global $version, $registered, $calls;
    $version = $core_version;
    $registered = $has_tokens;
    $calls = array();
    plugin_slug_enqueue_summary_layout( $hook );
    return $calls;
}
echo json_encode( array(
    'core' => run_case( '7.1', true, 'settings_page_plugin-slug' ),
    'older' => run_case( '7.0', false, 'settings_page_plugin-slug' ),
    'other' => run_case( '7.1', true, 'tools_page_other' ),
    'unapproved_backport' => run_case( '7.0.4', true, 'settings_page_plugin-slug' ),
    'missing_core_handle' => run_case( '7.1', false, 'settings_page_plugin-slug' ),
    'stable_patch' => run_case( '7.1.1', true, 'settings_page_plugin-slug' ),
    'next_prerelease' => run_case( '7.2-alpha', true, 'settings_page_plugin-slug' ),
    'patch_prerelease' => run_case( '7.1.1-alpha', true, 'settings_page_plugin-slug' ),
) );
"""
result = subprocess.run(
    [php], input=stub + example + checks, text=True, capture_output=True, check=False
)
if result.returncode:
    print(result.stderr, file=sys.stderr)
    raise SystemExit("FAIL: documented PHP example did not execute")

data = json.loads(result.stdout)
core_enqueue = data["core"][0][1]
older_enqueue = data["older"][0][1]
assert core_enqueue[2] == ["wp-theme"], core_enqueue
assert older_enqueue[2] == [], older_enqueue
assert "var(--wpds-dimension-gap-lg)" in data["core"][1][1][1]
assert "gap: 16px" in data["older"][1][1][1]
assert data["other"] == []
for case in ("unapproved_backport", "missing_core_handle", "next_prerelease", "patch_prerelease"):
    assert data[case][0][1][2] == [], data[case]
    assert "gap: 16px" in data[case][1][1][1], data[case]
assert data["stable_patch"][0][1][2] == ["wp-theme"]
assert "var(--wpds-dimension-gap-lg)" in data["stable_patch"][1][1][1]
assert "--wpds-dimension-gap-lg:" not in markdown
assert "var(--wpds-dimension-gap-lg, 16px)" not in markdown
assert "import { ThemeProvider } from '@wordpress/theme';" in markdown
assert "Private API unlocking is forbidden" in markdown
assert "No mandatory tokens, React, or component conversion" in markdown
print("VALID: versioned Core-token/fallback enqueue behavior and public-provider source guidance")
