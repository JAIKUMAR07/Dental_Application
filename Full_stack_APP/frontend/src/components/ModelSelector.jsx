export default function ModelSelector({ models, currentModel, onSelect }) {
  if (!models) return null;

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center">
        <i className="fas fa-brain mr-2"></i>Select Analysis Type
      </h2>
      <div className="grid md:grid-cols-2 gap-6">
        {/* Dental Disease Model */}
        <div
          className={`model-selector bg-white rounded-2xl shadow-lg p-6 ${currentModel === "dental" ? "selected" : ""}`}
          onClick={() => onSelect("dental")}
        >
          <div className="dental-gradient text-white rounded-xl p-4 mb-4">
            <div className="flex justify-between items-center">
              <div>
                <h3 className="text-2xl font-bold">Teeth Disease</h3>
                <p className="text-sm opacity-90">4-Class Detection</p>
              </div>
              <div className="text-4xl">🦷</div>
            </div>
          </div>
          <div className="space-y-2">
            {models.dental?.classes.map((info, idx) => (
              <div key={idx} className="flex items-center text-sm">
                <span className="mr-2">{info.icon}</span>
                <span className="font-medium">{info.name}</span>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t">
            <p className="text-xs text-gray-600">
              Detects caries, calculus, healthy teeth, and discoloration
            </p>
          </div>
        </div>

        {/* Gingivitis Model */}
        <div
          className={`model-selector bg-white rounded-2xl shadow-lg p-6 ${currentModel === "gingivitis" ? "selected" : ""}`}
          onClick={() => onSelect("gingivitis")}
        >
          <div className="gingivitis-gradient text-white rounded-xl p-4 mb-4">
            <div className="flex justify-between items-center">
              <div>
                <h3 className="text-2xl font-bold">Gum Disease</h3>
                <p className="text-sm opacity-90">2-Class Detection</p>
              </div>
              <div className="text-4xl">🩺</div>
            </div>
          </div>
          <div className="space-y-2">
            {models.gingivitis?.classes.map((info, idx) => (
              <div key={idx} className="flex items-center text-sm">
                <span className="mr-2">{info.icon}</span>
                <span className="font-medium">{info.name}</span>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t">
            <p className="text-xs text-gray-600">
              Analyzes gum health and detects gingivitis
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
