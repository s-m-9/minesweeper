import board as b


class guiBoard:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.guiboard = [["E" for i in range(rows)] for k in range(columns)]

    def setValue(self, row, col, value):
        try: 
            self.guiboard[row][col] = value
        except IndexError:
            return
    
    # return specific value
    def getValue(self, row, col):
        return self.guiboard[row][col]
    
    # Returns a guiBoard as a string
    def getGui(self):
        guiString = ""
        for row in range(self.rows):
            for col in range(self.columns):
                guiString += self.guiboard[row][col] + " "
            # print("\n")
        # print("\n")

        return guiString

    # Testing purposes
    def showBoard(self):
        for row in range(self.rows):
            for col in range(self.columns):
                print(self.guiboard[row][col])
            print("\n")
        print("\n")
