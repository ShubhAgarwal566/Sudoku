#Randomly generate puzzle for user
import pygame, sys
from pygame.locals import *
import funcs
import time

class Cell :
	#height and width of cell in px is fixed at 60*60    
	height = 60
	width = 60
	
	def __init__(self, row, col):
		self.row = row
		self.col = col
		self.selected = False
		self.changeable = True
		self.color = (0,0,255)
		self.val = 0
		self.rough_vals = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False, 9:False}
	#dual purpose - setting values and highlighting border if selected  
	def draw_cell(self, win) :        
		fnt = pygame.font.SysFont("comicsans", 40)
		fnt2 = pygame.font.SysFont("comicsans", 20)

		gap = 60
		x = self.col * gap
		y = self.row * gap

		if not self.changeable: 
			pygame.draw.rect(win, (128,128,128), (x,y,gap,gap), 0) 
			
		if self.changeable :
			pygame.draw.rect(win, (255,255,255), (x,y,gap,gap), 0) 
		
		row1 = ""
		if(self.rough_vals[1]==True):
			row1+="1"
		else:
			row1+=" "
		row1+="    "
		if(self.rough_vals[2]==True):
			row1+="2"
		else:
			row1+=" "
		row1+="    "
		if(self.rough_vals[3]==True):
			row1+="3"
		else:
			row1+=" "
		
		row2=""
		if(self.rough_vals[4]==True):
			row2+="4"
		else:
			row2+=" "
		row2+="    "
		if(self.rough_vals[5]==True):
			row2+="5"
		else:
			row2+=" "
		row2+="    "
		if(self.rough_vals[6]==True):
			row2+="6"
		else:
			row2+=" "
		
		row3=""
		if(self.rough_vals[7]==True):
			row3+="7"
		else:
			row3+=" "
		row3+="    "
		if(self.rough_vals[8]==True):
			row3+="8"
		else:
			row3+=" "
		row3+="    "
		if(self.rough_vals[9]==True):
			row3+="9"
		else:
			row3+=" "			

		win.blit(fnt2.render(str(row1), 1, (50, 50, 50)), (x + 2, y + 2))
		win.blit(fnt2.render(str(row2), 1, (50, 50, 50)), (x + 2, y + 22))
		win.blit(fnt2.render(str(row3), 1, (50, 50, 50)), (x + 2, y + 42))


		if  self.val != 0:
			text = fnt.render(str(self.val), 1, (0, 0, 0))
			win.blit(text, (x + 20, y + 20))
			


class Grid :
	def __init__(self, level): 
		#dimensions of grid in pixels
		self.width = 540
		self.height = 540
		self.cell_list = [[Cell(i,j) for j in range(9)] for i in range(9)]
		self.vals = [[0 for j in range(9)] for i in range(9)]
		#contains a tuple of row, col of selected cell
		self.selected = None
		#puzzle is a list of two matrices -
		#A random solved matrix
		#An unsolved matrix generated from above matrix (with proper difficulty level)        
		self.puzzle = funcs.random_grid(level)
		for row in range(9) :
			for col in range(9) :
				self.cell_list[row][col].val = self.puzzle[1][row][col]
				self.vals[row][col] = self.puzzle[1][row][col]
				if not self.cell_list[row][col].val == 0 :
					#preset values are unselectable and unchangeable
					self.cell_list[row][col].changeable = False
	
	#redraws table and its contents    
	def draw_board(self, win):
		#draw cells
		for i in range(9) :
			for j in range(9) :
				self.cell_list[i][j].draw_cell(win)
		# Draw Grid Lines
		gap = self.width / 9
		for i in range(10):
			if i % 3 == 0 and i != 0:
				thick = 4
			else:
				thick = 1
			pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
			pygame.draw.line(win, (0,0,0), (i*gap, 0), (i*gap, self.height), thick)
		for i in range(9) :
			for j in range(9) :
				if self.cell_list[i][j].selected :
					pygame.draw.rect(win, self.cell_list[i][j].color, (j*60,i*60,60,60), 3)
					
	def first_selection(self):
		for i in range(9):
			for j in range(9):
				if self.cell_list[i][j].changeable:
					self.cell_list[i][j].selected = True
					self.selected = i, j
					return i,j

	#making a selection (and deselecting others) - selects only changeable keys        
	def selection(self,row, col, color=(0,0,255)) :
		for i in range(9) :
			for j in range(9) :
				self.cell_list[i][j].selected = False
		if self.cell_list[row][col].changeable:
			self.cell_list[row][col].selected = True
			self.cell_list[row][col].color = color
			self.selected = row, col
		else :
			self.selected = None
	
	#to determine selected cell, given position of cursor  (not generalised for the rest of the board)  
	def click_loc(self, pos) :
		if pos[0] < self.width and pos[1] < self.height :
			return pos[1] // 60, pos[0] // 60   
		else : 
			return None
		
