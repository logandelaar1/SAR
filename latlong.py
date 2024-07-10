import socket
import re

# Function to extract latitude, longitude, and heading from the given data
def parse_data(data):
    lat, lon, heading = None, None, None
    
    # Regular expressions for latitude, longitude, and heading
    lat_lon_regex = re.compile(r'\$GPGGA,.*?,(\d{2})(\d{2}\.\d+),([NS]),(\d{3})(\d{2}\.\d+),([EW]),')
    heading_regex = re.compile(r'\$GPVTG,(\d+\.\d+),T')

    for line in data.split('\n'):
        lat_lon_match = lat_lon_regex.search(line)
        heading_match = heading_regex.search(line)
        
        if lat_lon_match:
            lat_deg = int(lat_lon_match.group(1))
            lat_min = float(lat_lon_match.group(2))
            lat_dir = lat_lon_match.group(3)
            lon_deg = int(lat_lon_match.group(4))
            lon_min = float(lat_lon_match.group(5))
            lon_dir = lat_lon_match.group(6)

            # Convert to decimal degrees
            latitude = lat_deg + lat_min / 60.0
            if lat_dir == 'S':
                latitude = -latitude

            longitude = lon_deg + lon_min / 60.0
            if lon_dir == 'W':
                longitude = -longitude

            lat, lon = latitude, longitude

        if heading_match:
            heading = float(heading_match.group(1))

    return lat, lon, heading

def main():
    host = '192.168.1.81'
    
    port = 8003
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Connected to {host}:{port}")
        
        while True:
            data = s.recv(1024).decode('utf-8')
            if not data:
                break
            
            lat, lon, heading = parse_data(data)
            
            if lat and lon and heading:
                print(f"Latitude: {lat}, Longitude: {lon}, Heading: {heading}")
                

if __name__ == "__main__":
    main()