import math

def meters_to_degrees(x, y, initial_lat, initial_lon, heading):
    R = 6378137  # Radius of the Earth in meters

    heading_rad = math.radians(heading)

    delta_x = x * math.cos(heading_rad) - y * math.sin(heading_rad)
    delta_y = x * math.sin(heading_rad) + y * math.cos(heading_rad)

    delta_lat = delta_y / R
    delta_lon = delta_x / (R * math.cos(math.radians(initial_lat)))

    new_lat = initial_lat + math.degrees(delta_lat)
    new_lon = initial_lon + math.degrees(delta_lon)

    return new_lat, new_lon

def read_initial_coords(file_path):
    with open(file_path, 'r') as file:
        line = file.readline().strip()
        parts = line.split(',')
        latitude = float(parts[0].split(': ')[1])
        longitude = float(parts[1].split(': ')[1])
        heading = float(parts[2].split(': ')[1])
    return latitude, longitude, heading

def calculate_new_position(x, y, file_path='coords2.txt'):
    initial_lat, initial_lon, heading = read_initial_coords(file_path)
    new_lat, new_lon = meters_to_degrees(x, y, initial_lat, initial_lon, heading)
    return new_lat, new_lon