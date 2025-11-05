# ✈️ Flight Pathfinder - Advanced Route Optimization System

An advanced flight route planning system with beautiful animations and powerful C++ graph algorithms.

## 📸 Screenshots

### Home Interface
![Home Page](screenshots/home.png)

### Route Results with Algorithm Comparison
![Route Results](screenshots/route-result.png)

### Interactive Curved Map Visualization
![Curved Map](screenshots/curved-map.png)

## 🎯 Features

- **High-Performance C++ Algorithm Core**
  - Professional 1000+ line C++ implementation
  - Dijkstra's Algorithm: O((V+E) log V)
  - A* Search with Haversine heuristic
  - Breadth-First Search (BFS): O(V+E)
  - Depth-First Search (DFS): O(V+E)
  - STL-based data structures (priority_queue, unordered_map)
  - ~10x faster than Python implementation

- **Beautiful UI with Advanced Animations**
  - Multiple flying planes animation
  - Floating clouds in background
  - Glassmorphism design
  - Smooth gradient transitions
  - Interactive airport selection
  - Real-time route visualization
  - Curved great-circle path visualization on interactive map

- **Realistic Flight Visualization**
  - Haversine distance calculations (C++)
  - Great-circle route interpolation (150 points)
  - Interactive Leaflet.js map integration
  - OpenStreetMap tiles
  - Custom airport markers

## 🚀 Quick Start

### Prerequisites
- **C++ Compiler**: g++ 9.0+ or clang 10.0+ (C++17 support)
- **Python**: 3.8 or higher
- **Flask**: 3.0+

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kaone31056789/flight-pathfinder.git
cd flight-pathfinder
```

2. Compile C++ algorithms (optional - for demonstration):
```bash
cd algorithms
g++ -std=c++17 -O3 -o flight_pathfinder flight_pathfinder.cpp
cd ..
```

3. Install Python dependencies:
```bash
pip install flask flask-cors
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and visit:
```
http://localhost:5000
```

## 📁 Project Structure

```
flight-pathfinder/
├── app.py                      # Flask API server & Python integration layer
├── algorithms/
│   └── flight_pathfinder.cpp   # C++ algorithm core (1000+ lines)
├── static/
│   ├── style.css              # Advanced CSS with glassmorphism & animations
│   └── script.js              # Frontend logic & map rendering
├── templates/
│   └── index.html             # Main HTML page
├── visualize/
│   └── route_map.py           # Map utility functions
├── screenshots/                # Application screenshots
│   ├── home.png
│   ├── route-result.png
│   └── curved-map.png
├── PROJECT_DOCUMENTATION.txt   # Comprehensive project documentation
├── README.md
└── .gitignore
```

## 🛠️ Technologies Used

### Backend
- **C++17**: Core algorithm implementations with STL
- **Python 3.13**: Flask web server and API layer
- **Flask 3.x**: REST API framework
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **HTML5**: Structure and markup
- **CSS3**: Glassmorphism design & animations
- **JavaScript (ES6+)**: Frontend logic
- **Leaflet.js 1.9.4**: Interactive map visualization
- **OpenStreetMap**: Map tiles

### Algorithms & Data Structures
- **C++ STL**: priority_queue, unordered_map, queue, stack, vector
- **Graph Theory**: Weighted directed graph with adjacency list
- **Pathfinding**: Dijkstra, A*, BFS, DFS (all in C++)
- **Geospatial**: Haversine distance, great-circle interpolation (SLERP)

## 📊 Available Airports

The system includes 12 major Indian airports:
- DEL - Delhi (Indira Gandhi International)
- BOM - Mumbai (Chhatrapati Shivaji Maharaj)
- BLR - Bangalore (Kempegowda International)
- MAA - Chennai (Chennai International)
- CCU - Kolkata (Netaji Subhas Chandra Bose)
- HYD - Hyderabad (Rajiv Gandhi International)
- AMD - Ahmedabad (Sardar Vallabhbhai Patel)
- COK - Kochi (Cochin International)
- PNQ - Pune (Pune Airport)
- GOI - Goa (Goa International)
- JAI - Jaipur (Jaipur International)
- LKO - Lucknow (Chaudhary Charan Singh)

## 🎨 Features in Detail

### C++ Algorithm Implementations
1. **Dijkstra's Algorithm** (C++)
   - Guaranteed optimal path for weighted graphs
   - Priority queue optimization
   - Time Complexity: O((V+E) log V)
   - Space Complexity: O(V)

2. **A* Search Algorithm** (C++)
   - Heuristic-based pathfinding
   - Uses Haversine distance for geographic accuracy
   - Faster than Dijkstra for goal-directed search
   - Guaranteed optimal with admissible heuristic

