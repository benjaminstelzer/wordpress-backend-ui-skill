[CmdletBinding()]
param(
    [string] $XamppRoot = $env:XAMPP_LITE_ROOT,
    [string] $ManifestPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repositoryRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($ManifestPath)) {
    $ManifestPath = Join-Path $repositoryRoot 'fixture\native-xampp.json'
}
if ([string]::IsNullOrWhiteSpace($XamppRoot)) {
    throw 'Pass -XamppRoot or set XAMPP_LITE_ROOT.'
}

function Resolve-RequiredPath {
    param([string] $Path, [string] $Label)

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "$Label does not exist: $Path"
    }
    return (Resolve-Path -LiteralPath $Path).Path
}

function Resolve-WithinRoot {
    param([string] $Root, [string] $RelativePath, [string] $Label)

    $candidate = Resolve-RequiredPath -Path (Join-Path $Root $RelativePath) -Label $Label
    $rootPrefix = $Root.TrimEnd('\', '/') + [IO.Path]::DirectorySeparatorChar
    if (-not $candidate.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "$Label escapes the XAMPP root."
    }
    return $candidate
}

function Assert-Equal {
    param([string] $Actual, [string] $Expected, [string] $Label)

    if ($Actual -cne $Expected) {
        throw "$Label expected '$Expected' but observed '$Actual'."
    }
}

function Invoke-Native {
    param([string] $FilePath, [string[]] $Arguments, [string] $Label)

    Write-Verbose ("{0}: {1} {2}" -f $Label, $FilePath, ($Arguments -join ' '))
    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try {
        $lines = @(& $FilePath @Arguments 2>&1 | ForEach-Object { $_.ToString() })
        $exitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $previousPreference
    }
    if ($exitCode -ne 0) {
        $detail = ($lines -join [Environment]::NewLine).Trim()
        throw "$Label failed with exit code $exitCode.`n$detail"
    }
    return ($lines -join [Environment]::NewLine).Trim()
}

$manifestFile = Resolve-RequiredPath -Path $ManifestPath -Label 'Fixture manifest'
$manifest = Get-Content -LiteralPath $manifestFile -Raw | ConvertFrom-Json
if ($manifest.schema_version -ne 1) {
    throw "Unsupported fixture manifest schema: $($manifest.schema_version)"
}

$xampp = Resolve-RequiredPath -Path $XamppRoot -Label 'XAMPP root'
$php = Resolve-WithinRoot -Root $xampp -RelativePath $manifest.binaries.php -Label 'PHP binary'
$wpCli = Resolve-WithinRoot -Root $xampp -RelativePath $manifest.binaries.wp_cli -Label 'WP-CLI phar'
$apache = Resolve-WithinRoot -Root $xampp -RelativePath $manifest.binaries.apache -Label 'Apache binary'
$mariaDb = Resolve-WithinRoot -Root $xampp -RelativePath $manifest.binaries.mariadb -Label 'MariaDB binary'
$pluginSource = Resolve-RequiredPath -Path (Join-Path $repositoryRoot $manifest.plugin_source) -Label 'Fixture plugin source'

foreach ($relativeArtifact in $manifest.required_build_artifacts) {
    [void](Resolve-RequiredPath -Path (Join-Path $repositoryRoot $relativeArtifact) -Label "Build artifact $relativeArtifact")
}

$previousXamppRoot = $env:XAMPP_LITE_ROOT
$env:XAMPP_LITE_ROOT = $xampp

try {
    $phpVersion = Invoke-Native -FilePath $php -Arguments @('-d', 'error_reporting=8191', '-r', 'echo PHP_VERSION;') -Label 'PHP version check'
    Assert-Equal -Actual $phpVersion -Expected $manifest.runtime.php -Label 'PHP version'

    $wpCliOutput = Invoke-Native -FilePath $php -Arguments @('-d', 'error_reporting=8191', $wpCli, 'cli', 'version') -Label 'WP-CLI version check'
    if ($wpCliOutput -notmatch '^WP-CLI\s+(.+)$') {
        throw "Could not parse WP-CLI version: $wpCliOutput"
    }
    $wpCliVersion = $Matches[1].Trim()
    Assert-Equal -Actual $wpCliVersion -Expected $manifest.runtime.wp_cli -Label 'WP-CLI version'

    $apacheOutput = Invoke-Native -FilePath $apache -Arguments @('-v') -Label 'Apache version check'
    if ($apacheOutput -notmatch 'Apache/([0-9.]+)') {
        throw 'Could not parse Apache version.'
    }
    Assert-Equal -Actual $Matches[1] -Expected $manifest.runtime.apache -Label 'Apache version'

    $mariaOutput = Invoke-Native -FilePath $mariaDb -Arguments @('--version') -Label 'MariaDB version check'
    if ($mariaOutput -notmatch 'from\s+([0-9.]+)-MariaDB') {
        throw 'Could not parse MariaDB version.'
    }
    Assert-Equal -Actual $Matches[1] -Expected $manifest.runtime.mariadb -Label 'MariaDB version'

    $siteResults = @()
    foreach ($site in $manifest.sites) {
        $siteRoot = Resolve-WithinRoot -Root $xampp -RelativePath $site.relative_path -Label "WordPress site $($site.name)"
        [void](Resolve-RequiredPath -Path (Join-Path $siteRoot 'wp-config.php') -Label "wp-config.php for $($site.name)")

        $wpPrefix = @('-d', 'error_reporting=8191', $wpCli)
        $coreVersion = Invoke-Native -FilePath $php -Arguments ($wpPrefix + @('core', 'version', "--path=$siteRoot")) -Label "WordPress version for $($site.name)"
        Assert-Equal -Actual $coreVersion -Expected $site.wordpress -Label "WordPress version for $($site.name)"

        $modeFlag = Invoke-Native -FilePath $php -Arguments ($wpPrefix + @('eval', 'echo is_multisite() ? 1 : 0;', "--path=$siteRoot", '--skip-plugins', '--skip-themes')) -Label "Site mode for $($site.name)"
        if ($modeFlag -eq '1') {
            $mode = 'multisite'
        } elseif ($modeFlag -eq '0') {
            $mode = 'single'
        } else {
            throw "Could not parse site mode for $($site.name): $modeFlag"
        }
        Assert-Equal -Actual $mode -Expected $site.mode -Label "Site mode for $($site.name)"

        $activationArguments = $wpPrefix + @('plugin', 'is-active', $manifest.plugin_slug, "--path=$siteRoot")
        if ($site.plugin_activation -eq 'network-active') {
            $activationArguments += '--network'
        } elseif ($site.plugin_activation -ne 'active') {
            throw "Unsupported plugin activation mode in manifest: $($site.plugin_activation)"
        }
        [void](Invoke-Native -FilePath $php -Arguments $activationArguments -Label "Plugin activation for $($site.name)")

        $pluginLinkPath = Resolve-WithinRoot -Root $xampp -RelativePath (Join-Path $site.relative_path "wp-content\plugins\$($manifest.plugin_slug)") -Label "Plugin link for $($site.name)"
        $pluginLink = Get-Item -LiteralPath $pluginLinkPath -Force
        if ($pluginLink.LinkType -ne 'Junction') {
            throw "Plugin path for $($site.name) is not a junction."
        }
        $linkTarget = Resolve-RequiredPath -Path (@($pluginLink.Target)[0]) -Label "Plugin link target for $($site.name)"
        Assert-Equal -Actual $linkTarget.ToLowerInvariant() -Expected $pluginSource.ToLowerInvariant() -Label "Plugin link target for $($site.name)"

        $siteLocale = Invoke-Native -FilePath $php -Arguments ($wpPrefix + @('option', 'get', 'WPLANG', "--path=$siteRoot")) -Label "Site locale for $($site.name)"
        Assert-Equal -Actual $siteLocale -Expected $site.locale -Label "Site locale for $($site.name)"

        $adminIds = Invoke-Native -FilePath $php -Arguments ($wpPrefix + @('user', 'list', '--role=administrator', '--field=ID', "--path=$siteRoot")) -Label "Administrative user lookup for $($site.name)"
        $adminId = @($adminIds -split '\r?\n' | Where-Object { $_ -match '^\d+$' })[0]
        if ([string]::IsNullOrWhiteSpace($adminId)) {
            throw "No administrative test user for $($site.name)."
        }
        $adminLocale = Invoke-Native -FilePath $php -Arguments ($wpPrefix + @('user', 'meta', 'get', $adminId, 'locale', "--path=$siteRoot")) -Label "Admin locale for $($site.name)"
        Assert-Equal -Actual $adminLocale -Expected $site.locale -Label "Admin locale for $($site.name)"

        $localeProbe = "wp_set_current_user( $adminId ); echo determine_locale();"
        $determinedLocale = Invoke-Native -FilePath $php -Arguments ($wpPrefix + @('eval', $localeProbe, "--path=$siteRoot", '--skip-plugins', '--skip-themes')) -Label "Determined locale for $($site.name)"
        Assert-Equal -Actual $determinedLocale -Expected $site.locale -Label "Determined locale for $($site.name)"

        $siteResults += [pscustomobject]@{
            name = $site.name
            wordpress = $coreVersion
            mode = $mode
            plugin = $site.plugin_activation
            locale = $site.locale
        }
    }

    [pscustomobject]@{
        status = 'passed'
        xampp_root = $xampp
        php = $phpVersion
        wp_cli = $wpCliVersion
        apache = $manifest.runtime.apache
        mariadb = $manifest.runtime.mariadb
        sites = $siteResults
    } | ConvertTo-Json -Depth 4
}
finally {
    if ($null -eq $previousXamppRoot) {
        Remove-Item Env:XAMPP_LITE_ROOT -ErrorAction SilentlyContinue
    } else {
        $env:XAMPP_LITE_ROOT = $previousXamppRoot
    }
}
