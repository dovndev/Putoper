#!/bin/bash
# Native package creator for Auto Typer

set -e

VERSION="1.0.0"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGES_DIR="$PROJECT_DIR/packages"

echo "🚀 Creating Auto Typer Native distribution packages..."

# Clean and create packages directory
rm -rf "$PACKAGES_DIR"
mkdir -p "$PACKAGES_DIR"

# Run the python build script for everything
# This will create the .deb and the portable tarball in ./installers/
echo "🔨 Running build script..."
cd "$PROJECT_DIR"
python3 build.py

# Move artifacts to final packages directory
echo "📦 organizing packages..."
cp installers/*.deb "$PACKAGES_DIR/" 2>/dev/null || true
cp installers/*.tar.gz "$PACKAGES_DIR/" 2>/dev/null || true
cp installers/*.zip "$PACKAGES_DIR/" 2>/dev/null || true
cp installers/AutoTyper "$PACKAGES_DIR/" 2>/dev/null || true

# Summary
echo ""
echo "🎉 Package creation complete!"
echo ""
echo "Created packages in $PACKAGES_DIR:"
ls -la "$PACKAGES_DIR"

echo "✅ Ready for distribution!"
