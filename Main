# Chess main driver file

import Chess_legalMoves, Chess_Engine
from Chess_legalMoves import Move, gameState
import pygame as p
import images
import time


WIDTH = HEIGHT = 512

DIMENSION = 8

SQUARE_SIZE = HEIGHT // DIMENSION

MAX_FPS = 15

IMAGES = {}

p.init

# Load in the images. Important that we only do this once

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQUARE_SIZE,SQUARE_SIZE))
    # can access an image by saying 'IMAGES['wp']' 


# main driver which does all sortsa shit
def main():
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))

    #generate game state
    gs = gameState()

    #figure out valid moves. Done by creating a list of all valid moves and checking if user makes one of the valid moves
    validMoves = gs.getValidMoves()

    #this line helps with efficiency because we dont want to continually check if a move is valid, only when a move is made do we generate the list of valid moves
    moveMade = False

    #load in the images on top of the board
    loadImages()
    running = True
    squareSelected = () #keep track of last square selected, (row, col)
    playerClicks = [] #keep track of player clicks

    print("Welcome! Please enjoy the game and press \"z\" to undo a move and press \"r\" to reset t")

    playerOneHuman = True #if human playing white true, if computer playing white false
    playerTwoHuman = False #if human playing black true, if computer playing black false

    while running:

        humanTurn = (gs.whiteToMove and playerOneHuman) or (not gs.whiteToMove and playerTwoHuman)

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            #mouse magic
            elif e.type == p.MOUSEBUTTONDOWN and humanTurn:
                location = p.mouse.get_pos() #gives the (x,y) postion of mouse
                col = location[0]//SQUARE_SIZE
                row = location[1]//SQUARE_SIZE

                if squareSelected == (row, col): #clicked same square twice
                    squareSelected = () #unselect square
                    playerClicks = [] #reset player clicks

                else: 
                    squareSelected = (row, col) #select the square
                    playerClicks.append(squareSelected)

                if len(playerClicks) == 2:
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    
                    
                    #check if valid move
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            print(move.getChessNotation(validMoves[i]))
                            squareSelected = ()
                            playerClicks = []

                    if not moveMade:
                        playerClicks = [squareSelected]
                        print("Please make a valid move")
                        
                        if gs.getTurn():
                            print("White to move")
                        if not gs.getTurn():
                            print("Black to move")
                        

            #keyboard magic
            elif e.type == p.KEYDOWN: #if a key is pressed
                if e.key == p.K_z: #if z is pressed
                    gs.undoMove() #undo the last move
                    moveMade = True
                
                #press r key to reset
                if e.key == p.K_r: #reset board
                    gs = Chess_legalMoves.gameState()
                    validMoves = gs.getValidMoves()
                    squareSelected = ()
                    playerClicks = []
                    moveMade = False

        if not humanTurn and len(validMoves) != 0:
            engineMove = Chess_Engine.findBestMove(gs, validMoves)

            if engineMove is None:
                print("here")
                engineMove = Chess_Engine.findRandomMove(validMoves)
                print("random move")
            
            p.time.wait(200)
            #print(move.getChessNotation(engineMove))
            gs.makeMove(engineMove)
            moveMade = True

        #if a move was made, check that it is valid, then reset
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        #draw the board
        drawGameState(screen, gs, validMoves, squareSelected)
        p.time.wait(16)
        p.display.flip()


#highlight selected square
def highlightSquares(screen, gs, validMoves, squareSelected):
    if squareSelected != ():
        r, c = squareSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #square selected is a piece that can be moved
            #highlight selected square
            s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100) #transparency value - 0 transparent 255 solid
            s.fill(p.Color("blue"))
            screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))
            s.fill(p.Color("turquoise"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQUARE_SIZE * move.endCol, SQUARE_SIZE * move.endRow))


#draw the pieces on the board
def drawGameState(screen, gs, validMoves, squareSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, squareSelected)
    drawPieces(screen, gs.board)

#responsible for drawing the board
def drawBoard(screen):
    colors = [p.Color("wheat"), p.Color("darkgoldenrod")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
           color = colors[((r+c) % 2)]
           p.draw.rect(screen, color,p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))




def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



if __name__ == '__main__':
    main() 
