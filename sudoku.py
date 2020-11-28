# Name: James Leflang
# CS 325: Analysis of Algorithms
# Portfolio Project
# (C) 2020 James Leflang - MIT License
import pygame
import copy

# Used the following link to do the GUI since I am 100% unfamiliar to PyGame
# https://geeksforgeeks.org/building-and-visualizing-sudoku-game-using-pygame/
# Puzzle generated here: https://qqwing.com/generate.html
# Some of the code mirrors this:
#  https://github.com/wyfok/Solve_Sudoku_with_Crook_algorithm
# 

# initialise the pygame font 
pygame.font.init() 

screen = pygame.display.set_mode((500, 600))  
pygame.display.set_caption("SUDOKU GAME") 
  
x = 0
y = 0
dif = 500 / 9
val = 0
# Default Sudoku Board. 
grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0] 
    ] 

# Load test fonts for future use 
font1 = pygame.font.SysFont("comicsans", 40) 
font2 = pygame.font.SysFont("comicsans", 20)


def get_cord(idx):
    global x 
    x = idx[0]//dif
    global y 
    y = idx[1]//dif


# Loads a puzzle from file
# If you want to replace the file provided, generate one on QQWing with
# The "Compact" setting to be in the correct format
def load_puzzle():
    try:
        with open('puzzle.txt', 'r') as puzzle:
            rows = puzzle.readlines()
            for i, row in enumerate(rows):
                for j, cell in enumerate(row.strip()):
                    if cell != '.':
                        grid[j][i] = int(cell)

    except IOError:
        text1 = font1.render("NO FILE FOUND", True, (0, 0, 0))
        screen.blit(text1, (20, 570))

  
# Highlight the cell selected 
def draw_box(): 
    for i in range(2): 
        pygame.draw.line(screen, (255, 0, 0), (x * dif-3, (y + i) * dif), (x * dif + dif + 3, (y + i)*dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ((x + i) * dif, y * dif), ((x + i) * dif, y * dif + dif), 7)


# Function to draw required lines for making Sudoku grid          
def draw(): 
    # Draw the lines     
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
  
                # Fill blue color in already numbered grid 
                pygame.draw.rect(screen, (0, 153, 153), pygame.Rect(i * dif, j * dif, dif + 1, dif + 1))
  
                # Fill gird with default numbers specified 
                text1 = font1.render(str(grid[i][j]), True, (0, 0, 0))
                screen.blit(text1, (i * dif + 15, j * dif + 15))

    # Draw lines horizontally and vertically to form grid
    for i in range(10): 
        if i % 3 == 0:
            thick = 7
        else: 
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick) 
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)       


# Fill value entered in cell       
def draw_val(cell):
    text1 = font1.render(str(cell), True, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif + 15))     


# Raise error when wrong value entered 
def raise_error1(): 
    text1 = font1.render("WRONG !!!", True, (0, 0, 0))
    screen.blit(text1, (20, 570))


def raise_error2(): 
    text1 = font1.render("Wrong !!! Not a valid Key", True, (0, 0, 0))
    screen.blit(text1, (20, 570))   


# Check if the value entered in board is valid 
def valid(m, i, j, cell):
    for it in range(9): 
        if m[i][it] == cell:
            return False
        if m[it][j] == cell:
            return False

    it = i//3
    jt = j//3
    for i in range(it * 3, it * 3 + 3): 
        for j in range(jt * 3, jt * 3 + 3):
            if m[i][j] == cell:
                return False

    return True


# Get rid of forced cells
def forced_cells(sol: dict):
    for k, v in sol.items():
        if len(v) == 1:
            # Fill the cell
            cell = v.pop()
            grid[k[0]][k[1]] = cell
            global x, y
            x = k[0]
            y = k[1]

            # white color background\
            screen.fill((255, 255, 255))
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(20)

            # Remove value from the any in box/row/col
            for i in range(9):
                try:
                    sol[k[0], i].remove(cell)
                except ValueError:
                    continue

            for i in range(9):
                try:
                    sol[i, k[1]].remove(cell)
                except ValueError:
                    continue

            it = k[0]//3
            jt = k[1]//3
            for i in range(it * 3, it * 3 + 3):
                for j in range(jt * 3, jt * 3 + 3):
                    try:
                        sol[i, j].remove(val)
                    except ValueError:
                        continue

        else:
            continue


# Remove all the impossible values from the solution
def remove_impossibles(sol, cur_possibles):
    # Get the range of possible values
    try:
        min_pos = min((len(v)) for _, v in cur_possibles.items())
        max_pos = max((len(v)) for _, v in cur_possibles.items())
    except ValueError:
        return

    # For each value in that range
    for i in reversed(range(min_pos, max_pos + 1)):

        for k, v in {k: v for k, v in cur_possibles.items() if len(v) == i}.items():

            subset_size = 0
            matched = set()

            for k_1, v_1 in cur_possibles.items():
                if len(v) < len(v_1):
                    continue
                else:
                    if set(v_1).issubset(set(v)):
                        matched.add(k_1)
                        subset_size += 1

                if subset_size == len(v):
                    for k_2, v_2 in {k: v for k, v in cur_possibles.items() if k not in matched}.items():
                        cur_possibles[k_2] = [t for t in v_2 if t not in v]
                        while True:
                            old = copy.deepcopy(sol)
                            forced_cells(sol)
                            if old == sol:
                                break


