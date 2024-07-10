from map_component import MapComponent
from header_component import HeaderComponent
from drawer_component import DrawerComponent
import time
from fastapi import Response
from nicegui import app, run, ui
import base64
import cv2
import numpy as np
from ultralytics import YOLO
import homography

with ui.tabs().style('color: 808080') as tabs:
    one = ui.tab('Map')
    #two = ui.tab('Video')
    three = ui.tab('Yolo')

with ui.tab_panels(tabs, value=three).classes('w-full'):
    with ui.tab_panel(one):
        map_component = MapComponent()
        map_component.render()

    
    with ui.tab_panel(three):
        black_1px = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjYGBg+A8AAQQBAHAgZQsAAAAASUVORK5CYII='
        placeholder = Response(content=base64.b64decode(black_1px.encode('ascii')), media_type='image/png')
        YOLO_image = ui.interactive_image().classes('w-full h-full')
        model = YOLO("yolov8n.pt")
        target_class = "person"
        class_names = model.names
        video_capture_yolo = cv2.VideoCapture(0)

        def process_frame(frame):
            results = model(frame)
            highest_confidence = 0
            best_detection = None

            for result in results:
                for detection in result.boxes.data:
                    class_id = int(detection[5])
                    class_name = class_names[class_id]
                    confidence = float(detection[4])

                    if class_name == target_class and confidence > highest_confidence:
                        highest_confidence = confidence
                        best_detection = detection

            if best_detection is not None:
                x1, y1, x2, y2 = map(int, best_detection[:4])
                mid_x = (x1 + x2) // 2
                bottom_y = y2
                homography.get_distance(mid_x, bottom_y)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (mid_x, bottom_y), 5, (0, 0, 255), -1)
                cv2.putText(frame, f"{target_class}: ({mid_x}, {bottom_y})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            _, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

        @app.get('/yolo/frame')
        async def yolo_video_frame() -> Response:
            if not video_capture_yolo.isOpened():
                return placeholder
            _, frame = await run.io_bound(video_capture_yolo.read)
            if frame is None:
                return placeholder
            processed_frame = await run.cpu_bound(process_frame, frame)
            return Response(content=processed_frame, media_type='image/jpeg')

        ui.timer(interval=0.1, callback=lambda: YOLO_image.set_source(f'/yolo/frame?{time.time()}'))

drawer_component = DrawerComponent()
right_drawer = drawer_component.render()

header_component = HeaderComponent()
header_component.set_drawer(right_drawer)
header_component.render()

ui.run(native=True, reload=False)