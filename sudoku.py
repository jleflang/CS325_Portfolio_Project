# Name: James Leflang
# CS 325: Analysis of Algorithms
# Portfolio Project
# (C) 2020 James Leflang - MIT License
import pygame
import copy

# Used the following link to do the GUI since I am 100% unfamiliar to PyGame
# https://geeksforgeeks.org/building-and-visualizing-sudoku-game-using-pygame/
# Puzzle generated here: https://qqwing.com/generate.html
# Some of the code mirrors/replicates this 
# (modifications are needed to match application):
#  https://github.com/wyfok/Solve_Sudoku_with_Crook_algorithm
# 
# The verify_board() method is the primary graded objective for this assignment.
#

# Initialise the pygame font 
pygame.font.init() 
# Configure the window
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


def get_cord(idx: list):
    """Gets the cell location.
    Args:
        idx (list): cell coordinates
    """
    global x 
    x = idx[0]//dif
    global y 
    y = idx[1]//dif


# Loads a puzzle from file
# If you want to replace the file provided, generate one on QQWing with
# The "Compact" setting to be in the correct format
def load_puzzle():
    """Loads a puzzle from file."""
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
    """Highlights a cell.""" 
    for i in range(2): 
        pygame.draw.line(screen, (255, 0, 0), (x * dif-3, (y + i) * dif),
                         (x * dif + dif + 3, (y + i)*dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ((x + i) * dif, y * dif),
                         ((x + i) * dif, y * dif + dif), 7)


# Function to draw required lines for making Sudoku grid          
def draw():
    """Draws the Sudoku board."""      
    for i in range(9):
        for j in range(9):
            # If the cell is not empty
            if grid[i][j] != 0:
  
                # Fill blue color in already numbered grid 
                pygame.draw.rect(screen, (0, 153, 153),
                                 pygame.Rect(i * dif, 
                                 j * dif, dif + 1, dif + 1))
  
                # Fill grid with default numbers specified
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
def draw_val(cell: int):
    """Draws the cell's value.
    Args:
        cell (int): Value to draw
    """
    text1 = font1.render(str(cell), True, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif + 15))     


# Raise error when wrong value entered 
def error_puzzle_incomplete():
    """Error: Puzzle state is Incomplete.""" 
    text1 = font1.render("WRONG !!!", True, (0, 0, 0))
    screen.blit(text1, (20, 570))


# Raise error when wrong key is pressed
def error_unk_key():
    """Error: Key not recognized.""" 
    text1 = font1.render("Wrong !!! Not a valid Key", True, (0, 0, 0))
    screen.blit(text1, (20, 570))   


# Check if the value entered in board is valid 
def valid(m: list, i: int, j: int, cell: int) -> bool:
    """Determine if a value is valid for a cell.
    Args:
        m (list): The board
        i (int): Column number
        j (int): Row number
        cell: Value to verify
    Returns:
        bool: True if valid, else False
    """
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


# This is the core verification method. This method takes a solved board and 
# determines if the solution is valid.
def verify_board(board: list) -> bool:
    """Verifies the board in O(n^2) time complexity.
    Args:
        board (list): Current puzzle
    Returns:
        bool: True if valid, else false
    """
    
    # Row/Column verification
    for i in range(9):
        row = [cell for cell in [board[col][i] for col in range(9)]]
        col = board[i]
        # Unique values must be there!
        for val in range(1, 10):
            if row.count(val) != 1:
                return False
            if col.count(val) != 1:
                return False

    # Box verification
    for i in range(3):
        for j in range(3):
            box = list([board[col][row] for col in range(j * 3, j * 3 + 3)
                            for row in range(i * 3, i * 3 + 3)])

            for val in range(1, 10):
                if box.count(val) != 1:
                    return False

    return True



