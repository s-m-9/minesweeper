class Point:
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def getRow(self):
        return self.r
    
    def getColumn(self):
        return self.c
    
    # Testing purposes
    def printPoint(self):
        point_print = "(" + str(self.r) + ", " + str(self.c) + ")"
        print(point_print)
