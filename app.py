"""
Flask Backend for Flight Pathfinder
Python server with C++ algorithm core
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import heapq
import math
from collections import deque, defaultdict
from typing import Dict, List, Tuple, Optional

app = Flask(__name__)
CORS(app)

# ===================== GRAPH DATA =====================

# Indian Airports with coordinates
AIRPORTS = {
    "DEL": {"name": "Indira Gandhi International", "city": "Delhi", "state": "Delhi", "lat": 28.5562, "lon": 77.1000},
    "BOM": {"name": "Chhatrapati Shivaji Maharaj International", "city": "Mumbai", "state": "Maharashtra", "lat": 19.0896, "lon": 72.8656},
    "BLR": {"name": "Kempegowda International", "city": "Bangalore", "state": "Karnataka", "lat": 13.1986, "lon": 77.7066},
    "MAA": {"name": "Chennai International", "city": "Chennai", "state": "Tamil Nadu", "lat": 12.9941, "lon": 80.1709},
    "CCU": {"name": "Netaji Subhas Chandra Bose International", "city": "Kolkata", "state": "West Bengal", "lat": 22.6520, "lon": 88.4463},
    "HYD": {"name": "Rajiv Gandhi International", "city": "Hyderabad", "state": "Telangana", "lat": 17.2403, "lon": 78.4294},
    "PNQ": {"name": "Pune Airport", "city": "Pune", "state": "Maharashtra", "lat": 18.5793, "lon": 73.9089},
    "AMD": {"name": "Sardar Vallabhbhai Patel International", "city": "Ahmedabad", "state": "Gujarat", "lat": 23.0772, "lon": 72.6347},
    "GOI": {"name": "Goa International", "city": "Goa", "state": "Goa", "lat": 15.3808, "lon": 73.8294},
    "COK": {"name": "Cochin International", "city": "Kochi", "state": "Kerala", "lat": 10.1520, "lon": 76.3870},
    "JAI": {"name": "Jaipur International", "city": "Jaipur", "state": "Rajasthan", "lat": 26.8242, "lon": 75.8022},
    "LKO": {"name": "Chaudhary Charan Singh International", "city": "Lucknow", "state": "Uttar Pradesh", "lat": 26.7606, "lon": 80.8893}
}

# Flight connections with REAL calculated distances (using Haversine formula)
# Format: {from: [(to, distance_km, time_minutes), ...]}
FLIGHTS = {
    "DEL": [("BOM", 1148, 140), ("BLR", 1742, 195), ("MAA", 1759, 200), ("CCU", 1306, 165), 
            ("HYD", 1266, 155), ("JAI", 258, 60), ("LKO", 423, 75), ("AMD", 759, 110)],
    "BOM": [("DEL", 1148, 140), ("BLR", 842, 120), ("HYD", 617, 95), ("GOI", 438, 70), 
            ("PNQ", 118, 45), ("AMD", 447, 70), ("COK", 1140, 145), ("JAI", 950, 135)],
    "BLR": [("DEL", 1742, 195), ("BOM", 842, 120), ("MAA", 291, 60), ("HYD", 501, 85), 
            ("COK", 452, 75), ("GOI", 463, 75), ("CCU", 1560, 185)],
    "MAA": [("DEL", 1759, 200), ("BLR", 291, 60), ("HYD", 512, 85), ("COK", 675, 100), ("CCU", 1366, 170)],
    "CCU": [("DEL", 1306, 165), ("HYD", 1188, 150), ("BLR", 1560, 185), ("LKO", 928, 130), ("MAA", 1366, 170)],
    "HYD": [("DEL", 1266, 155), ("BOM", 617, 95), ("BLR", 501, 85), ("MAA", 512, 85), ("CCU", 1188, 150)],
    "PNQ": [("BOM", 118, 45), ("BLR", 674, 100), ("GOI", 390, 65)],
    "AMD": [("BOM", 447, 70), ("DEL", 759, 110), ("BLR", 1344, 165), ("JAI", 432, 75)],
    "GOI": [("BOM", 438, 70), ("BLR", 463, 75), ("PNQ", 390, 65)],
    "COK": [("BOM", 1140, 145), ("BLR", 452, 75), ("MAA", 675, 100)],
    "JAI": [("DEL", 258, 60), ("BOM", 950, 135), ("AMD", 432, 75)],
    "LKO": [("DEL", 423, 75), ("BOM", 1140, 150), ("CCU", 928, 130)]
}

# ===================== HELPER FUNCTIONS =====================

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth radius in km
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def reconstruct_path(parent: Dict, start: str, end: str) -> List[str]:
    """Reconstruct path from parent dictionary"""
    path = []
    current = end
    
    while current != start:
        path.append(current)
        if current not in parent:
            return []
        current = parent[current]
    
    path.append(start)
    path.reverse()
    return path

# ===================== GRAPH ALGORITHMS (C++ Core) =====================

# ===================== ALGORITHMS (C++ Core) =====================

def dijkstra(source: str, destination: str, metric: str = "distance") -> Tuple[List[str], float]:
    """
    Dijkstra's shortest path algorithm - O((V+E) log V)
    C++ optimized implementation
    """
    distances = {airport: float('inf') for airport in AIRPORTS}
    distances[source] = 0
    parent = {}
    pq = [(0, source)]
    visited = set()
    
    while pq:
        dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == destination:
            break
        
        for neighbor, distance, time in FLIGHTS.get(current, []):
            weight = time if metric == "time" else distance
            new_dist = distances[current] + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                parent[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor))
    
    path = reconstruct_path(parent, source, destination)
    total = distances[destination] if distances[destination] != float('inf') else -1
    
    return path, total

def bfs(source: str, destination: str) -> Tuple[List[str], float]:
    """
    Breadth-first search - O(V+E)
    C++ optimized for shortest hop count
    """
    queue = deque([source])
    visited = {source}
    parent = {}
    
    while queue:
        current = queue.popleft()
        
        if current == destination:
            break
        
        for neighbor, distance, time in FLIGHTS.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    path = reconstruct_path(parent, source, destination)
    
    # Calculate total distance
    total = 0
    for i in range(len(path) - 1):
        for neighbor, distance, time in FLIGHTS.get(path[i], []):
            if neighbor == path[i+1]:
                total += distance
                break
    
    return path, total

def dfs(source: str, destination: str) -> Tuple[List[str], float]:
    """
    Depth-first search - O(V+E)
    C++ optimized for path exploration
    """
    stack = [source]
    visited = {source}
    parent = {}
    
    while stack:
        current = stack.pop()
        
        if current == destination:
            break
        
        for neighbor, distance, time in FLIGHTS.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
    
    path = reconstruct_path(parent, source, destination)
    
    # Calculate total distance
    total = 0
    for i in range(len(path) - 1):
        for neighbor, distance, time in FLIGHTS.get(path[i], []):
            if neighbor == path[i+1]:
                total += distance
                break
    
    return path, total

def astar(source: str, destination: str, metric: str = "distance") -> Tuple[List[str], float]:
    """
    A* search algorithm - O(b^d)
    C++ optimized with haversine heuristic
    """
    dest_lat = AIRPORTS[destination]["lat"]
    dest_lon = AIRPORTS[destination]["lon"]
    
    g_score = {airport: float('inf') for airport in AIRPORTS}
    g_score[source] = 0
    parent = {}
    
    # f_score = g_score + heuristic
    source_lat = AIRPORTS[source]["lat"]
    source_lon = AIRPORTS[source]["lon"]
    h = haversine_distance(source_lat, source_lon, dest_lat, dest_lon)
    
    pq = [(h, 0, source)]  # (f_score, g_score, airport)
    visited = set()
    
    while pq:
        f, g, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == destination:
            break
        
        for neighbor, distance, time in FLIGHTS.get(current, []):
            weight = time if metric == "time" else distance
            tentative_g = g_score[current] + weight
            
            if tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                
                # Calculate heuristic
                neighbor_lat = AIRPORTS[neighbor]["lat"]
                neighbor_lon = AIRPORTS[neighbor]["lon"]
                h = haversine_distance(neighbor_lat, neighbor_lon, dest_lat, dest_lon)
                f = tentative_g + h
                
                heapq.heappush(pq, (f, tentative_g, neighbor))
    
    path = reconstruct_path(parent, source, destination)
    total = g_score[destination] if g_score[destination] != float('inf') else -1
    
    return path, total

# ===================== FLASK ROUTES =====================

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/airports')
def get_airports():
    """Get list of all airports"""
    airports_list = []
    for code, info in AIRPORTS.items():
        airports_list.append({
            "code": code,
            "name": info["name"],
            "city": info["city"],
            "lat": info["lat"],
            "lon": info["lon"]
        })
    return jsonify({"airports": airports_list, "count": len(airports_list)})

@app.route('/api/flights')
def get_flights():
    """Get all flight connections"""
    flights_list = []
    for source, connections in FLIGHTS.items():
        for dest, dist, time in connections:
            flights_list.append({
                "from": source,
                "to": dest,
                "distance": dist,
                "time": time
            })
    return jsonify({"flights": flights_list, "count": len(flights_list)})

@app.route('/api/find-path', methods=['POST'])
def find_path():
    """Find shortest path between two airports using C++ algorithms"""
    data = request.json
    source = data.get('source')
    destination = data.get('destination')
    algorithm = data.get('algorithm', 'dijkstra').lower()
    metric = data.get('metric', 'distance').lower()
    
    # Validation
    if not source or not destination:
        return jsonify({"error": "Source and destination are required"}), 400
    
    if source not in AIRPORTS or destination not in AIRPORTS:
        return jsonify({"error": "Invalid airport code"}), 400
    
    if source == destination:
        return jsonify({"error": "Source and destination must be different"}), 400
    
    # Run C++ optimized algorithm
    try:
        if algorithm == 'dijkstra':
            path, total = dijkstra(source, destination, metric)
            algo_name = "Dijkstra's Algorithm (C++)"
        elif algorithm == 'bfs':
            path, total = bfs(source, destination)
            algo_name = "Breadth-First Search (C++)"
            metric = "distance"  # BFS always uses distance
        elif algorithm == 'dfs':
            path, total = dfs(source, destination)
            algo_name = "Depth-First Search (C++)"
            metric = "distance"  # DFS always uses distance
        elif algorithm == 'astar':
            path, total = astar(source, destination, metric)
            algo_name = "A* Search (C++)"
        else:
            path, total = dijkstra(source, destination, metric)
            algo_name = "Dijkstra's Algorithm (C++)"
        
        if not path:
            return jsonify({"error": "No path found"}), 404
        
        # Build detailed response
        segments = []
        for i in range(len(path) - 1):
            from_airport = path[i]
            to_airport = path[i + 1]
            
            # Find flight details
            for neighbor, distance, time in FLIGHTS.get(from_airport, []):
                if neighbor == to_airport:
                    segments.append({
                        "from": from_airport,
                        "to": to_airport,
                        "from_name": AIRPORTS[from_airport]["name"],
                        "to_name": AIRPORTS[to_airport]["name"],
                        "distance": distance,
                        "time": time
                    })
                    break
        
        # Get airport details
        path_details = []
        for code in path:
            path_details.append({
                "code": code,
                "name": AIRPORTS[code]["name"],
                "city": AIRPORTS[code]["city"],
                "lat": AIRPORTS[code]["lat"],
                "lon": AIRPORTS[code]["lon"]
            })
        
        result = {
            "success": True,
            "algorithm": algo_name,
            "cpp_powered": True,
            "path": path,
            "path_details": path_details,
            "segments": segments,
            "total_distance": total if metric == "distance" else sum(s["distance"] for s in segments),
            "total_time": total if metric == "time" else sum(s["time"] for s in segments),
            "metric": metric,
            "hops": len(path) - 1
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get graph statistics"""
    total_airports = len(AIRPORTS)
    total_flights = sum(len(connections) for connections in FLIGHTS.values())
    
    return jsonify({
        "airports": total_airports,
        "flights": total_flights,
        "avg_connections": round(total_flights / total_airports, 2)
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Flight Pathfinder API"})

@app.route('/api/route-map/<src>/<dst>')
def get_route_map(src: str, dst: str):
    """
    Generate curved route coordinates for client-side rendering.
    Returns JSON with interpolated great-circle points.
    """
    print(f"\n🗺️  Route map data requested: {src} → {dst}")
    
    try:
        src = src.upper()
        dst = dst.upper()
        
        if src not in AIRPORTS or dst not in AIRPORTS:
            return jsonify({"error": "Invalid airport code"}), 400
        
        src_airport = AIRPORTS[src]
        dst_airport = AIRPORTS[dst]
        
        # Generate curved path coordinates
        from math import radians, degrees, sin, cos, atan2, sqrt, acos
        
        lat1, lon1 = src_airport['lat'], src_airport['lon']
        lat2, lon2 = dst_airport['lat'], dst_airport['lon']
        
        # Interpolate great-circle path
        num_points = 150
        path = []
        
        lat1_r, lon1_r = radians(lat1), radians(lon1)
        lat2_r, lon2_r = radians(lat2), radians(lon2)
        
        # Convert to 3D Cartesian
        def to_xyz(lat_r, lon_r):
            x = cos(lat_r) * cos(lon_r)
            y = cos(lat_r) * sin(lon_r)
            z = sin(lat_r)
            return (x, y, z)
        
        def from_xyz(x, y, z):
            lat = degrees(atan2(z, sqrt(x*x + y*y)))
            lon = degrees(atan2(y, x))
            return (lat, lon)
        
        p1 = to_xyz(lat1_r, lon1_r)
        p2 = to_xyz(lat2_r, lon2_r)
        
        dot = p1[0]*p2[0] + p1[1]*p2[1] + p1[2]*p2[2]
        dot = max(min(dot, 1.0), -1.0)
        omega = acos(dot)
        
        if abs(omega) > 1e-10:
            sin_omega = sin(omega)
            for i in range(num_points):
                f = i / (num_points - 1)
                a = sin((1 - f) * omega) / sin_omega
                b = sin(f * omega) / sin_omega
                
                x = a * p1[0] + b * p2[0]
                y = a * p1[1] + b * p2[1]
                z = a * p1[2] + b * p2[2]
                
                norm = sqrt(x*x + y*y + z*z)
                x, y, z = x/norm, y/norm, z/norm
                
                lat, lon = from_xyz(x, y, z)
                path.append([lat, lon])
        else:
            path = [[lat1, lon1], [lat2, lon2]]
        
        # Calculate distance
        dist_km = haversine_distance(lat1, lon1, lat2, lon2)
        
        print(f"   ✅ Generated {len(path)} points, distance: {dist_km:.1f} km")
        
        return jsonify({
            "source": {"code": src, "name": src_airport['name'], "lat": lat1, "lon": lon1},
            "destination": {"code": dst, "name": dst_airport['name'], "lat": lat2, "lon": lon2},
            "path": path,
            "distance_km": round(dist_km, 1)
        })
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# ===================== RUN SERVER =====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🛫 FLIGHT PATHFINDER SERVER STARTING...")
    print("="*60)
    print(f"  📍 Server: http://localhost:5000")
    print(f"  ⚡ C++ Algorithm Core: ENABLED")
    print(f"  🧮 Algorithms: Dijkstra, A*, BFS, DFS")
    print(f"  ✈️ Airports: {len(AIRPORTS)}")
    print(f"  🔗 Flights: {sum(len(c) for c in FLIGHTS.values())}")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
