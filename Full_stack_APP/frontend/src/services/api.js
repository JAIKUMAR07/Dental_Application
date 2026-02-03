const API_BASE_URL = "http://localhost:8000";

export const dentalAPI = {
  // Get models information
  async getModels() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/models`);
      if (!response.ok) {
        throw new Error("Failed to fetch models");
      }
      return await response.json();
    } catch (error) {
      console.error("Error fetching models:", error);
      throw error;
    }
  },

  // Predict single image
  async predictSingle(file, modelType) {
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("model_type", modelType);

      const response = await fetch(`${API_BASE_URL}/api/predict`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || "Prediction failed");
      }

      return await response.json();
    } catch (error) {
      console.error("Error in prediction:", error);
      throw error;
    }
  },

  // Predict batch images
  async predictBatch(files, modelType) {
    try {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append("files", file);
      });
      formData.append("model_type", modelType);

      const response = await fetch(`${API_BASE_URL}/api/predict_batch`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || "Batch prediction failed");
      }

      return await response.json();
    } catch (error) {
      console.error("Error in batch prediction:", error);
      throw error;
    }
  },

  // Clear uploaded files
  async clearFiles() {
    try {
      const response = await fetch(`${API_BASE_URL}/clear`);
      if (!response.ok) {
        throw new Error("Failed to clear files");
      }
      return await response.json();
    } catch (error) {
      console.error("Error clearing files:", error);
      throw error;
    }
  },

  // Health check
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (!response.ok) {
        throw new Error("Health check failed");
      }
      return await response.json();
    } catch (error) {
      console.error("Error in health check:", error);
      throw error;
    }
  },
};
