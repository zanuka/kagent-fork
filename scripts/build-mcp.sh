#!/bin/bash

set -e

# Get the current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
MCP_DIR="$ROOT_DIR/dev/mcp"
PYTHON_DIR="$ROOT_DIR/python"

# Default values
REGISTRY="ghcr.io/kagent-dev"
IMAGE_NAME="kagent-mcp"
TAG="latest"
PUSH=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --registry)
      REGISTRY="$2"
      shift 2
      ;;
    --image-name)
      IMAGE_NAME="$2"
      shift 2
      ;;
    --tag)
      TAG="$2"
      shift 2
      ;;
    --push)
      PUSH=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Create a temporary directory for the build context
TEMP_DIR=$(mktemp -d)
echo "Using temporary directory: $TEMP_DIR"

# Copy the necessary files
echo "Copying files to build context..."
cp "$PYTHON_DIR/pyproject.toml" "$PYTHON_DIR/requirements.txt" "$TEMP_DIR/"
cp -r "$PYTHON_DIR/src" "$TEMP_DIR/"
cp "$MCP_DIR/Dockerfile" "$TEMP_DIR/"

# Build the image
echo "Building MCP service image..."
docker build -f "$TEMP_DIR/Dockerfile" -t "$REGISTRY/$IMAGE_NAME:$TAG" "$TEMP_DIR"

# Push the image if requested
if [ "$PUSH" = true ]; then
  echo "Pushing MCP service image to $REGISTRY..."
  docker push "$REGISTRY/$IMAGE_NAME:$TAG"
fi

# Clean up
echo "Cleaning up..."
rm -rf "$TEMP_DIR"

echo "Done!" 
