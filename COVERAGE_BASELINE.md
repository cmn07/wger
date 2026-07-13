# Baseline coverage report

This repository contains a complete HTML coverage report for the automated
test suite that existed before the course group's contributions.

## Baseline

- Commit: `7fc2fddf9`
- Tests found: 1,776
- Tests skipped: 17
- Failures: 0
- Statements: 22,281
- Missing statements: 2,493
- Coverage: 89%
- Generated on: 2026-07-13
- Report entry point: [`htmlcov/index.html`](htmlcov/index.html)

The baseline commit immediately precedes commit `c89e892e0`, which introduced
the group's new pytest tests. Consequently, those new tests and all later
changes are excluded from this report.

## Reproduction

Run these commands from a clean checkout of commit `7fc2fddf9`, with the
project's development dependencies installed:

```shell
export DJANGO_SETTINGS_MODULE=settings.ci
coverage erase
coverage run --source=wger manage.py test --parallel auto --noinput
coverage combine
coverage html -d htmlcov
```

On PowerShell, set the environment variable with:

```powershell
$env:DJANGO_SETTINGS_MODULE = 'settings.ci'
```
