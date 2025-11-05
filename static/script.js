// API Base URL
const API_URL = 'http://localhost:5000';

// State
let airports = [];
let flights = [];
let stats = {};
let map = null;
let markers = [];

// Algorithm descriptions
const algoDescriptions = {
    'dijkstra': "Optimal weighted pathfinding - O((V+E) log V) [C++ Core]",
    'astar': "Heuristic search with geographic distance - O(b^d) [C++ Core]",
    'bfs': "Shortest hop count - O(V+E) [C++ Core]",
    'dfs': "Depth-first path exploration - O(V+E) [C++ Core]"
};

// Initialize MapLibre GL JS Map
function initMap() {
    console.log('Attempting to initialize MapLibre map...');
    
    // Check if MapLibre is loaded
    if (typeof maplibregl === 'undefined') {
        console.error('MapLibre GL library not loaded!');
        setTimeout(initMap, 500); // Retry
        return;
    }
    
    // Check if map container exists
    const mapContainer = document.getElementById('map');
    if (!mapContainer) {
        console.error('Map container not found!');
        setTimeout(initMap, 500); // Retry
        return;
    }
    
    console.log('Map container found, initializing MapLibre...');
    
    try {
        // Center of India
        const indiaCenter = [78.9629, 22.5937]; // [lng, lat]
        
        map = new maplibregl.Map({
            container: 'map',
            style: {
                version: 8,
                sources: {
                    'osm': {
                        type: 'raster',
                        tiles: [
                            'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png',
                            'https://b.tile.openstreetmap.org/{z}/{x}/{y}.png',
                            'https://c.tile.openstreetmap.org/{z}/{x}/{y}.png'
                        ],
                        tileSize: 256,
                        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    }
                },
                layers: [{
                    id: 'osm',
                    type: 'raster',
                    source: 'osm',
                    minzoom: 0,
                    maxzoom: 22
                }]
            },
            center: indiaCenter,
            zoom: 4.5,
            minZoom: 4,
            maxZoom: 12,
            maxBounds: [
                [68.0, 6.0],   // Southwest corner [lng, lat]
                [98.0, 36.0]   // Northeast corner [lng, lat]
            ]
        });
        
        // Add zoom and rotation controls
        map.addControl(new maplibregl.NavigationControl(), 'top-right');
        
        console.log('MapLibre GL Map initialized successfully - India view');
    } catch (error) {
        console.error('Error initializing map:', error);
    }
}

// DOM Elements
const sourceSelect = document.getElementById('source');
const destSelect = document.getElementById('destination');
const algorithmSelect = document.getElementById('algorithm');
const metricSelect = document.getElementById('metric');
const findPathBtn = document.getElementById('findPathBtn');

const sourceInfo = document.getElementById('sourceInfo');
const destInfo = document.getElementById('destInfo');
const algoInfo = document.getElementById('algoInfo');

const loading = document.getElementById('loading');
const welcome = document.getElementById('welcome');
const results = document.getElementById('results');
const error = document.getElementById('error');

// Initialize app
async function init() {
    console.log('Starting application initialization...');
    try {
        await loadAirports();
        await loadFlights();
        await loadStats();
        setupEventListeners();
        
        // Don't initialize map yet - wait until results are shown
        console.log('Application initialized successfully (map will load when route is found)');
    } catch (err) {
        console.error('Initialization error:', err);
        showError('Failed to initialize application. Please refresh the page.');
    }
}

// Load airports from API
async function loadAirports() {
    try {
        const response = await fetch(`${API_URL}/api/airports`);
        const data = await response.json();
        
        // Convert array to object with code as key
        airports = {};
        data.airports.forEach(airport => {
            airports[airport.code] = airport;
        });
        
        populateAirportSelects();
    } catch (err) {
        console.error('Error loading airports:', err);
        throw err;
    }
}

// Load flights from API
async function loadFlights() {
    try {
        const response = await fetch(`${API_URL}/api/flights`);
        const data = await response.json();
        
        // Convert array to nested object structure for easy lookup
        flights = {};
        data.flights.forEach(flight => {
            if (!flights[flight.from]) {
                flights[flight.from] = {};
            }
            flights[flight.from][flight.to] = {
                distance: flight.distance,
                time: flight.time
            };
        });
    } catch (err) {
        console.error('Error loading flights:', err);
        throw err;
    }
}

