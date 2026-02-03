export default function InfoPanel({ models }) {
  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-2xl p-6">
      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <h3 className="text-xl font-bold text-blue-800 mb-4">
            <i className="fas fa-info-circle mr-2"></i>About This System
          </h3>
          <p className="text-gray-700 mb-4">
            This AI system provides two specialized models for comprehensive
            dental analysis:
          </p>

          <div className="bg-white/50 rounded-lg p-4 mb-3">
            <h4 className="font-bold text-gray-700 mb-2">
              🦷 Teeth Disease Model
            </h4>
            <p className="text-sm text-gray-600">
              Detects 4 conditions: caries, calculus, healthy teeth, and
              discoloration using ResNet50 architecture.
            </p>
          </div>

          <div className="bg-white/50 rounded-lg p-4">
            <h4 className="font-bold text-gray-700 mb-2">
              🩺 Gum Disease Model
            </h4>
            <p className="text-sm text-gray-600">
              Binary classification for gingivitis detection focusing on gum
              health.
            </p>
          </div>
        </div>

        <div>
          <div className="bg-white/50 rounded-lg p-4 mb-4">
            <h4 className="font-bold text-gray-700 mb-2">📁 How to Use:</h4>
            <ol className="list-decimal list-inside text-sm text-gray-600 space-y-1">
              <li>Select analysis type (Teeth or Gum)</li>
              <li>Upload clear dental images</li>
              <li>AI analyzes images instantly</li>
              <li>View detailed results with confidence scores</li>
              <li>Multiple images can be analyzed together</li>
            </ol>
          </div>

          <div className="bg-white/50 rounded-lg p-4 mb-4">
            <h4 className="font-bold text-gray-700 mb-2">
              ⚕️ Medical Disclaimer
            </h4>
            <p className="text-gray-600 text-sm">
              This tool is for educational and screening purposes only. Always
              consult with a qualified dental professional for diagnosis and
              treatment.
            </p>
          </div>

          <div className="bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg p-4">
            <div className="flex justify-between items-center">
              <div>
                <h4 className="font-bold">System Status</h4>
                <p className="text-sm opacity-90">
                  Dental:{" "}
                  {models?.dental?.loaded ? "✅ Loaded" : "⚠️ Test Mode"}
                  <br />
                  Gum:{" "}
                  {models?.gingivitis?.loaded ? "✅ Loaded" : "⚠️ Test Mode"}
                </p>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold">2</div>
                <div className="text-sm opacity-90">AI Models</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
