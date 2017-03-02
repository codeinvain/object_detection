import cv2
import time
import numpy as np
import imutils
import tracks
from target import Target


class ObjectDetector:

    def report(self):
        pass


    def __init__(self):
        
        tracks.logger.debug(""" opencv version: """+cv2.__version__)
        tracks.logger.info("capturing camera port "+str(tracks.config["camera"]))
        firstFrame = None
        camera = cv2.VideoCapture(tracks.config['camera'])
        low = np.array(tracks.config['detection']['from_color']) # [h,v,s] color format
        heigh = np.array(tracks.config['detection']['to_color'])
        blur_radius = tracks.config['detection']['blur_radius']

        while True:
            (grabbed, frame) = camera.read()
            if not grabbed:
                break

            # blure image 
            blur = cv2.blur(frame, (blur_radius,blur_radius))
            # convert to hsv
            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            # mask by low / heigh hsv values
            mask = cv2.inRange(hsv, low, heigh)

            dialateElm =cv2.getStructuringElement(cv2.MORPH_RECT,(24,24))
            erodeElm =cv2.getStructuringElement(cv2.MORPH_RECT,(12,12))
            mask = cv2.erode(mask, erodeElm, iterations=2)
            mask = cv2.dilate(mask, dialateElm, iterations=2)

            final =mask 

            if self.debug('frame',final):
                break
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            if (len(cnts)>1):
                self.find_and_report_target(cnts)


    def find_and_report_target(self,cnts):
        targets = list(map(lambda c: Target(c) ,cnts))
        pair = self.find_pair(targets)



    def find_pair(self,targets):
        pair = []
        left  = list(targets)
        right = list(targets)

        for l in left:
            t = [abs(l.rect().h -r.rect().h) for r in right]
            ind = t.index(min(t))
            pair.append((l,right[ind]))
            left.remove(l)
            right.remove(right[ind])
        return pair




    def debug(self,name,frame):
        if (tracks.config['gui']==True):
            display = imutils.resize(frame, width=600)
            cv2.imshow('frame',display)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return True
        return False


