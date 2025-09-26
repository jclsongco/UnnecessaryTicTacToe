import pygame
import pygame_textinput
import sys
from pygame import mixer

pygame.init()

#For text input
textinput = pygame_textinput.TextInputVisualizer()
input_font = pygame.font.SysFont('arial', 100)
input_field = pygame_textinput.TextInputVisualizer(font_object=input_font)

#pygame essentials
clock = pygame.time.Clock()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Tic Tac Toe!")
pygame.display.set_icon(pygame.image.load('logo.png'))


#set up of global variables
#for the main game
coords= [ ]
coords_dupe = coords
move_history_x = []
move_history_o = []

pattern1 = []
pattern2 = []

#for various states
move_type = 'X'
error = "none"
game_mode = "input"

cursor = (-10,-10) #just to reset the x and o position of the cursor

def grid(width,height,no): #Setup the grid equally depending on no - (number of cells per row or column)
    width_lines = width/no
    height_lines = height/no

    width_count = 0
    height_count = 0

    for _ in range(no-1):
        width_count += width_lines
        pygame.draw.line(screen,'Black',(0,width_count),(screen_width,width_count),5)

        height_count += height_lines
        pygame.draw.line(screen,'Black',(height_count,0),(height_count,screen_height),5)
    
    return width_lines, height_lines

def four_points(x,y,row_size,col_size): #cell method, finds the coordinates of the points
    x = round(x)
    y = round(y)
    row_size = round(row_size)
    col_size = round(col_size)
    
    coor1 = (x,y)
    coor2 = (x+col_size,y)
    coor3 = (x,y+row_size)
    coor4 = (x+col_size,y+row_size)

    coords = [coor1,coor2,coor3,coor4]
    return coords

def coordinator(no, row_size : int, col_size : int): #gets the coordinates of the board
    
    topleft = (0,0)
    for j in range(no): #controls which row are we
        for i in range(no): #controls whats in the rows
            coords.append(four_points(topleft[0],topleft[1],row_size,col_size))
            topleft = (topleft[0]+row_size,topleft[1])
        
        topleft = (0,topleft[1]+col_size)
    
def locator(coords_dupe: list,mouse): #identifies which cell you clicked on
    entry_no = 0
    for entry in coords_dupe:
        x_bounds = (entry[0][0],entry[3][0])
        y_bounds = (entry[0][1],entry[3][1])
        if x_bounds[0] < mouse[0] < x_bounds[1] and y_bounds[0] < mouse[1] < y_bounds[1]:
            return entry_no,entry
        
        entry_no += 1
        
def x_drawer(entry): #just draws x's on the board
    pygame.draw.line(screen,'Red',entry[0],entry[3],10)
    pygame.draw.line(screen,'Red',entry[1],entry[2],10)

def o_drawer(entry,row_size,col_size): #just draw o's on the board
    y_coor = entry[3][1] - (col_size/2)
    x_coor = entry[3][0] - (row_size/2)
    if row_size >= col_size:shorter = col_size
    else: shorter = row_size
    
    radius = shorter/2
    pygame.draw.circle(screen,'Blue',(x_coor,y_coor),radius,width=10)

def hori_check(cell_list,number): #number is the number of rows or columns, check for horizontal win conditions
    positions = []
    for place in cell_list:
        positions.append(place[0][1])
    index = set(positions)

    for num in index:
        counter = positions.count(num)
        if counter == number:
            return True

def verti_check(cell_list,number): #number is the number of rows or columns, check for vertica; win conditions
    positions = []
    for place in cell_list:
        positions.append(place[0][0])
    index = set(positions)

    for num in index:
        counter = positions.count(num)
        if counter == number:
            return True

def diag_patterns(number): #identifies the cells that are in the diagonal win condition
    global coords
    pattern1 = []
    pattern2 = []
    for i in range(number):
        pattern1.append((number*i)+i)
        pattern2.append((number-1)*(i+1))
    
    pattern1_coords = []
    pattern2_coords = []

    for i in pattern1:
        pattern1_coords.append(coords[i])
    
    for i in pattern2:
        pattern2_coords.append(coords[i])

    
    return pattern1_coords,pattern2_coords

def diag_check(cell_list,number): #matches the cells with the diagonal pattern winning conditions
    global pattern1,pattern2
    tester1 = []
    tester2 = []

    for cell in pattern1:
        if cell in cell_list:
            tester1.append(True)
    
    for cell in pattern2:
        if cell in cell_list:
            tester2.append(True)
    
    if len(tester1) == number or len(tester2) == number:
        return True

def master_checker(cell_list,number): #uses all _check functions and outputs True if win
    if hori_check(cell_list,number):
        return True
    elif verti_check(cell_list,number):
        return True
    elif diag_check(cell_list,number):
        return True
    else:
        return False

