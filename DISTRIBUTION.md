# Distribution Guide for pipup

This document explains how to distribute pipup through various channels.

## Distribution Channels

### 1. PyPI (Python Package Index)
- **Status**: Ready
- **Files**: `setup.py`, `pipup.py`
- **Process**: Automated via GitHub Actions on tag push

### 2. Homebrew (macOS)
- **Status**: Ready
- **Files**: `homebrew/pipup.rb`, `homebrew/update_formula.sh`
- **Process**: Manual submission to homebrew-core

## Release Process

### Automated Release (PyPI)
1. Update version in `pipup.py` and `setup.py`
2. Commit changes: `git commit -m "Bump version to X.Y.Z"`
3. Create and push tag: `git tag vX.Y.Z && git push origin vX.Y.Z`
4. GitHub Actions will automatically build and upload to PyPI

### Manual Release (Homebrew)
1. Run the release script: `./scripts/release.sh X.Y.Z`
2. Test the formula: `brew install --build-from-source homebrew/pipup.rb`
3. Submit PR to [homebrew-core](https://github.com/Homebrew/homebrew-core)

## Files Created for Distribution

### Homebrew Files
- `homebrew/pipup.rb` - Homebrew formula
- `homebrew/update_formula.sh` - Script to update formula with new versions
- `homebrew/README.md` - Homebrew-specific documentation

### GitHub Actions
- `.github/workflows/release.yml` - Automated PyPI release workflow

### Scripts
- `scripts/release.sh` - Complete release automation script

## Testing

### Local Testing
```bash
# Test Homebrew formula
brew install --build-from-source homebrew/pipup.rb

# Test functionality
pipup --version
pipup test_requirements.txt --dry-run
```

### PyPI Testing
```bash
# Install from PyPI
pip install pipup

# Test functionality
pipup --version
```

## Installation Instructions

### For Users

#### Homebrew (macOS)
```bash
brew install abozaralizadeh/pipup/pipup
```

#### PyPI
```bash
pip install requp
```

#### From Source
```bash
git clone https://github.com/abozaralizadeh/pipup.git
cd pipup
pip install -e .
```

## Maintenance

### Updating Versions
1. Update version in `pipup.py` and `setup.py`
2. Run `./scripts/release.sh X.Y.Z` for complete automation
3. Or manually follow the release process steps

### Homebrew Formula Updates
- Use `./homebrew/update_formula.sh X.Y.Z` to update the formula
- Test locally before submitting to homebrew-core
- Follow homebrew-core contribution guidelines

## Notes

- The Homebrew formula uses Python 3.12 as dependency
- All releases should be tagged in git
- GitHub Actions requires `PYPI_API_TOKEN` secret to be set
- Homebrew submission requires manual PR to homebrew-core
