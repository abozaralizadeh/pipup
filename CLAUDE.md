# CLAUDE.md

Guidance for Claude Code (and humans) working in this repo.

## What this is

pipup is a single-file Python CLI that rewrites the version pins in an existing
`requirements.txt` to the exact versions currently installed (from `pip freeze`), without adding
any new packages. It can also pull the latest versions from PyPI (`-U`), strip version
constraints (`free`), and uninstall packages (`remove`). It is published to PyPI as **`requp`**
and installs two identical console commands, `pipup` and `requp`. All logic lives in `pipup.py`;
there are no runtime dependencies beyond the Python standard library.

## Commands

```bash
# Run from source (no install, no deps needed)
python pipup.py --dry-run                 # preview changes to ./requirements.txt
python pipup.py final_test.txt --dry-run  # preview against the sample file in the repo
python pipup.py --version                 # -> "pipup 1.2.1"
python pipup.py --help

# Install locally
pip install -e .                          # or ./install.sh

# Subcommands (also usable as `requp ...`)
pipup                 # update requirements.txt in place from pip freeze
pipup -U              # update to latest versions from PyPI (uses `pip index versions`)
pipup free [file]     # remove version specifiers, keep names (and extras)
pipup remove [file]   # pip-uninstall the packages listed in the file
pipup remove --all    # uninstall everything except editable installs

# Build a distribution
python -m build
```

There is **no automated test suite**. The README's "Running Tests" section shows
`python -m pytest tests/`, but there is no `tests/` directory and pytest is not used — that command
does not work. Verify changes by running `pipup.py` against `final_test.txt` with `--dry-run`
(confirmed working here on Python 3.13).

## Layout

```
pipup.py                     the entire tool: pip-freeze parsing, requirements rewriting, subcommands, main()
setup.py                     packaging; name="requp", two console_scripts (pipup, requp) -> pipup:main
install.sh                   convenience `pip3 install -e .`
final_test.txt               sample requirements file used for manual checks (tracked; not matched by the test_*.txt ignore)
scripts/release.sh           version bump + tag + push + formula update
homebrew/pipup.rb            Homebrew formula (served from the abozaralizadeh/brew tap)
homebrew/update_formula.sh   recompute tarball SHA256 and rewrite url/sha256 in the formula
homebrew/update_latest.sh    same, plus patches a locally-tapped formula if present
.github/workflows/release.yml  tag-triggered PyPI publish + GitHub release
DISTRIBUTION.md, homebrew/README.md  distribution notes
pipup.egg-info/, requp.egg-info/     stale committed build metadata (see gotchas)
```

## Releasing

Releases are tag-driven. `.github/workflows/release.yml` fires on any `v*` tag push: it builds with
`python -m build`, uploads to PyPI with twine (needs the `PYPI_API_TOKEN` repo secret), and creates
a GitHub release with the built artifacts.

The intended flow (`scripts/release.sh X.Y.Z`, run from a clean main/master tree):
1. `sed`-bumps the version in `pipup.py` (the `version='pipup X.Y.Z'` argparse string) and in
   `setup.py` (`version="X.Y.Z"`), commits as "Bump version to X.Y.Z".
2. Creates and pushes tag `vX.Y.Z` (this triggers the PyPI workflow).
3. Runs `homebrew/update_formula.sh X.Y.Z`, which downloads the GitHub source tarball, computes its
   SHA256, and rewrites `url`/`sha256` in `homebrew/pipup.rb`. The Homebrew update is manual and not
   part of CI.

## Conventions / gotchas

- **Version lives in three places** and must stay in sync: `setup.py`, the `--version` string in
  `pipup.py`, and `homebrew/pipup.rb` (url tag + sha256). `release.sh` + `update_formula.sh` handle
  the first two and the formula respectively; nothing updates the formula automatically.
- **PyPI name vs command name:** the distribution is `requp` (PyPI), but it installs both `pipup`
  and `requp` commands pointing at the same `main()`. Install docs use `pip install requp`.
- **Two egg-info directories are committed** (`pipup.egg-info/`, `requp.egg-info/`). They are stale
  build artifacts (not in `.gitignore`); do not treat their `PKG-INFO` as source of truth.
- `setup.py` declares `author_email="abozar@example.com"` (a placeholder); the real contact in the
  README/PKG-INFO is the maintainer's address. Left as-is — don't change packaging metadata unless asked.
- The tool only ever **rewrites existing lines**; it never adds packages. Missing packages produce a
  warning and the original line is kept. Comments, blank lines and order are preserved.
- Skip conventions are literal full-line comments: `#skip-pipup`/`#skip-requp` skip the next package
  line, `#stop-pipup`/`#stop-requp` leave everything below untouched.
- `main()` has a legacy-vs-subcommand dispatch: a first arg that is `update`/`remove`/`free` (or
  `-h`/`--help`/`--version`) uses subcommand parsing, otherwise it falls back to legacy "update" mode.
- Homebrew formula has no `resource` blocks because the tool is pure-stdlib; keep it that way if the
  dependency set stays empty.
```
