# BioBeat UI Automation Home Assignment

Live Playwright UI automation suite for the BioBeat Patient Admission workflow.

## Target Application

- URL: `https://bpm-demo.eu.bio-beat.cloud/login`
- Business hierarchy: `Clients -> Departments -> Patients -> Sessions`

Verified live behavior used by the suite:

- Session Management is the reliable source for admission verification.
- Patient Lookup may lag behind newly created admissions.
- Session removal requires the same Patient ID, not Device ID.
- Assignment-capable device availability is live-data dependent, so the suite uses the known-good assignment devices `989898` and `676767`.
- Device reuse is validated deterministically by creating a live session first and then proving the same device returns `Device is in use.` when reassigned.
- Verified invalid device state:
  - `676733`: not activated or does not exist

## Repository Layout

```text
.
|-- .github/workflows/ui-tests.yml
|-- config/
|-- core/
|-- docs/
|   `-- manual_test_cases.md
|-- flows/
|   `-- admission_flow.py
|-- skills/
|-- test_data/
|   `-- patient_admission_cases.py
|-- tests/
|   `-- ui/
|       |-- patient_admission/
|       |   |-- conftest.py
|       |   |-- support.py
|       |   |-- test_admission_cleanup.py
|       |   |-- test_admission_happy_path.py
|       |   |-- test_admission_negative_validation.py
|       |   `-- test_admission_popup_behavior.py
|       |-- conftest.py
|       |-- test_login.py
|       `-- test_navigation.py
|-- ui/
|   `-- pages/
|-- utils/
|   `-- assertions.py
|-- .env.example
|-- conftest.py
|-- pyproject.toml
|-- pytest.ini
`-- run-tests.ps1
```

## Architecture Summary

- `config/`: typed runtime settings from environment variables.
- `ui/pages/`: locator-first page objects containing locators, UI actions, and data reads only.
- `flows/`: thin orchestration across page objects.
- `tests/ui/`: 24 scenario tests organized by login, navigation, happy path, validation, popup behavior, and cleanup.
- `utils/assertions.py`: small assertion facade used consistently across tests and fixtures.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .[dev]
python -m playwright install chromium
Copy-Item .env.example .env
```

Fill the local `.env` with the live credentials before running the suite locally:

```dotenv
WEB_BASE_URL= the provided url
BIOBEAT_USERNAME= the provided username
BIOBEAT_PASSWORD= the provided password
```

## Configuration

The suite reads the following environment variables:

- `WEB_BASE_URL`
- `BIOBEAT_USERNAME`
- `BIOBEAT_PASSWORD`
- `BROWSER`
- `HEADLESS`
- `SLOW_MO_MS`
- `DEFAULT_TIMEOUT_MS`
- `EXPECT_TIMEOUT_MS`
- `NAVIGATION_TIMEOUT_MS`
- `BROWSER_EVIDENCE_MODE`
- `IGNORE_HTTPS_ERRORS`
- `ARTIFACT_DIR`

For local runs, prefer the same names used by CI secrets:

- `BIOBEAT_USERNAME`
- `BIOBEAT_PASSWORD`

Compatibility aliases are also supported when a local environment already uses older names:

- `APP_USERNAME`
- `APP_PASSWORD`

## Evidence Modes

`BROWSER_EVIDENCE_MODE` supports:

- `full`: always attach screenshot, trace, video, and framework log evidence
- `failure_only`: record evidence during the run and attach it only when a test fails
- `screenshot_only`: attach only failure screenshots

Legacy values are normalized for compatibility:

- `always -> full`
- `on_failure -> failure_only`
- `off -> screenshot_only`

The `collect_all_evidence` marker overrides the global mode for a test and forces the full configured evidence set.

## Running Tests

Collect tests only:

```powershell
.venv\Scripts\python -m pytest tests\ui --collect-only -q
```

Run the complete UI suite:

```powershell
.venv\Scripts\python -m pytest tests\ui -m ui -q --alluredir artifacts\allure-results
```

Current live verified scope:

- 24 UI tests
- login, navigation, happy-path creation, popup behavior, cleanup, and validation coverage
- teardown cleanup for every generated `AUTO...` patient ID, even if a test fails after creation

Run smoke coverage:

```powershell
.venv\Scripts\python -m pytest tests\ui -m "ui and smoke" -q --alluredir artifacts\allure-results
```

Run through the helper script:

```powershell
.\run-tests.ps1
.\run-tests.ps1 -Headed -SlowMoMs 100
```

## Allure

Pytest writes raw Allure results to `artifacts\allure-results` when tests are run with `--alluredir`.

Generate a local HTML report after a run:

```powershell
allure generate artifacts\allure-results --clean -o artifacts\allure-report
allure open artifacts\allure-report
```

If you use the helper script, it also generates the HTML report automatically when the Allure CLI is installed:

```powershell
.\run-tests.ps1
```

At the end of a run, collect these folders if you want to archive the execution evidence locally:

- `artifacts\allure-results`
- `artifacts\allure-report`
- `artifacts\playwright`
- `artifacts\screenshots`
- `artifacts\logs`

## CI

Workflow: [`.github/workflows/ui-tests.yml`](.github/workflows/ui-tests.yml)

Expected GitHub repository secrets:

- `BIOBEAT_USERNAME`
- `BIOBEAT_PASSWORD`

These are the same variable names supported by the local `.env`, so local and CI configuration stay aligned.

Optional repository variable:

- `WEB_BASE_URL`

The workflow:

- installs Python dependencies
- installs Playwright Chromium
- runs `python -m pytest tests/ui -m ui -q --alluredir artifacts/allure-results`
- generates a multi-file Allure HTML report
- uploads Allure results
- uploads the Allure HTML report
- uploads Playwright screenshots, videos, traces, and logs
- publishes the HTML report to `gh-pages` for manual runs and pushes to `main`

Manual dispatch supports:

- `marker_selection=all_markers`: run the full `ui` suite
- `marker_selection=smoke`: run `ui and smoke`
- `marker_selection=custom`: run the expression provided in `custom_marker`
- `evidence_mode`: choose `failure_only`, `full`, or `screenshot_only`

## Manual Test Cases

See [docs/manual_test_cases.md](docs/manual_test_cases.md).

## Submission Notes

- The suite was verified live against the BioBeat application.
- Cleanup is centralized in fixture teardown and verified through a dedicated cleanup test.
- Any generated `AUTO...` patient IDs are cleaned after each test, even if the test fails mid-flow.
- The device reuse business rule is covered as an explicit negative test:
  - create a live session with an available device
  - attempt to reuse that same device for a second patient
  - assert `Device is in use.`
