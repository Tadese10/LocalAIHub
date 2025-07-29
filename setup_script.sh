#!/bin/bash

# LocalAIHub Setup Script
set -e

echo "🌟 Getting LocalAIHub ready..."

# Check for Python 3.8 or higher
python_version=$(python3 --version 2>&1 | grep -oP '(?<=Python )\d+\.\d+' || echo "0.0")
minimum_version="3.8"

if [ "$(printf '%s\n' "$minimum_version" "$python_version" | sort -V | head -n1)" != "$minimum_version" ]; then
    echo "❌ We need Python 3.8 or higher. You have: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Set up a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Setting up a virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "🔧 Switching to virtual environment..."
source venv/bin/activate

# Install required Python packages
echo "📥 Installing needed packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create a logs folder
mkdir -p logs

# Make the CLI script executable
chmod +x cli.py

echo ""
echo "✅ All set!"
echo ""
echo "🚀 Start the server with:"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "🔧 Use the CLI with:"
echo "   source venv/bin/activate"
echo "   python cli.py --help"
echo ""
echo "💡 For smarter AI responses:"
echo "   1. Install Ollama: https://ollama.ai"
echo "   2. Run: ollama pull llama2"
echo "   3. Run: ollama serve"
echo ""
echo "🐳 Prefer Docker? Run:"
echo "   docker-compose up --build"