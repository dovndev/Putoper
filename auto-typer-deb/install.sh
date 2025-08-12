#!/bin/bash
# Auto Typer Installation Script

echo "Installing Auto Typer..."

# Create directories
sudo mkdir -p /usr/local/bin
sudo mkdir -p /usr/share/applications

# Copy executable
sudo cp auto-typer /usr/local/bin/
sudo chmod +x /usr/local/bin/auto-typer

# Copy desktop entry
sudo cp auto-typer.desktop /usr/share/applications/

echo "Auto Typer installed successfully!"
echo "You can now run it from the terminal with: auto-typer"
echo "Or find it in your applications menu under 'Auto Typer'"
