from flask import Flask, render_template, Response, request, send_from_directory
from camera import VideoCamera
import os

def webpage():
  return render_template('Webpage.html') #rendering the Webpage for the camera display
