import { useState } from "react";
import "./App.css";

// Layout Components
import Header from "./components/layout/Header";
import Footer from "./components/layout/Footer";

// Pages
import HomePage from "./pages/HomePage";
import AnalysisPage from "./pages/AnalysisPage";
import ClinicLocatorPage from "./pages/ClinicLocatorPage";
import AboutPage from "./pages/AboutPage";

function App() {
  const [currentView, setCurrentView] = useState("home");
  const [models, setModels] = useState({
    dental: { loaded: true },
    gingivitis: { loaded: true },
  });

  const renderPage = () => {
    switch (currentView) {
      case "home":
        return <HomePage setView={setCurrentView} />;
      case "analysis":
        return <AnalysisPage setModels={setModels} />;
      case "locator":
        return <ClinicLocatorPage />;
      case "about":
        return <AboutPage />;
      default:
        return <HomePage setView={setCurrentView} />;
    }
  };

  return (
    <div className="bg-gradient-to-br from-blue-50 to-purple-50 min-h-screen flex flex-col">
      <Header
        models={models}
        currentView={currentView}
        setView={setCurrentView}
      />

      <main className="container mx-auto px-4 py-8 max-w-6xl flex-grow">
        {renderPage()}
      </main>

      <Footer />
    </div>
  );
}

export default App;
