# Pipup

**Update Python Package versions in requirements.txt with exact versions from pip freeze**

[![PyPI version](https://badge.fury.io/py/requp.svg)](https://badge.fury.io/py/requp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A command-line tool that updates existing packages in requirements.txt with their exact versions from pip freeze, without adding new packages. Perfect for keeping your requirements.txt files up-to-date with your current environment.

## ✨ Features

- ✅ **Safe Updates**: Only updates existing packages, never adds new ones
- ✅ **Preserves Formatting**: Maintains package order, comments, and empty lines
- ✅ **Smart Version Handling**: Supports all version specifiers (>=, <, ~, etc.)
- ✅ **Package Extras**: Correctly handles packages with extras (e.g., `Flask[async]`)
- ✅ **Dry Run Mode**: Preview changes before applying them
- ✅ **Enhanced Dry Run**: Shows complete updated requirements.txt content
- ✅ **Error Handling**: Warns about packages not found in pip freeze
- ✅ **Cross-Platform**: Works on macOS, Linux, and Windows

## 🚀 Installation

### Homebrew (macOS) - Recommended
```bash
brew install abozaralizadeh/brew/pipup
```

### PyPI
```bash
pip install requp
```

**Note**: After installation, you can use either `pipup` or `requp` commands - they work identically!

### From Source
```bash
git clone https://github.com/abozaralizadeh/pipup.git
cd pipup
pip install -e .
```

### Direct Installation
```bash
pip install git+https://github.com/abozaralizadeh/pipup.git
```

## 📖 Usage

### Basic Usage
```bash
pipup                                    # Update requirements.txt (default)
# or
requp                                    # Update requirements.txt (default)
```

### Dry Run (Preview Changes)
```bash
pipup --dry-run                          # Preview changes to requirements.txt
# or
requp --dry-run                          # Preview changes to requirements.txt
```

### Upgrade to Latest Versions
```bash
pipup -U                                 # Update to latest versions from PyPI
pipup -U --dry-run                       # Preview latest version updates
pipup requirements-dev.txt -U            # Update specific file to latest
# or use requp instead of pipup
```

### Update Different Requirements Files
```bash
pipup requirements-dev.txt               # Update specific file
pipup requirements-prod.txt              # Update specific file
pipup requirements-test.txt              # Update specific file
# or use requp instead of pipup
```

### Get Help
```bash
pipup --help
pipup --version
# or
requp --help
requp --version
```

## 🎛️ Skip Conventions

Pipup supports special comment conventions to control which packages get updated:

### Skip Single Package
```txt
# This package should not be updated
#skip-pipup
requests==2.31.0

# Or use the requp alias
#skip-requp
Flask>=2.0.0
```

### Skip All Remaining Packages
```txt
# Everything below this line should be ignored
#stop-pipup
pydantic==1.10.15
azure-storage-blob==12.19.1
# This comment will also be preserved
```

### Supported Conventions
- `#skip-pipup` or `#skip-requp` - Skip the next package line
- `#stop-pipup` or `#stop-requp` - Skip all remaining lines

## 🔄 Upgrade Mode

The `-U` or `--upgrade` flag updates packages to their latest versions from PyPI instead of using the versions from `pip freeze`. This is useful when you want to:

- **Update to latest**: Get the newest versions of all packages
- **Stay current**: Keep your dependencies up-to-date
- **Test compatibility**: Check if your code works with latest versions

**Note**: Skip and stop conventions work the same way in upgrade mode, giving you fine-grained control over which packages get updated.

## 📋 Examples

### Before Running Pipup
```txt
requests
Flask>=2.0.0
langchain
pydantic>=1.0.0,<2.0.0
# This is a comment
azure-storage-blob
Flask[async]
duckduckgo-search
```

### After Running Pipup
```txt
requests==2.32.4
Flask==3.1.1
langchain==0.3.27
pydantic==2.11.7
# This is a comment
azure-storage-blob==12.26.0
Flask[async]==3.1.1
duckduckgo-search
```

### Dry Run Output
```bash
$ pipup --dry-run
Running pip freeze...
Found 246 installed packages
Dry run: Updating test_requirements.txt...
Warning: flask not found in pip freeze, keeping original specification
Warning: duckduckgo-search not found in pip freeze, keeping original specification

Dry run: Would update 4 packages
Packages not found in pip freeze: flask, duckduckgo-search

Updated requirements.txt content:
--------------------------------------------------
requests==2.31.0
Flask>=2.0.0
langchain==0.0.329
pydantic==1.10.15
# This is a comment
azure-storage-blob==12.19.1
Flask[async]
duckduckgo-search
--------------------------------------------------
```

## 🔧 How It Works

1. **Runs pip freeze** to get all installed packages with exact versions
2. **Parses requirements.txt** line by line, preserving formatting and comments
3. **Matches packages** by name (case-insensitive) and handles extras
4. **Updates version specifiers** to exact versions (==) from pip freeze
5. **Preserves everything else** (comments, empty lines, package order, warnings)

## 📦 Supported Version Specifiers

Pipup handles all standard pip version specifiers:

| Specifier | Example | Result |
|-----------|---------|--------|
| No version | `requests` | `requests==2.32.4` |
| Exact version | `requests==1.0.0` | `requests==2.32.4` |
| Minimum version | `requests>=1.0.0` | `requests==2.32.4` |
| Maximum version | `requests<3.0.0` | `requests==2.32.4` |
| Version range | `requests>=1.0.0,<3.0.0` | `requests==2.32.4` |
| Compatible release | `requests~=1.0.0` | `requests==2.32.4` |
| Exclusion | `requests!=1.0.0` | `requests==2.32.4` |

## 🎯 Package Extras Support

Pipup correctly handles packages with extras:

```txt
# Before
Flask[async]
requests[security]
django[postgresql]

# After
Flask[async]==3.1.1
requests[security]==2.32.4
django[postgresql]==4.2.7
```

## ⚠️ Error Handling

- **Missing requirements.txt**: Exits with clear error message
- **Package not found**: Warns and keeps original specification
- **pip not found**: Exits with helpful error message
- **Invalid requirements.txt**: Preserves malformed lines as-is
- **Permission errors**: Clear error messages for file access issues

## 🛠️ Development

### Setup Development Environment
```bash
git clone https://github.com/abozaralizadeh/pipup.git
cd pipup
pip install -e .
```

### Running Tests
```bash
python -m pytest tests/
```

### Building Package
```bash
python -m build
```

## 📝 Changelog

### 1.1.1
- **Upgrade Mode**: Added `-U`/`--upgrade` flag to update to latest PyPI versions
- **PyPI Integration**: Get latest package versions directly from PyPI
- **Skip Conventions**: Skip and stop conventions work with upgrade mode
- **Enhanced Control**: Fine-grained control over which packages get updated

### 1.1.0
- **Homebrew Migration**: Changed from `abozaralizadeh/tap/pipup` to `abozaralizadeh/brew/pipup`
- **Better Naming**: More standard Homebrew tap naming convention
- **Improved Documentation**: Updated all installation instructions

### 1.0.9
- **Default File**: Added default value for requirements.txt file
- **Simplified Usage**: Can now run `pipup` or `requp` without specifying file
- **Skip Conventions**: Added `#skip-pipup`/`#skip-requp` and `#stop-pipup`/`#stop-requp` comments
- **Fine-grained Control**: Users can now skip individual packages or all remaining packages
- **Better UX**: More intuitive for common use case
- **Updated Documentation**: Examples now show default behavior and skip conventions

### 1.0.8
- **GitHub Permissions**: Fixed GitHub Actions release permissions
- **Release Attachments**: Added built packages to GitHub releases

### 1.0.7
- **Better Permissions**: Added explicit contents: write permissions
- **Improved Workflow**: Enhanced CI/CD pipeline reliability

### 1.0.6
- **CI/CD Fixes**: Fixed GitHub Actions build and upload process
- **Build Verification**: Added steps to verify dist/ contents before upload
- **Clean Builds**: Ensures fresh builds without cached files
- **Better Debugging**: Added logging to track build process

### 1.0.5
- **Workflow Fixes**: Fixed GitHub Actions release workflow permissions
- **Modern Actions**: Updated to use `softprops/action-gh-release@v1`
- **Auto Changelog**: Added automatic release notes generation
- **Better Reliability**: Improved CI/CD pipeline stability

### 1.0.3
- **Command Alias**: Added `requp` as an alias command for PyPI users
- **Dual Commands**: Users can now use either `pipup` or `requp` commands
- **Enhanced Documentation**: Updated README with comprehensive examples and badges
- **Improved Workflow**: Fixed GitHub Actions release workflow
- **Better User Experience**: More intuitive for users installing from PyPI

### 1.0.2
- **PyPI Package Name**: Changed to `requp` to avoid naming conflicts
- **Enhanced Dry Run**: Now shows complete updated requirements.txt content
- **Improved Documentation**: Better examples and clearer instructions
- **Homebrew Support**: Added Homebrew installation via repository

### 1.0.1
- **Enhanced Dry Run**: Added display of updated requirements.txt content
- **Better Error Messages**: Improved warning and error output
- **Documentation Updates**: Added comprehensive examples

### 1.0.0
- **Initial Release**: Basic package version updating
- **Dry Run Mode**: Preview changes before applying
- **Version Specifier Support**: All standard pip version specifiers
- **Package Extras Support**: Handles packages with extras correctly
- **Cross-Platform**: Works on macOS, Linux, and Windows

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need for safe requirements.txt updates
- Built with Python's excellent packaging tools
- Thanks to all contributors and users

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/abozaralizadeh/pipup/issues)
- **Discussions**: [GitHub Discussions](https://github.com/abozaralizadeh/pipup/

---

**Made with ❤️ for the Python community**