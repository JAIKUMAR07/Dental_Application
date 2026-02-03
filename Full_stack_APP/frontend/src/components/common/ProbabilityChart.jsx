import { useEffect, useState } from "react";

export default function ProbabilityChart({
  probabilities,
  color,
  compact = false,
}) {
  const [isAnimated, setIsAnimated] = useState(false);

  useEffect(() => {
    // Reset animation when probabilities change (or component mounts)
    setIsAnimated(false);

    // Trigger animation after a brief delay
    const timer = setTimeout(() => {
      setIsAnimated(true);
    }, 100);

    return () => clearTimeout(timer);
  }, [probabilities]);

  return (
    <div
      className={`bg-white rounded-xl ${compact ? "" : "p-6 border border-gray-200"}`}
    >
      {!compact && (
        <h4 className="font-bold text-gray-800 mb-4">
          Probability Distribution
        </h4>
      )}

      <div className={`${compact ? "space-y-2" : "space-y-4"}`}>
        {Object.entries(probabilities).map(([disease, prob]) => (
          <div key={disease} className="space-y-1">
            <div className="flex justify-between text-xs">
              <div className="flex items-center">
                <span
                  className={`font-medium capitalize ${compact ? "text-gray-600" : ""}`}
                >
                  {disease}
                </span>
              </div>
              <span className="font-bold">
                {typeof prob === "number" ? (prob * 100).toFixed(1) : prob}%
              </span>
            </div>

            <div
              className={`bg-gray-100 rounded-full overflow-hidden ${compact ? "h-1.5" : "h-2"}`}
            >
              <div
                className="h-full rounded-full transition-all duration-700 ease-out"
                style={{
                  width: isAnimated
                    ? `${typeof prob === "number" ? prob * 100 : prob}%`
                    : "0%",
                  backgroundColor: color,
                }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
