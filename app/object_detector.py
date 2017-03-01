import cv2
import time
import numpy as np



class ObjectDetector:

    def report(self):
        pass

    def __init__(self,app,options):
        self.options = options
        
        app.logger.debug(""" opencv version: """+cv2.__version__)
        app.logger.info("capturing camera port "+str(app.config["camera"]))
        firstFrame = None
        camera = cv2.VideoCapture(app.config['camera'])
        low = np.array([app.config['detection']['hue'][0],app.config['detection']['saturation'][0],app.config['detection']['value'][0]])
        heigh = np.array([app.config['detection']['hue'][1],app.config['detection']['saturation'][1],app.config['detection']['value'][1]])

        while True:
            (grabbed, frame) = camera.read()
            if not grabbed:
                break

            blur = cv2.blur(frame, (7,7))
            # Convert BGR to HSV
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, low, heigh)

            # Bitwise-AND mask and original image
            res = cv2.bitwise_and(frame,frame, mask= mask)
            if (options['gui']==True):
                display = cv2.resize(mask, (0,0), fx=0.5,fy=0.5) 
                cv2.imshow('frame',display)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