#check whether board is filled and is worthy of being checked !
#return value - NONE (if incompletely filled), TRUE(if correctly filled), FALSE(if incorrectly filled)
def check(board) :   
	for i in range(9) :
		for j in range(9) :
			if board.cell_list[i][j].val == 0 :
				return None
	#sudoku matrix 
	for i in range(9) :
		for j in range(9) :
			if  not funcs.valid(board.vals, board.vals[i][j], (i, j)) :
				return False
	return True

#return formatted time
def format_time(secs):
	sec = secs%60
	minute = secs//60
	hour = minute//60
	hour = str(hour + 100)[-2:]
	minute = str(minute + 100)[-2:]
	sec = str(sec + 100)[-2:]

	timer = hour + ":" + minute + ":" + sec
	return timer

def solve(board, win, puzzle):
	cell = funcs.find_empty(puzzle)
	if not cell:
		return True
	else:
		row, col = cell

	for num in range(1,10):
		if funcs.valid(puzzle, num, (row, col)):
			puzzle[row][col] = num
			board.cell_list[row][col].val = num
			board.selection(row,col)
			time.sleep(.3) #shubh
			board.draw_board(win)
			pygame.display.update()
			if solve(board, win, puzzle):
				return True

			puzzle[row][col] = 0

	return False


