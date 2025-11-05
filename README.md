# ✈️ Flight Pathfinder - Advanced Route Optimization System

An advanced flight route planning system with beautiful animations and powerful graph algorithms.

## 🎯 Features

- **Advanced Graph Algorithms**
  - Dijkstra's Algorithm: O((V+E) log V)
  - A* Search with Haversine heuristic: O(b^d)
  - Breadth-First Search: O(V+E)

- **Beautiful UI with Animations**
  - Flying planes animation
  - Floating clouds in background
  - Smooth gradient designs
  - Interactive airport selection
  - Real-time route visualization

- **C++ Algorithm Implementation**
  - Professional 1000+ line C++ code
  - 4 different pathfinding algorithms
  - Detailed comments and documentation
  - Performance metrics

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Flask

### Installation

1. Navigate to the project directory:
```bash
cd flight-pathfinder
```

2. Install dependencies:
```bash
pip install flask flask-cors
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and visit:
```
http://localhost:5000
```

## 📁 Project Structure

```
flight-pathfinder/
├── app.py                      # Flask backend server
├── algorithms/
│   └── flight_pathfinder.cpp   # Advanced C++ algorithms (for demo)
├── static/
│   ├── style.css              # Advanced CSS with animations
│   └── script.js              # JavaScript for API calls
├── templates/
│   └── index.html             # Main HTML page
└── README.md
```

## 🛠️ Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Algorithms**: Graph theory, pathfinding
- **Animations**: CSS keyframes, SVG

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

### Animations
- **Flying Plane**: Animated plane flying across the screen
- **Floating Clouds**: 5 cloud layers with parallax effect
- **Smooth Transitions**: CSS animations throughout the UI

### Algorithms
1. **Dijkstra's Algorithm**: Finds shortest weighted path
2. **A* Search**: Uses geographic heuristics for faster search
3. **BFS**: Finds path with minimum number of hops

### Metrics
- Total distance in kilometers
- Total flight time in minutes
- Number of hops (connections)
- Detailed segment-by-segment breakdown

## 🎓 Academic Project

This is a semester 3 ADSA (Advanced Data Structures and Algorithms) project demonstrating:
- Graph data structures
- Shortest path algorithms
- API development
- Modern web design
- Code documentation

## 👨‍💻 API Endpoints

- `GET /` - Main web interface
- `GET /api/airports` - List all airports
- `GET /api/flights` - Get flight connections
- `POST /api/find-path` - Find optimal route
- `GET /api/stats` - Network statistics
- `GET /health` - Health check

## 🔧 Development

To modify the project:

1. **Add new airports**: Edit the `AIRPORTS` dictionary in `app.py`
2. **Add new routes**: Update the `FLIGHTS` dictionary in `app.py`
3. **Modify UI**: Edit files in `static/` and `templates/`
4. **Add algorithms**: Implement in `app.py` and expose via API

## 📝 License

This is an academic project for educational purposes.

## 🙏 Acknowledgments

Created for ADSA Semester 3 Project
Made with ❤️ using Python Flask, HTML5, CSS3, and JavaScript

---

**Note**: The C++ file (`algorithms/flight_pathfinder.cpp`) is for demonstration purposes and showcases advanced algorithm implementations. The actual runtime uses Python implementations for easier web integration.
