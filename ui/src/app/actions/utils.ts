import { getBackendUrl } from "@/lib/utils";

export async function getCurrentUserId() {
  // TODO: this should come from login state
  return "admin@kagent.dev";
}

type ApiOptions = RequestInit & {
  method?: "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
};

/**
 * Generic API fetch function with error handling
 * @param path API path to fetch
 * @param options Fetch options
 * @returns Promise with the response data
 * @throws Error with a descriptive message if the request fails
 */
export async function fetchApi<T>(path: string, options: ApiOptions = {}): Promise<T> {
  const userId = await getCurrentUserId();
  // Ensure path starts with a slash
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  const url = `${getBackendUrl()}${cleanPath}`;
  const urlWithUser = url.includes("?") ? `${url}&user_id=${userId}` : `${url}?user_id=${userId}`;

  console.log(`Making API request to: ${urlWithUser}`);

  try {
    const response = await fetch(urlWithUser, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        ...options.headers,
      },
      signal: AbortSignal.timeout(15000), // 15 second timeout
    });

    console.log(`Response status: ${response.status}`);
    console.log(`Response headers:`, Object.fromEntries(response.headers.entries()));

    if (!response.ok) {
      // Try to extract error message from response
      let errorMessage = `Request failed with status ${response.status}. ${url}`;

      try {
        const contentType = response.headers.get("content-type");
        console.log(`Error response content-type: ${contentType}`);

        if (contentType && contentType.includes("application/json")) {
          const errorData = await response.json();
          console.log("Error response data:", errorData);
          if (errorData.error) {
            errorMessage = errorData.error;
          } else if (errorData.message) {
            errorMessage = errorData.message;
          }
        } else {
          const text = await response.text();
          console.log("Error response text:", text);
          errorMessage = `${errorMessage} - ${text}`;
        }
      } catch (parseError) {
        console.error("Could not parse error response:", parseError);
      }

      throw new Error(errorMessage);
    }

    // Handle 204 No Content response (common for DELETE)
    if (response.status === 204) {
      return {} as T;
    }

    const contentType = response.headers.get("content-type");
    console.log(`Success response content-type: ${contentType}`);

    if (!contentType || !contentType.includes("application/json")) {
      const text = await response.text();
      console.log("Non-JSON response:", text);
      throw new Error(`Response was not JSON: ${text}`);
    }

    const jsonResponse = await response.json();
    console.log("Success response data:", jsonResponse);
    return jsonResponse?.data || jsonResponse;
  } catch (error) {
    console.error("Error in fetchApi:", {
      path,
      url: urlWithUser,
      error: error instanceof Error ? error.message : "Unknown error",
      stack: error instanceof Error ? error.stack : undefined,
    });

    if (error instanceof TypeError && error.message === "Failed to fetch") {
      throw new Error(`Network error - Could not reach backend server. ${url}`);
    }
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error(`Request timed out - server took too long to respond. ${url}`);
    }

    // Include more error details for debugging
    throw new Error(`Failed to fetch (${url}): ${error instanceof Error ? error.message : "Unknown error"}`);
  }
}

/**
 * Helper function to create a standardized error response
 * @param error The error object
 * @param defaultMessage Default error message if the error doesn't have a message
 * @returns A BaseResponse object with error information
 */
export function createErrorResponse<T>(error: unknown, defaultMessage: string): { success: false; error: string; data?: T } {
  const errorMessage = error instanceof Error ? error.message : defaultMessage;
  console.error(defaultMessage, error);
  return { success: false, error: errorMessage };
}
