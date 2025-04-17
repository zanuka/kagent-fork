"use server";
import { BaseResponse, Model } from "@/lib/types";
import { createErrorResponse, fetchApi } from "./utils";

/**
 * Gets all available models
 * @returns A promise with all models
 */
export async function getModels(): Promise<BaseResponse<Model[]>> {
  try {
    console.log("Fetching models from /modelconfigs...");
    const response = await fetchApi<Model[]>("/modelconfigs");
    console.log("Models response:", response);

    if (!response) {
      console.error("No response received from /modelconfigs");
      throw new Error("Failed to get models: No response received");
    }

    if (!Array.isArray(response)) {
      console.error("Response is not an array:", response);
      throw new Error("Failed to get models: Invalid response format");
    }

    return {
      success: true,
      data: response,
    };
  } catch (error) {
    console.error("Error in getModels:", error);
    return createErrorResponse<Model[]>(error, "Error getting models");
  }
}

/**
 * Gets a specific model by name
 * @param configName The model configuration name
 * @returns A promise with the model data
 */
export async function getModel(configName: string): Promise<BaseResponse<Model>> {
  try {
    console.log(`Fetching model ${configName} from /modelconfigs/${configName}...`);
    const response = await fetchApi<Model>(`/modelconfigs/${configName}`);
    console.log("Model response:", response);

    if (!response) {
      console.error(`No response received for model ${configName}`);
      throw new Error("Failed to get model");
    }

    return {
      success: true,
      data: response,
    };
  } catch (error) {
    console.error(`Error in getModel for ${configName}:`, error);
    return createErrorResponse<Model>(error, "Error getting model");
  }
}