# Goes through a column
def col_fill(sol: dict):
    for i in range(9):
        possibles = {k: v for k, v in sol.items() if k[0] == i and len(v) > 0}
        remove_impossibles(sol, possibles)


# Goes through a row
def row_fill(sol: dict):
    for i in range(9):
        possibles = {k: v for k, v in sol.items() if k[1] == i and len(v) > 0}
        remove_impossibles(sol, possibles)


# Goes through a box
def box_fill(sol: dict):
    for i in range(3):
        possible = {k: v for k, v in sol.items() if k[0] in
                    [g for g in range(i * 3, i * 3 + 3)] and k[1] in
                    [z for z in range(i * 3, i * 3 + 3)] and len(v) > 0}
        remove_impossibles(sol, possible)


# Crook's algorithm
def crooks(sol):
    row_fill(sol)
    col_fill(sol)
    box_fill(sol)


# Solves the sudoku board using J. F. Crook's Pencil-and-Paper Algorithm
# http://www.ams.org/notices/200904/tx090400460p.pdf
def solve(board):
    sol = {}

    pygame.event.pump()

    # Make the solution scratchpad and Mark up every cell
    for i in range(9):
        for j in range(9):
            sol[i, j] = list()
            if board[i][j] == 0:
                for it in range(1, 10):
                    if valid(board, i, j, it):
                        sol[i, j].append(it)
                    else:
                        continue
            else:
                continue

    # Go through and rid of uniques (forced cells)
    forced_cells(sol)

    # Run the algorithm until we can't (no change)
    while True:
        old = copy.deepcopy(sol)
        crooks(sol)
        if old == sol:
            break

    del old

    # Check for completeness
    # If the puzzle was not solved, return false
    for j, row in enumerate(board):
        for i, cell in enumerate(row):
            if not valid(board, i, j, cell):
                return False

    return True


# Display instruction for the game 
def instruction(): 
    text1 = font2.render("PRESS D TO RESET TO DEFAULT / R TO EMPTY", True, (0, 0, 0))
    text2 = font2.render("ENTER VALUES AND PRESS ENTER TO VISUALIZE", True, (0, 0, 0))
    screen.blit(text1, (20, 520))         
    screen.blit(text2, (20, 540)) 


# Display options when solved 
def result(): 
    text1 = font1.render("FINISHED PRESS R or D", True, (0, 0, 0))
    screen.blit(text1, (20, 570))


# FLAGS
run = True
flag1 = 0
flag2 = 0
rs = 0
error = 0

# GAME ACTIVE LOOP
while run: 
      
    # White color background 
    screen.fill((255, 255, 255))

    # Load the puzzle file
    load_puzzle()

    # Loop through the events stored in event.get() 
    for event in pygame.event.get(): 
        # Quit the game window 
        if event.type == pygame.QUIT: 
            run = False  
        # Get the mouse position to insert number
        if event.type == pygame.MOUSEBUTTONDOWN: 
            flag1 = 1
            pos = pygame.mouse.get_pos() 
            get_cord(pos) 
        # Get the number to be inserted if key pressed     
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT: 
                x -= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT: 
                x += 1
                flag1 = 1
            if event.key == pygame.K_UP: 
                y -= 1
                flag1 = 1
            if event.key == pygame.K_DOWN: 
                y += 1
                flag1 = 1    
            if event.key == pygame.K_1: 
                val = 1
            if event.key == pygame.K_2: 
                val = 2    
            if event.key == pygame.K_3: 
                val = 3
            if event.key == pygame.K_4: 
                val = 4
            if event.key == pygame.K_5: 
                val = 5
            if event.key == pygame.K_6: 
                val = 6 
            if event.key == pygame.K_7: 
                val = 7
            if event.key == pygame.K_8: 
                val = 8
            if event.key == pygame.K_9: 
                val = 9  
            if event.key == pygame.K_RETURN: 
                flag2 = 1   
            # If R pressed, clear the sudoku board 
            if event.key == pygame.K_r: 
                rs = 0
                error = 0
                flag2 = 0
                grid = [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]
                ] 
            # If D is pressed, reset the board  
            if event.key == pygame.K_d: 
                rs = 0
                error = 0
                flag2 = 0
                load_puzzle() 

    if flag2 == 1: 
        if solve(grid):
            error = 1
        else: 
            rs = 1
        flag2 = 0    
    if val != 0:             
        draw_val(val) 
        # print(x) 
        # print(y) 
        if valid(grid, int(x), int(y), val):
            grid[int(x)][int(y)] = val
            flag1 = 0
        else: 
            grid[int(x)][int(y)] = 0
            raise_error2()    
        val = 0    
        
    if error == 1: 
        raise_error1() 

    if rs == 1: 
        result() 

    draw()

    if flag1 == 1: 
        draw_box()

    instruction()     
  
    # Update window 
    pygame.display.update()   
  
# Quit pygame window     
pygame.quit()
