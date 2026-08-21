# Reproducibility and release evidence

## Scope of this evidence

This document describes how to reproduce package and repository checks. Passing these checks demonstrates only that the listed commands completed for the stated source and environment. It does not demonstrate vehicle safety, real-time behavior, geofence accuracy under GPS uncertainty, model quality, or operational fitness.

## Supported release contract

- Package: `autoguard-ai` version `0.1.0`
- Supported Python: 3.11 and 3.12
- Release source: an immutable GitHub tag beginning with `v`
- Release artifacts: source distribution, wheel, `SHA256SUMS`, JUnit XML, coverage XML, and GitHub build provenance attestation
- Release gate: `pytest` excluding microbenchmarks with coverage at or above 85%, followed by `python -m build` and `twine check`

## Clean checkout procedure

```bash
git clone https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform.git
cd AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform
git checkout v0.1.0
python3.11 -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
PYTHONPATH=. pytest tests --ignore=tests/benchmarks --cov=. --cov-report=xml --junitxml=pytest-results.xml --cov-fail-under=85
python -m build
python -m twine check dist/*
sha256sum dist/* > dist/SHA256SUMS
```

On Windows PowerShell, replace `sha256sum dist/*` with:

```powershell
Get-FileHash dist\* -Algorithm SHA256
```

## Local validation record

The release hardening change was validated on 2026-08-21 from a clean virtual environment using Python 3.12.13 on Windows. The package-level checks use the same commands as the release workflow, except that GitHub Actions runs its release gate on Ubuntu with Python 3.11.

| Check | Command | Result |
|---|---|---|
| Dependency consistency | `python -m pip check` | Passed: no broken requirements |
| Test gate | `PYTHONPATH=. pytest tests --ignore=tests/benchmarks --cov=. --cov-fail-under=85` | Passed: 60 tests; 97.70% coverage |
| Distribution build | `python -m build` | Passed: one `.tar.gz` and one `py3-none-any.whl` |
| Metadata rendering | `python -m twine check dist/*` | Passed for both distributions |
| CI dependency vulnerability check | `python -m pip_audit -r requirements-ci.txt` | Passed: no known vulnerabilities |
| Integrity | `sha256sum dist/* > dist/SHA256SUMS` | Published as a release asset |

The local Windows run must use `--basetemp .pytest-tmp` if host policy denies access to the default user temporary directory. That condition is an execution-environment restriction, not an application test failure.

## Verifying a release download

1. Download the wheel or source distribution, `SHA256SUMS`, and the release attestation from the same GitHub release.
2. Compute the SHA-256 hash locally and compare it with the matching `SHA256SUMS` entry.
3. Inspect the GitHub artifact attestation and confirm its subject digest matches the downloaded artifact.
4. Install in a new virtual environment and run the clean-checkout test command above.

Do not use a benchmark run from a different host, Python version, CPU, network configuration, or commit as evidence for a release timing claim. Store the raw benchmark JSON with its command, commit, environment, and hardware provenance before comparing runs.

## Known reproducibility limits

- `requirements-ci.txt` defines the CI dependency set but is not hash-locked. Its compatible-version ranges are intentionally bounded in the package extras; a future release should add a generated, hash-locked constraints file per supported platform.
- GPU/CUDA code and full ML dependencies are optional and outside the core wheel build. Reproducing those experiments requires a separately recorded CUDA/Torch/toolchain environment.
- External Google-geocoding responses, network behavior, and credentials are not reproducible test inputs and are excluded from the geometry benchmark.
