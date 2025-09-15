#!/bin/bash

# Script to create a new release and prepare for Homebrew submission

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 1.0.2"
    exit 1
fi

VERSION=$1
TAG="v$VERSION"

echo "Creating release $VERSION..."

# Check if we're on the main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "master" ]; then
    echo "Warning: You're not on main/master branch. Current branch: $CURRENT_BRANCH"
    read -p "Continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "Error: Working directory is not clean. Please commit or stash changes."
    exit 1
fi

# Update version in files
echo "Updating version to $VERSION..."
sed -i.bak "s/version='pipup [^']*'/version='pipup $VERSION'/" pipup.py
sed -i.bak "s/version=\"[^\"]*\"/version=\"$VERSION\"/" setup.py
rm pipup.py.bak setup.py.bak

# Commit version changes
git add pipup.py setup.py
git commit -m "Bump version to $VERSION"

# Create and push tag
echo "Creating tag $TAG..."
git tag -a "$TAG" -m "Release $VERSION"
git push origin "$TAG"

# Update Homebrew formula
echo "Updating Homebrew formula..."
./homebrew/update_formula.sh "$VERSION"

echo ""
echo "Release $VERSION created successfully!"
echo ""
echo "Next steps:"
echo "1. Wait for GitHub Actions to build and upload to PyPI"
echo "2. Test the Homebrew formula: brew install --build-from-source homebrew/pipup.rb"
echo "3. Submit PR to homebrew-core with the updated formula"
echo ""
echo "Files updated:"
echo "- pipup.py: version updated to $VERSION"
echo "- setup.py: version updated to $VERSION"
echo "- homebrew/pipup.rb: formula updated for $VERSION"
