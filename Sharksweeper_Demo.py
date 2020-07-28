# 07/28/2020 note: This is a demo of shark sweeper game(mouse click) based on mine sweeper, which we have to avoid 4 sharks
# and find the treasure(our last click must be treasure). We will also have a pearl that can shine around the box in 4 sides:
# top, down, right, left. If the pearl reveal the shark, the mine won't be triggered because the shark will be gone.

# This program(pygame) mainly use arraylist to store information as information, which 0 as unrevealed box, 1 as revealed,
# -1 as mine, and 9 as pearl. Just like mine sweeper, the revealed boxes will show up the number of mines around it,
# and we can also raise on flag on suspected location of mines by pressing left/ right key on keyboard and click on the box.
# To unflag it, press up/down key on keyboard and click on the box.

# Import the pygame& random& numpy library
import pygame
import random
import numpy as np

# Define colors
BLACK = (0, 0, 0)
GRAY = (128,128,128)
WHITE = (255, 255, 255)
flag = (255,0,0) # Red as flags
mine = (0,0,255) # Blue as mines/sharks
pearl = (255,255,0) # Yellow as pearl
treasure = (0,128,0) # Green as treasure

# Create a 2d array to store info: 0 = unrevealed, -1 = bomb, 1 = revealed, 9 = pearl
grid = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

# Set the entire array as unrevealed
def clear_board():
    for row in range(4):
        for col in range(4):
            grid[row][col] = 0 

# Assign the location of sharks and pearl randomly
def set_mines_pearls():
    clear_board() # This makes sure there are no mines before setting just in case we have to reset it
    for produce_mine in range(4): # 4 sharks are hiding at different location in the grid randomly
        r = random.randint(0,3)
        c = random.randint(0,3) 
        while(grid[r][c] == -1):
            r = random.randint(0,3)
            c = random.randint(0,3)
        grid[r][c] = -1
        print("row", r, " , col", c)

    r = random.randint(0,3) # Do the same thing for our pearl
    c = random.randint(0,3) 
    while(grid[r][c] == -1):
        r = random.randint(0,3)
        c = random.randint(0,3)
    grid[r][c] = 9
    print("pearl: row", r, " , col", c)
    print(grid)

def draw_Background():
    for i in range(4):
        pygame.draw.line(screen, BLACK, [100 * i,0], [100* i, 400])
        pygame.draw.line(screen, BLACK, [0,100 * i], [400, 100* i])    

# Display number of mines around the clicked box on screen
def show_count(num, r, c):
    font = pygame.font.SysFont("comicsansms", 150)
    number = str(num) # We have to convert int to string before display
    number = font.render(number, True, (255,255,0), BLACK) # font color is yellow
    location = (c*100, r*100)
    screen.blit(number,location) # blit(TextSurf, TextRect)

# Count the number of mines around the clicked box by loop and check through 8 boxes around it: from [r-1][c-1] to [r+1][c+1]
def count_mines_around(r, c):
    count = 0
    for i in range(-1, 2): # [-1,2) -1 to 1 inclusive, it means 1 row before and 1 row after the selected row
        for j in range(-1, 2):
            x_pos = r + i
            y_pos = c + j
            if x_pos > -1 and y_pos > -1 and x_pos < len(grid) and y_pos < len(grid[i]):
                if grid[x_pos][y_pos] == -1:
                    count += 1
    return count

# Loop through from [r-1][c-1] to [r+1][c+1], but reveal boxes that are only at the same row / col as the clicked location
# Won't lose if it reveals sharks.
def reveal_around(r,c):
    for i in range(-1, 2): # [-1,2) -1 to 1 inclusive, it means 1 row before and 1 row after the selected row
        for j in range(-1, 2):
            x_pos = r + i
            y_pos = c + j
            if x_pos > -1 and y_pos > -1 and x_pos < len(grid) and y_pos < len(grid[i]):        
                if i == 0 or j == 0: # same row/col
                    if grid[x_pos][y_pos] == -1: # there is a bomb here
                        reveal_image(mine, x_pos, y_pos)
                    elif grid[x_pos][y_pos] == 0 or grid[x_pos][y_pos] == 1:
                        reveal_space(x_pos,y_pos)
                    else:
                        reveal_image(pearl, x_pos, y_pos)
                

# We will raise a flag on the suspected bomb *supposed to be an image of a flag*
def raise_flag(r,c):
    reveal_image(flag,r,c)

# Turn down the flag
def unflag(r,c):
    pygame.draw.rect(screen,GRAY,[(100 * c) +1, (100 * r)+1, 99, 99])  

# Reveal an image at the clicked position, but at this point we act like the color is our image
def reveal_image(img,r,c):
    pygame.draw.rect(screen,img, [(100 * c) +1, (100 * r)+1, 99, 99])
'''# Case if it's an image
    while True:
        location = (100 * c) +1, (100 * r) +1
        img = pygame.transform.scale (img, (99, 99)
        screen.blit(img, location)
        pygame.display.flip()'''

# When we clicked on a bomb, it will loop through to find all -1 in array and reveal all sharks on the board
# *supposed to be an image of a shark*
def reveal_bomb():
    for row in range(4):
        for column in range(4):
            if grid[row][column] == -1 :
                reveal_image(mine,row,column)

# When we clicked on neither mine nor pearl, it will show a blank spot and set value of its location the array as 1
def reveal_space(r,c):
    grid[r][c] = 1
    pygame.draw.rect(screen,WHITE,[(100 * c) +1, (100 * r)+1, 99, 99]) 
    num_mines = count_mines_around(r, c)
    show_count(num_mines, r, c)      

# Initialize pygame
pygame.init()
# Open a new window
size = (400, 400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Shark sweeper demox")

# The program will keep running until the user exit the game
run = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# First, clear the screen to gray.
screen.fill(GRAY) 
draw_Background()
set_mines_pearls()
lose = False
win = False
# -------- Main Program Loop -----------
while run:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            run = False # Flag that we are done so we exit this loop
        elif not win and not lose and event.type == pygame.MOUSEBUTTONDOWN: # Else if user clicks the mouse
            x,y = pygame.mouse.get_pos() # Get the position of clicked location in (x,y)
            column = x // 100 # 0 - 3
            row = y // 100
            print(x, " " , y, " ", row, " ", column)
            count_revealed = len(grid[grid == 1])
            keys = pygame.key.get_pressed()
            editMode = False
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]: # when you press left key/ right key, the computer will enter the edit mode
                editMode = True
                raise_flag(row,column) # when you click on a box, nothing will show up and won't trigger anything even it's a mine
            if keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                editMode = True
                unflag(row, column) # take back the flag
            if editMode == False:   
                if grid[row][column] == -1: # if we click on mine...
                    if count_revealed == 0: # 11 spots are unrevealed
                        set_mines_pearls()
                        reveal_space(row, column)
                    else:
                        reveal_bomb() # case2: not first click
                        print("You lose!")
                        lose = True
                elif grid[row][column] == 9:
                    reveal_image(pearl, row, column)
                    if count_revealed < 11: # not last one
                        reveal_around(row,column)
                    grid[row][column] = 1
                else:
                    reveal_space(row,column)
                    #num_mines = count_mines_around(row, column)
                    #show_count(num_mines, row, column)
                if count_revealed == 11: # because array is from 0-11
                    reveal_image(treasure,row,column)
                    print("You win!")
                    win = True
                print(grid)
                print(grid[grid == 1])
                print(count_revealed)
    

 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)
 
#Once we have exited the main program loop we can stop the game engine:
pygame.quit()
