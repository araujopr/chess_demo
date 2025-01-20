"""
This is our driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15  
IMAGES = {}

"""
Load all the images and initizallized a global dictionary of images. This will be called exactly once
"""
def loadImages():
    # Note: we can access an image by saying 'IMAGES['wp']' for example 
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bp", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR", "wp"]
    for piece in pieces: 
        IMAGES[piece] = p.transform.scale(p.image.load("images\\" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

"""
Draw squares on the board
"""
def drawBoard(screen): 
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION): 
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) 

"""
Draw pieces on the board using the curren GameState.board
"""
def drawPieces(screen, board):
    for r in range(DIMENSION): 
        for c in range(DIMENSION): 
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
Responsible for all the graphics within a current game state
"""
def drawGameState(screen, gs): 
    drawBoard(screen)                           # Draw squares on the board
    drawPieces(screen, gs.board)                # Draw pieces on top of those squares

     
"""
The main driver for our code. This will handle user input and updating the graphics
"""
def main(): 
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # Flag variable to know if player made a valid move

    loadImages()
    running = True
    sqSelected = () # No square is selected, keep track of the last click of the suer (tuple: (row, col))
    playerClicks = [] # Keep track of player clicks (two tuples: [(6,4), (4,4)])

    while running: 
        for e in p.event.get(): 
            if e.type == p.QUIT: 
                running = False
            
            # Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): 
                    sqSelected = () # Deselect
                    playerClicks = [] # Clear player clicks
                elif sqSelected == () and gs.board[row][col] == "--":
                    sqSelected = () # Deselect
                    playerClicks = [] # Clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # Append for both 1st and 2nd clicks
                if len(playerClicks) == 2: 
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    for engMove in validMoves:
                        if move == engMove: 
                            gs.makeMove(move, False)
                            moveMade = True
                            print("Se realizó el siguiente movimiento: " + move.getChessNotation())
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
        
            # Key handler
            elif e.type == p.KEYDOWN: 
                if e.key == p.K_z: 
                    gs.undoMove()
                    moveMade = True

        if moveMade: 
            validMoves = gs.getValidMoves()
            moveMade = False
             
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__": 
    main()