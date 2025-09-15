#!/bin/bash

# Script to update Homebrew formula with latest version

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 1.0.9"
    exit 1
fi

VERSION=$1
TARBALL_URL="https://github.com/abozaralizadeh/pipup/archive/v${VERSION}.tar.gz"

echo "Updating formula to version $VERSION..."

# Download the tarball and calculate SHA256
echo "Downloading tarball to calculate SHA256..."
TEMP_FILE=$(mktemp)
curl -L -o "$TEMP_FILE" "$TARBALL_URL"
SHA256=$(shasum -a 256 "$TEMP_FILE" | cut -d' ' -f1)
rm "$TEMP_FILE"

echo "SHA256: $SHA256"

# Update the local formula file
sed -i.bak "s|url \"https://github.com/abozaralizadeh/pipup/archive/v[^\"]*\.tar\.gz\"|url \"$TARBALL_URL\"|" homebrew/pipup.rb
sed -i.bak "s|sha256 \"[^\"]*\"|sha256 \"$SHA256\"|" homebrew/pipup.rb
rm homebrew/pipup.rb.bak

# Update the tap formula file
if [ -f "/opt/homebrew/Library/Taps/abozaralizadeh/homebrew-brew/Formula/pipup.rb" ]; then
    sed -i.bak "s|url \"https://github.com/abozaralizadeh/pipup/archive/v[^\"]*\.tar\.gz\"|url \"$TARBALL_URL\"|" /opt/homebrew/Library/Taps/abozaralizadeh/homebrew-brew/Formula/pipup.rb
    sed -i.bak "s|sha256 \"[^\"]*\"|sha256 \"$SHA256\"|" /opt/homebrew/Library/Taps/abozaralizadeh/homebrew-brew/Formula/pipup.rb
    rm /opt/homebrew/Library/Taps/abozaralizadeh/homebrew-brew/Formula/pipup.rb.bak
    echo "Updated tap formula file"
fi

echo ""
echo "Formula updated successfully!"
echo "Updated formula:"
echo "  Version: $VERSION"
echo "  URL: $TARBALL_URL"
echo "  SHA256: $SHA256"
echo ""
echo "Next steps:"
echo "1. Test the formula: brew install --build-from-source abozaralizadeh/brew/pipup"
echo "2. Commit and push changes to the tap repository"
