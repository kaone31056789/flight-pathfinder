"""
Route Map Visualization - Pure Python + Folium
Generates realistic great-circle curved flight paths with NO NumPy dependency.
"""

from math import radians, degrees, sin, cos, atan2, sqrt, acos
from typing import List, Tuple, Dict
import folium
from folium import Map, Marker, PolyLine
from folium.features import DivIcon

# Try to import AntPath for animation (optional)
try:
    from folium.plugins import AntPath
    HAS_ANTPATH = True
except:
    HAS_ANTPATH = False

# Airport data
AIRPORTS: Dict[str, Dict] = {
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


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance in kilometers."""
    R = 6371.0
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def interpolate_great_circle(lat1: float, lon1: float, lat2: float, lon2: float, num_points: int = 150) -> List[Tuple[float, float]]:
    """
    Interpolate points along great-circle route using spherical linear interpolation.
    Pure Python implementation - no NumPy required.
    """
    if num_points < 2:
        return [(lat1, lon1), (lat2, lon2)]
    
    # Convert to radians
    lat1_r, lon1_r = radians(lat1), radians(lon1)
    lat2_r, lon2_r = radians(lat2), radians(lon2)
    
    # Convert to 3D Cartesian coordinates
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
    
    # Calculate angle between points
    dot = p1[0]*p2[0] + p1[1]*p2[1] + p1[2]*p2[2]
    dot = max(min(dot, 1.0), -1.0)  # Clamp to avoid math domain error
    omega = acos(dot)
    
    # Handle same or antipodal points
    if abs(omega) < 1e-10:
        return [(lat1, lon1) for _ in range(num_points)]
    
    sin_omega = sin(omega)
    points = []
    
    for i in range(num_points):
        f = i / (num_points - 1)
        a = sin((1 - f) * omega) / sin_omega
        b = sin(f * omega) / sin_omega
        
        x = a * p1[0] + b * p2[0]
        y = a * p1[1] + b * p2[1]
        z = a * p1[2] + b * p2[2]
        
        # Normalize
        norm = sqrt(x*x + y*y + z*z)
        x, y, z = x/norm, y/norm, z/norm
        
        lat, lon = from_xyz(x, y, z)
        points.append((lat, lon))
    
    return points


def generate_route_map(
    src_code: str,
    dst_code: str,
    airports: Dict[str, Dict] = None,
    num_points: int = 150,
    tiles: str = 'CartoDB positron',
    animate: bool = True
) -> folium.Map:
    """Generate folium map with curved great-circle route."""
    
    if airports is None:
        airports = AIRPORTS
    
    src = airports.get(src_code)
    dst = airports.get(dst_code)
    
    if not src or not dst:
        raise ValueError(f'Airport codes not found: {src_code}, {dst_code}')
    
    lat1, lon1 = src['lat'], src['lon']
    lat2, lon2 = dst['lat'], dst['lon']
    
    # Interpolate great-circle path
    path = interpolate_great_circle(lat1, lon1, lat2, lon2, num_points)
    
    # Center map
    mid_lat = (lat1 + lat2) / 2
    mid_lon = (lon1 + lon2) / 2
    
    m = folium.Map(location=[mid_lat, mid_lon], zoom_start=5, tiles=tiles)
    
    # Title
    title_html = f'''
    <div style="position:fixed;top:10px;left:50px;z-index:9999;background:rgba(255,255,255,0.9);
                padding:10px 15px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.2);">
        <h3 style="margin:0;color:#2563eb;">✈️ {src_code} → {dst_code}</h3>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Distance
    total_km = haversine_distance(lat1, lon1, lat2, lon2)
    distance_html = f'''
    <div style="position:fixed;bottom:20px;left:50px;z-index:9999;background:rgba(255,255,255,0.9);
                padding:8px 12px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.2);">
        <strong>Distance: {total_km:.1f} km</strong>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(distance_html))
    
    # Draw route
    locations = [[lat, lon] for lat, lon in path]
    
    if animate and HAS_ANTPATH:
        from folium.plugins import AntPath
        AntPath(locations, dash_array=[10, 20], delay=2000, weight=4, color='#2563eb', opacity=0.8).add_to(m)
    else:
        PolyLine(locations, color='#2563eb', weight=4, opacity=0.7).add_to(m)
    
    # Origin marker
    Marker(
        [lat1, lon1],
        popup=f"{src_code} - {src['name']}",
        icon=folium.Icon(color='green', icon='plane', prefix='fa')
    ).add_to(m)
    
    # Destination marker
    Marker(
        [lat2, lon2],
        popup=f"{dst_code} - {dst['name']}",
        icon=folium.Icon(color='red', icon='flag', prefix='fa')
    ).add_to(m)
    
    # IATA labels
    folium.map.Marker(
        [lat1, lon1],
        icon=DivIcon(html=f'''
            <div style="font-weight:bold;color:#fff;background:#16a34a;
                        padding:4px 8px;border-radius:4px;box-shadow:0 2px 6px rgba(0,0,0,0.3);">
                {src_code}
            </div>
        ''')
    ).add_to(m)
    
    folium.map.Marker(
        [lat2, lon2],
        icon=DivIcon(html=f'''
            <div style="font-weight:bold;color:#fff;background:#ef4444;
                        padding:4px 8px;border-radius:4px;box-shadow:0 2px 6px rgba(0,0,0,0.3);">
                {dst_code}
            </div>
        ''')
    ).add_to(m)
    
    return m


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate curved flight route map')
    parser.add_argument('--from', dest='src', required=True, help='Source IATA')
    parser.add_argument('--to', dest='dst', required=True, help='Destination IATA')
    parser.add_argument('--points', type=int, default=150, help='Interpolation points')
    parser.add_argument('--out', default='route.html', help='Output file')
    args = parser.parse_args()
    
    m = generate_route_map(args.src.upper(), args.dst.upper(), num_points=args.points)
    m.save(args.out)
    print(f'✅ Saved {args.out}')
