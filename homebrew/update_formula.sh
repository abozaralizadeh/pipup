#!/bin/bash

# Script to update Homebrew formula with new version and SHA256

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 1.0.1"
    exit 1
fi

VERSION=$1
FORMULA_FILE="homebrew/pipup.rb"
TARBALL_URL="https://github.com/abozaralizadeh/pipup/archive/v${VERSION}.tar.gz"

echo "Updating formula for version $VERSION..."

# Download the tarball and calculate SHA256
echo "Downloading tarball to calculate SHA256..."
TEMP_FILE=$(mktemp)
curl -L -o "$TEMP_FILE" "$TARBALL_URL"
SHA256=$(shasum -a 256 "$TEMP_FILE" | cut -d' ' -f1)
rm "$TEMP_FILE"

echo "SHA256: $SHA256"

# Update the formula file
sed -i.bak "s/version \"[^\"]*\"/version \"$VERSION\"/" "$FORMULA_FILE"
sed -i.bak "s/url \"[^\"]*\"/url \"$TARBALL_URL\"/" "$FORMULA_FILE"
sed -i.bak "s/sha256 \"[^\"]*\"/sha256 \"$SHA256\"/" "$FORMULA_FILE"

# Remove backup file
rm "${FORMULA_FILE}.bak"

echo "Formula updated successfully!"
echo "Updated formula:"
echo "  Version: $VERSION"
echo "  URL: $TARBALL_URL"
echo "  SHA256: $SHA256"
echo ""
echo "Next steps:"
echo "1. Test the formula locally: brew install --build-from-source homebrew/pipup.rb"
echo "2. Submit a PR to homebrew-core with the updated formula"