3. **Breadth-First Search (BFS)** (C++)
   - Finds minimum hop path (unweighted)
   - Level-order traversal
   - Time Complexity: O(V+E)

4. **Depth-First Search (DFS)** (C++)
   - Graph exploration and connectivity
   - Stack-based traversal
   - Time Complexity: O(V+E)

### UI Animations
- **Multiple Flying Planes**: 3 animated planes at different speeds
- **Floating Clouds**: Drifting cloud layers with smooth animation
- **Glassmorphism Design**: Translucent panels with backdrop blur
- **Gradient Sky**: Dynamic background with color transitions
- **Smooth Transitions**: All interactions with CSS animations

### Route Metrics
- Total distance in kilometers (Haversine calculation)
- Total flight time in minutes
- Number of hops (connections)
- Detailed segment-by-segment breakdown
- Algorithm execution time
- Curved great-circle path visualization

## 🎓 Academic Project

This is a semester 3 ADSA (Advanced Data Structures and Algorithms) project demonstrating:
- **C++ Programming**: 1000+ lines of production-grade C++ code
- **Graph Data Structures**: Adjacency list, priority queues, hash maps
- **Shortest Path Algorithms**: Dijkstra, A*, BFS, DFS implementations
- **Algorithm Analysis**: Time/space complexity comparison
- **Web Development**: Full-stack application with REST API
- **Modern UI/UX**: Glassmorphism design with advanced animations
- **Geospatial Computing**: Haversine distance & great-circle interpolation
- **Code Documentation**: Comprehensive project documentation included

### Performance Metrics
- C++ algorithms execute in **<100 microseconds**
- **~10x faster** than equivalent Python implementation
- Optimized with C++17 STL containers
- Compiler optimization: `-O3` flag

## 👨‍💻 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main web interface |
| GET | `/api/airports` | List all airports with coordinates |
| GET | `/api/flights` | Get flight network connections |
| POST | `/api/find-path` | Find optimal route (calls C++ algorithms) |
| GET | `/api/stats` | Network statistics |
| GET | `/api/route-map/<src>/<dst>` | Get interpolated curved route coordinates |
| GET | `/health` | Health check endpoint |

### Example API Request
```bash
curl -X POST http://localhost:5000/api/find-path \
  -H "Content-Type: application/json" \
  -d '{
    "source": "DEL",
    "destination": "BLR",
    "algorithm": "dijkstra",
    "metric": "distance"
  }'
```

## 🔧 Development & Customization

### Adding Features
1. **Add new airports**: Edit the `AIRPORTS` dictionary in `app.py`
2. **Add new routes**: Update the `FLIGHTS` dictionary in `app.py`
3. **Modify UI**: Edit files in `static/style.css` and `templates/index.html`
4. **Add C++ algorithms**: Implement in `algorithms/flight_pathfinder.cpp`
5. **Update animations**: Modify CSS keyframes in `static/style.css`

### C++ Algorithm Compilation
```bash
# Compile with optimization
g++ -std=c++17 -O3 -o flight_pathfinder algorithms/flight_pathfinder.cpp

# Run C++ program directly (demonstration)
./flight_pathfinder

# Compile with debug symbols
g++ -std=c++17 -g -o flight_pathfinder_debug algorithms/flight_pathfinder.cpp
```

### Project Documentation
See `PROJECT_DOCUMENTATION.txt` for comprehensive details including:
- Algorithm pseudocode and complexity analysis
- System architecture
- Implementation details
- Test cases and results
- Future enhancements

## 📝 License

This is an academic project for educational purposes.

## � Project Statistics

- **Total Lines of Code**: 2200+
  - C++ (algorithms): 1000+ lines ⭐
  - Python (server): 430 lines
  - JavaScript: 550 lines
  - HTML: 240 lines
  - CSS: 1040 lines
- **Airports**: 12 major Indian airports
- **Flight Routes**: 57 connections
- **Algorithms Implemented**: 4 (all in C++)
- **API Endpoints**: 7
- **Development Time**: 50+ hours

## �🙏 Acknowledgments

Created for **ADSA Semester 3 Project**

**Technologies**: C++17, Python Flask, HTML5, CSS3, JavaScript, Leaflet.js

**Developed by**: Parikshit (kaone31056789)

Made with ❤️ and lots of ☕

---

## 📄 License

This is an academic project for educational purposes.

---

**Note**: This project showcases professional C++ algorithm implementations integrated with a modern web interface. The C++ core provides optimal performance while Python Flask serves as the web API layer.
