import { useState, useEffect } from "react";

export default function HomePage({ setView }) {
  const [stats, setStats] = useState({
    diseases: 4,
    accuracy: 97,
    processed: 1250,
  });

  // Animated counter effect
  useEffect(() => {
    const interval = setInterval(() => {
      setStats((prev) => ({
        ...prev,
        processed: prev.processed + Math.floor(Math.random() * 3),
      }));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center py-12 md:py-20">
        <div className="inline-block mb-6 px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-semibold">
          <i className="fas fa-sparkles mr-2"></i>AI-Powered Dental Health
        </div>

        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
          Advanced Dental Disease
          <br />
          <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Detection System
          </span>
        </h1>

        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Harness the power of deep learning to identify dental conditions
          instantly. Our dual-model system provides accurate analysis for both
          tooth diseases and gum health.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => setView("analysis")}
            className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white px-8 py-4 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
          >
            <i className="fas fa-microscope mr-2"></i>Start Analysis
          </button>
          <button
            onClick={() => setView("locator")}
            className="bg-white hover:bg-gray-50 text-blue-600 px-8 py-4 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all border-2 border-blue-600"
          >
            <i className="fas fa-map-marked-alt mr-2"></i>Find Clinic
          </button>
        </div>
      </section>

      {/* Stats Section */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-8 rounded-2xl text-center shadow-lg hover:shadow-xl transition-shadow">
          <div className="text-5xl font-bold text-blue-600 mb-2">
            {stats.diseases}
          </div>
          <div className="text-gray-700 font-semibold">Disease Types</div>
          <div className="text-sm text-gray-500 mt-2">
            Caries, Calculus, Discoloration, Gingivitis
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-50 to-green-100 p-8 rounded-2xl text-center shadow-lg hover:shadow-xl transition-shadow">
          <div className="text-5xl font-bold text-green-600 mb-2">
            {stats.accuracy}%
          </div>
          <div className="text-gray-700 font-semibold">Model Accuracy</div>
          <div className="text-sm text-gray-500 mt-2">
            Validated on 3-fold cross-validation
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-8 rounded-2xl text-center shadow-lg hover:shadow-xl transition-shadow">
          <div className="text-5xl font-bold text-purple-600 mb-2">
            {stats.processed.toLocaleString()}
          </div>
          <div className="text-gray-700 font-semibold">Images Analyzed</div>
          <div className="text-sm text-gray-500 mt-2">Growing every day</div>
        </div>
      </section>

      {/* Features Section */}
      <section>
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Powerful Features
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-all hover:-translate-y-1">
            <div className="w-14 h-14 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <i className="fas fa-brain text-blue-600 text-2xl"></i>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Dual AI Models
            </h3>
            <p className="text-gray-600">
              ResNet50-based architecture for 4-class dental disease detection
              and specialized binary model for gingivitis screening.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-all hover:-translate-y-1">
            <div className="w-14 h-14 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <i className="fas fa-bolt text-green-600 text-2xl"></i>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Instant Results
            </h3>
            <p className="text-gray-600">
              Get comprehensive analysis in seconds with detailed probability
              distributions and confidence scores.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-all hover:-translate-y-1">
            <div className="w-14 h-14 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <i className="fas fa-images text-purple-600 text-2xl"></i>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Batch Processing
            </h3>
            <p className="text-gray-600">
              Analyze multiple images simultaneously for efficient screening of
              large datasets.
            </p>
          </div>

          {/* Feature 4 */}
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-all hover:-translate-y-1">
            <div className="w-14 h-14 bg-red-100 rounded-lg flex items-center justify-center mb-4">
              <i className="fas fa-shield-alt text-red-600 text-2xl"></i>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Privacy First
            </h3>
            <p className="text-gray-600">
              All processing happens locally. Your images are never stored or
              transmitted to external servers.
            </p>
          </div>

          {/* Feature 5 */}
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-all hover:-translate-y-1">
            <div className="w-14 h-14 bg-yellow-100 rounded-lg flex items-center justify-center mb-4">
              <i className="fas fa-map-marked-alt text-yellow-600 text-2xl"></i>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Clinic Locator
            </h3>
            <p className="text-gray-600">
              Find nearby dental clinics on an interactive map powered by
              OpenStreetMap.
            </p>
          </div>

          {/* Feature 6 */}
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-all hover:-translate-y-1">
            <div className="w-14 h-14 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
              <i className="fas fa-chart-line text-indigo-600 text-2xl"></i>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">
              Visual Analytics
            </h3>
            <p className="text-gray-600">
              Interactive charts and visualizations help you understand
              prediction confidence and disease probabilities.
            </p>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-3xl p-8 md:p-12">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          How It Works
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              1
            </div>
            <h3 className="font-bold text-lg mb-2">Upload Image</h3>
            <p className="text-gray-600 text-sm">
              Select a dental X-ray or photo
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              2
            </div>
            <h3 className="font-bold text-lg mb-2">Choose Model</h3>
            <p className="text-gray-600 text-sm">
              Select dental or gum analysis
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              3
            </div>
            <h3 className="font-bold text-lg mb-2">AI Analysis</h3>
            <p className="text-gray-600 text-sm">
              Deep learning model processes image
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              4
            </div>
            <h3 className="font-bold text-lg mb-2">Get Results</h3>
            <p className="text-gray-600 text-sm">
              View detailed predictions & insights
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="text-center py-12 bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl text-white">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          Ready to Get Started?
        </h2>
        <p className="text-xl mb-8 opacity-90">
          Experience the future of dental diagnostics today
        </p>
        <button
          onClick={() => setView("analysis")}
          className="bg-white text-blue-600 px-10 py-4 rounded-xl font-bold text-lg shadow-xl hover:shadow-2xl transition-all transform hover:scale-105"
        >
          Try It Now <i className="fas fa-arrow-right ml-2"></i>
        </button>
      </section>

      {/* Disclaimer */}
      <section className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg">
        <div className="flex items-start">
          <i className="fas fa-exclamation-triangle text-yellow-600 text-xl mr-3 mt-1"></i>
          <div>
            <h3 className="font-bold text-gray-900 mb-2">Medical Disclaimer</h3>
            <p className="text-gray-700 text-sm">
              This tool is designed for educational and research purposes only.
              It should not be used as a substitute for professional medical
              advice, diagnosis, or treatment. Always consult with a qualified
              healthcare provider for any dental health concerns.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
