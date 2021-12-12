import random
import Chess_legalMoves

pieceScore = {"K": 100, "Q": 9, "R": 5, "B": 3.5, "N": 3, "p": 1}
CHECKMATE = 10000
STALEMATE = 0



def findRandomMove(validMoves):
    print("random")
    return validMoves[random.randint(0, (len(validMoves)-1))]

#method which makes a move solely on the piece value
#doesn't fucking work
def findBestMove(gs, validMoves):
    #depending on whose turn it is will affect piece value
    turnMultiplier = 1 if gs.whiteToMove else -1
    maxScore = -CHECKMATE
    bestMove = None

    #go through each move and find which one has the highest material count
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        if gs.checkmate:
            score = CHECKMATE
        elif gs.stalemate:
            score = STALEMATE

        else: 
            score = turnMultiplier * scoreMaterial(gs.board)

        if score > maxScore:
            score = maxScore
            bestMove = playerMove
        gs.undoMove()

    return bestMove

    

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]

            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    
    return score

