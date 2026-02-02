#!/usr/bin/env bash
set -e

echo "Setting up development environment..."

# Ensure Poetry is in PATH
export PATH="$HOME/.local/bin:$PATH"

# Ensure python symlink exists (for Poetry compatibility)
if [ ! -f "$HOME/.local/bin/python" ]; then
    mkdir -p "$HOME/.local/bin"
    ln -sf /usr/bin/python3.11 "$HOME/.local/bin/python"
fi

# Configure Poetry to use Python 3.11 explicitly
poetry env use /usr/bin/python3.11 || true

# Install Python dependencies
if [ -f "pyproject.toml" ]; then
    echo "Installing Python dependencies with Poetry..."
    poetry install
fi

# Install Node.js dependencies
if [ -f "package.json" ]; then
    echo "Installing Node.js dependencies..."
    yarn install || npm install
fi

echo "Development environment setup complete!"
echo ""
echo "To get started:"
echo "  Backend:  poetry run python backend/app.py"
echo "  Frontend: yarn dev"
echo ""
echo "Database services:"
echo "  MongoDB:   mongodb:27017 (or localhost:27017 from host)"
echo "  PostgreSQL: postgres:5432 (or localhost:5432 from host)"
echo "    User: postgres"
echo "    Password: password"
echo "    Database: products"

