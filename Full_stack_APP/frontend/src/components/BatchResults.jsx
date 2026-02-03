import ProbabilityChart from "./common/ProbabilityChart";

export default function BatchResults({ batchResults, clearResults }) {
  return (
    <div className="bg-white rounded-2xl shadow-xl p-6 mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        <i className="fas fa-chart-pie mr-2"></i>Batch Analysis Results
        <span className="text-sm font-normal text-gray-600">
          ({batchResults.model_type === "dental" ? "Dental" : "Gingivitis"}{" "}
          Model)
        </span>
      </h2>

      {/* Results Grid - Adjusted gap and cols for better fit with charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {batchResults.results.map((item, idx) => (
          <div
            key={idx}
            className="rounded-xl p-5 shadow-lg border border-gray-100 bg-white hover:shadow-xl transition-shadow duration-300 flex flex-col"
          >
            {/* Header: Image & Top Prediction */}
            <div className="flex gap-4 mb-4">
              {/* Image Thumbnail */}
              {item.image_url && (
                <div className="w-24 h-24 flex-shrink-0">
                  <img
                    src={item.image_url}
                    alt={item.filename}
                    className="w-full h-full object-cover rounded-lg shadow-sm"
                  />
                </div>
              )}

              {/* Top Result Info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center mb-1">
                  <span className="text-xl mr-2">{item.icon || "📋"}</span>
                  <h4
                    className="font-bold capitalize text-lg truncate"
                    title={item.prediction}
                  >
                    {item.prediction}
                  </h4>
                </div>
                <div
                  className="text-xs font-bold px-2 py-1 rounded inline-block mb-1"
                  style={{
                    color: item.color,
                    backgroundColor: `${item.color}15`, // 10% opacity hex
                  }}
                >
                  {item.confidence}% Confidence
                </div>
                <div
                  className="text-xs text-gray-500 truncate"
                  title={item.filename}
                >
                  {item.filename}
                </div>
              </div>
            </div>

            {/* Probability Distribution Chart */}
            {item.all_probabilities && !item.error && (
              <div className="mt-auto pt-4 border-t border-gray-100">
                <ProbabilityChart
                  probabilities={item.all_probabilities}
                  color={item.color || "#667eea"}
                  compact={true}
                />
              </div>
            )}

            {/* Error Message */}
            {item.error && (
              <div className="mt-2 text-xs text-red-700 bg-red-50 p-2 rounded">
                <i className="fas fa-exclamation-circle mr-1"></i>
                {item.error}
              </div>
            )}

            {/* Description (Optional) */}
            {!item.error && item.description && (
              <p className="mt-3 text-xs text-gray-500 italic line-clamp-2">
                {item.description}
              </p>
            )}
          </div>
        ))}
      </div>

      {/* Clear Button */}
      <div className="mt-8 text-center">
        <button
          onClick={clearResults}
          className="bg-gray-200 hover:bg-gray-300 text-gray-700 px-6 py-2 rounded-lg transition-colors"
        >
          <i className="fas fa-trash-alt mr-2"></i>Clear All Results
        </button>
      </div>
    </div>
  );
}
