#Class to model grid point data
#X = x coordinate
#Y = y coordinate
#df = list of MAC Address and RSSI values associated with the grid point

class GridPoint:
    def __init__(self, x, y, df):
        self.x = x
        self.y = y
        self.df = df

    def __str__(self):
        return f"X={self.x}, Y={self.y}"
