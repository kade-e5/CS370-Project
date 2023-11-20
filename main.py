from flask import Flask, render_template, Response, request, send_from_directory
from cameraStream import Camera
import os

camera_pi = Camera() 

# App Globals
app = Flask(__name__)

@app.route('/')
def webpage():
  return render_template('index.html') #rendering the Webpage for the camera display

def gen(cameraStream):
    #get camera frame
    while True:
        frame = cameraStream.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_stream():
    return Response(gen(camera_pi),boundarytype='multipart/x-mixed-replace; boundary=frame')

# Take a photo when pressing camera button
@app.route('/picture')
def take_picture():
    pi_camera.take_picture()
    return "None"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)

