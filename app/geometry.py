from ostruct import OpenStruct

class Geometry:
    def __init__(self):
        pass

    def get_coordinates(self,pair,frame):
        res = OpenStruct()
        res.x_distance = self.get_x_distance(pair,frame)
        res.y_distance = self.get_y_distance(pair,frame)
        res.angle = self.get_angle(pair,frame)
        return res


    def get_x_distance(self,pair,frame):
        return 10

    def get_y_distance(self,pair,frame):
        return 10

    def get_angle(self,pair,frame):
        return 360
