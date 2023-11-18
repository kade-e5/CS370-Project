from flask import Flask, render_template, Response, request, send_from_directory
from camera import Camera
import os

camera_pi = Camera(flip=False) #Camera is not upside down set flip to false

def webpage():
  return render_template('Webpage.html') #rendering the Webpage for the camera display
