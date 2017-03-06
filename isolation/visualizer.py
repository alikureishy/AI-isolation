'''
Created on Mar 4, 2017

@author: safdar

Example program to show using an array to back a grid on-screen.
    http://programarcadegames.com/python_examples/f.php?file=pygame_base_template.py
'''

from time import sleep
import pygame
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128,128,128)
BLUE = (0,0,255)
BROWN = (165,42,42)
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 60
HEIGHT = 60
 
# This sets the margin between each cell
MARGIN = 10

# Players:
O = 0
X = 1

# Cell states:
EMPTY = (WHITE, None)
O_HERE = (BLUE, O)
X_HERE = (BROWN, X)
O_VISITED = (GRAY, O)
X_VISITED = (GRAY, X)
VISITED = (GRAY, None)
O_WIN = (GREEN, O)
X_WIN = (GREEN, X)
O_LOSE = (RED, O)
X_LOSE = (RED, X)

# Cell colors
BLANK = WHITE
VISITED = GRAY
WINNER = GREEN
LOSER = RED

class Visualizer(object):
    pass

    def __init__(self, O_name, X_name, moves):
        # Create a 2 dimensional array. A two dimensional
        # array is simply a list of lists.
        self.cols = 7
        self.rows = 7
        self.grid = []
        for row in range(self.rows):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(self.cols):
                self.grid[row].append(EMPTY)  # Append a cell
         
        # Save the moves of the game
        self.moves = sum(moves, [])
        
        # Set row 1, cell 5 to one. (Remember rows and
        # column numbers start at zero.)
        o_initial = self.moves[0]
        self.grid[o_initial[0]][o_initial[1]] = O_HERE
        x_initial = self.moves[1]
        self.grid[x_initial[0]][x_initial[1]] = X_HERE

        # Initialize pygame
        pygame.init()
        
        # Set the HEIGHT and WIDTH of the screen
        WINDOW_SIZE = [self.rows*WIDTH + (self.rows+1)*MARGIN, self.cols*WIDTH + (self.cols+1)*MARGIN]
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
         
        # Set title of screen
        pygame.display.set_caption("O = {}, X = {}".format(O_name, X_name))
        self.__redraw__()
         
        # Loop until the user clicks the close button.
        self.done = False
         
        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()
     
    # -------- Main Program Loop -----------

    def __redraw__(self):
        # Set the screen background
        self.screen.fill(BLACK)
         
        # Draw the grid
        for row in range(self.rows):
            for column in range(self.cols):
                color, player = self.grid[row][column][0], self.grid[row][column][1]
                if player == O:
                    pygame.draw.rect(self.screen, WHITE, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
                    pygame.draw.circle(self.screen, color, [(MARGIN + WIDTH) * column + MARGIN + WIDTH//2, (MARGIN + HEIGHT) * row + MARGIN + HEIGHT//2], WIDTH//2)
                elif player == X:
                    pygame.draw.rect(self.screen, WHITE, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
                    pygame.draw.line(self.screen, color, \
                                    [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN], \
                                    [(MARGIN + WIDTH) * (column+1), (MARGIN + HEIGHT) * (row+1)], \
                                    5)
                    pygame.draw.line(self.screen, color, \
                                    [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * (row+1)], \
                                    [(MARGIN + WIDTH) * (column+1), (MARGIN + HEIGHT) * row + MARGIN], \
                                    5)
                else:
                    pygame.draw.rect(self.screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
                    
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    def play(self):
        idx = 2
        while not self.done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True  # Flag that we are done so we exit this loop
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if idx >= len(self.moves):
                        self.clock.tick(300)
                        continue
                    nextmove = self.moves[idx]
                    nextplayer = X if idx % 2 == 1 else O
                    if nextmove == (-1,-1):
                        nextmove = self.moves[idx-2]
                        self.grid[nextmove[0]][nextmove[1]] = X_LOSE if nextplayer == X else O_LOSE
                        self.__redraw__()
                        sleep(3)
                        othermove = self.moves[idx-1]
                        self.grid[othermove[0]][othermove[1]] = O_WIN if nextplayer == X else X_WIN
                        self.__redraw__()
                    else:
                        self.grid[nextmove[0]][nextmove[1]] = X_HERE if nextplayer == X else O_HERE
                        lastmove = self.moves[idx-2]
#                         self.grid[lastmove[0]][lastmove[1]] = X_VISITED if nextplayer == X else O_VISITED
                        self.grid[lastmove[0]][lastmove[1]] = VISITED
                        self.__redraw__()
                    idx+=1
         
            # Limit to 60 frames per second
            self.clock.tick(60)
         
    def quit(self):
        # Be IDLE friendly. If you forget this line, the program will 'hang'
        # on exit.
        pygame.quit()
        
