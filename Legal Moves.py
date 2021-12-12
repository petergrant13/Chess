#Chess engine attempt

#This class stores information

class gameState():
    def __init__(self):
        # board is a list of lists
        self.board = [
        #     a     b     c     d     e     f     g     h
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], #8

            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"], #7

            ["--", "--", "--", "--", "--", "--", "--", "--"], #6

            ["--", "--", "--", "--", "--", "--", "--", "--"], #5

            ["--", "--", "--", "--", "--", "--", "--", "--"], #4

            ["--", "--", "--", "--", "--", "--", "--", "--"], #3

            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"], #2

            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]  #1
        #     a     b     c     d     e     f     g     h
        ]
        
        self.whiteToMove = True

        self.moveLog = []

        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)

        self.checkmate = False
        self.stalemate = False

        self.enPassantPossible = () #coordinates for square for holy hell

        self.currentCastlingRight = CastleRights(True, True, True, True) #can castle to any side at start (true until false)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                                self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    def getTurn(self):
        return self.whiteToMove

    #function which makes a move
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        #update where the king moved since hes an important cunt
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        #pawn promotion stuff
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q' 

        #en passant
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = '--'

        #update en passant square
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #2 square pawn advance
            self.enPassantPossible = ((move.startRow + move.endRow) // 2, move.endCol)
        else:
            self.enPassantPossible = ()

        #castle
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #moves the rook
                self.board[move.endRow][move.endCol+1] = '--' #get rid of rook on h file

            else: #queenside castle
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] #moves the rook
                self.board[move.endRow][move.endCol-2] = '--' #get rid of rook on a file

        #update castle rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                                self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
        

    #function which undoes a move
    def undoMove(self):
        if len(self.moveLog) != 0: #can't use pop on an empty list

            move = self.moveLog.pop() #pop off the last move made
            self.board[move.startRow][move.startCol] = move.pieceMoved #put the piece moved back at the starting square
            self.board[move.endRow][move.endCol] = move.pieceCaptured #put the piece captured (or empty square) back at the end square
            self.whiteToMove = not self.whiteToMove # change who it is to move

            #update where the king moved since hes an important cunt
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            #undo en passant move
            if move.isEnPassantMove: 
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enPassantPossible = (move.endRow, move.endCol)

            #undo 2 square pawn move
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()

            #undo castle rights
            self.castleRightsLog.pop() #get rid of new castle rights
            newRights = self.castleRightsLog[-1] #set current castle rights to the now last ones
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            #for undoing castling
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #kingside castle
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1] #moves the rook back
                    self.board[move.endRow][move.endCol-1] = '--' #get rid of rook on f file

                else: #queenside castle
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1] #moves the rook back
                    self.board[move.endRow][move.endCol+1] = '--' #get rid of rook on d file

    
    #updates the right to castle for each player
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
            
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False

        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #This is the white queenside rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: #This is the white kingside rook
                    self.currentCastlingRight.wks = False

        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: #This is the black queenside rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7: #This is the black kingside rook
                    self.currentCastlingRight.bks = False

        #if a rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False


    #legal moves
    def getValidMoves(self):
        tempEnPassantPossible = self.enPassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs) #copy current castling rights
        
        #generate all moves
        moves = self.getAllPossibleMoves()

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        #for each move, make the move
        #loop through list backwards to avoid bugs
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])

            #generate all opponent moves
            #see if any result in check
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
               #if true then not valid
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0: #checkmate or stalemate
            if self.inCheck():
                checkmate = True
                if self.whiteToMove:
                    print("Black Wins by Checkmate")
                else:
                    print("White Wins by Checkmate")
            else:
                stalemate = True
                print("stalemate")
        else:
            checkmate = False
            stalemate = False

        self.enPassantPossible = tempEnPassantPossible
        self.currentCastlingRight = tempCastleRights

        return moves


    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        opponentMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in opponentMoves:
            if move.endRow == r and move.endCol == c:
                return True
        
        return False


    #every move available which doesn't account for checks and such
    def getAllPossibleMoves(self): 
        moves = [] #make an array of all possible moves
        
        #loop through board
        for r in range(len(self.board)): 
            for c in range(len(self.board[r])):
                
                # figure out if white or black to play
                turn = self.board[r][c][0]

                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):

                    #at this point it is the right side moving and next line figures out the piece that is moving
                    piece = self.board[r][c][1]

                    #basically a switch statement
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves) #call the helper function for the pawn moves

                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves) #pretty fuckin self explanatory

                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)

                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)

                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)

                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)

        return moves

