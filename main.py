from flask import Flask, render_template, Response, request, send_from_directory
from cameraStream import Camera
import os

camera_pi = Camera(flip=False) #Camera is not upside down set flip to false

# App Globals
app = Flask(__name__)

@app.route('/')
def webpage():
  return render_template('Webpage.html') #rendering the Webpage for the camera display

def gen(cameraStream):
    #get camera frame
    while True:
        frame = cameraStream.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_stream():
    return Response(gen(camera_pi),boundarytype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)