// Load statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/api/stats`);
        const data = await response.json();
        stats = data;
        
        updateStatsDisplay();
    } catch (err) {
        console.error('Error loading stats:', err);
        throw err;
    }
}

// Populate airport select dropdowns
function populateAirportSelects() {
    // Sort airports by code for better UX
    const sortedAirports = Object.entries(airports)
        .sort(([codeA], [codeB]) => codeA.localeCompare(codeB));
    
    const airportOptions = sortedAirports
        .map(([code, info]) => `
            <option value="${code}">${code} - ${info.city} (${info.name})</option>
        `)
        .join('');
    
    sourceSelect.innerHTML = '<option value="">Select source...</option>' + airportOptions;
    destSelect.innerHTML = '<option value="">Select destination...</option>' + airportOptions;
}

// Update statistics display
function updateStatsDisplay() {
    document.getElementById('totalAirports').textContent = stats.airports || '-';
    document.getElementById('totalFlights').textContent = stats.total_flights || '-';
    document.getElementById('avgConnections').textContent = 
        stats.avg_connections ? stats.avg_connections.toFixed(1) : '-';
}

// Setup event listeners
function setupEventListeners() {
    sourceSelect.addEventListener('change', handleSourceChange);
    destSelect.addEventListener('change', handleDestChange);
    algorithmSelect.addEventListener('change', handleAlgorithmChange);
    findPathBtn.addEventListener('click', handleFindPath);
    
    // Curved map toggle button
    const toggleMapBtn = document.getElementById('toggleMapBtn');
    if (toggleMapBtn) {
        toggleMapBtn.addEventListener('click', handleToggleCurvedMap);
    }
}

// Handle source airport selection
function handleSourceChange() {
    const code = sourceSelect.value;
    if (code && airports[code]) {
        const airport = airports[code];
        sourceInfo.innerHTML = `
            📍 ${airport.city}, ${airport.state} 
            <br>
            🌍 ${airport.lat.toFixed(4)}°N, ${airport.lon.toFixed(4)}°E
        `;
    } else {
        sourceInfo.innerHTML = '';
    }
}

// Handle destination airport selection
function handleDestChange() {
    const code = destSelect.value;
    if (code && airports[code]) {
        const airport = airports[code];
        destInfo.innerHTML = `
            📍 ${airport.city}, ${airport.state}
            <br>
            🌍 ${airport.lat.toFixed(4)}°N, ${airport.lon.toFixed(4)}°E
        `;
    } else {
        destInfo.innerHTML = '';
    }
}

// Handle algorithm selection
function handleAlgorithmChange() {
    const algo = algorithmSelect.value;
    algoInfo.innerHTML = `<small>${algoDescriptions[algo]}</small>`;
}

