export default function Footer() {
  return (
    <footer className="mt-12 bg-gradient-to-r from-gray-800 to-gray-900 text-white py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <h3 className="text-xl font-bold mb-2">
              Dental & Gum Disease Classifier
            </h3>
            <p className="text-gray-400">
              Dual AI-powered dental health screening
            </p>
          </div>
          <div className="text-center md:text-right">
            <p className="text-gray-400">
              Teeth: ResNet50 (4 classes) • Gum: Binary (2 classes)
            </p>
            <p className="text-gray-500 text-sm mt-1">
              Version 2.0 • Optimized for CPU
            </p>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-6 pt-6 text-center text-gray-400 text-sm">
          <p>
            © 2024 Dental AI Research Project. For educational and research
            purposes.
          </p>
        </div>
      </div>
    </footer>
  );
}