# This method is a direct copy of lines 218-242 in
# https://github.com/wyfok/Solve_Sudoku_with_Crook_algorithm/blob/master/function.py
def do_box(sol: dict):
    """Checks a box for the possible values.
    Args:
        sol (dict): The solutions scratchpad
    """
    # For the range of boxes
    for i in range(3):
        for j in range(3):
            # Get a set of the possible values for each cell relative to 
            # each box they are in
            possible = set([k for b in [value for key, value in sol.items() if
                                        key[1] in range(i * 3, i * 3 + 3) and
                                        key[0] in range(j * 3, j * 3 + 3) and
                                        len(value) > 0]
                            for k in b])

            # For each of those cells
            for cell in possible:
                # Get a list of possible values
                avail = [key for key, value in sol.items() if x in value if
                         key[1] in range(i * 3, i * 3 + 3) and
                         key[0] in range(j * 3, j * 3 + 3)]

                # Set those values when they are actually available 
                # relative to the box
                if len(set([cell[0] for cell in avail])) == 1:
                    for key in [key for key, value in sol.items()
                                if key[0] == avail[0][0] and key not in avail]:
                        sol[key] = [possi for possi in 
                                    sol[key] if possi != cell]
                if len(set([cell[1] for cell in avail])) == 1:
                    for key in [key for key, value in sol.items()
                                if key[1] == avail[0][1] and key not in avail]:
                        sol[key] = [possi for possi in 
                                    sol[key] if possi != cell]


# Remove all the impossible values from the solution
def remove_impossibles(sol: dict, cur_possibles: dict, board: list):
    """Core part of Crook's Algorithm.
    Args:
        sol (dict): The solution scratchpad
        cur_possibles (dict): Values to attempt to fill
        board (list): Current board
    """
    # Get the range of possible values
    try:
        min_pos = min((len(v)) for _, v in cur_possibles.items())
        max_pos = max((len(v)) for _, v in cur_possibles.items())
    except ValueError:
        return

    # For each value in that range
    for i in reversed(range(min_pos, max_pos + 1)):
        # For each cell that matches that range
        for k, v in {k: v for k, v in cur_possibles.items() if 
                     len(v) == i}.items():

            subset_size = 0
            matched = set()

            # Create the necessary subsets
            for k_1, v_1 in cur_possibles.items():
                if len(v) < len(v_1):
                    continue
                else:
                    if set(v_1).issubset(set(v)):
                        matched.add(k_1)
                        subset_size += 1

                # When the subset is the same size of the possible values
                if subset_size == len(v):
                    for k_2, v_2 in {k: v for k, v in cur_possibles.items()
                                     if k not in matched}.items():
                        cur_possibles[k_2] = [t for t in v_2 if t not in v]
                        do_check_render(sol, board)


# Goes through a column
def col_fill(sol: dict, board: list):
    """Perform Crook's on the columns.
    Args:
        sol (dict): The solution scratchpad
        board (list): Current board
    """
    for i in range(9):
        possibles = {k: v for k, v in sol.items() if k[0] == i and len(v) > 0}
        remove_impossibles(sol, possibles, board)


# Goes through a row
def row_fill(sol: dict, board: list):
    """Perform Crook's on the rows.
    Args:
        sol (dict): The solution scratchpad
        board (list): Current board
    """
    for i in range(9):
        possibles = {k: v for k, v in sol.items() if k[1] == i and len(v) > 0}
        remove_impossibles(sol, possibles, board)


# Goes through a box
def box_fill(sol: dict, board: list):
    """Perform Crook's on the boxes.
    Args:
        sol (dict): The solution scratchpad
        board (list): Current board
    """
    for i in range(3):
        possible = {k: v for k, v in sol.items() if k[0] in
                    [g for g in range(i * 3, i * 3 + 3)] and k[1] in
                    [z for z in range(i * 3, i * 3 + 3)] and len(v) > 0}
        remove_impossibles(sol, possible, board)


# Crook's algorithm
def crooks(sol: dict, board: list):
    """Top level Crook's.
    Args:
        sol (dict): The solution scratchpad
        board (list): Current board
    """
    while True:
        old = copy.deepcopy(board)
        row_fill(sol, board)
        col_fill(sol, board)
        box_fill(sol, board)
        if old == board:
            break


