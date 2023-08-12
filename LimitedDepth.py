# MODULES
import pygame, sys
import numpy as np
import random
import time
# initializes pygame
pygame.init()

# ---------
# CONSTANTS
# ---------
WIDTH = 600
HEIGHT = WIDTH
LINE_WIDTH = 6 
WIN_LINE_WIDTH = 10 
BOARD_ROWS = 3   
BOARD_COLS = BOARD_ROWS
SQUARE_SIZE = WIDTH/BOARD_ROWS
CIRCLE_RADIUS = SQUARE_SIZE/3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE/4

RED = (235, 47, 6)
BG_COLOR = (72, 84, 96)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (255, 211, 42)
CROSS_COLOR = (186, 220, 88)

# ---------
# VARIABLES
# ---------
player = 1
game_over = False

# ------
# SCREEN
# ------
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption('TIC TAC TOE AI 3v3')
screen.fill( BG_COLOR )

# -------------
# CONSOLE BOARD
# -------------
board = np.zeros( (BOARD_ROWS, BOARD_COLS) )

# ---------
# FUNCTIONS
# ---------
def draw_lines():

	for i in range(1,BOARD_ROWS):
		# Ngang
		pygame.draw.line( screen, LINE_COLOR, (0, SQUARE_SIZE*i), (WIDTH, SQUARE_SIZE*i), LINE_WIDTH )

	for i in range(1,BOARD_COLS):
		# Dọc 
		pygame.draw.line( screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH )


def draw_figures():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 2:
				pygame.draw.circle( screen, CIRCLE_COLOR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
			elif board[row][col] == 1:
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )	
				pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )

def mark_square(row, col, player):
	board[row][col] = player
	# print ("----------------------------------------------------")
	# print("Player " + str(player) + " marked square : (" + str(row) + "," + str(col) + ")")
	# print(board)
	# print ("----------------------------------------------------")

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 0:
				return False

	return True

def check_win(player):
	# Dọc 
	for col in range(BOARD_COLS):
		if board[0][col] == player and board[1][col] == player and board[2][col] == player:
			draw_vertical_winning_line(col, player)
			return True

	# Ngang 
	for row in range(BOARD_ROWS):
		if board[row][0] == player and board[row][1] == player and board[row][2] == player:
			draw_horizontal_winning_line(row, player)
			return True

	# Chéo Phải 
	if board[2][0] == player and board[1][1] == player and board[0][2] == player:
		draw_asc_diagonal(player)
		return True

	# Chéo Trái 
	if board[0][0] == player and board[1][1] == player and board[2][2] == player:
		draw_desc_diagonal(player)
		return True

	return False

# =========
# Hàm vẽ đường win 
# =========
def draw_vertical_winning_line(col, player):
	posX = col * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH )

def draw_horizontal_winning_line(row, player):
	posY = row * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH )

def draw_asc_diagonal(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH )

def draw_desc_diagonal(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH )

def restart():
	screen.fill( BG_COLOR )
	draw_lines()
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			board[row][col] = 0


def checkWinner():
	winner = None;

	# Ngang
	for row in range(BOARD_ROWS):
		if(board[row][0]==board[row][1]==board[row][2]!=0):
			winner = board[row][0]
			return winner
	
	#  Dọc 
	for col in range(BOARD_COLS):
		if(board[0][col]==board[1][col]==board[2][col]!=0):
			winner = board[0][col]
			return winner
	
	# Chéo 
	if board[0][0]==board[1][1]==board[2][2]!=0:
		winner = board[0][0]
		return winner

	if board[2][0]==board[1][1]==board[0][2]!=0:
		winner = board[2][0]
		return winner

	# Hòa 
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 0:
				return None

	return 0

# Tính nước đi tốt nhất cho máy 
mytime = 0
def bestMove():
    global mytime
    start_time = time.time()
    bestScore = -100000
    move = None
    empty_cells = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] == 0]

    if not empty_cells:
        return (-1, -1)

    for row, col in empty_cells:
        board[row][col] = 2
        score = minimax(board, 0, -100000, 100000, False)
        board[row][col] = 0

        if score > bestScore:
            bestScore = score
            move = (row, col)

    if move:
        mark_square(move[0], move[1], 2)
        draw_figures()
    end_time = time.time()
    elapsed_time = end_time - start_time
    mytime = mytime + elapsed_time
    print("LimitedDepth:time to make first move :%f"%(mytime))
    return move

scores = {
  1: -10,
  2: 10, 
  0: 0
}
		
i = 0 
def minimax(board, depth, alpha, beta, isMaximizing):
    global i
    i = i + 1
    print(i) 
    n = 5
    # print(n)         
    result = checkWinner()
    if result is not None:
        return scores[result]
  
    if isMaximizing:
        bestScore = -100000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2

                    if(depth > n):
                        board[row][col] = 0
                        break
                    score = minimax(board, depth+1, alpha, beta, False)
                    board[row][col] = 0
                    bestScore = max(score, bestScore)
                    alpha = max(alpha, bestScore)

                    if beta <= alpha:
                        break
        return bestScore

    else:
        bestScore = 100000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    if(depth > n):
                        board[row][col] = 0
                        break
                    score = minimax(board, depth+1, alpha, beta, True)
                    board[row][col] = 0
                    bestScore = min(score, bestScore)
                    beta = min(beta, bestScore)

                    if beta <= alpha:
                        break
        return bestScore

draw_lines()


# --------
# MAINLOOP
# --------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            mouseX = event.pos[0] # x
            mouseY = event.pos[1] # y

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            if available_square( clicked_row, clicked_col ):

                player = 1
                mark_square( clicked_row, clicked_col, player )
                draw_figures()
                
                if check_win( player ):
                    font = pygame.font.SysFont(None, 120)
                    text = font.render("You win", True, pygame.Color(RED))
                    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                    screen.blit(text, text_rect)
                    game_over = True
                
                elif is_board_full():
                    font = pygame.font.SysFont(None, 120)
                    text = font.render("Hòa", True, pygame.Color(RED))               
                    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                    screen.blit(text, text_rect)
                    game_over = True

                else:
                    player = 2
                    draw_figures()
                    pygame.display.update()
                    bestMove()
                    draw_figures()
                    
                    if check_win( player ):
                        font = pygame.font.SysFont(None, 120)
                        text = font.render("Máy win", True, pygame.Color(RED))
                        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
                        screen.blit(text, text_rect)
                        game_over = True
                    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1
                game_over = False
                draw_figures()

    pygame.display.update()


