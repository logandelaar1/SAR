from nicegui import events
import generate_waypoints as waypoint
from nicegui import ui
from pyMOOS import MOOSCommClient
import time
def filter_coordinates(input_list):
    filtered_list = []
    for sublist in input_list:
        for coord in sublist:
            filtered_list.append([coord['lng'], coord['lat']])
    return filtered_list



class EventHandlers:
    def __init__(self, map_instance):
        self.map_instance = map_instance
            
    def handle_draw(self, e: events.GenericEventArguments):
        if e.args['layerType'] == 'marker':
            latlng = (e.args['layer']['_latlng']['lat'], e.args['layer']['_latlng']['lng'])
            self.map_instance.marker(latlng=latlng)
        if e.args['layerType'] == 'polygon':
            latlngs = e.args['layer']['_latlngs']
            self.map_instance.generic_layer(name='polygon', args=[latlngs])

            
            def path_creation():
                step_meters = 10  # Adjust this value as needed
                wp=waypoint.generate_waypoints(filter_coordinates(latlngs), step_meters)
                
                SARPath = [{'lat': max(s), 'lng': min(s)} for s in wp]
                self.map_instance.generic_layer(name='polyline', args=[SARPath])
                print(SARPath)
                comms = MOOSCommClient()

                comms.run('localhost', 9000, 'WaypointPublisher')

                while not comms.is_connected():
                    time.sleep(0.1)

                for waypoint in wp:
                    comms.notify('WAYPOINT', f"{waypoint[0]},{waypoint[1]}")
                    time.sleep(0.1)
        
                
            ui.button('Generate Path', on_click=lambda: path_creation())

            
                
                            
        