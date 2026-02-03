import { useState } from "react";

export default function Header({ models, currentView, setView }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { id: "home", label: "Home", icon: "fa-home" },
    { id: "analysis", label: "AI Analysis", icon: "fa-microscope" },
    { id: "locator", label: "Find Clinic", icon: "fa-map-marked-alt" },
    { id: "about", label: "About", icon: "fa-info-circle" },
  ];

  const handleNavClick = (view) => {
    setView(view);
    setMobileMenuOpen(false);
  };

  return (
    <header className="gradient-bg text-white shadow-xl sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <div
            className="flex items-center cursor-pointer hover:opacity-80 transition-opacity"
            onClick={() => handleNavClick("home")}
          >
            <i className="fas fa-tooth text-3xl mr-3"></i>
            <div>
              <h1 className="text-2xl font-bold">Dental AI</h1>
              <p className="text-xs text-gray-200 hidden sm:block">
                Advanced Disease Detection
              </p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-2 bg-white/10 rounded-lg p-1">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`px-4 py-2 rounded-md transition-all font-medium ${
                  currentView === item.id
                    ? "bg-white text-blue-900 shadow-md"
                    : "text-gray-100 hover:bg-white/10"
                }`}
              >
                <i className={`fas ${item.icon} mr-2`}></i>
                {item.label}
              </button>
            ))}
          </nav>

          {/* Status Badge & Mobile Menu Button */}
          <div className="flex items-center gap-3">
            {!models?.dental?.loaded && (
              <span className="hidden sm:inline-block bg-yellow-500 text-white px-3 py-1 rounded-full text-xs font-bold">
                Test Mode
              </span>
            )}

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors"
            >
              <i
                className={`fas ${mobileMenuOpen ? "fa-times" : "fa-bars"} text-xl`}
              ></i>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <nav className="md:hidden mt-4 pb-2 space-y-2 animate-fadeIn">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`w-full text-left px-4 py-3 rounded-lg transition-all font-medium ${
                  currentView === item.id
                    ? "bg-white text-blue-900 shadow-md"
                    : "bg-white/10 text-gray-100 hover:bg-white/20"
                }`}
              >
                <i className={`fas ${item.icon} mr-3 w-5`}></i>
                {item.label}
              </button>
            ))}
          </nav>
        )}
      </div>
    </header>
  );
}
