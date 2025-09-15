# Homebrew Distribution for pipup

This directory contains files needed to distribute pipup through Homebrew.

## Files

- `pipup.rb` - The Homebrew formula file
- `update_formula.sh` - Script to update the formula with new versions
- `README.md` - This guide

## How to Submit to Homebrew

### Prerequisites

1. **GitHub Repository**: Ensure your project is hosted on GitHub
2. **Tagged Release**: Create a git tag for the version you want to release
3. **Source Archive**: GitHub automatically creates tarballs for tags

### Steps to Submit

1. **Update the Formula**:
   ```bash
   ./homebrew/update_formula.sh 1.0.1
   ```

2. **Test the Formula Locally**:
   ```bash
   brew install --build-from-source homebrew/pipup.rb
   ```

3. **Fork homebrew-core**:
   - Go to https://github.com/Homebrew/homebrew-core
   - Click "Fork" to create your fork

4. **Add the Formula**:
   - Clone your fork: `git clone https://github.com/YOUR_USERNAME/homebrew-core.git`
   - Copy `homebrew/pipup.rb` to `Formula/p/pipup.rb` in the homebrew-core repo
   - Commit and push your changes

5. **Submit Pull Request**:
   - Create a pull request to homebrew-core
   - Follow their [contribution guidelines](https://github.com/Homebrew/homebrew-core/blob/master/CONTRIBUTING.md)

### Formula Details

The formula includes:
- **Description**: Brief description of the tool
- **Homepage**: GitHub repository URL
- **URL**: Direct link to source tarball
- **SHA256**: Checksum for verification
- **Dependencies**: Python 3.12
- **Installation**: Uses virtualenv for clean installation
- **Test**: Basic version check test

### Updating for New Versions

1. Update the version in `setup.py` and `pipup.py`
2. Create a git tag: `git tag v1.0.2 && git push origin v1.0.2`
3. Run the update script: `./homebrew/update_formula.sh 1.0.2`
4. Test the updated formula
5. Submit a new PR to homebrew-core

### Notes

- The formula uses `virtualenv_install_with_resources` which automatically handles Python dependencies
- The test block runs `pipup --version` to verify installation
- Make sure to update the SHA256 when creating new releases
