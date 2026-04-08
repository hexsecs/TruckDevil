# RELEASING.md

Release instructions for TruckDevil using the `Publish` GitHub Actions workflow.

## Overview

TruckDevil now builds and publishes from GitHub Actions using `uv` and PyPI trusted publishing.

Release flow:

1. Merge packaging/release changes to upstream `main`
2. Configure trusted publishers on TestPyPI and PyPI
3. Run a TestPyPI dry run from `main`
4. Verify installation from TestPyPI
5. Publish to PyPI

## Repository Assumptions

These instructions assume the canonical repository is:

- repo: `LittleBlondeDevil/TruckDevil`
- default branch: `main`
- publish workflow path: `.github/workflows/publish.yml`

If any of those change, trusted publisher settings must match the new values exactly.

## Workflow Files

- CI: `.github/workflows/ci.yml`
- Publish: `.github/workflows/publish.yml`

The publish workflow:

- builds distributions with `uv build`
- publishes to TestPyPI via `workflow_dispatch` with `repository=testpypi`
- publishes to PyPI from `v*` tags or manual dispatch with `repository=pypi`

## Trusted Publisher Setup

Trusted publishing is the only release prerequisite that cannot be validated from a fork.

Configure TestPyPI and PyPI to trust this exact upstream workflow identity:

- Owner: `LittleBlondeDevil`
- Repository: `TruckDevil`
- Workflow file: `.github/workflows/publish.yml`
- Branch: `main`

For the GitHub Actions environments used by the workflow, keep these environment names:

- `testpypi`
- `pypi`

If using environment-scoped trusted publishing, the expected identities are:

- TestPyPI environment: `testpypi`
- PyPI environment: `pypi`

The fork `hexsecs/TruckDevil` cannot satisfy the upstream trusted publisher claims, so dry-run failures there are expected and do not indicate a packaging problem.

## One-Time TestPyPI Setup

1. Sign in to TestPyPI with the maintainer account that owns the package.
2. Create the `truckdevil` project on TestPyPI if it does not exist yet.
3. Add a trusted publisher for:
   - repository owner: `LittleBlondeDevil`
   - repository name: `TruckDevil`
   - workflow file: `.github/workflows/publish.yml`
   - branch: `main`
   - environment: `testpypi`

## One-Time PyPI Setup

1. Sign in to PyPI with the maintainer account that owns the package.
2. Create or claim the `truckdevil` project on PyPI if needed.
3. Add a trusted publisher for:
   - repository owner: `LittleBlondeDevil`
   - repository name: `TruckDevil`
   - workflow file: `.github/workflows/publish.yml`
   - branch: `main`
   - environment: `pypi`

## Pre-Release Checklist

Before publishing from upstream:

1. Ensure the branch is merged to `main`
2. Ensure the version in `truckdevil/__init__.py` and `pyproject.toml` is correct
3. Ensure CI is green
4. Ensure `uv.lock` is committed if dependency changes were made
5. Ensure `README.md` install instructions match the current package behavior

## Local Validation

From repo root:

```bash
uv sync
uv run pytest tests/ -v
uv run flake8 . --max-line-length=120
uv build
uv tool install .
truckdevil --version
```

Install-smoke validation against built artifacts:

```bash
uv venv .venv-release-smoke
uv pip install --python .venv-release-smoke/bin/python dist/truckdevil-*.whl
./.venv-release-smoke/bin/truckdevil --version
./.venv-release-smoke/bin/python -c "from importlib.resources import files; resource = files('truckdevil').joinpath('resources', 'json_files', 'pgn_list.json'); assert resource.is_file(), resource"
```

## TestPyPI Dry Run

After merge to upstream `main`, run the publish workflow manually:

1. Open Actions in `LittleBlondeDevil/TruckDevil`
2. Select `Publish`
3. Choose `Run workflow`
4. Set `repository` to `testpypi`
5. Run from branch `main`

Expected outcome:

- build succeeds
- publish to TestPyPI succeeds

## Verify TestPyPI Install

After a successful TestPyPI publish, verify installability:

CLI install:

```bash
uv tool install --index-url https://test.pypi.org/simple truckdevil
truckdevil --version
```

One-shot execution:

```bash
uvx --index-url https://test.pypi.org/simple truckdevil --version
```

If dependency resolution needs the main PyPI index for transitive packages, use `--extra-index-url https://pypi.org/simple` with the appropriate tool.

## PyPI Release

PyPI publish can happen in either of two ways.

### Option 1: Tagged release

1. Bump version
2. Merge to `main`
3. Create and push a tag:

```bash
git tag v1.1.0
git push upstream v1.1.0
```

4. The `Publish` workflow will publish to PyPI automatically

### Option 2: Manual release

1. Open Actions in `LittleBlondeDevil/TruckDevil`
2. Select `Publish`
3. Choose `Run workflow`
4. Set `repository` to `pypi`
5. Run from branch `main`

## Verify PyPI Install

After a successful PyPI publish:

```bash
uv tool install truckdevil
truckdevil --version
uvx truckdevil --version
pip install truckdevil
```

Optional pretty extra:

```bash
uv tool install 'truckdevil[pretty]'
pip install 'truckdevil[pretty]'
```

## Troubleshooting

### `invalid-publisher`

This means the package index does not have a trusted publisher matching the workflow claims.

Check:

1. repo owner is `LittleBlondeDevil`
2. repo name is `TruckDevil`
3. workflow path is `.github/workflows/publish.yml`
4. branch is `main`
5. environment name matches `testpypi` or `pypi`

### Workflow runs from a fork but publish fails

Expected. Trusted publishing must be configured for the canonical repository, not a contributor fork.

### TestPyPI install cannot resolve dependencies

Use the main PyPI index as an extra index for dependencies while still installing `truckdevil` from TestPyPI.

### Upload fails because version already exists

Bump the package version and rebuild. PyPI and TestPyPI do not allow overwriting an existing release file.