#My Function callable in main        
def PLAY(win) :
	img = pygame.image.load("left_arrow.png")
	re = pygame.image.load("undo.png")
	while True :
		#clear window contents
		win.fill((255,255,255))
		#drawing the buttons for level setting
		term_x = [200, 400]
		term_y = [200, 250, 300, 350]
		gamerun = True
		level = None  
		key = 0
		run = True
		while run :
			#redraw options table    
			for i in range(4) :
				pygame.draw.line(win, (128, 128, 128), (term_x[0], term_y[i]), (term_x[1], term_y[i]))
			for i in range(2) :
				pygame.draw.line(win, (128, 128, 128), (term_x[i], 200), (term_x[i], 350))
			fnt = pygame.font.SysFont("comicsans", 40)    
			options = ["EASY", "MEDIUM", "HARD"]
			text = [fnt.render(options[i], 0, (128, 128, 128)) for i in range(3)]
			x = [200, 400]
			y = [200, 250, 300,350]
			for i in range(3) :
				win.blit(text[i], (250, y[i] + 15))  
			win.blit(img, (0, 550))
			pygame.display.update()
				
			for event in pygame.event.get() :
				#if quit detected
				if(event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE) ):
					pygame.quit()
					sys.exit()         
				#detecting the mouseclick and checking which button was selected (and breaking out from 2 loops)
				elif event.type == MOUSEBUTTONDOWN :
					x, y = pygame.mouse.get_pos()
					if( x > 200 and x < 400 and y > 200):
						if( y < 250 ):
							level = 0
							run = False
							break
						elif( y < 300 ):
							level = 1
							run = False
							break
						elif( y < 350 ):
							level = 2
							run = False
							break
					elif( x > 0 and x < 50 and y > 560 and y < 600): # back button pressed
						return

		#clear window contents to construct Sudoku grid
		win.fill((255,255,255))
		board = Grid(level) 
		org_board = board
		exit = False
		back = False
		rough = False
		start = time.time()
		timer = 0
		#print solution in terminal in readable format to make evaluation easier
		if(False):
			for row in board.puzzle[0] :
				print(row)
			print
			print
		row, col = board.first_selection()
		while gamerun :
			if not exit :
				board.draw_board(win) 
				pygame.draw.rect(win, (150,150,150), (0, 544, 300, 60))
				style = pygame.font.SysFont("comicsans", 40)
				win.blit(style.render("Solve", 0, (0, 0, 0)), (70,560))
				if(rough==True):
					win.blit(style.render("Rough", 0, (255, 0, 0)), (180,560))
				else:
					win.blit(style.render("Rough", 0, (0, 0, 0)), (180,560))
				win.blit(img, (0, 550))
				pygame.draw.line(win, (0,0,0), (60,540), (60,600), 4) # start of solve
				pygame.draw.line(win, (0,0,0), (150,540), (150,600), 4) # end of solve button 
				pygame.draw.rect(win,(255,255,255), (300,560,300,55),0)
				pygame.draw.line(win, (0,0,0), (300,540), (300,600), 4) # begin of eval block
				pygame.draw.line(win, (0,0,0), (360,540), (360,600), 4) # end of eval block
				timer = int(time.time() - start)
				lstyle = pygame.font.SysFont("comicsans", 40)
				win.blit(lstyle.render(format_time(timer), 1, (0,0,0)), (400, 560))
				if board.selected != None :
					if funcs.valid(board.vals, board.vals[board.selected[0]][board.selected[1]], board.selected) == False:
						win.blit(lstyle.render("X", 1, (255,0,0)), (320, 560))
						board.selection(row,col,(255,0,0))
					elif funcs.valid(board.vals, board.vals[board.selected[0]][board.selected[1]], board.selected) == True:
						win.blit(lstyle.render("V", 1, (0,255,0)), (320, 560))
						board.selection(row,col,(0,255,0))
				pygame.display.update()
			for event in pygame.event.get() :
				#if quit is detected
				if( event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE)):
					pygame.quit()
					sys.exit()
				#if user clicks on screen
				elif event.type == MOUSEBUTTONDOWN and not exit:
					x, y = pygame.mouse.get_pos()
					#if user clicks somewhere on the grid
					if not board.click_loc((x,y)) == None :
						row, col =  board.click_loc((x,y))
						board.selection(row, col)
					#if user clicks on "Solve"
					elif x > 60 and x < 150 and y > 540 and y < 600:
						solve(board.org_puzzle)
					#user clicks onn rough
					elif( x > 150 and x < 300 and 540<y<600):
						rough = not rough
					#user clicks on back
					elif x > 0 and x < 50 and y > 560 and y < 600:
						gamerun = False 
						run = True
				#if user presses a key                     
				elif event.type == KEYDOWN and not exit:
					# conditions for keyboard shortcuts
					if(event.key == pygame.K_r):
						rough = not(rough)
					elif(event.key == pygame.K_s):
						board = org_board
						solve(board, win, board.puzzle[1]) #shubh

					# conditions for arrow keys
					if(event.key == pygame.K_UP):
						temp_row = row
						for i in range(row-1, -1, -1):
							if(board.cell_list[i][col].changeable):
								temp_row = i
								break
						row = temp_row
						board.selection(row, col)
					elif(event.key == pygame.K_DOWN):
						temp_row = row
						for i in range(row+1, 9):
							if(board.cell_list[i][col].changeable):
								temp_row = i
								break
						row = temp_row
						board.selection(row, col)
					elif(event.key == pygame.K_RIGHT):
						temp_col = col
						for i in range(col+1, 9):
							if(board.cell_list[row][i].changeable):
								temp_col = i
								break
						col = temp_col
						board.selection(row, col)
					elif(event.key == pygame.K_LEFT):
						temp_col = col
						for i in range(col-1, -1, -1):
							if(board.cell_list[row][i].changeable):
								temp_col = i
								break
						col = temp_col
						board.selection(row, col)

					# conditions for numbers
					key = None
					if event.key in [pygame.K_1, pygame.K_KP1]:
						key = 1
					elif event.key in [pygame.K_2, pygame.K_KP2]:
						key = 2
					elif event.key in [pygame.K_3, pygame.K_KP3]:
						key = 3
					elif event.key in [pygame.K_4, pygame.K_KP4]:
						key = 4
					elif event.key in [pygame.K_5, pygame.K_KP5]:
						key = 5
					elif event.key in [pygame.K_6, pygame.K_KP6]:
						key = 6
					elif event.key in [pygame.K_7, pygame.K_KP7]:
						key = 7
					elif event.key in [pygame.K_8, pygame.K_KP8]:
						key = 8
					elif event.key in [pygame.K_9, pygame.K_KP9]:
						key = 9
					#offers delete feature    
					elif event.key in [pygame.K_DELETE, pygame.K_BACKSPACE, pygame.K_0, pygame.K_KP0] : 
						key = 0

					#if some box has been selected prior to hitting key
					if board.selected != None and key!=None :
						if board.cell_list[board.selected[0]][board.selected[1]].changeable:
							if(rough==False):
								board.cell_list[row][col].val = key
								board.vals[row][col] = key
								for i in range(1,10):
										board.cell_list[row][col].rough_vals[i] = False
							else:
								board.cell_list[row][col].val = 0
								board.vals[row][col] = 0
								if(key==0): #removing all the rough_vals
									for i in range(1,10):
										board.cell_list[row][col].rough_vals[i] = False	
								else: #toggling rough val
									board.cell_list[row][col].rough_vals[key] = not(board.cell_list[row][col].rough_vals[key])
							board.draw_board(win)
					
					
				#check if the puzzle is completed 
				if(funcs.empty_left(board.vals)==0):
					result = check(board)
					if result :
						text = "Solved in %s" % (format_time(timer))
						color = (0,255,0)
						win.fill((255,255,255))
						fnt = pygame.font.SysFont("comicsans", 50)
						txt = fnt.render(text, True, color)
						win.blit(txt, (130, 300))
						win.blit(re, (200, 400))
						pygame.display.update()
						while True :
							for event in pygame.event.get() :
								if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
									pygame.quit()
									sys.exit()
								elif event.type == MOUSEBUTTONDOWN : # click on re button
									x, y = pygame.mouse.get_pos()
									if x > 200 and x < 264 and y > 400 and y < 464 :
										return
				pygame.display.update()
			 
				
	
	