#-------------------------------------------------------------------------------------------------
#piece moves functions

    # gets the pawn moves completely works
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white turn
            if r >= 1 and self.board[r-1][c] == "--":
                moves.append(Move((r,c), (r-1, c), self.board))

                #if it can move twice
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c), (r-2, c), self.board))

            #for captures
            if c-1 >= 0: #capture left
                if self.board[r-1][c-1][0] == 'b': 
                    moves.append(Move((r,c), (r-1, c-1), self.board))
                
                elif (r-1, c-1) == self.enPassantPossible: #holy hell
                    moves.append(Move((r,c), (r-1, c-1), self.board, isEnPassantMove = True))

            if c+1 <= 7: #capture right
                if self.board[r-1][c+1][0] == 'b': 
                    moves.append(Move((r,c), (r-1, c+1), self.board))
                
                elif (r-1, c+1) == self.enPassantPossible: #holy hell
                    moves.append(Move((r,c), (r-1, c+1), self.board, isEnPassantMove = True))
            

        #black to move
        if not self.whiteToMove: #white turn
            if r <= 6 and self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1, c), self.board))

                #if it can move twice
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c), (r+2, c), self.board))

                #for captures
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w': #capture left
                    moves.append(Move((r,c), (r+1, c-1), self.board))
                
                elif (r+1, c-1) == self.enPassantPossible: #holy hell
                    moves.append(Move((r,c), (r+1, c-1), self.board, isEnPassantMove = True))

            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w': #capture right
                    moves.append(Move((r,c), (r+1, c+1), self.board))
                
                elif (r+1, c+1) == self.enPassantPossible: #holy hell
                    moves.append(Move((r,c), (r+1, c+1), self.board, isEnPassantMove = True))

    #bob seger baby TOTALLY FUCKING DONE
    def getKnightMoves(self, r, c, moves):
        #WHITE to move
        if self.whiteToMove:
            #jump to left up
            if  r >= 1 and c >= 2 and self.board[r-1][c-2][0] != 'w':
                 moves.append(Move((r,c), (r-1, c-2), self.board))

            #jump to up left
            if  r >= 2 and c >= 1 and self.board[r-2][c-1][0] != 'w':
                 moves.append(Move((r,c), (r-2, c-1), self.board))

            #up right
            if  r >= 2 and c <= 6 and self.board[r-2][c+1][0] != 'w':
                 moves.append(Move((r,c), (r-2, c+1), self.board))

            #right up
            if  r >= 1 and c <= 5 and self.board[r-1][c+2][0] != 'w':
                 moves.append(Move((r,c), (r-1, c+2), self.board))

            #right down
            if  r <= 6 and c <= 5 and self.board[r+1][c+2][0] != 'w':
                 moves.append(Move((r,c), (r+1, c+2), self.board))

            #down right
            if  r <= 5 and c <= 6 and self.board[r+2][c+1][0] != 'w':
                 moves.append(Move((r,c), (r+2, c+1), self.board))

            #down left
            if  r <= 5 and c >= 1 and self.board[r+2][c-1][0] != 'w':
                 moves.append(Move((r,c), (r+2, c-1), self.board))

            #left down
            if  r <= 6 and c >= 2 and self.board[r+1][c-2][0] != 'w':
                 moves.append(Move((r,c), (r+1, c-2), self.board))

        #BLACK to move
        if not self.whiteToMove: #white turn
            #jump to left up
            if  r >= 1 and c >= 2 and self.board[r-1][c-2][0] != 'b':
                 moves.append(Move((r,c), (r-1, c-2), self.board))

            #jump to up left
            if  r >= 2 and c >= 1 and self.board[r-2][c-1][0] != 'b':
                 moves.append(Move((r,c), (r-2, c-1), self.board))

            #up right
            if  r >= 2 and c <= 6 and self.board[r-2][c+1][0] != 'b':
                 moves.append(Move((r,c), (r-2, c+1), self.board))

            #right up
            if  r >= 1 and c <= 5 and self.board[r-1][c+2][0] != 'b':
                 moves.append(Move((r,c), (r-1, c+2), self.board))

            #right down
            if  r <= 6 and c <= 5 and self.board[r+1][c+2][0] != 'b':
                 moves.append(Move((r,c), (r+1, c+2), self.board))

            #down right
            if  r <= 5 and c <= 6 and self.board[r+2][c+1][0] != 'b':
                 moves.append(Move((r,c), (r+2, c+1), self.board))

            #down left
            if  r <= 5 and c >= 1 and self.board[r+2][c-1][0] != 'b':
                 moves.append(Move((r,c), (r+2, c-1), self.board))

            #left down
            if  r <= 6 and c >= 2 and self.board[r+1][c-2][0] != 'b':
                 moves.append(Move((r,c), (r+1, c-2), self.board))

    # fuck ya she works
    def getBishopMoves(self, r, c, moves):
        directions = ((-1,-1), (-1,1), (1,1), (1,-1)) #get the directions
        enemycolor = 'b' if self.whiteToMove else 'w' #figure out whether a piece is capturable
        for d in directions: #check all four directions
            for i in range(1,8): #this is to stay on the board
                endRow = r + d[0] * i #loop through each square
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7: #on board
                    endPiece = self.board[endRow][endCol] #if empty square
                    
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    
                    elif endPiece[0] == enemycolor: #if enemy piece
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                
                else:
                    break

    # fuck ya she works
    def getRookMoves(self, r, c, moves):
        #basically the same as the bishop but with files and ranks instead of diagonals
        directions = ((-1,0), (0,-1), (1,0), (0,1)) #get the directions
        enemycolor = 'b' if self.whiteToMove else 'w' #figure out whether a piece is capturable
        for d in directions: #check all four directions
            for i in range(1,8): #this is to stay on the board
                endRow = r + d[0] * i #loop through each square
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7: #on board
                    endPiece = self.board[endRow][endCol] #if empty square
                    
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    
                    elif endPiece[0] == enemycolor: #if enemy piece
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                
                else:
                    break


        #freddie mercury has got some moves
    
    # fuck ya she works
    def getQueenMoves(self, r, c, moves):
        directions = ((-1,0), (0,-1), (1,0), (0,1), (-1,-1), (-1,1), (1,1), (1,-1)) #get the directions
        enemycolor = 'b' if self.whiteToMove else 'w' #figure out whether a piece is capturable
        for d in directions: #check all eight directions
            for i in range(1,8): #this is to stay on the board
                endRow = r + d[0] * i #loop through each square
                endCol = c + d[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7: #on board
                    endPiece = self.board[endRow][endCol] #if empty square
                    
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    
                    elif endPiece[0] == enemycolor: #if enemy piece
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                
                else:
                    break

    #if in france the head moves separately from rest of body
    #works except for castling
    def getKingMoves(self, r, c, moves):
        #GET CHECKS AND ALL THAT SHIT AND CASTLING

        allyColour = "w" if self.whiteToMove else "b"

        #WHITE to move
        if self.whiteToMove:
            #left
            if  r >= 0 and c >= 1 and self.board[r][c-1][0] != 'w':
                 moves.append(Move((r,c), (r, c-1), self.board))

            #left up
            if  r >= 1 and c >= 1 and self.board[r-1][c-1][0] != 'w':
                 moves.append(Move((r,c), (r-1, c-1), self.board))

            #up
            if  r >= 1 and c <= 7 and self.board[r-1][c][0] != 'w':
                 moves.append(Move((r,c), (r-1, c), self.board))

            #right up
            if  r >= 1 and c <= 6 and self.board[r-1][c+1][0] != 'w':
                 moves.append(Move((r,c), (r-1, c+1), self.board))

            #right
            if  r <= 7 and c <= 6 and self.board[r][c+1][0] != 'w':
                 moves.append(Move((r,c), (r, c+1), self.board))

            #down right
            if  r <= 6 and c <= 6 and self.board[r+1][c+1][0] != 'w':
                 moves.append(Move((r,c), (r+1, c+1), self.board))

            #down
            if  r <= 6 and c >= 0 and self.board[r+1][c][0] != 'w':
                 moves.append(Move((r,c), (r+1, c), self.board))

            #left down
            if  r <= 6 and c >= 1 and self.board[r+1][c-1][0] != 'w':
                 moves.append(Move((r,c), (r+1, c-1), self.board))

        #BLACK to move
        if not self.whiteToMove: #white turn
            #left
            if  r >= 0 and c >= 1 and self.board[r][c-1][0] != 'b':
                 moves.append(Move((r,c), (r, c-1), self.board))

            #left up
            if  r >= 1 and c >= 1 and self.board[r-1][c-1][0] != 'b':
                 moves.append(Move((r,c), (r-1, c-1), self.board))

            #up
            if  r >= 1 and c <= 7 and self.board[r-1][c][0] != 'b':
                 moves.append(Move((r,c), (r-1, c), self.board))

            #right up
            if  r >= 1 and c <= 6 and self.board[r-1][c+1][0] != 'b':
                 moves.append(Move((r,c), (r-1, c+1), self.board))

            #right
            if  r <= 7 and c <= 6 and self.board[r][c+1][0] != 'b':
                 moves.append(Move((r,c), (r, c+1), self.board))

            #down right
            if  r <= 6 and c <= 6 and self.board[r+1][c+1][0] != 'b':
                 moves.append(Move((r,c), (r+1, c+1), self.board))

            #down
            if  r <= 6 and c >= 0 and self.board[r+1][c][0] != 'b':
                 moves.append(Move((r,c), (r+1, c), self.board))

            #left down
            if  r <= 6 and c >= 1 and self.board[r+1][c-1][0] != 'b':
                 moves.append(Move((r,c), (r+1, c-1), self.board))

        
    #figure out if possible to castle
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r,c): #can't castle in check
            return

        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(r, c, moves)
        
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)

    #make the castle queenside move
    def getQueensideCastleMoves(self, r, c, moves):
        if (self.board[r][c-1] == '--') and (self.board[r][c-2]) == '--' and (self.board[r][c-3] == '--'):
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r,c), (r,c-2), self.board, isCastleMove = True))
                global qsCastle;
                qsCastle = True

    #make the castle kingside move
    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r,c), (r,c+2), self.board, isCastleMove = True))
                global ksCastle;
                ksCastle = True


