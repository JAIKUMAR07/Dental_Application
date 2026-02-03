export default function AboutPage() {
  return (
    <div className="space-y-12">
      {/* Header */}
      <section className="text-center">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          About This System
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          A cutting-edge AI platform combining deep learning and medical imaging
          to revolutionize dental disease detection and patient care.
        </p>
      </section>

      {/* Mission */}
      <section className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-3xl p-8 md:p-12">
        <div className="flex items-center mb-6">
          <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mr-4">
            <i className="fas fa-bullseye text-white text-xl"></i>
          </div>
          <h2 className="text-3xl font-bold text-gray-900">Our Mission</h2>
        </div>
        <p className="text-lg text-gray-700 leading-relaxed">
          To democratize access to advanced dental diagnostics by leveraging
          artificial intelligence. We aim to assist healthcare professionals and
          empower individuals with instant, accurate preliminary assessments of
          dental conditions, ultimately improving oral health outcomes
          worldwide.
        </p>
      </section>

      {/* Technology Stack */}
      <section>
        <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
          Technology Stack
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* AI/ML */}
          <div className="bg-white rounded-xl shadow-lg p-6 border-t-4 border-blue-600">
            <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <i className="fas fa-brain text-blue-600 mr-3"></i>
              AI & Machine Learning
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>TensorFlow 2.x</strong> - Deep learning framework
                </span>
              </li>
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>ResNet50</strong> - Transfer learning backbone
                </span>
              </li>
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>ImageNet Weights</strong> - Pre-trained features
                </span>
              </li>
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>3-Fold Cross-Validation</strong> - Robust training
                </span>
              </li>
            </ul>
          </div>

          {/* Backend */}
          <div className="bg-white rounded-xl shadow-lg p-6 border-t-4 border-green-600">
            <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <i className="fas fa-server text-green-600 mr-3"></i>
              Backend Infrastructure
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>FastAPI</strong> - High-performance Python API
                </span>
              </li>
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>Uvicorn</strong> - ASGI server
                </span>
              </li>
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>PIL/Pillow</strong> - Image processing
                </span>
              </li>
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>NumPy</strong> - Numerical computations
                </span>
              </li>
            </ul>
          </div>

          {/* Frontend */}
          <div className="bg-white rounded-xl shadow-lg p-6 border-t-4 border-purple-600">
            <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <i className="fas fa-palette text-purple-600 mr-3"></i>
              Frontend Technologies
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>React 19</strong> - Modern UI library
                </span>
              </li>
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>Vite</strong> - Lightning-fast build tool
                </span>
              </li>
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>Tailwind CSS</strong> - Utility-first styling
                </span>
              </li>
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>Leaflet</strong> - Interactive maps
                </span>
              </li>
            </ul>
          </div>

          {/* APIs */}
          <div className="bg-white rounded-xl shadow-lg p-6 border-t-4 border-yellow-600">
            <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <i className="fas fa-plug text-yellow-600 mr-3"></i>
              External Services
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>OpenStreetMap</strong> - Map tiles & geocoding
                </span>
              </li>
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>Nominatim API</strong> - Location search
                </span>
              </li>
              <li className="flex items-start">
                <i className="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
                <span>
                  <strong>FontAwesome</strong> - Icon library
                </span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Model Architecture */}
      <section className="bg-white rounded-xl shadow-xl p-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-6 flex items-center">
          <i className="fas fa-project-diagram text-blue-600 mr-3"></i>
          Model Architecture
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Dental Model */}
          <div>
            <h3 className="text-xl font-bold text-blue-600 mb-4">
              Dental Disease Model
            </h3>
            <div className="space-y-3">
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="font-semibold text-gray-900 mb-1">
                  Architecture
                </div>
                <div className="text-sm text-gray-700">
                  ResNet50 + Custom Classification Head
                </div>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="font-semibold text-gray-900 mb-1">
                  Classes (4)
                </div>
                <div className="text-sm text-gray-700">
                  Caries, Calculus, Healthy, Discoloration
                </div>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="font-semibold text-gray-900 mb-1">
                  Input Size
                </div>
                <div className="text-sm text-gray-700">224 × 224 × 3 (RGB)</div>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg">
                <div className="font-semibold text-gray-900 mb-1">Accuracy</div>
                <div className="text-sm text-gray-700">~97% (3-fold CV)</div>
              </div>
            </div>
          </div>

          {/* Gingivitis Model */}
          <div>
            <h3 className="text-xl font-bold text-green-600 mb-4">
              Gingivitis Detection Model
            </h3>
            <div className="space-y-3">
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="font-semibold text-gray-900 mb-1">
                  Architecture
                </div>
                <div className="text-sm text-gray-700">
                  Custom CNN + Binary Classification
                </div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="font-semibold text-gray-900 mb-1">
                  Classes (2)
                </div>
                <div className="text-sm text-gray-700">Healthy, Gingivitis</div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="font-semibold text-gray-900 mb-1">
                  Input Size
                </div>
                <div className="text-sm text-gray-700">224 × 224 × 3 (RGB)</div>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <div className="font-semibold text-gray-900 mb-1">
                  Threshold
                </div>
                <div className="text-sm text-gray-700">
                  0.5 (Balanced Sensitivity/Specificity)
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section>
        <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
          Key Features
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex items-start bg-white p-6 rounded-xl shadow-lg">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
              <i className="fas fa-upload text-blue-600 text-xl"></i>
            </div>
            <div>
              <h3 className="font-bold text-lg mb-2">Single & Batch Upload</h3>
              <p className="text-gray-600 text-sm">
                Analyze individual images or process multiple files
                simultaneously for efficient screening.
              </p>
            </div>
          </div>

          <div className="flex items-start bg-white p-6 rounded-xl shadow-lg">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
              <i className="fas fa-chart-bar text-green-600 text-xl"></i>
            </div>
            <div>
              <h3 className="font-bold text-lg mb-2">
                Probability Distribution
              </h3>
              <p className="text-gray-600 text-sm">
                View detailed confidence scores across all disease categories
                with interactive visualizations.
              </p>
            </div>
          </div>

          <div className="flex items-start bg-white p-6 rounded-xl shadow-lg">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
              <i className="fas fa-lock text-purple-600 text-xl"></i>
            </div>
            <div>
              <h3 className="font-bold text-lg mb-2">Privacy & Security</h3>
              <p className="text-gray-600 text-sm">
                All processing occurs locally. Images are not stored or
                transmitted to external servers.
              </p>
            </div>
          </div>

          <div className="flex items-start bg-white p-6 rounded-xl shadow-lg">
            <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
              <i className="fas fa-mobile-alt text-red-600 text-xl"></i>
            </div>
            <div>
              <h3 className="font-bold text-lg mb-2">Fully Responsive</h3>
              <p className="text-gray-600 text-sm">
                Optimized for desktop, tablet, and mobile devices with adaptive
                layouts.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Disclaimer */}
      <section className="bg-red-50 border-l-4 border-red-500 p-6 rounded-lg">
        <div className="flex items-start">
          <i className="fas fa-exclamation-circle text-red-600 text-2xl mr-4 mt-1"></i>
          <div>
            <h3 className="font-bold text-gray-900 text-lg mb-3">
              Important Medical Disclaimer
            </h3>
            <div className="text-gray-700 space-y-2 text-sm">
              <p>
                <strong>
                  This system is intended for educational and research purposes
                  only.
                </strong>{" "}
                It is not a medical device and should not be used for clinical
                diagnosis or treatment decisions.
              </p>
              <p>
                The AI models provide preliminary assessments based on image
                analysis and may not account for all clinical factors. Results
                should always be verified by qualified dental professionals.
              </p>
              <p>
                <strong>
                  Always consult with a licensed dentist or healthcare provider
                </strong>{" "}
                for proper diagnosis, treatment recommendations, and medical
                advice regarding dental health concerns.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Version Info */}
      <section className="bg-gray-100 rounded-xl p-6 text-center">
        <div className="text-sm text-gray-600">
          <p className="mb-2">
            <strong>Version 2.0</strong> • Built with ❤️ for Dental AI Research
          </p>
          <p className="text-xs text-gray-500">
            © 2024 Dental AI Project • For Educational & Research Use
          </p>
        </div>
      </section>
    </div>
  );
}
