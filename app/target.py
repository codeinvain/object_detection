import cv2
import tracks
from ostruct import OpenStruct

class Target:
    def __init__(self,contour):
        self.contour = contour
        self._ratio = None
        self._rect = None

    def area(self):
        self._area = self._area  or cv2.contourArea(self.contour)
        return self._area

    def rect(self):
        if self._rect==None:
            self._rect = OpenStruct()
            self._rect.y,self._rect.x,self._rect.w,self._rect.h = cv2.boundingRect(self.contour)
        return self._rect

    def ratio(self):
        self._ratio = self._ratio or (self.rect().w / self.rect().h)
        return self._ratio


    def isValid(self):
        return self.isInRatio()

    # expecting ratio of 2/5 ~ 0.4 
    def isInRatio(self):
        return self.ratio() > tracks.config['target']['min_ratio'] and self.ratio() < tracks.config['target']['max_ratio']


