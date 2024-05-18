from PIL import Image
import numpy
import pandas
import Const

class Track():

    def __init__(self, track):
        self.track = Image.open(track).load()
        self.np_img = numpy.array(self.track)
        self.pixels = numpy.zeros((Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT))
        for x in range(Const.SCREEN_WIDTH):
            for y in range(Const.SCREEN_HEIGHT):
                if self.track[x, y] == 0:
                    self.pixels[x][y] = 1
        
        DF = pandas.DataFrame(self.pixels)



