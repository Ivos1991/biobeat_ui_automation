param(
    [ValidateSet("failure_only", "full", "screenshot_only")] [string]$EvidenceMode = "failure_only",
    [switch]$Headed,
    [int]$SlowMoMs = 0,
    [ValidateSet("chromium", "firefox", "webkit")] [string]$Browser = "chromium",
    [string]$PytestTarget = "tests\ui",
    [string]$PytestMarker = "ui",
    [switch]$OpenReport
)

$ErrorActionPreference = "Stop"

$python = ".\.venv\Scripts\python"
$allureResultsDir = "artifacts\allure-results"
$allureReportDir = "artifacts\allure-report"

$env:BROWSER_EVIDENCE_MODE = $EvidenceMode
$env:BROWSER = $Browser
$env:HEADLESS = if ($Headed) { "false" } else { "true" }
$env:SLOW_MO_MS = $SlowMoMs.ToString()

$pytestArgs = @(
    "-m",
    "pytest",
    $PytestTarget,
    "-q",
    "-rs",
    "--alluredir",
    $allureResultsDir
)

if ($PytestMarker -ne "") {
    $pytestArgs += @("-m", $PytestMarker)
}

& $python @pytestArgs

$allureCli = Get-Command allure.cmd -ErrorAction SilentlyContinue
if ($null -ne $allureCli) {
    & $allureCli.Source generate $allureResultsDir --clean -o $allureReportDir
    Write-Host "Allure report generated at $allureReportDir"
    Write-Host "Open it with: & `"$($allureCli.Source)`" open $allureReportDir"

    if ($OpenReport) {
        & $allureCli.Source open $allureReportDir
    }
}
else {
    Write-Warning "allure.cmd was not found on PATH. Allure results are still available in $allureResultsDir."
}
