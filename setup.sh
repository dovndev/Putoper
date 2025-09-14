#!/bin/bash
# Quick setup script for Auto Typer development

set -e

echo "🔧 Setting up Auto Typer development environment..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Install build dependencies
echo "🔨 Installing build dependencies..."
pip install pyinstaller

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use Auto Typer:"
echo "  1. Activate environment: source .venv/bin/activate"
echo "  2. Run application: python auto_typing.py"
echo "  3. Build distributables: python build.py"
echo "  4. Install on Linux: ./install.sh"
echo ""
