#!/usr/bin/env python
from flask import Flask, render_template, Response
import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)


#%%
app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    profile = pipeline.start(config)
    
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        frame = color_image
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