# Examine a column and fill uniques
def column_examine(sol: dict, board: list):
    """Perform basic check & fill on the column.
    Args:
        sol (dict): The solution scratchpad
        board (list): Current board
    """
    for i in range(9):
        # Get the column
        existent = board[i]

        # Update the possibilities
        for j in range(9):
            sol[j, i] = [k for k in sol[j, i] if k not in existent]

        pos_cell = [k for q in [value for key, value in sol.items() if 
                                key[1] == i and len(value) > 0] for k in q]
        uniques = [k for k in pos_cell if pos_cell.count(k) == 1]
        if len(uniques) > 0:
            for k in uniques:
                for key, value in {key: value for key, value in sol.items() if
                                   key[1] == i and len(value) > 0}.items():
                    if k in value:
                        sol[key].clear()
                        board[key[1]][key[0]] = k
                        global x, y
                        x = key[1]
                        y = key[0]

                        # white color background\
                        screen.fill((255, 255, 255))
                        draw()
                        draw_box()
                        pygame.display.update()
                        pygame.time.delay(20)


# Examine a row and fill uniques
def row_examine(sol: dict, board: list):
    """Perform basic check & fill on the row.
    Args:
        sol (dict): The solution scratchpad
        board (list): Current board
    """
    for i in range(9):
        existent = [cell for cell in [board[col][i] for col in range(9)]]

        for j in range(9):
            sol[i, j] = [k for k in sol[i, j] if k not in existent]

        pos_cell = [k for q in [value for key, value in sol.items() if 
                                key[0] == i and len(value) > 0] for k in q]
        uniques = [k for k in pos_cell if pos_cell.count(k) == 1]
        if len(uniques) > 0:
            for k in uniques:
                for key, value in {key: value for key, value in sol.items() if
                                   key[0] == i and len(value) > 0}.items():
                    if k in value:
                        sol[key].clear()
                        board[key[1]][key[0]] = k
                        global x, y
                        x = key[1]
                        y = key[0]

                        # white color background\
                        screen.fill((255, 255, 255))
                        draw()
                        draw_box()
                        pygame.display.update()
                        pygame.time.delay(20)


# Examine a box and fill uniques
def box_examine(sol: dict, board: list):
    """Perform basic check & fill on the box.
    Args:
        sol (dict): The solution scratchpad
        board (list): Current board
    """
    for i in range(3):
        for j in range(3):
            existent = set([board[col][row] for col in range(j * 3, j * 3 + 3)
                            for row in range(i * 3, i * 3 + 3)])

            for q in range(j * 3, j * 3 + 3):
                for r in range(i * 3, i * 3 + 3):
                    sol[r, q] = [k for k in sol[r, q] if k not in existent]

            pos_cell = [k for q in [value for key, value in sol.items() if
                                    key[1] in range(j * 3, j * 3 + 3) and
                                    key[0] in range(i * 3, i * 3 + 3) and
                                    len(value) > 0] for k in q]
            uniques = [k for k in pos_cell if pos_cell.count(k) == 1]
            if len(uniques) > 0:
                for k in uniques:
                    box = {key: value for key, value in sol.items() if
                           key[1] in range(j * 3, j * 3 + 3) and
                           key[0] in range(i * 3, i * 3 + 3) and
                           len(value) > 0}
                    for key, value in box.items():
                        if k in value:
                            sol[key].clear()
                            board[key[1]][key[0]] = k
                            global x, y
                            x = key[1]
                            y = key[0]

                            # white color background\
                            screen.fill((255, 255, 255))
                            draw()
                            draw_box()
                            pygame.display.update()
                            pygame.time.delay(20)


