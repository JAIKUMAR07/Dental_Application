import { useState, useEffect } from "react";
import "./App.css";
import { dentalAPI } from "./services/api";

// Components
import Header from "./components/Header";
import Footer from "./components/Footer";
import ModelSelector from "./components/ModelSelector";
import UploadSection from "./components/UploadSection";
import ResultsDisplay from "./components/ResultsDisplay";
import BatchResults from "./components/BatchResults";
import InfoPanel from "./components/InfoPanel";

function App() {
  // State management
  const [models, setModels] = useState(null);
  const [currentModel, setCurrentModel] = useState("dental");
  const [activeTab, setActiveTab] = useState("single");
  const [result, setResult] = useState(null);
  const [batchResults, setBatchResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch models on mount
  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      const data = await dentalAPI.getModels();
      setModels(data);
    } catch (err) {
      setError("Failed to load models. Is the backend running?");
    }
  };

  // Select model
  const handleModelSelect = (model) => {
    setCurrentModel(model);
    setResult(null);
    setBatchResults(null);
    setError(null);
  };

  // Switch tabs
  const handleTabSwitch = (tab) => {
    setActiveTab(tab);
    setResult(null);
    setBatchResults(null);
    setError(null);
  };

  // Submit single prediction
  const handleSingleSubmit = async (selectedFile) => {
    if (!selectedFile) {
      setError("Please select an image");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await dentalAPI.predictSingle(selectedFile, currentModel);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Submit batch prediction
  const handleBatchSubmit = async (selectedFiles) => {
    if (!selectedFiles || selectedFiles.length === 0) {
      setError("Please select at least one image");
      return;
    }

    setLoading(true);
    setError(null);
    setBatchResults(null);

    try {
      const data = await dentalAPI.predictBatch(selectedFiles, currentModel);
      setBatchResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Clear results
  const clearResults = () => {
    setResult(null);
    setBatchResults(null);
    setError(null);
  };

  if (!models) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50">
        <div className="text-center">
          <div className="text-4xl mb-4">🦷</div>
          <div className="text-lg text-gray-700">Loading models...</div>
          {error && <div className="text-red-600 mt-2">{error}</div>}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-br from-blue-50 to-purple-50 min-h-screen">
      <Header models={models} />

      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <ModelSelector
          models={models}
          currentModel={currentModel}
          onSelect={handleModelSelect}
        />

        <UploadSection
          currentModel={currentModel}
          activeTab={activeTab}
          onSwitchTab={handleTabSwitch}
          onSingleSubmit={handleSingleSubmit}
          onBatchSubmit={handleBatchSubmit}
          loading={loading}
        />

        {error && (
          <div className="bg-gradient-to-r from-red-50 to-orange-50 border border-red-200 rounded-xl p-6 mb-8">
            <div className="flex items-center">
              <div className="bg-red-100 p-3 rounded-full mr-4">
                <i className="fas fa-exclamation-triangle text-red-600 text-xl"></i>
              </div>
              <div>
                <h3 className="text-lg font-bold text-red-800">Error</h3>
                <p className="text-red-700 mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {result && (
          <ResultsDisplay result={result} clearResults={clearResults} />
        )}
        {batchResults && (
          <BatchResults
            batchResults={batchResults}
            clearResults={clearResults}
          />
        )}

        <InfoPanel models={models} />
      </main>

      <Footer />
    </div>
  );
}

export default App;
