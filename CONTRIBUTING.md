# Contributing to AutoGuard AI

Thank you for your interest in contributing! Please follow the guidelines below.

## Development setup

```bash
# 1. Clone the repo
git clone https://github.com/CoreyLeath-code/AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform.git
cd AutoGuard-AI-Real-Time-Autonomous-Vehicle-Safety-Geofencing-Platform

# 2. Create a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
make install

# 4. Start backing services (Kafka + Redis)
make infra-up
```

See [`docs/development.md`](docs/development.md) for the full guide.

## Branching and commit conventions

- Create feature branches from `main`: `git checkout -b feat/my-feature`
- Use conventional commit messages:
  - `feat:` – new feature
  - `fix:` – bug fix
  - `refactor:` – code restructure with no behaviour change
  - `docs:` – documentation only changes
  - `chore:` – dependency bumps, CI tweaks, etc.
- Keep commits focused; one logical change per commit.

## Pull requests

1. Open PRs against the `main` branch.
2. Include a clear description of **what** changed and **why**.
3. Ensure CI passes (`pytest`, coverage, Trivy scan).
4. Request a review from at least one maintainer.

## Code style

- Python: follow [PEP 8](https://peps.python.org/pep-0008/); max line length 120 characters.
- C++: follow [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html).
- YAML/JSON/Terraform: 2-space indent, as enforced by `.editorconfig`.

## Reporting issues

Use GitHub Issues and fill in the provided template. Include reproduction steps, expected vs actual behaviour, and environment details.

## Security vulnerabilities

Please report security issues privately via the GitHub "Security" → "Report a vulnerability" workflow rather than opening a public issue.
