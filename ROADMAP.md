# ROADMAP.md

## Goal

Make TruckDevil installable and usable through standard Python package managers, with `PyPI` as the distribution source and `uv`/`pip`/`pipx` as supported install methods.

Target user experience:

```bash
pip install truckdevil
uv tool install truckdevil
uvx truckdevil --version
truckdevil
```

## Current State

TruckDevil already has basic packaging metadata in `setup.py`, but installed-package support is incomplete.

Main blockers:

1. Runtime code uses repo-layout-dependent imports such as `from libs...`, `from j1939...`, and `from __init__...`.
2. There is no installable CLI entry point named `truckdevil`.
3. JSON resources under `truckdevil/resources/json_files/` are required at runtime but are not explicitly packaged.
4. The project does not yet use a modern `pyproject.toml` configuration.
5. Some tests assume repo-local execution semantics and will need packaging smoke coverage.

## Guiding Principles

1. Prefer the smallest viable change set.
2. Preserve current development workflows while making installed usage first-class.
3. Keep upstream PRs focused and reviewable.
4. Verify wheel/sdist installs, not just editable installs.
5. Treat `truckdevil` CLI usability as a required outcome, not an optional extra.

## Desired End State

When this roadmap is complete:

1. `truckdevil` can be installed from PyPI.
2. `uv tool install truckdevil` works cleanly.
3. `uvx truckdevil` works for one-shot execution.
4. Runtime imports are package-safe.
5. Bundled JSON resources are available from installed wheels and sdists.
6. `truckdevil --version` works in installed environments.
7. CI or release validation includes packaging smoke tests.

## Implementation Phases

### Phase 1: Modern packaging base

Objective: establish modern packaging metadata while minimizing churn.

Tasks:

1. Add `pyproject.toml` using `setuptools` as the build backend.
2. Mirror or migrate metadata from `setup.py`.
3. Define project dependencies and optional extras such as `pretty`.
4. Keep the change minimal rather than redesigning the project structure.

Deliverables:

1. `pyproject.toml`
2. Working local package build via `python -m build`

### Phase 2: Installable CLI

Objective: make installed usage first-class.

Tasks:

1. Refactor `truckdevil/truckdevil.py` to expose a `main()` function.
2. Add a package script entry point named `truckdevil`.
3. Preserve `--version` support.
4. Decide whether direct `python truckdevil.py` remains supported for development only or indefinitely.

Deliverables:

1. Installable `truckdevil` command
2. `truckdevil --version` working from an installed environment

### Phase 3: Runtime import cleanup

Objective: remove repo-layout assumptions from runtime code.

Tasks:

1. Replace imports like `from libs.device import Device` with package-safe imports.
2. Replace imports like `from j1939.j1939 import J1939Interface` with package-safe imports.
3. Replace `from __init__ import __version__` with a package-safe alternative.
4. Update all runtime modules under `truckdevil/` consistently.

Likely affected files:

1. `truckdevil/truckdevil.py`
2. `truckdevil/modules/*.py`
3. `truckdevil/libs/*.py`
4. `truckdevil/j1939/j1939.py`

Deliverables:

1. Installed package imports successfully outside the repo root
2. REPL and module loading still work

### Phase 4: Resource packaging

Objective: guarantee runtime JSON assets are present in installs.

Tasks:

1. Explicitly package files in `truckdevil/resources/json_files/`.
2. Add `MANIFEST.in` if needed for source distributions.
3. Verify wheel and sdist both contain required JSON files.
4. Confirm runtime resource loading works after installation.

Deliverables:

1. Resource files included in wheel
2. Resource files included in sdist
3. Installed runtime can read bundled JSON metadata

### Phase 5: Packaging validation tests

Objective: verify installed-package behavior, not only repo-local behavior.

Tasks:

1. Add smoke tests for package import.
2. Add smoke tests for `truckdevil --version`.
3. Add validation for JSON resource availability.
4. Keep existing pytest coverage for current behavior.
5. Reduce unnecessary test dependence on repo-only import hacks where practical.

Deliverables:

1. Packaging smoke tests
2. Confidence that wheel installs behave like local development installs

### Phase 6: Documentation updates

Objective: document the new install path clearly.

Tasks:

1. Update `README.md` with install instructions for `pip`, `uv`, and optional extras.
2. Separate basic installation from hardware-specific setup.
3. Document the preferred installed CLI usage.

Deliverables:

1. Updated README install section
2. Clear examples for `pip install truckdevil` and `uv tool install truckdevil`

### Phase 7: Publishing workflow

Objective: publish safely and repeatably.

Tasks:

1. Add a build-and-publish workflow.
2. Test publishing to TestPyPI first.
3. Publish to PyPI after verification.
4. Prefer tag-based releases.
5. Prefer trusted publishing if feasible.

Deliverables:

1. TestPyPI release flow
2. PyPI release flow

## Local Verification Checklist

Before publishing, verify all of the following:

1. `python -m build`
2. `pip install dist/*.whl`
3. `truckdevil --version`
4. `python -m pytest tests/ -v`
5. Verify packaged JSON assets exist in built artifacts
6. `uv tool install .`
7. Installed CLI launches successfully

## Recommended PR Breakdown

To keep upstream review manageable, split the work into focused PRs:

### PR 1: CLI and import safety

Include:

1. `main()` entry point
2. Script entry point wiring
3. Runtime import cleanup

### PR 2: Packaging metadata and resources

Include:

1. `pyproject.toml`
2. Package data configuration
3. `MANIFEST.in` if needed

### PR 3: Validation and docs

Include:

1. Packaging smoke tests
2. README installation updates
3. Release workflow scaffolding

## First Development Steps

The recommended implementation order is:

1. Add `pyproject.toml`
2. Refactor `truckdevil/truckdevil.py` to expose `main()`
3. Convert runtime imports to package-safe imports
4. Add package-data configuration for JSON files
5. Build and install locally from wheel
6. Add packaging smoke tests
7. Update README
8. Add TestPyPI and PyPI publishing workflow

## Notes On `uv`

`uv` is not the distribution source. `PyPI` is the source; `uv` is one of the package management clients. The practical goal is:

1. Publish a correct package to PyPI
2. Ensure `pip`, `uv`, and `pipx` can all install and run it cleanly

## Success Criteria

This effort is complete when:

1. A clean environment can install TruckDevil from a package index.
2. The installed CLI works without depending on repo-local paths.
3. Runtime JSON resources are available from installed artifacts.
4. Packaging validation is automated enough to prevent regressions.
5. The upstream project can review and merge the work in small, understandable pieces.
