# MCP Development Setup

This directory contains Kubernetes manifests for running the MCP (Multi-Command Processor) service in a development environment.

## Quick Start

1. Apply the manifests:
```bash
kubectl apply -f dev/mcp/
```

2. Verify the service is running:
```bash
kubectl get pods -n kagent -l app=mcp-dev
kubectl get svc -n kagent mcp-dev
```

## Local Development

For local development, you can run the MCP service directly:

```bash
cd python && PYTHONPATH=. uvicorn kagent.api.main:app --host 0.0.0.0 --port 8083
```

## Testing the SSE Endpoint

The MCP service exposes an SSE endpoint at `/api/mcp/sse`. You can test it using curl:

```bash
curl -N http://localhost:8083/api/mcp/sse
```

## Test Button Functionality

The MCP service includes a test button feature that appears for all MCP servers loaded in the Tools Library. This allows you to:

1. Test individual tools within each MCP server
2. Verify tool functionality before using them in workflows
3. Debug tool configurations and responses

To test a tool:
1. Navigate to the Tools Library in the UI
2. Find an MCP server in the list
3. Click the test button next to the server
4. The test will validate the tool's configuration and return a success/failure response

## Cleanup

To remove the development resources:
```bash
kubectl delete -f dev/mcp/
```

## Notes

- The service runs on port 8083
- The deployment uses the `kagent:latest` image
- Resources are limited to prevent excessive resource usage in development
- All resources have the `-dev` suffix to avoid conflicts with production resources
- The test button is available for all MCP servers in the Tools Library
