#!/bin/bash
# Post-create script for dev container setup

set -e

echo "🔧 Setting up development environment..."

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip install --user -r requirements.txt
fi

# Install Node.js dependencies if package.json exists
if [ -f "package.json" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Set up Git configuration (if not already configured)
if [ -z "$(git config --global user.name)" ]; then
    echo "⚙️  Configuring Git..."
    git config --global user.name "Agent Developer"
    git config --global user.email "agent@example.com"
    git config --global init.defaultBranch main
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p logs
mkdir -p data
mkdir -p .cache

# Set permissions
chmod +x agent/*.py 2>/dev/null || true
chmod +x mcp-server/*.py 2>/dev/null || true
chmod +x examples/*.py 2>/dev/null || true

# Display welcome message
echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "🚀 Quick Start:"
echo "   1. Start MCP server: python mcp-server/server.py"
echo "   2. Run agent demo: python agent/orchestrator.py --help"
echo "   3. Try examples: python examples/laptop_refresh.py"
echo ""
echo "📚 Documentation: See README.md for more details"
echo ""
