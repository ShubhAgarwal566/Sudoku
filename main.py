import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, sys
from pygame.locals import *
import play

pygame.init()

width = 540
height = 600

if __name__ == "__main__" :
	win = pygame.display.set_mode((width, height))
	win.fill((255, 255, 255))

	pygame.display.set_caption("Sudoku-Game")

	while True: # main game loop
		#drawing the play button
		term_x = [width//2-100, width//2+100]
		term_y = [300, 350]
		for i in range(2) :
			pygame.draw.line(win, (128, 128, 128), (term_x[0], term_y[i]), (term_x[1], term_y[i]))
		for i in range(2) :
			pygame.draw.line(win, (128, 128, 128), (term_x[i], 300), (term_x[i], 350))
				
		fnt = pygame.font.SysFont("comicsans", 40) 
		FNT = pygame.font.SysFont("comicsans", 60)   
	   
		#render title
		win.blit(FNT.render("SUDOKU", 1, (0, 128, 0)), (width//2-90, 100))
		win.blit(fnt.render("PLAY", 0, (128, 128, 128)), (width//2-35,310)) 
		
		for event in pygame.event.get():
			#quit game if user clicks the cross
			if(event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE)):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN :
				x, y = pygame.mouse.get_pos()
				if(x>width//2-100 and x<width//2+100 and y>300 and y<350):
					play.PLAY(win)
					win.fill((255, 255, 255))
					
				
		pygame.display.update()
		
