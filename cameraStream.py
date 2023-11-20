import cv2 as cv
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
from datetime import datetime
import numpy as np

class Camera(object): 
  def __init__(self, file_type  = ".jpg", filename= "camera_photo"):
        self.vs = PiVideoStream(framerate=60).start()
        self.file_type = file_type 
        self.filename = filename 
        
    
  def __del__(self):
      self.vs.stop()

  def get_frame(self):
        frame = self.vs.read()
        ret, jpeg = cv.imencode(self.file_type, frame)
        return jpeg.tobytes()
