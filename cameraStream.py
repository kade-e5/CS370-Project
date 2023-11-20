import cv2 as cv
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
from datetime import datetime
import numpy as np

class Camera(object): 
  def __init__(self, flip = False, file_type  = ".jpg", filename= "camera_photo"):
        # self.vs = PiVideoStream(resolution=(1920, 1080), framerate=30).start()
        self.vs = PiVideoStream().start()
        self.flip = flip # Flip frame vertically
        self.file_type = file_type # image type i.e. .jpg
        self.filename = filename # Name to save the photo
        time.sleep(2.0)
    
  def __del__(self):
      self.vs.stop()

  def get_frame(self):
        frame = self.vs.read()
        ret, jpeg = cv.imencode(self.file_type, frame)
        self.last_frame = jpeg
        return jpeg.tobytes()
