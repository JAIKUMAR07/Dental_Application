import ProbabilityChart from "./common/ProbabilityChart";

export default function ResultsDisplay({ result, clearResults }) {
  const getStrokeDashoffset = (confidence) => {
    return 283 - (283 * confidence) / 100;
  };

  return (
    <div className="bg-white rounded-2xl shadow-xl p-6 mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        <i className="fas fa-chart-bar mr-2"></i>Analysis Results
        <span className="text-sm font-normal text-gray-600">
          ({result.selected_model === "dental" ? "Dental" : "Gingivitis"} Model)
        </span>
      </h2>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Left Column: Image */}
        <div className="lg:col-span-1">
          <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-4">
            <h3 className="font-bold text-gray-700 mb-3">Uploaded Image</h3>
            <div className="relative">
              <img
                src={result.image_url}
                alt="Dental scan"
                className="w-full rounded-lg shadow-lg"
              />
              <div className="absolute top-2 right-2 bg-black/70 text-white text-xs px-2 py-1 rounded">
                {result.upload_time}
              </div>
            </div>
            <div className="mt-3 p-3 bg-white rounded-lg">
              <p className="text-sm text-gray-600 truncate">
                {result.filename}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                Processing: {result.processing_time_ms} ms
              </p>
            </div>
          </div>
        </div>

        {/* Middle & Right Column: Prediction */}
        <div className="lg:col-span-2">
          <div className="space-y-6">
            {/* Main Prediction Card */}
            <div
              className="rounded-xl p-6"
              style={{
                background: `linear-gradient(135deg, ${result.color}20, ${result.color}40)`,
              }}
            >
              <div className="flex flex-col md:flex-row justify-between items-center">
                <div>
                  <div className="flex items-center mb-2">
                    <span className="text-3xl mr-3">{result.icon}</span>
                    <h3 className="text-2xl font-bold capitalize">
                      {result.prediction}
                    </h3>
                  </div>
                  <p className="text-gray-700">{result.description}</p>
                  {result.interpretation && (
                    <p className="text-sm text-gray-600 mt-1 italic">
                      {result.interpretation}
                    </p>
                  )}
                </div>
                <div className="mt-4 md:mt-0">
                  {/* Confidence Circle */}
                  <div className="relative w-24 h-24">
                    <svg className="w-full h-full" viewBox="0 0 100 100">
                      <circle
                        cx="50"
                        cy="50"
                        r="45"
                        stroke="#e5e7eb"
                        strokeWidth="8"
                        fill="none"
                      />
                      <circle
                        cx="50"
                        cy="50"
                        r="45"
                        stroke={result.color}
                        strokeWidth="8"
                        fill="none"
                        strokeLinecap="round"
                        strokeDasharray="283"
                        strokeDashoffset={getStrokeDashoffset(
                          result.confidence,
                        )}
                        className="progress-ring"
                      />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="text-center">
                        <div className="text-2xl font-bold">
                          {result.confidence}%
                        </div>
                        <div className="text-xs text-gray-600">Confidence</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Probability Chart */}
            <ProbabilityChart
              probabilities={result.all_probabilities}
              color={result.color}
            />
          </div>
        </div>
      </div>

      {/* Clear Button */}
      <div className="mt-8 text-center">
        <button
          onClick={clearResults}
          className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-6 py-2 rounded-lg transition"
        >
          <i className="fas fa-trash-alt mr-2"></i>Clear Results
        </button>
      </div>
    </div>
  );
}
