#!/usr/bin/env python3
"""Validate frozen golden cases and package invariants without third-party modules."""

from __future__ import annotations

import json
import hashlib
import re
import sys
from pathlib import Path


REQUIRED_ROUTING_FIELDS = {
    "surface",
    "support_status",
    "runtime_owner",
    "shell_owner",
    "spacing_owner",
    "experimental_components_policy",
    "references",
    "prohibited_recommendations",
}
FLEX_GAPS = {4: 1, 8: 2, 12: 3, 16: 4, 24: 6, 32: 8, 40: 10}
VIEWPORTS = {783, 782, 600, 390, 320}
ARCHETYPES = {"focused-settings", "workflow-dashboard", "data-view"}


def load_json_yaml(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def sha256_text(path: Path) -> str:
    """Hash UTF-8 text with canonical LF line endings across Git checkouts."""
    canonical_text = path.read_text(encoding="utf-8")
    return hashlib.sha256(canonical_text.encode("utf-8")).hexdigest()


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    repository = root
    root = repository / "development"
    cases_dir = root / "tests" / "cases"

    manifest_path = cases_dir / "MANIFEST.sha256"
    manifest_entries: dict[str, str] = {}
    if manifest_path.is_file():
        for line_number, line in enumerate(manifest_path.read_text(encoding="utf-8").splitlines(), start=1):
            match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9._-]+\.yaml)", line)
            require(bool(match), f"oracle manifest:{line_number}: invalid line", errors)
            if match:
                manifest_entries[match.group(2)] = match.group(1)
    else:
        errors.append("oracle manifest: missing tests/cases/MANIFEST.sha256")
    case_paths = sorted(cases_dir.glob("*.yaml"), key=lambda path: path.name)
    require(
        set(manifest_entries) == {path.name for path in case_paths},
        "oracle manifest: file set does not match golden cases",
        errors,
    )
    for case_path in case_paths:
        actual_hash = sha256_text(case_path)
        require(
            manifest_entries.get(case_path.name) == actual_hash,
            f"oracle manifest:{case_path.name}: hash mismatch",
            errors,
        )

    routing = load_json_yaml(cases_dir / "routing.yaml")
    require(len(routing["cases"]) >= 12, "routing: fewer than 12 cases", errors)
    require(
        len({case["id"] for case in routing["cases"]}) == len(routing["cases"]),
        "routing: duplicate IDs",
        errors,
    )
    for case in routing["cases"]:
        missing = REQUIRED_ROUTING_FIELDS - case.keys()
        require(not missing, f"routing:{case['id']}: missing {sorted(missing)}", errors)
    routing_by_id = {case["id"]: case for case in routing["cases"]}
    require(
        {"route-editor-canvas", "route-profile-field"} <= routing_by_id.keys(),
        "routing: excluded surface coverage is incomplete",
        errors,
    )
    same_fields = set(routing["composition_invariant"]["same_wordpress_fields"])
    require(
        REQUIRED_ROUTING_FIELDS - {"references"} <= same_fields,
        "routing: composition invariant omits WordPress-owned output fields",
        errors,
    )

    agent_prompts = load_json_yaml(root / "tests" / "agent-prompts.json")
    require(agent_prompts.get("schema_version") == 1, "agent prompts: schema version", errors)
    require(agent_prompts.get("prohibited_match") == "required-subset", "agent prompts: prohibited match", errors)
    prompt_manifest = (root / "tests" / "agent-prompts.sha256").read_text(encoding="utf-8").strip()
    prompt_hash = sha256_text(root / "tests" / "agent-prompts.json")
    require(
        prompt_manifest == f"{prompt_hash}  agent-prompts.json",
        "agent prompts: frozen hash mismatch",
        errors,
    )
    require(len(agent_prompts.get("cases", [])) == 8, "agent prompts: exact case count", errors)
    prompt_fields = agent_prompts.get("output_fields", [])
    for prompt_case in agent_prompts.get("cases", []):
        source_case = routing_by_id.get(prompt_case.get("source_case"))
        require(source_case is not None, f"agent prompts: missing source for {prompt_case.get('id')}", errors)
        if source_case is None:
            continue
        require(
            prompt_case.get("input") == source_case.get("input"),
            f"agent prompts: input drift for {prompt_case['id']}",
            errors,
        )
        for field in prompt_fields:
            require(
                prompt_case.get("expected", {}).get(field) == source_case.get(field),
                f"agent prompts: {field} drift for {prompt_case['id']}",
                errors,
            )

    spacing = load_json_yaml(cases_dir / "spacing.yaml")
    for policy in ("allow", "deny", "unknown"):
        for pixels, multiplier in FLEX_GAPS.items():
            case_id = f"flex-{policy}-{pixels}"
            matches = [case for case in spacing["cases"] if case["id"] == case_id]
            require(len(matches) == 1, f"spacing: missing or duplicate {case_id}", errors)
            if len(matches) != 1:
                continue
            expected = matches[0]["expected"]
            require(expected.get("api") == "Flex", f"spacing:{case_id}: wrong API", errors)
            require(expected.get("direction") == "column", f"spacing:{case_id}: direction", errors)
            require(expected.get("align") == "stretch", f"spacing:{case_id}: align", errors)
            require(expected.get("justify") == "flex-start", f"spacing:{case_id}: justify", errors)
            require(expected.get("wrap") is False, f"spacing:{case_id}: wrap", errors)
            require(expected.get("expanded") is True, f"spacing:{case_id}: expanded", errors)
            require(expected.get("gap") == multiplier, f"spacing:{case_id}: gap", errors)
            require(
                {"FlexItem", "FlexBlock"} <= expected.get("child_roles", {}).keys(),
                f"spacing:{case_id}: child roles",
                errors,
            )
            if policy == "unknown":
                require(
                    expected.get("new_experimental_api") is False,
                    f"spacing:{case_id}: unknown introduced experimental API",
                    errors,
                )

    heading_intro = [case for case in spacing["cases"] if case["id"] == "wpds-heading-intro"]
    require(len(heading_intro) == 1, "spacing: missing or duplicate wpds-heading-intro", errors)
    if len(heading_intro) == 1:
        expected = heading_intro[0]["expected"]
        require(expected.get("direction") == "column", "spacing:wpds-heading-intro: direction", errors)
        require(expected.get("token") == "sm", "spacing:wpds-heading-intro: token", errors)
        require(expected.get("gap_px_default") == 8, "spacing:wpds-heading-intro: gap", errors)

    css = load_json_yaml(cases_dir / "css-ownership.yaml")
    for case in css["cases"]:
        if case["decision"] == "exception":
            require(bool(case.get("flex_gap_proven")), f"css:{case['id']}: no Flex gap", errors)
            require(bool(case.get("smallest_scope")), f"css:{case['id']}: no scope", errors)
            require(bool(case.get("required_checks")), f"css:{case['id']}: no checks", errors)

    responsive = load_json_yaml(cases_dir / "responsive.yaml")
    for archetype in ARCHETYPES:
        observed = {
            case["viewport_css_px"]
            for case in responsive["cases"]
            if case["archetype"] == archetype
        }
        require(observed == VIEWPORTS, f"responsive:{archetype}: wrong viewport matrix", errors)
    require(
        any(
            case.get("zoom_percent") == 400 and case.get("equivalent_css_width") == 320
            for case in responsive["cases"]
        ),
        "responsive: missing 400% zoom case",
        errors,
    )

    ui = load_json_yaml(cases_dir / "ui-guidance.yaml")
    ui_fields = {
        "navigation",
        "primary_action",
        "notice_owner",
        "inline_owner",
        "states",
        "recovery",
        "accessibility_invariants",
    }
    for case in ui["cases"]:
        require(not (ui_fields - case.keys()), f"ui:{case['id']}: incomplete", errors)

    i18n = load_json_yaml(cases_dir / "i18n.yaml")
    for language in ("php", "javascript"):
        for kind in ("positive", "negative"):
            require(
                any(case["language"] == language and case["kind"] == kind for case in i18n["cases"]),
                f"i18n: missing {language}/{kind}",
                errors,
            )
    require(i18n["registered_script_path"] == "build/index.js", "i18n: wrong build path", errors)

    package = json.loads((root / "package.json").read_text(encoding="utf-8"))
    required_versions = {
        "@wordpress/admin-ui": "1.8.1",
        "@wordpress/components": "32.2.1",
        "@wordpress/theme": "0.7.1",
        "@wordpress/ui": "0.7.1",
        "@wordpress/scripts": "32.0.0",
        "@playwright/test": "1.58.2",
    }
    for name, version in required_versions.items():
        require(
            package["devDependencies"].get(name) == version,
            f"package: {name} must equal {version}",
            errors,
        )
    require(package.get("license") == "MIT", "package: license must be MIT", errors)
    require("@wordpress/env" not in package["devDependencies"], "package: @wordpress/env must be absent", errors)
    require(
        "validate-xampp-fixtures.ps1" in package.get("scripts", {}).get("test:xampp", ""),
        "package: missing native XAMPP validation script",
        errors,
    )
    require((root / ".nvmrc").read_text(encoding="utf-8").strip() == "24", "package: .nvmrc", errors)

    license_text = (repository / "LICENSE").read_text(encoding="utf-8")
    require(
        license_text.startswith("MIT License\n")
        and "Copyright (c) 2026 Benjamin" in license_text
        and "Permission is hereby granted, free of charge" in license_text,
        "license: missing or non-canonical MIT grant",
        errors,
    )
    lock_package = json.loads((root / "package-lock.json").read_text(encoding="utf-8"))
    require(
        lock_package.get("packages", {}).get("", {}).get("license") == "MIT",
        "package-lock: root license must be MIT",
        errors,
    )

    for config_name in (".wp-env.json", ".wp-env.multisite.json"):
        require(not (root / config_name).exists(), f"package: obsolete {config_name} must be absent", errors)

    native_manifest = json.loads((root / "fixture" / "native-xampp.json").read_text(encoding="utf-8"))
    require(native_manifest.get("schema_version") == 1, "native fixture: schema version", errors)
    require(native_manifest.get("plugin_slug") == "wordpress-backend-skill-fixture", "native fixture: plugin slug", errors)
    expected_sites = {
        "single": ("www/wordpress-backend-skill-test", "7.0", "single", "active"),
        "network": ("www/wordpress-backend-skill-test-multisite", "7.0.4", "multisite", "network-active"),
    }
    observed_sites = {site.get("name"): site for site in native_manifest.get("sites", [])}
    require(set(observed_sites) == set(expected_sites), "native fixture: exact site set", errors)
    for name, expected in expected_sites.items():
        site = observed_sites.get(name, {})
        actual = (
            site.get("relative_path"),
            site.get("wordpress"),
            site.get("mode"),
            site.get("plugin_activation"),
        )
        require(actual == expected, f"native fixture: {name} contract", errors)
        require(site.get("locale") == "de_DE", f"native fixture: {name} locale", errors)

    skill_root = repository / "wordpress-backend-ui"
    skill_text = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    routing_reference = (skill_root / "references" / "routing.md").read_text(encoding="utf-8")
    for field in ("surface", "support_status", "runtime_owner", "shell_owner", "spacing_owner"):
        for value in {str(case[field]) for case in routing["cases"]}:
            require(
                f"`{value}`" in routing_reference,
                f"routing reference: missing canonical {field} value {value}",
                errors,
            )
    network_hybrid = next(case for case in routing["cases"] if case["id"] == "route-network-admin-hybrid")
    require(
        network_hybrid["experimental_components_policy"] == "deny",
        "routing: Core-only Network Admin hybrid must deny experimental components",
        errors,
    )
    classic_required = {
        "frontend-theme-spacing",
        "inject-wpds-into-classic",
        "global-wp-admin-overrides",
        "custom-css-before-core",
    }
    for case_id in ("route-classic-settings", "route-classic-tools", "route-network-admin-classic"):
        require(
            classic_required <= set(routing_by_id[case_id]["prohibited_recommendations"]),
            f"routing:{case_id}: missing Classic prohibition",
            errors,
        )
    links = re.findall(r"\]\((references/[^)]+)\)", skill_text)
    for link in links:
        require((skill_root / link).is_file(), f"skill: missing {link}", errors)

    for markdown_path in (repository / "README.md", repository / "CHANGELOG.md"):
        markdown = markdown_path.read_text(encoding="utf-8")
        for raw_link in re.findall(r"\]\(([^)]+)\)", markdown):
            link = raw_link.split("#", 1)[0]
            if not link or re.match(r"^[a-z][a-z0-9+.-]*:", link, flags=re.IGNORECASE):
                continue
            require(
                (markdown_path.parent / link).exists(),
                f"markdown:{markdown_path.name}: missing {raw_link}",
                errors,
            )
    require("[`LICENSE`](LICENSE)" in (repository / "README.md").read_text(encoding="utf-8"), "README: missing MIT license link", errors)
    require("Added the MIT license." in (repository / "CHANGELOG.md").read_text(encoding="utf-8"), "CHANGELOG: missing MIT license entry", errors)

    source_files = list((root / "fixture" / "plugin").rglob("*.php"))
    source_files += list((root / "fixture" / "plugin" / "src").rglob("*.*"))
    for path in source_files:
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if re.search(r"--wpds-[\w-]+\s*:", line):
                errors.append(f"fixture:{path.relative_to(root)}:{line_number}: defines --wpds-*")

    fixture_root = root / "fixture" / "plugin"
    fixture_php = (fixture_root / "wordpress-backend-skill-fixture.php").read_text(encoding="utf-8")
    fixture_js = (fixture_root / "src" / "index.js").read_text(encoding="utf-8")
    examples = (skill_root / "references" / "examples.md").read_text(encoding="utf-8")
    version_compatibility = (
        skill_root / "references" / "version-compatibility.md"
    ).read_text(encoding="utf-8")

    require(
        "import { ThemeProvider }" not in fixture_js and "<ThemeProvider" not in fixture_js,
        "fixture: provider import is unsupported by the pinned 7.0 package",
        errors,
    )
    require(
        "import { ThemeProvider }" not in examples and "<ThemeProvider" not in examples,
        "examples: keep the 7.1 public provider example in the versioned reference",
        errors,
    )
    require(
        "build/design-tokens.css" in examples,
        "examples: missing emitted token stylesheet",
        errors,
    )
    for contract in (
        r"preg_match( '/^7\.1(?:\.\d+)?$/', $wp_version )",
        "wp_style_is( 'wp-theme', 'registered' )",
        "array( 'wp-theme' )",
        "var(--wpds-dimension-gap-lg)",
        "import { ThemeProvider } from '@wordpress/theme';",
        "No mandatory tokens, React, or component conversion",
    ):
        require(
            contract in version_compatibility,
            f"version compatibility: missing {contract}",
            errors,
        )
    require(
        "var(--wpds-dimension-gap-lg, 16px)" not in version_compatibility,
        "version compatibility: hand-written token fallback in the source example",
        errors,
    )
    require("privateApis" not in fixture_js, "fixture: private theme API", errors)
    token_copy_script = (root / "scripts" / "copy-design-tokens.mjs").read_text(encoding="utf-8")
    require(
        "require.resolve( '@wordpress/theme/design-tokens.css' )" in token_copy_script,
        "fixture: missing public design-token export resolver",
        errors,
    )
    require(
        re.search(r"<Stack\b[^>]*\bdirection=\"column\"[^>]*\bgap=\"sm\"", fixture_js)
        is not None,
        "fixture: heading-to-intro Stack must use the semantic 8px gap",
        errors,
    )
    fallback_match = re.search(
        r"function WpdsLoadingRegion\b(?P<body>.*?)(?=\nfunction )",
        fixture_js,
        flags=re.DOTALL,
    )
    fallback_body = fallback_match.group("body") if fallback_match else ""
    require(
        bool(fallback_match)
        and 'data-wbui-wpds-fallback="true"' in fallback_body
        and '<h2 id="wbui-wpds-title"' in fallback_body
        and '<span role="status">' in fallback_body
        and "fallback={ <WpdsLoadingRegion title={ title } /> }" in fixture_js,
        "fixture: WPDS Suspense fallback lacks its aria-labelledby target",
        errors,
    )
    require("DOMAIN" not in fixture_js, "fixture: variable JavaScript text domain", errors)
    gettext_calls = re.findall(r"\b__\s*\((.*?)\)", fixture_js, flags=re.DOTALL)
    require(bool(gettext_calls), "fixture: no JavaScript gettext calls", errors)
    for index, call in enumerate(gettext_calls, start=1):
        require(
            re.search(r",\s*'wordpress-backend-skill-fixture'\s*$", call.strip()) is not None,
            f"fixture: JavaScript gettext call {index} lacks literal domain",
            errors,
        )

    require("__next40pxDefaultSize" in fixture_js, "fixture: current 40px component opt-in missing", errors)
    require(
        'className="wbui-fixture-action-row"' in fixture_js
        and 'direction="row"' in fixture_js
        and 'wrap={ true }' in fixture_js
        and "Reset test value" in fixture_js,
        "fixture: responsive primary/secondary action row is missing",
        errors,
    )
    require(
        'className="wbui-fixture-help-text"' in fixture_js
        and ".wbui-fixture-help-text" in (fixture_root / "src" / "style.scss").read_text(encoding="utf-8")
        and "4.04:1" in (fixture_root / "src" / "style.scss").read_text(encoding="utf-8"),
        "fixture: measured Core help-text contrast exception is missing",
        errors,
    )
    require("accessibleWhenDisabled" in fixture_js, "fixture: disabled action is not focusable", errors)
    require(
        "const [ state, setState ] = useState( fixtureData.state || 'initial' );" in fixture_js
        and "! [ 'empty', 'loading', 'error' ].includes( state )" in fixture_js
        and "fixtureData.state !== 'empty'" not in fixture_js,
        "fixture: empty-state recovery does not own data-view visibility",
        errors,
    )
    require(
        "'label_for' => 'wbui-fixture-endpoint'" in fixture_php,
        "fixture: classic settings field lacks label_for association",
        errors,
    )
    require(
        'aria-describedby={ disabledDescription }' in fixture_js,
        "fixture: disabled action lacks programmatic reason",
        errors,
    )
    state_feedback_match = re.search(
        r"function StateFeedback\b(?P<body>.*?)(?=\nfunction )",
        fixture_js,
        flags=re.DOTALL,
    )
    state_feedback_body = state_feedback_match.group("body") if state_feedback_match else ""
    core_workflow_match = re.search(
        r"function CoreWorkflow\b(?P<body>.*?)(?=\nfunction )",
        fixture_js,
        flags=re.DOTALL,
    )
    core_workflow_body = core_workflow_match.group("body") if core_workflow_match else ""
    require(
        bool(state_feedback_match)
        and bool(core_workflow_match)
        and 'role="status"' not in state_feedback_body
        and 'role="alert"' not in state_feedback_body
        and 'role="status"' not in core_workflow_body
        and 'role="alert"' not in core_workflow_body,
        "fixture: state messages duplicate the Core Notice speak() announcement path",
        errors,
    )
    require(
        state_feedback_body.count("actions={ [") == 4
        and state_feedback_body.count("spokenMessage={ message }") == 5
        and "label: __( 'Retry fixture checks'" in fixture_js
        and "label: __( 'Create example result'" in fixture_js
        and "label: __( 'Retry fixture load'" in fixture_js
        and "label: __( 'Return to the dashboard'" in fixture_js,
        "fixture: Notice recovery controls must use the public actions prop",
        errors,
    )
    require(
        "spokenMessage={ successMessage }" in core_workflow_body,
        "fixture: success Notice lacks an explicit message-only announcement",
        errors,
    )
    require(
        "is_network_admin() ? network_admin_url() : admin_url()" in fixture_php
        and "wbuiFixtureData?.dashboardUrl" in fixture_js,
        "fixture: permission recovery does not preserve admin context",
        errors,
    )
    require(
        "WBUI_FIXTURE_TIMESTAMP" in fixture_php
        and "wp_date( get_option( 'date_format' ), WBUI_FIXTURE_TIMESTAMP )" in fixture_php
        and "wp_date( get_option( 'date_format' ), time() )" not in fixture_php
        and "new Date()" not in fixture_js,
        "fixture: date output is not deterministic",
        errors,
    )
    require(
        "dateI18n( fixtureData.dateFormat, fixtureData.fixtureDateIso )" in fixture_js,
        "fixture: JavaScript date does not use the WordPress format and fixed value",
        errors,
    )
    fixture_scss = (fixture_root / "src" / "style.scss").read_text(encoding="utf-8")
    require(
        ".wbui-fixture-data-scroll" in fixture_scss and "&:focus-visible" in fixture_scss,
        "fixture: keyboard-scroll region lacks a visible focus rule",
        errors,
    )
    require("build/design-tokens.css" in fixture_php, "fixture: token CSS is not enqueued", errors)
    require("build/style-index.css" in fixture_php, "fixture: local CSS is not enqueued", errors)
    require(
        "wp_style_add_data( 'wordpress-backend-skill-fixture-style', 'rtl', 'replace' )" in fixture_php,
        "fixture: generated RTL stylesheet is not registered",
        errors,
    )
    require("add_settings_error(" in fixture_php, "fixture: no Core page Notice producer", errors)
    require("settings_errors(" in fixture_php, "fixture: no Core page Notice output", errors)
    for mode in ("classic", "core", "wpds", "hybrid"):
        require(f"'{mode}'" in fixture_php, f"fixture: missing runtime mode {mode}", errors)
    for state in ("initial", "loading", "partial", "empty", "success", "error", "disabled", "permission"):
        require(f"'{state}'" in fixture_php, f"fixture: missing state {state}", errors)
    require(
        "function wbui_fixture_get_notice()" in fixture_php
        and "wbui_fixture_get_notice();" in fixture_php,
        "fixture: page Notice is not independently owned",
        errors,
    )

    build_root = fixture_root / "build"
    for build_name in ("index.js", "index.asset.php", "design-tokens.css", "style-index.css", "style-index-rtl.css"):
        require((build_root / build_name).is_file(), f"fixture: missing build/{build_name}", errors)
    if (build_root / "index.asset.php").is_file():
        asset_text = (build_root / "index.asset.php").read_text(encoding="utf-8")
        require(
            "wp-theme/design-tokens.css" not in asset_text,
            "fixture: CSS subpath was externalized as a script dependency",
            errors,
        )
    if (build_root / "index.js").is_file():
        built_js = (build_root / "index.js").read_text(encoding="utf-8")
        require(
            "data-wbui-wpds-fallback" in built_js
            and "wbui-wpds-title" in built_js
            and built_js.count('role:"status"') == 1
            and 'role:"alert"' not in built_js,
            "fixture: built WPDS Suspense fallback is stale or incomplete",
            errors,
        )
    if (build_root / "design-tokens.css").is_file():
        built_css = (build_root / "design-tokens.css").read_text(encoding="utf-8")
        require(
            "--wpds-dimension-gap-sm:" in built_css,
            "fixture: built CSS does not contain exported WPDS tokens",
            errors,
        )

    language_root = fixture_root / "languages"
    pot_path = language_root / "wordpress-backend-skill-fixture.pot"
    po_path = language_root / "wordpress-backend-skill-fixture-de_DE.po"
    mo_path = language_root / "wordpress-backend-skill-fixture-de_DE.mo"
    json_hash = hashlib.md5(b"build/index.js").hexdigest()
    json_path = language_root / f"wordpress-backend-skill-fixture-de_DE-{json_hash}.json"
    for path, label in (
        (pot_path, "POT"),
        (po_path, "de_DE PO"),
        (mo_path, "de_DE MO"),
        (json_path, "de_DE Jed JSON"),
    ):
        require(path.is_file(), f"fixture: missing {label} artifact", errors)
    if po_path.is_file():
        po_text = po_path.read_text(encoding="utf-8")
        require("#: build/index.js" in po_text, "fixture: PO lacks build/index.js reference", errors)
        require("src/index.js" not in po_text, "fixture: PO contains forbidden src/index.js reference", errors)
        require(
            'msgid "Core Components workflow"' in po_text and 'msgstr "Core-Komponenten-Ablauf"' in po_text,
            "fixture: PO lacks representative React translation",
            errors,
        )
        require(
            'msgid "Backend UI Fixture"' in po_text and 'msgstr "Backend-UI-Testoberfläche"' in po_text,
            "fixture: PO lacks representative PHP translation",
            errors,
        )

    i18n_script = package.get("scripts", {}).get("i18n:pot", "")
    require("--exclude=src" in i18n_script, "package: i18n POT command must exclude src", errors)

    fixture_readme = (root / "fixture" / "README.md").read_text(encoding="utf-8")
    for command in (
        "npm run test:xampp -- -XamppRoot",
        "fixture/native-xampp.json",
        "validate-xampp-fixtures.ps1",
    ):
        require(command in fixture_readme, f"fixture docs: missing {command}", errors)

    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAILED: {len(errors)} error(s)")
        return 1
    print("VALID: frozen contracts, package pins, fixture ownership, and skill links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