# Examine any uniques and fill them
def unique_examine(sol: dict, board: list):
    """Perform basic check & fill for unique values.
    Args:
        sol (dict): The solution scratchpad
        board (list): Current board
    """
    for k, v in sol.items():
        if len(v) == 1:
            value = v[0]
            v.clear()
            board[k[1]][k[0]] = value
            global x, y
            x = k[1]
            y = k[0]

            # white color background\
            screen.fill((255, 255, 255))
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(20)


def do_check_render(sol: dict, board: list):
    """Top level basic check & fill.
    Args:
        sol (dict): The solution scratchpad
        board (list): Current board
    """
    while True:
        old = copy.deepcopy(board)
        column_examine(sol, board)
        row_examine(sol, board)
        box_examine(sol, board)
        unique_examine(sol, board)
        if old == board:
            break


# Solves the sudoku board using J. F. Crook's Pencil-and-Paper Algorithm
# http://www.ams.org/notices/200904/tx090400460p.pdf
def solve(board: list) -> bool:
    """Solve a puzzle with Crook's Algorithm.
    Args:
        board (list): Current Board
    Returns:
        bool: True if solved, else False
    """
    sol = {}

    pygame.event.pump()

    # Make the solution scratchpad
    for i in range(9):
        for j in range(9):
            sol[i, j] = list(range(1, 10))
            if board[i][j] != 0:
                sol[i, j] = []

    # Run the algorithm until we can't (no change)
    while True:
        old = copy.deepcopy(board)
        # Basic check and render
        do_check_render(sol, board)
        # Perform Crook's
        crooks(sol, board)
        # Deal with boxes
        do_box(sol)
        if old == board:
            break

    del old

    # Check for completeness
    # If the puzzle was not solved, return false
    return verify_board(board)


# Display instruction for the game 
def instruction():
    """Draw instructions.""" 
    text1 = font2.render(
                         "PRESS D TO RESET / R TO EMPTY / E TO VERIFY", 
                         True, (0, 0, 0))
    text2 = font2.render("ENTER VALUES AND PRESS ENTER TO SOLVE", 
                         True, (0, 0, 0))
    screen.blit(text1, (20, 520))         
    screen.blit(text2, (20, 540)) 


# Display options when solved 
def result():
    """Draw ending message.""" 
    text1 = font1.render("FINISHED PRESS R or D", True, (0, 0, 0))
    screen.blit(text1, (20, 570))


# FLAGS
# Run
run = True
# Render event
render_event = False
# Solve Event
solve_puz = False
# Result
is_solved = False
# Error
error = False
# Verification
verific = False

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
            render_event = True
            pos = pygame.mouse.get_pos() 
            get_cord(pos) 
        # Get the number to be inserted if key pressed     
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT: 
                x -= 1
                render_event = True
            if event.key == pygame.K_RIGHT: 
                x += 1
                render_event = True
            if event.key == pygame.K_UP: 
                y -= 1
                render_event = True
            if event.key == pygame.K_DOWN: 
                y += 1
                render_event = True    
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
                solve_puz = True   
            # If R pressed, clear the sudoku board 
            if event.key == pygame.K_r: 
                is_solved = False
                error = False
                solve_puz = False
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
                is_solved = False
                error = False
                solve_puz = False
                load_puzzle()
            # If E is pressed, verify the user input
            if event.key == pygame.K_e:
                verific = True 

    if solve_puz: 
        if not solve(grid):
            error = True
        else: 
            is_solved = True
        solve_puz = False    
    if val != 0:             
        draw_val(val) 
        # print(x) 
        # print(y) 
        if valid(grid, int(x), int(y), val):
            grid[int(x)][int(y)] = val
            render_event = False
        else: 
            grid[int(x)][int(y)] = 0
            error_unk_key()    
        val = 0    

    if verific:
        is_solved = verify_board(grid)

    if error: 
        error_puzzle_incomplete() 

    if is_solved: 
        result() 

    draw()

    if render_event: 
        draw_box()

    instruction()     
  
    # Update window 
    pygame.display.update()   
  
# Quit pygame window     
pygame.quit()
