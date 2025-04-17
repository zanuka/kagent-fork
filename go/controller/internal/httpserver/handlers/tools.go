package handlers

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
	"github.com/kagent-dev/kagent/go/autogen/api"
	"github.com/kagent-dev/kagent/go/controller/api/v1alpha1"
	"github.com/kagent-dev/kagent/go/controller/internal/httpserver/errors"
	ctrllog "sigs.k8s.io/controller-runtime/pkg/log"
	"k8s.io/apimachinery/pkg/types"
	"sigs.k8s.io/controller-runtime/pkg/client"
)

// ToolsHandler handles tool-related requests
type ToolsHandler struct {
	*Base
}

// convertAnyTypeMapToInterfaceMap converts a map[string]v1alpha1.AnyType to map[string]interface{}
func convertAnyTypeMapToInterfaceMap(input map[string]v1alpha1.AnyType) map[string]interface{} {
	result := make(map[string]interface{})
	for key, value := range input {
		result[key] = value.RawMessage // Assuming v1alpha1.AnyType has a RawMessage field of type json.RawMessage
	}
	return result
}

// NewToolsHandler creates a new ToolsHandler
func NewToolsHandler(base *Base) *ToolsHandler {
	return &ToolsHandler{Base: base}
}

// HandleListTools handles GET /api/tools requests
func (h *ToolsHandler) HandleListTools(w ErrorResponseWriter, r *http.Request) {
	log := ctrllog.FromContext(r.Context()).WithName("tools-handler").WithValues("operation", "list")

	userID, err := GetUserID(r)
	if err != nil {
		w.RespondWithError(errors.NewBadRequestError("Failed to get user ID", err))
		return
	}
	log = log.WithValues("userID", userID)

	log.V(1).Info("Listing tools from Autogen")
	tools, err := h.AutogenClient.ListTools(userID)
	if err != nil {
		w.RespondWithError(errors.NewInternalServerError("Failed to list tools", err))
		return
	}

	var allToolServers v1alpha1.ToolServerList
	if err = h.KubeClient.List(r.Context(), &allToolServers); err != nil {
		w.RespondWithError(errors.NewInternalServerError("Failed to list tools from Kubernetes", err))
		return
	}

	discoveredTools := make([]*api.Component, 0)
	for _, toolServer := range allToolServers.Items {
		for _, t := range toolServer.Status.DiscoveredTools {
			// Set the server name in the component label
			t.Component.Label = toolServer.Name
			discoveredTools = append(discoveredTools, &api.Component{
				Provider:      t.Component.Provider,
				Label:         t.Component.Label,
				Description:   t.Component.Description,
				Config:        convertAnyTypeMapToInterfaceMap(t.Component.Config),
				ComponentType: t.Component.ComponentType,
			})
		}
	}

	for _, tool := range tools {
		if strings.HasPrefix(tool.Component.Provider, "kagent") {
			discoveredTools = append(discoveredTools, tool.Component)
		}
	}

	log.Info("Successfully listed tools", "count", len(tools))
	RespondWithJSON(w, http.StatusOK, discoveredTools)
}

func convertMapToMCPToolConfig(data map[string]v1alpha1.AnyType) (api.MCPToolConfig, error) {
	var config api.MCPToolConfig

	// Extract server_params if it exists
	if serverParamsRaw, ok := data["server_params"]; ok {
		// First unmarshal to a map to check the type
		var serverParamsMap map[string]interface{}
		if err := json.Unmarshal(serverParamsRaw.RawMessage, &serverParamsMap); err != nil {
			return config, fmt.Errorf("failed to unmarshal server_params: %w", err)
		}

		// Now convert to SseMcpServerConfig
		var sseConfig api.SseMcpServerConfig
		if err := json.Unmarshal(serverParamsRaw.RawMessage, &sseConfig); err != nil {
			return config, fmt.Errorf("failed to unmarshal server_params as SseMcpServerConfig: %w", err)
		}

		config.ServerParams = sseConfig
	}

	// Extract tool information
	toolRaw, ok := data["tool"]
	if !ok {
		return config, fmt.Errorf("missing required field 'tool'")
	}

	var tool api.MCPTool
	if err := json.Unmarshal(toolRaw.RawMessage, &tool); err != nil {
		return config, fmt.Errorf("failed to unmarshal tool: %w", err)
	}
	config.Tool = tool

	return config, nil
}

// HandleTestTool handles POST /api/tools/{provider}/{tool}/test requests
func (h *ToolsHandler) HandleTestTool(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	provider := vars["provider"]
	tool := vars["tool"]

	log := ctrllog.FromContext(r.Context())
	log.Info("testing tool", "provider", provider, "tool", tool)

	var toolServerName string
	if provider == "mcp" {
		toolServerName = "mcp-tool-server"
	} else {
		toolServerName = fmt.Sprintf("%s-tool-server", provider)
	}

	var toolServer v1alpha1.ToolServer
	if err := h.KubeClient.Get(r.Context(), types.NamespacedName{
		Name:      toolServerName,
		Namespace: "kagent",
	}, &toolServer); err != nil {
		if client.IgnoreNotFound(err) != nil {
			log.Error(err, "failed to get tool server")
			errors.WriteInternalError(w, err)
			return
		}
		log.Info("tool server not found", "name", toolServerName)
		errors.WriteNotFoundError(w, fmt.Sprintf("tool server %s not found", toolServerName))
		return
	}

	toolFound := false
	for _, discoveredTool := range toolServer.Status.DiscoveredTools {
		if discoveredTool.Name == tool {
			toolFound = true
			break
		}
	}

	if !toolFound {
		log.Info("tool not found in tool server", "tool", tool, "server", toolServerName)
		errors.WriteNotFoundError(w, fmt.Sprintf("tool %s not found in tool server %s", tool, toolServerName))
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"success": true,
		"message": fmt.Sprintf("tool %s found in tool server %s", tool, toolServerName),
	})
}
