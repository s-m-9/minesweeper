import random
import Point as p
import guiboard as gb
import json

class Board:
    def __init__(self, rows, columns, num_of_bombs):
        self.rows = rows
        self.columns = columns
        self.num_of_bombs = num_of_bombs
        self.board = [[0 for i in range(rows)] for k in range(columns)]
        self.bomb_list = []
        self.guiboard = gb.guiBoard(rows, columns)
        self.isLocked = False

    #  Create Coordinate for bomb on the board, generated at random positions
    def generateBombs(self):
        for _ in range(self.num_of_bombs):
            accepted = False
            while accepted == False:
                r = random.randint(0, self.rows - 1)
                c = random.randint(0, self.columns - 1)
                
                # check to see if there is a duplicate in this loop
                duplicate = False
                
                for bomb in self.bomb_list:
                    if r == bomb.getRow() and c == bomb.getColumn():
                        duplicate = True
                        break;
                
                if duplicate == False:
                    self.bomb_list.append(p.Point(r, c))
                    accepted = True

    # Place the bombs on the board
    def createBoard(self):
        self.generateBombs()
        for bomb in self.bomb_list:
            self.placeBomb(bomb.getRow(), bomb.getColumn())

    # place the bomb at the coordinates
    def placeBomb(self, row, column):
        # place bomb at position
        # print(row, column);
        self.board[row][column] = -1
        # Top-Left:     [-1, -1]
        self.changePointValue(row, column, -1, -1)
        # Top:          [-1,  0]
        self.changePointValue(row, column, -1, 0)
        # Top-Right:    [-1,  1]
        self.changePointValue(row, column, -1, 1)

        # Right:        [ 0,  1]
        self.changePointValue(row, column, 0, 1)
        # Left:         [ 0, -1]
        self.changePointValue(row, column, 0, -1)

        # Bottom-Right: [ 1,  1]
        self.changePointValue(row, column, 1, 1)
        # Bottom:       [ 1,  0]
        self.changePointValue(row, column, 1, 0)
        # Bottom-Left:  [ 1, -1]
        self.changePointValue(row, column, 1, -1)
    
    # when placing bombs, increment the area around them by one
    def changePointValue(self, row, column, offsetRow, offsetCol):
        # print("offset: " + str(offsetRow) + ", " + str(offsetCol))
        newRow = row + offsetRow
        newCol = column + offsetCol
        if newRow >= 0 and newRow < self.rows and newCol >= 0 and newCol < self.columns:
            # e = "====changing " + str(newRow) + "," + str(newCol)
            # print(e)
            if self.board[newRow][newCol] != -1:
                self.board[newRow][newCol] += 1 

    # Testing purposes
    def showBoard(self):
        for row in range(self.rows):
            for col in range(self.columns):
                print(self.board[row][col])
            print("\n")
    
    # generated a boardString used to populate board on front end if game was saved
    def populateBoard(self, state, guiString):
        boardString = ""
        guiList = state.split("-")
        pointList = []
        guiBoard = guiString.split(" ");
        # guiList = [1:]
        # for point in guiList
        
        # create the coordinates that the player has already hit
        for i in range(len(guiList)):
            if guiList[i] != "_" and guiList[i] != "":
                point = []
                point = guiList[i].split(",")
                # print(point)
                # return point[0]
                pointList.append(p.Point(point[0], point[1]))
        
        k = 0
        # get string of board using the guiBoard and players pointList
        for row in range(self.rows):
            for col in range(self.columns):
                if p.Point(row, col) in pointList:
                    boardString += guiBoard[k] + " "
                else:
                    boardString += "E "
                k += 1

        return boardString

    # Player can click
    def unlockGame(self):
        self.isLocked = False      

    # Player can't click anymore 
    def lockGame(self):
        self.isLocked = True

    def  click(self, row, col):
        hitValue = self.board[row][col]
        answer = "-"
        gui = None
        if self.isLocked == True:
            return json.dumps({'answer': "GAME OVER!", 'guiString': None})

        # if hit place is zero, recursively set hit board to H
        if hitValue == 0:
            # print("Empty Spot")
            answer = "EmptySpot"
            # change value of guiboard
            # self.guiboard.setValue(row, col, "H")
            self.guiboard.setValue(row, col, "H")
            self.clearEmptySpace(row, col)
            gui = self.guiboard.getGui()
            self.guiboard.showBoard()
        # if hit place is neg. one, say "HIT"
        elif hitValue == -1:
            # print("BOMB! YOU LOSE!")
            answer = "BOMB! YOU LOSE!"
            self.guiboard.setValue(row, col, "E")
            gui = self.guiboard.getGui()
        # if hit a number, uncover, number
        else:
            # print("Number: ", hitValue)
            answer = str(hitValue)
            hit = "[" + str(hitValue) + "]"
            self.guiboard.setValue(row, col, hit)
            gui = self.guiboard.getGui()

        answer = self.getGameStatus(answer)
        return json.dumps({ 'answer': answer, 'guiString': gui })
    
    # recursively clears empty spaces if empty space is clicked
    def clearEmptySpace(self, row, col):        
        # Right
        self.clear(row, col + 1, 0, 1)

        #Left
        self.clear(row, col - 1, 0, -1)

        # Bottom
        self.clear(row + 1, col, 1, 0)
        
        # Top
        self.clear(row - 1, col, -1, 0)


    # continuously clears empty spaces
    def clear(self, row, col, offsetRow, offsetCol):
        
        # bounds check
        if row < 0 or row >= self.rows or col < 0 or col >= self.columns:
            
            return
        
        #  if it has a bracket, there is a number then it has been hit, return
        check = self.guiboard.getValue(row, col)
        if check[0] == "[" or self.guiboard.getValue(row, col) == "H":      
            return
        
        #  if there is a -1, there is a bomb, don't touch
        if self.board[row][col] == -1:
            return

        # if there is a number there, then set value
        if self.board[row][col] > 0:
            number = "[" + str(self.board[row][col]) + "]"
            self.guiboard.setValue(row, col, number)
            return


        # put hit on board
        self.guiboard.setValue(row, col, "H")
        
        # continue recursion
        return self.clearEmptySpace(row, col)

    # Checks for a win
    def getGameStatus(self, answer):
        newAnswer = "YOU WIN!"
        if answer == "BOMB! YOU LOSE!":
            return answer
        else:
            #  counting to see if all squares but the bombs have been clicked. If so the player won
            squareCount = self.rows * self.columns
            hitCount = 0

            for row in range(self.rows):
                for col in range(self.columns):
                    if self.guiboard.getValue(row, col)[0] == "[" or self.guiboard.getValue(row, col) == "H":
                        hitCount += 1

        if squareCount - hitCount == self.num_of_bombs:    
            return newAnswer

        return answer

    


        
        

    

    


   


        

