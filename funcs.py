# solver.py

#DOCUMENTATION
#Use of math and random library for floor and random functions
#solve(board) solves input list and returns True if succesful, else False
#valid(board, num, pos) returns Boolean according to validity of given number
#find_empty(board) returns first vacant cell row, col if present else None
#random_grid(level) returns list according to level of difficulty chosen by user

import random

def solve(board):
	cell = find_empty(board)
	if not cell:
		return True
	else:
		row, col = cell

	for num in range(1,10):
		if valid(board, num, (row, col)):
			board[row][col] = num

			if solve(board):
				return True

			board[row][col] = 0

	return False


def valid(board, num, pos):
	if num == 0 :
		return None
	# Check row
	for i in range(len(board[0])):
		if board[pos[0]][i] == num and pos[1] != i:
			return False

	# Check column
	for i in range(len(board)):
		if board[i][pos[1]] == num and pos[0] != i:
			return False

	# Check box
	cell_i = pos[1] // 3
	cell_j = pos[0] // 3

	for i in range(cell_j*3, cell_j*3 + 3):
		for j in range(cell_i * 3, cell_i*3 + 3):
			if board[i][j] == num and (i,j) != pos:
				return False

	return True


def find_empty(board):
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] == 0:
				return (i, j)  # row, col

	return None

#level is an int in [0,1,2]
def random_grid(level) :
	L = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
							[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]

	#fill in diagonal blocks
	for k in [0, 3, 6] :
		fill = [i for i in range(1, 10) ]
		for i in range(k, k + 3) :
			for j in range(k, k + 3) :
				num = fill[random.randrange(0, len(fill), 1)]
				L[i][j] = num
				fill.remove(num)

	#solve
	solve(L) #L is a solved puzzle
	A = [[],[],[],[],[],[],[],[],[]]
	for row in range(9) :
		for col in range(9) :
			A[row].append(L[row][col])
	#number of cells to be vacated
	vacate = [25, 40, 60]

	for loop in range(vacate[level]) :
		#choosing a random cell
		i, j = int(9 * random.random()), int(9 * random.random())
		#check if it has been vacated already
		while L[i][j] == 0 :
			i, j = int(9 * random.random()), int(9 * random.random())
		
		#empty the cell
		L[i][j] = 0 
		
	return A,L 

def empty_left(grid):
	count = 0
	for i in range(9):
		for j in range(9):
			if(grid[i][j]==0):
				count+=1
	return count