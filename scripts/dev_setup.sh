#!/bin/bash

# Development setup script for GitHub Backup Tool

set -e

echo "🚀 Setting up GitHub Backup Tool development environment..."

# Check if Python 3.8+ is available
python_version=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
echo "📍 Python version: $python_version"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "❌ Python 3.8 or higher is required"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install package in development mode
echo "🔨 Installing package in development mode..."
pip install -e .

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install

# Run initial code quality checks
echo "🔍 Running code quality checks..."
black --check src/ scripts/ tests/ || echo "⚠️  Code formatting issues found. Run 'black src/ scripts/ tests/' to fix."
isort --check-only src/ scripts/ tests/ || echo "⚠️  Import sorting issues found. Run 'isort src/ scripts/ tests/' to fix."
flake8 src/ scripts/ tests/ || echo "⚠️  Linting issues found."

# Run tests
echo "🧪 Running tests..."
pytest

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Activate the virtual environment: source venv/bin/activate"
echo "   2. Set up your environment variables: python scripts/setup.py"
echo "   3. Run a quick backup: python scripts/quick_backup.py"
echo "   4. Or use the CLI: python -m github_backup.cli --help"
