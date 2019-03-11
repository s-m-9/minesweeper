import board as b
import guiboard as gb

# Testing purposes

board = b.Board(9, 9, 10)
board.createBoard()

# board.click(1, 2)

board.showBoard()

row = int(input("Input row: "))
column = int(input("Input column: "))

# board.click(row, column)
# board.showBoard()

print("\n")
# guiboard = gb.guiBoard(board)
# guiboard.showBoard()

