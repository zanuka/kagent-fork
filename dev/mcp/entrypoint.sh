#!/bin/bash

echo "Starting MCP service..."

echo "Checking Python environment..."
which python3
python3 --version
python3 -c "import sys; print('Python executable:', sys.executable)"

echo "Checking PYTHONPATH..."
echo "PYTHONPATH: $PYTHONPATH"

echo "Checking OpenAI package..."
pip show openai
python3 -c "import openai; print('OpenAI version:', openai.__version__)"
python3 -c "from openai import NOT_GIVEN; print('NOT_GIVEN is available')"

echo "Checking autogen_ext..."
pip show autogen-ext

echo "Running main application..."
exec python3 -m kagent.cli k8s
