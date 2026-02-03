import { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Fix Leaflet default icon issue in React
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

L.Marker.prototype.options.icon = DefaultIcon;

// Component to handle map center updates
function ChangeView({ center, zoom }) {
  const map = useMap();
  map.setView(center, zoom);
  return null;
}

export default function ClinicLocatorPage() {
  const [query, setQuery] = useState("");
  const [clinics, setClinics] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mapCenter, setMapCenter] = useState([40.7128, -74.006]); // Default to New York
  const [zoom, setZoom] = useState(13);
  const [selectedClinic, setSelectedClinic] = useState(null);

  // Search function using OpenStreetMap Nominatim API
  const searchClinics = async (e) => {
    if (e) e.preventDefault();
    if (!query) return;

    setLoading(true);
    try {
      // 1. First find the location coordinates
      const locationRes = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1`,
      );
      const locationData = await locationRes.json();

      if (locationData.length > 0) {
        const { lat, lon } = locationData[0];
        const newCenter = [parseFloat(lat), parseFloat(lon)];
        setMapCenter(newCenter);

        // 2. Then search for dental clinics around that location
        const clinicRes = await fetch(
          `https://nominatim.openstreetmap.org/search?format=json&q=dentist+near+${encodeURIComponent(query)}&addressdetails=1&limit=30`,
        );
        const clinicData = await clinicRes.json();

        setClinics(clinicData);
      }
    } catch (error) {
      console.error("Error finding clinics:", error);
    } finally {
      setLoading(false);
    }
  };

  // Get current location
  const handleMyLocation = () => {
    if (navigator.geolocation) {
      setLoading(true);
      navigator.geolocation.getCurrentPosition(
        async (position) => {
          const { latitude, longitude } = position.coords;
          setMapCenter([latitude, longitude]);
          setZoom(14);

          try {
            const clinicRes = await fetch(
              `https://nominatim.openstreetmap.org/search?format=json&q=dentist&viewbox=${longitude - 0.1},${latitude + 0.1},${longitude + 0.1},${latitude - 0.1}&bounded=1&limit=30&addressdetails=1`,
            );
            const clinicData = await clinicRes.json();
            setClinics(clinicData);
          } catch (err) {
            console.error(err);
          }
          setLoading(false);
        },
        (error) => {
          console.error(error);
          setLoading(false);
          alert("Could not get your location.");
        },
      );
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-200px)] rounded-xl overflow-hidden shadow-2xl bg-white">
      {/* Top Bar */}
      <div className="bg-blue-600 p-4 text-white flex flex-col md:flex-row justify-between items-center gap-4">
        <h2 className="text-xl font-bold flex items-center">
          <i className="fas fa-map-marked-alt mr-2"></i> Dental Clinic Locator
        </h2>

        <form onSubmit={searchClinics} className="flex w-full md:w-auto gap-2">
          <input
            type="text"
            placeholder="Enter city or zip code..."
            className="px-4 py-2 rounded-lg text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-300 w-full md:w-80"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            type="submit"
            className="bg-blue-800 hover:bg-blue-900 px-4 py-2 rounded-lg transition-colors font-semibold"
            disabled={loading}
          >
            {loading ? <i className="fas fa-spinner fa-spin"></i> : "Search"}
          </button>
          <button
            type="button"
            onClick={handleMyLocation}
            className="bg-green-500 hover:bg-green-600 px-3 py-2 rounded-lg transition-colors"
            title="Use My Location"
          >
            <i className="fas fa-location-arrow"></i>
          </button>
        </form>
      </div>

      <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
        {/* Sidebar / Results List */}
        <div className="w-full md:w-1/3 bg-gray-50 overflow-y-auto border-r border-gray-200">
          <div className="p-4">
            <h3 className="font-bold text-gray-700 mb-3">
              {clinics.length > 0
                ? `Found ${clinics.length} Clinics`
                : "Search to find clinics"}
            </h3>

            <div className="space-y-3">
              {clinics.map((clinic, idx) => (
                <div
                  key={idx}
                  onClick={() => {
                    setMapCenter([
                      parseFloat(clinic.lat),
                      parseFloat(clinic.lon),
                    ]);
                    setSelectedClinic(clinic);
                  }}
                  className={`p-4 rounded-lg cursor-pointer transition-all ${
                    selectedClinic === clinic
                      ? "bg-blue-100 border-blue-400 border shadow-md"
                      : "bg-white border-gray-100 border hover:shadow-md hover:border-blue-200"
                  }`}
                >
                  <h4 className="font-bold text-blue-800 mb-1">
                    {clinic.display_name.split(",")[0]}
                  </h4>
                  <p className="text-xs text-gray-600 line-clamp-2">
                    {clinic.display_name}
                  </p>
                </div>
              ))}

              {clinics.length === 0 && !loading && (
                <div className="text-center py-10 text-gray-400">
                  <i className="fas fa-search-location text-4xl mb-3"></i>
                  <p>Enter a location to find nearby dental care.</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Map Area */}
        <div className="w-full md:w-2/3 h-full relative z-0">
          <MapContainer
            center={mapCenter}
            zoom={zoom}
            style={{ height: "100%", width: "100%" }}
          >
            <ChangeView center={mapCenter} zoom={zoom} />
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {clinics.map((clinic, idx) => (
              <Marker
                key={idx}
                position={[parseFloat(clinic.lat), parseFloat(clinic.lon)]}
                eventHandlers={{
                  click: () => setSelectedClinic(clinic),
                }}
              >
                <Popup>
                  <div className="font-sans">
                    <strong className="text-sm block mb-1">
                      {clinic.display_name.split(",")[0]}
                    </strong>
                    <span className="text-xs text-gray-600">
                      {clinic.display_name}
                    </span>
                    <a
                      href={`https://www.google.com/maps/dir/?api=1&destination=${clinic.lat},${clinic.lon}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block mt-2 text-xs text-blue-600 hover:underline"
                    >
                      Get Directions{" "}
                      <i className="fas fa-external-link-alt"></i>
                    </a>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>
      </div>
    </div>
  );
}
