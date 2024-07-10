from nicegui import ui
from event_handlers import EventHandlers
import location
options = {
    'zoomControl': True,
    'doubleClickZoom': False,
}

draw_control = {
    'draw': {
        'polygon': True,
        'marker': False,
        'circle': False,
        'rectangle': False,
        'polyline': False,
        'circlemarker': False,
    },
    'featureGroup': 'drawnItems',
    'edit': False,
}
def read_initial_coords(file_path):
    with open(file_path, 'r') as file:
        line = file.readline().strip()
        parts = line.split(',')
        latitude = float(parts[0].split(': ')[1])
        longitude = float(parts[1].split(': ')[1])
        heading = float(parts[2].split(': ')[1])
    return latitude, longitude, heading
class MapComponent:
    def __init__(self):
        self.center_location = [41.35036468760044, -74.06017358880491]
        self.map_instance = None

    def render(self):
        self.map_instance = ui.leaflet(center=self.center_location, zoom=19, options=options, draw_control=draw_control).style('width: 100%; height: 70vh')
        self.map_instance.tile_layer(url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}')
        event_handlers = EventHandlers(self.map_instance)
        self.map_instance.on('draw:created', event_handlers.handle_draw)
        self.map_instance.generic_layer(name='circle', args=[self.center_location, {'color': 'red', 'radius': 20}])
        

        