import geopandas as gpd
from shapely.geometry import Polygon as SPolygon, LineString
from geopy.distance import geodesic


class PolygonProcessor:
    def __init__(self, coords, step_meters):
        self.coords = coords
        self.step_meters = step_meters
        self.process_polygon()

    def meters_to_degrees(self, meters, at_lat):
        # Conversion factor for meters to degrees at a given latitude
        degrees_per_meter_lat = 1 / geodesic((at_lat, 0), (at_lat + 1, 0)).meters
        degrees_per_meter_lng = 1 / geodesic((at_lat, 0), (at_lat, 1)).meters
        return meters * degrees_per_meter_lat, meters * degrees_per_meter_lng

    def process_polygon(self):
        shapely_polygon = SPolygon(self.coords)
        buffered_polygon = shapely_polygon.buffer(-0.00005)  # Adjusted for degrees

        step_lat, step_lng = self.meters_to_degrees(self.step_meters, self.coords[0][1])
        x_min, y_min, x_max, y_max = buffered_polygon.bounds

        x_min += step_lng
        x_max -= step_lng
        y_min += step_lat
        y_max -= step_lat

        lines = []
        direction = 'right'
        y = y_min
        while y <= y_max:
            if direction == 'right':
                lines.append(LineString([(x_min, y), (x_max, y)]))
                direction = 'left'
            else:
                lines.append(LineString([(x_max, y), (x_min, y)]))
                direction = 'right'
            y += step_lat

        lines_gdf = gpd.GeoDataFrame(geometry=lines, crs='EPSG:4326')
        self.clipped = gpd.clip(lines_gdf, buffered_polygon)

    def get_path_points(self):
        # Function to get all points in a LineString
        def process_line_points(geom):
            xs, ys = geom.xy
            return [(x, y) for x, y in zip(xs, ys)]

        path_points = []
        for geom in self.clipped.geometry:
            if geom.geom_type == 'LineString':
                path_points.extend(process_line_points(geom))
        return path_points



def generate_waypoints(bounding_box_coords, step_meters):
    processor = PolygonProcessor(bounding_box_coords, step_meters)
    path_points = processor.get_path_points()
    return path_points