// Handle find path button click
async function handleFindPath() {
    const source = sourceSelect.value;
    const dest = destSelect.value;
    const algorithm = algorithmSelect.value;
    const metric = metricSelect.value;
    
    // Validation
    if (!source || !dest) {
        showError('Please select both source and destination airports');
        return;
    }
    
    if (source === dest) {
        showError('Source and destination must be different');
        return;
    }
    
    // Show loading
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/api/find-path`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                source,
                destination: dest,
                algorithm,
                metric
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError(data.error);
        } else {
            showResults(data, algorithm);
        }
    } catch (err) {
        console.error('Error finding path:', err);
        showError('Failed to find path. Please try again.');
    }
}

// Show loading state
function showLoading() {
    loading.classList.remove('hidden');
    welcome.classList.add('hidden');
    results.classList.add('hidden');
    error.classList.add('hidden');
}

// Show results
function showResults(data, algorithm) {
    loading.classList.add('hidden');
    welcome.classList.add('hidden');
    results.classList.remove('hidden');
    error.classList.add('hidden');
    
    // Initialize map if not already initialized
    if (!map) {
        console.log('Initializing map for first time...');
        initMap();
    }
    
    // Algorithm used
    document.getElementById('algorithmUsed').textContent = 
        algorithm.toUpperCase().replace('_', ' ');
    
    // Path route
    const pathRoute = document.getElementById('pathRoute');
    pathRoute.innerHTML = data.path
        .map((code, index) => {
            if (index === data.path.length - 1) {
                return `<span>${code}</span>`;
            }
            return `<span>${code}</span> <span style="opacity: 0.7;">✈️</span>`;
        })
        .join(' ');
    
    // Metrics
    document.getElementById('totalDistance').textContent = 
        `${data.total_distance.toFixed(1)} km`;
    document.getElementById('totalTime').textContent = 
        `${data.total_time.toFixed(0)} min`;
    document.getElementById('totalHops').textContent = 
        data.path.length - 1;
    
    // Segments
    const segmentsContainer = document.getElementById('segments');
    segmentsContainer.innerHTML = data.path
        .slice(0, -1)
        .map((code, index) => {
            const nextCode = data.path[index + 1];
            const segment = findFlightSegment(code, nextCode);
            
            return `
                <div class="segment">
                    <div class="segment-number">${index + 1}</div>
                    <div class="segment-info">
                        <div class="segment-route">
                            ${code} → ${nextCode}
                        </div>
                        <div class="segment-details">
                            ${airports[code].city} to ${airports[nextCode].city} • 
                            ${segment.distance.toFixed(0)} km • 
                            ${segment.time} min
                        </div>
                    </div>
                </div>
            `;
        })
        .join('');
    
    // Draw route on map (with delay to ensure map is ready)
    setTimeout(() => {
        drawMaplibreMapRoute(data.path);
    }, 100);
}

// Draw route on MapLibre GL Map
function drawMaplibreMapRoute(path) {
    console.log('Drawing route on MapLibre map...', path);
    
    if (!map) {
        console.error('MapLibre Map not initialized');
        return;
    }
    
    // Clear previous markers
    markers.forEach(marker => marker.remove());
    markers = [];
    
    // Remove previous route if exists
    if (map.getLayer('route')) {
        map.removeLayer('route');
    }
    if (map.getSource('route')) {
        map.removeSource('route');
    }
    
    // Get coordinates for path [lng, lat] format
    const pathCoordinates = path.map(code => [
        airports[code].lon,
        airports[code].lat
    ]);
    
    console.log('Path coordinates:', pathCoordinates);
    
    // Add route as GeoJSON LineString
    map.addSource('route', {
        type: 'geojson',
        data: {
            type: 'Feature',
            properties: {},
            geometry: {
                type: 'LineString',
                coordinates: pathCoordinates
            }
        }
    });
    
    map.addLayer({
        id: 'route',
        type: 'line',
        source: 'route',
        layout: {
            'line-join': 'round',
            'line-cap': 'round'
        },
        paint: {
            'line-color': '#667eea',
            'line-width': 4,
            'line-opacity': 0.8
        }
    });
    
    console.log('Flight path added');
    
    // Add markers for each airport
    path.forEach((code, index) => {
        const airport = airports[code];
        const position = [airport.lon, airport.lat]; // [lng, lat]
        
        // Determine marker color
        let markerColor = '#667eea'; // default blue
        if (index === 0) markerColor = '#4ade80'; // green for start
        if (index === path.length - 1) markerColor = '#f87171'; // red for end
        
        // Create custom marker element
        const el = document.createElement('div');
        el.style.cssText = `
            background-color: ${markerColor};
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 11px;
            color: white;
            cursor: pointer;
        `;
        el.textContent = code;
        
        // Create popup
        const popup = new maplibregl.Popup({ offset: 25 }).setHTML(`
            <div style="padding: 8px; min-width: 200px;">
                <h3 style="margin: 0 0 5px 0; color: #1e293b; font-size: 16px;">${code}</h3>
                <p style="margin: 0; color: #64748b; font-size: 13px;">${airport.name}</p>
                <p style="margin: 5px 0 0 0; color: #64748b; font-size: 12px;">
                    📍 ${airport.city}, ${airport.state}
                </p>
            </div>
        `);
        
        // Add marker to map
        const marker = new maplibregl.Marker({ element: el })
            .setLngLat(position)
            .setPopup(popup)
            .addTo(map);
        
        markers.push(marker);
    });
    
    console.log('Markers added:', markers.length);
    
    // Fit map bounds to show all markers
    const bounds = new maplibregl.LngLatBounds();
    pathCoordinates.forEach(coord => bounds.extend(coord));
    
    map.fitBounds(bounds, {
        padding: { top: 50, bottom: 50, left: 50, right: 50 },
        duration: 1000
    });
    
    console.log('Map bounds fitted');
}

// Find flight segment details
function findFlightSegment(from, to) {
    if (flights[from] && flights[from][to]) {
        return flights[from][to];
    }
    return { distance: 0, time: 0 };
}

// Show error state
function showError(message) {
    loading.classList.add('hidden');
    welcome.classList.add('hidden');
    results.classList.add('hidden');
    error.classList.remove('hidden');
    
    document.getElementById('errorMessage').textContent = message;
}

// Handle curved map toggle (render curved route with Leaflet directly - no server HTML)
function handleToggleCurvedMap() {
    console.log('Toggle map button clicked!');
    const toggleBtn = document.getElementById('toggleMapBtn');
    const mapContainer = document.getElementById('curvedMapContainer');
    const mapFrame = document.getElementById('curvedMapFrame');
    const mapLoader = document.getElementById('mapLoader');
    
    const source = sourceSelect.value;
    const dest = destSelect.value;
    
    console.log('Source:', source, 'Dest:', dest);
    
    // Toggle visibility
    const isHidden = mapContainer.classList.contains('hidden');
    
    if (isHidden) {
        // Validate inputs
        if (!source || !dest) {
            alert('Please select source and destination airports first');
            return;
        }
        
        if (source === dest) {
            alert('Source and destination must be different');
            return;
        }
        
        // Show container and loader
        mapContainer.classList.remove('hidden');
        mapLoader.classList.remove('hidden');
        toggleBtn.classList.add('expanded');
        toggleBtn.innerHTML = '<span class="btn-icon">▼</span> Hide Map';
        
        // Fetch curved route data from server and render with Leaflet
        fetch(`${API_URL}/api/route-map/${source}/${dest}`)
            .then(response => response.json())
            .then(data => {
                mapLoader.classList.add('hidden');
                renderCurvedRouteMap(data, mapFrame);
            })
            .catch(error => {
                mapLoader.classList.add('hidden');
                console.error('Map loading error:', error);
                mapFrame.srcdoc = `<div style="padding:20px;text-align:center;">
                    <h3>❌ Map Loading Error</h3>
                    <p>${error.message}</p>
                </div>`;
            });
        
    } else {
        // Hide container
        mapContainer.classList.add('hidden');
        toggleBtn.classList.remove('expanded');
        toggleBtn.innerHTML = '<span class="btn-icon">▼</span> Show Map';
        mapFrame.srcdoc = '';
    }
}

// Render curved route map using Leaflet (client-side)
function renderCurvedRouteMap(data, iframe) {
    const html = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body { margin: 0; padding: 0; }
        #map { height: 100vh; width: 100%; }
        .info-box { 
            background: white; 
            padding: 10px 15px; 
            border-radius: 8px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        .info-box h3 { margin: 0 0 5px 0; color: #2563eb; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        const mapData = ${JSON.stringify(data)};
        
        // Create map centered between source and destination
        const midLat = (mapData.source.lat + mapData.destination.lat) / 2;
        const midLon = (mapData.source.lon + mapData.destination.lon) / 2;
        
        const map = L.map('map').setView([midLat, midLon], 5);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(map);
        
        // Draw curved path
        const pathCoords = mapData.path;
        L.polyline(pathCoords, {
            color: '#2563eb',
            weight: 4,
            opacity: 0.8,
            smoothFactor: 1
        }).addTo(map);
        
        // Add markers
        L.marker([mapData.source.lat, mapData.source.lon], {
            icon: L.icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41]
            })
        }).bindPopup('<b>' + mapData.source.code + '</b><br>' + mapData.source.name).addTo(map);
        
        L.marker([mapData.destination.lat, mapData.destination.lon], {
            icon: L.icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41]
            })
        }).bindPopup('<b>' + mapData.destination.code + '</b><br>' + mapData.destination.name).addTo(map);
        
        // Add title and distance info
        const info = L.control({position: 'topright'});
        info.onAdd = function() {
            const div = L.DomUtil.create('div', 'info-box');
            div.innerHTML = '<h3>✈️ ' + mapData.source.code + ' → ' + mapData.destination.code + '</h3>' +
                           '<strong>Distance:</strong> ' + mapData.distance_km + ' km';
            return div;
        };
        info.addTo(map);
        
        // Fit bounds to show entire route
        const bounds = L.latLngBounds(pathCoords);
        map.fitBounds(bounds, {padding: [50, 50]});
    </script>
</body>
</html>
    `;
    
    iframe.srcdoc = html;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);

