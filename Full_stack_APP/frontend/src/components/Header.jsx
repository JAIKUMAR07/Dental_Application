export default function Header({ models, currentView, setView }) {
  return (
    <header className="gradient-bg text-white shadow-xl">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center gap-6">
            <div>
              <h1 className="text-3xl font-bold">
                <i className="fas fa-tooth mr-3"></i>Dental AI
              </h1>
              <p className="text-gray-200 mt-2 text-sm">
                Advanced Disease Detection
              </p>
            </div>

            {/* Navigation Tabs */}
            <nav className="hidden md:flex bg-white/10 rounded-lg p-1">
              <button
                onClick={() => setView("analysis")}
                className={`px-4 py-2 rounded-md transition-all ${currentView === "analysis" ? "bg-white text-blue-900 font-bold shadow-md" : "text-gray-100 hover:bg-white/10"}`}
              >
                <i className="fas fa-microscope mr-2"></i>AI Analysis
              </button>
              <button
                onClick={() => setView("locator")}
                className={`px-4 py-2 rounded-md transition-all ${currentView === "locator" ? "bg-white text-blue-900 font-bold shadow-md" : "text-gray-100 hover:bg-white/10"}`}
              >
                <i className="fas fa-map-marked-alt mr-2"></i>Find Clinic
              </button>
            </nav>
          </div>

          <div className="mt-4 md:mt-0 flex gap-2">
            {!models?.dental?.loaded && (
              <span className="bg-yellow-500 text-white px-3 py-1 rounded-full text-xs font-bold">
                Dental: Test
              </span>
            )}
            {/* Mobile Nav Only */}
            <div className="md:hidden flex gap-2">
              <button
                onClick={() => setView("analysis")}
                className={`p-2 rounded ${currentView === "analysis" ? "bg-white text-blue-900" : "bg-white/20"}`}
              >
                <i className="fas fa-microscope"></i>
              </button>
              <button
                onClick={() => setView("locator")}
                className={`p-2 rounded ${currentView === "locator" ? "bg-white text-blue-900" : "bg-white/20"}`}
              >
                <i className="fas fa-map-marked-alt"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
