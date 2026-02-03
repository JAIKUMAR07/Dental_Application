import { useState } from "react";

export default function UploadSection({
  currentModel,
  activeTab,
  onSwitchTab,
  onSingleSubmit,
  onBatchSubmit,
  loading,
}) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedFiles, setSelectedFiles] = useState([]);

  // Handle single file selection
  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  // Handle multiple files selection
  const handleFilesSelect = (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      setSelectedFiles(files);
    }
  };

  const handleSingleFormSubmit = (e) => {
    e.preventDefault();
    onSingleSubmit(selectedFile);
  };

  const handleBatchFormSubmit = (e) => {
    e.preventDefault();
    onBatchSubmit(selectedFiles);
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-6 mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        <i className="fas fa-cloud-upload-alt mr-2"></i>Upload Image
      </h2>

      {/* Tabs */}
      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8">
            <button
              onClick={() => onSwitchTab("single")}
              className={`py-3 px-1 font-medium text-lg border-b-2 ${
                activeTab === "single"
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500"
              }`}
            >
              <i className="fas fa-image mr-2"></i>Single Image
            </button>
            <button
              onClick={() => onSwitchTab("batch")}
              className={`py-3 px-1 font-medium text-lg border-b-2 ${
                activeTab === "batch"
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500"
              }`}
            >
              <i className="fas fa-layer-group mr-2"></i>Batch Analysis
            </button>
          </nav>
        </div>
      </div>

      {/* Current Model Display */}
      <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
        <div className="flex items-center">
          <i className="fas fa-info-circle text-blue-600 mr-2"></i>
          <span className="text-sm font-medium text-blue-800">
            Selected Model:{" "}
            <span className="font-bold">
              {currentModel === "dental"
                ? "Teeth Disease (4 classes)"
                : "Gum Disease (2 classes)"}
            </span>
          </span>
        </div>
      </div>

      {/* Single Upload */}
      {activeTab === "single" && (
        <form onSubmit={handleSingleFormSubmit} className="space-y-6">
          <div
            className="upload-area p-8 text-center cursor-pointer"
            onClick={() => document.getElementById("singleFile").click()}
          >
            <input
              type="file"
              id="singleFile"
              accept="image/*"
              className="hidden"
              onChange={handleFileSelect}
            />
            <div className="py-8">
              <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center">
                <i className="fas fa-tooth text-3xl text-blue-500"></i>
              </div>
              <p className="text-gray-600 mb-2">Click to upload dental image</p>
              <p className="text-gray-500 text-sm">JPG, PNG • Max 10MB</p>
              <button
                type="button"
                className="mt-4 gradient-bg hover:opacity-90 text-white px-6 py-2 rounded-lg"
              >
                Choose Image
              </button>
            </div>
            {selectedFile && (
              <div className="mt-4 text-blue-600 font-medium">
                Selected: {selectedFile.name}
              </div>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full gradient-bg hover:opacity-90 text-white font-bold py-3 rounded-lg text-lg disabled:opacity-50"
          >
            {loading ? (
              <>
                <i className="fas fa-spinner fa-spin mr-2"></i>Analyzing...
              </>
            ) : (
              <>
                <i className="fas fa-search mr-2"></i>Analyze Image
              </>
            )}
          </button>
        </form>
      )}

      {/* Batch Upload */}
      {activeTab === "batch" && (
        <form onSubmit={handleBatchFormSubmit} className="space-y-6">
          <div
            className="upload-area p-8 text-center cursor-pointer"
            onClick={() => document.getElementById("batchFiles").click()}
          >
            <input
              type="file"
              id="batchFiles"
              accept="image/*"
              multiple
              className="hidden"
              onChange={handleFilesSelect}
            />
            <div className="py-8">
              <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-purple-100 to-pink-100 flex items-center justify-center">
                <i className="fas fa-images text-3xl text-purple-500"></i>
              </div>
              <p className="text-gray-600 mb-2">
                Click to upload multiple images
              </p>
              <p className="text-gray-500 text-sm">
                Hold Ctrl/Cmd to select multiple files
              </p>
              <button
                type="button"
                className="mt-4 bg-gradient-to-r from-purple-500 to-pink-500 hover:opacity-90 text-white px-6 py-2 rounded-lg"
              >
                Choose Files
              </button>
            </div>
            {selectedFiles.length > 0 && (
              <div className="mt-4 text-purple-600 font-medium">
                {selectedFiles.length} file(s) selected
              </div>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:opacity-90 text-white font-bold py-3 rounded-lg text-lg disabled:opacity-50"
          >
            {loading ? (
              <>
                <i className="fas fa-spinner fa-spin mr-2"></i>Analyzing...
              </>
            ) : (
              <>
                <i className="fas fa-search mr-2"></i>Analyze All Images
              </>
            )}
          </button>
        </form>
      )}
    </div>
  );
}