#----------------------------------------------------------------------------------------------

#class to figure out castling
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


#class to make a move and get the notation and such
class Move():

    #maps keys to values
    #key : val

    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}

    rowsToRanks = {v:k for k, v in ranksToRows.items()}

    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}

    colsToFiles = {v:k for k, v in filesToCols.items()}



    def __init__(self, startSquare, endSquare, board, isEnPassantMove = False, isCastleMove = False):
        #mainly just defining a bunch of stuff
        self.startRow = startSquare[0]
        self.startCol = startSquare[1]
        self.endRow = endSquare[0]
        self.endCol = endSquare[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        #checking to see if en passant is possible, basically check to make sure it's a pawn and that it would capture at the right square
        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        
        #very noice way to check to see if the pawn should be promoted
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7) #check to see if pawn promotion
        
        #check to see if it's a castle move
        self.isCastleMove = isCastleMove

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #print(self.moveID)


    #check for equality with moves
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    
    def getChessNotation(self, move):
        #not quite proper chess notation yet - just missing checkmate and checks

        #TODO figure out if a move results in check and then make a bool to add the + and # if checkmate
        check = False
        

        #castle
        if self.pieceMoved[1] == 'K':
            if (move.endCol - move.startCol == 2): #kingside castle
                return "0-0"
            if (move.endCol - move.startCol == -2): #queenside
                return "0-0-0"

        #pawn moves, works except for holy hell
        if self.pieceMoved[1] == 'p':
            if self.startCol != self.endCol:
                return self.getFile(self.startCol) + "x" + self.getRankFile(self.endRow, self.endCol)
            else:
                return self.getRankFile(self.endRow, self.endCol)
                
        #bigger pieces moves
        piece = self.pieceMoved[1]
        if self.pieceCaptured == '--':
            return piece + self.getRankFile(self.endRow, self.endCol)
        else:
            return piece + "x" + self.getRankFile(self.endRow, self.endCol)

        #check and checkmate stuff

        
       
    

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def getRank(self, r):
        return self.rowsToRanks[r]

    def getFile(self, c):
        return self.colsToFiles[c]













