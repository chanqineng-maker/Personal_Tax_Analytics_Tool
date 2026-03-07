board = []
col = 1

for i in range(3):      # Create 3 rows
    row = []
    for j in range(3):  # Create 3 columns per row
        row.append(col)
        col += 1
    board.append(row)

def display_board(board):
	print("+-------" * 3,"+", sep="")
	for row in range(3):
		print("|       " * 3,"|", sep="")
		for col in range(3):
			print("|   " + str(board[row][col]) + "   ", end="")
		print("|")
		print("|       " * 3,"|",sep="")
		print("+-------" * 3,"+",sep="")

display_board(board)

def enter_move:
    move= input()
    
