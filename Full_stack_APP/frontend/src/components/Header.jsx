export default function Header({ models }) {
  return (
    <header className="gradient-bg text-white shadow-xl">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold">
              <i className="fas fa-tooth mr-3"></i>Dental & Gum Disease
              Classifier
            </h1>
            <p className="text-gray-200 mt-2">
              AI-powered detection with dual model selection
            </p>
          </div>
          <div className="mt-4 md:mt-0 flex gap-2">
            {!models?.dental?.loaded && (
              <span className="bg-yellow-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                <i className="fas fa-exclamation-triangle mr-1"></i>Dental: Test
                Mode
              </span>
            )}
            {!models?.gingivitis?.loaded && (
              <span className="bg-yellow-500 text-white px-3 py-1 rounded-full text-sm font-bold">
                <i className="fas fa-exclamation-triangle mr-1"></i>Gum: Test
                Mode
              </span>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