def winner_text(state,winner = ""): #blits text if you are a winner or draw
    global screen_width,screen_height
    font = pygame.font.SysFont('arial', 100) 
    if state == 'win':
        text_surf = font.render(f"{winner} WINS!",False,'Black')
    elif state == 'draw':
        text_surf = font.render("DRAW!",False,'Black')
    text_rect = text_surf.get_rect(center = (screen_width/2,screen_height/2))
    screen.blit(text_surf,text_rect)

    instructions = pygame.font.SysFont('arial', 30) 
    ins_surf = instructions.render("Press ENTER to continue",False,'Black','White')
    ins_rect = text_surf.get_rect(center = (screen_width/2,(screen_height/2)+200))
    screen.blit(ins_surf,ins_rect)

def input_text(): #blits text during input mode
    inp = pygame.font.SysFont('arial', 20) 
    inp_surf = inp.render("Enter desired number of rows or columns (n x n)",False,'Black','White')
    ins_rect = inp_surf.get_rect(center = (screen_width/2,(screen_height/2)-170))
    screen.blit(inp_surf,ins_rect)

def error_text(): #blits text if invalid input
    inp = pygame.font.SysFont('arial', 20) 
    inp_surf = inp.render("Input must be a positive integer",False,'Black','White')
    ins_rect = inp_surf.get_rect(center = (screen_width/2,(screen_height/2)+100))
    screen.blit(inp_surf,ins_rect)

def cursor_draw(coor): #draws the indicator (which turn) near the cursor
    if move_type == 'O':
        pygame.draw.circle(screen,'Blue',coor,20,width=3)
    if move_type == 'X':
        pygame.draw.line(screen,'Red',(coor[0]-10,coor[1]-10),(coor[0]+10,coor[1]+10),3)
        pygame.draw.line(screen,'Red',(coor[0]-10,coor[1]+10),(coor[0]+10,coor[1]-10),3)
      
while True:
    screen.fill('White')
    events = pygame.event.get()

    for event in events: 

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_mode == 'active':

            if event.type == pygame.MOUSEMOTION:
                cursor = pygame.mouse.get_pos()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                try:
                    cell_no, cell_coords = locator(coords_dupe,mouse_pos) 
                    mixer.Sound('sounds/place.mp3').play()
                    if move_type == 'X': 
                        move_history_x.append(cell_coords)
                        move_type = 'O'
                    elif move_type == 'O':
                        move_history_o.append(cell_coords)
                        move_type = 'X'
                    
                    coords_dupe.pop(cell_no) 
                    
                except TypeError:
                    mixer.Sound('sounds/error.mp3').play()
                    pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_mode = 'input'

        
        elif game_mode == 'inactive':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    move_history_x = []
                    move_history_o = []
                    coordinator(number,row_size,col_size) 
                    move_type = 'X'
                    game_mode = 'input'
            
        elif game_mode == 'input':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        number = int(input_field.value)
                        if number <= 0:
                            raise ValueError
                        error = "none"
                        mixer.Sound('sounds/start_game.mp3').play()
                        coords= [ ]
                        coords_dupe = coords
                        row_size,col_size = grid(screen_width,screen_height,number)
                        coordinator(number,row_size,col_size) 
                        pattern1,pattern2 = diag_patterns(number)
                        move_history_x = []
                        move_history_o = []
                        move_type = 'X'

                     
                        cursor = (-10,-10)
                        game_mode = 'active'
                    except ValueError:
                        mixer.Sound('sounds/error.mp3').play()
                        error = 'found'
                        input_field.value =""
                        continue

            

    if game_mode == 'active': #just for the cursor indicator
        cursor_draw(cursor)
    
    if game_mode == 'active' or game_mode == 'inactive':
        #draws the xs and os
        for entry in move_history_x:
            x_drawer(entry)
            
        for entry in move_history_o:
            o_drawer(entry,row_size,col_size)

        grid(screen_width,screen_height,number) #draws the grid


        #checks for winning conditions
        if master_checker(move_history_x,number):
            winner_text('win','X')
            if game_mode == 'active': mixer.Sound('sounds/winner.mp3').play()
            game_mode = 'inactive'
        elif master_checker(move_history_o,number):
            winner_text('win','O')
            if game_mode == 'active': mixer.Sound('sounds/winner.mp3').play()
            game_mode = 'inactive'
        elif len(coords_dupe) == 0:
            winner_text('draw')
            if game_mode == 'active': mixer.Sound('sounds/draw.mp3').play()
            game_mode = 'inactive'

    if game_mode == 'input':
        screen.fill('White')
        input_text()
        input_field.update(events)
        input_rect = input_field.surface.get_rect(center = (screen_width/2,screen_height/2))
        screen.blit(input_field.surface,input_rect)

    if error == 'found':
        error_text()
    


    pygame.display.update()
