"""
Stores all the information about the current state of a chess game. It wil also be responsable for determining the valid moves
of the current state. It will also keep a move log.
"""
class GameState():
    def __init__(self):
        # Board is an 8x8 2D list, each element of the list has 2 characters. 
        # The first character correspond to the color of the piece.
        # Second character represents the type of piece.
        # "--" represents an empty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],            
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunction = {'p': self.getPawsMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 
                             'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.checkmate = False
        self.stalemate = False
        self.inCheck = False
    
    """
    Takes a move as a parameter and executes it (this will not work for castling, pawn promotion and en-passsant)
    """
    def makeMove(self, move, validMoves = True):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        if not validMoves:
            self.pawnPromotion(move)
        self.whiteToMove = not self.whiteToMove
    
    """
    Undo previous move
    """
    def undoMove(self): 
        if len(self.moveLog) != 0:
            lastMove = self.moveLog.pop()
            self.board[lastMove.startRow][lastMove.startCol] = lastMove.pieceMoved
            self.board[lastMove.endRow][lastMove.endCol] = lastMove.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    
    def pawnPromotion(self, move):
        if self.isThisPawnPromotion(move):
            #loop = True
            color = self.board[move.endRow][move.endCol][0]
            piece = 'Q'
            # while loop:
            #     print('Chose a piece to promote pawn')
            #     print('Press "Q" for queen')
            #     print('Press "N" for knight')
            #     print('Press "B" for bishop')
            #     print('Press "R" for rook')
            #     option = input()
            #     if option == 'q' or option == 'Q':
            #         piece = 'Q'
            #         loop = False
            #     elif option == 'n' or option == 'N':
            #         piece = 'N'
            #         loop = False
            #     elif option == 'b' or option == 'B':
            #         piece = 'B'
            #         loop = False
            #     elif option == 'r' or option == 'R':
            #         piece = 'R'
            #         loop = False
            #     else:
            #         print('Invalid option!!!')
            self.board[move.endRow][move.endCol] = color + piece
            


    def isThisPawnPromotion(self, move):
        if move.pieceMoved == 'wp' and move.endRow == 0:
            return True
        elif move.pieceMoved == 'bp' and move.endRow == len(self.board)-1:
            return True
        else: 
            return False


    """
    All moves without considering checks 
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not(self.whiteToMove)):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r, c, moves)
        return moves

    """
    Get all possible moves for pawns
    """
    def getPawsMoves(self, r, c, moves):
        if self.whiteToMove: 
            if r-1 >= 0:
                if self.board[r-1][c] == '--':
                    moves.append(Move((r,c), (r-1,c), self.board))
                    if r == len(self.board)-2 and self.board[r-2][c] == '--':
                        moves.append(Move((r,c), (r-2,c), self.board))
                if c-1 >= 0 and self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c-1), self.board))
                if c+1 < len(self.board[r]) and self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c+1), self.board))
        else:
            if r+1 < len(self.board):
                if self.board[r+1][c] == '--':
                    moves.append(Move((r,c), (r+1,c), self.board))
                    if r == 1 and self.board[r+2][c] == '--':
                        moves.append(Move((r,c), (r+2,c), self.board))
                if c-1 >= 0 and self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c), (r+1,c-1), self.board))
                if c+1 < len(self.board[r]) and self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c), (r+1,c+1), self.board))
            
    """
    Get all possible moves for Rook
    """
    def getRookMoves(self, r, c, moves):
        colorToCapture = 'b' if self.whiteToMove else 'w'
        rowRanges = [range(r+1, len(self.board)), range(r-1, -1, -1), 
                     [r]*(len(self.board[r])-(c+1)), [r]*c]
        colRanges = [[c]*(len(self.board)-(r+1)), [c]*r,
                     range(c+1, len(self.board[r])), range(c-1, -1, -1)]
        for rowRange, colRange in zip(rowRanges, colRanges):
            for rowEnd, colEnd in zip(rowRange, colRange):
                if self.board[rowEnd][colEnd] != "--": 
                    if self.board[rowEnd][colEnd][0] == colorToCapture:
                        moves.append(Move((r,c), (rowEnd, colEnd), self.board))
                    break
                else: 
                    moves.append(Move((r,c), (rowEnd, colEnd), self.board))
        
    """
    Get all possible moves for Knight
    """
    def getKnightMoves(self, r, c, moves):
        allyColor = 'w' if self.whiteToMove else 'b'
        boardRows = len(self.board)
        boardCols = len(self.board[r])
        possibleMoves = [(r+2,c+1), (r+2,c-1),
                         (r-2,c+1), (r-2,c-1),
                         (r+1,c+2), (r-1,c+2),
                         (r+1,c-2), (r-1,c-2)]
        for possibleMove in possibleMoves:
            rowEnd, colEnd = possibleMove[0], possibleMove[1]
            if 0 <= rowEnd < boardRows and 0 <= colEnd < boardCols:
                if self.board[rowEnd][colEnd][0] != allyColor:
                    moves.append(Move((r,c), (rowEnd,colEnd), self.board))

    """
    Get all possible moves for bishop
    """
    def getBishopMoves(self, r, c, moves): 
        colorToCapture = 'b' if self.whiteToMove else 'w'
        boardRows = len(self.board)
        boardCols = len(self.board[r])
        rowRanges = [range(r+1, boardRows), range(r+1, boardRows),
                     range(r-1, -1, -1), range(r-1, -1, -1)]
        colRanges = [range(c+1, boardCols), range(c-1, -1, -1),
                     range(c+1, boardCols), range(c-1, -1, -1)]
        
        for rowRange, colRange in zip(rowRanges, colRanges):
            rangeLimit = min(len(list(rowRange)), len(list(colRange)))
            rowRange = rowRange[:rangeLimit]
            colRange = colRange[:rangeLimit]
            for rowEnd, colEnd in zip(rowRange, colRange):
                if self.board[rowEnd][colEnd] == '--':
                    moves.append(Move((r,c), (rowEnd, colEnd), self.board))
                elif self.board[rowEnd][colEnd][0] == colorToCapture:
                    moves.append(Move((r,c), (rowEnd, colEnd), self.board))
                    break
                else:
                    break

    """
    Get all possible moves for queen
    """
    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    """
    Get all possible moves for king
    """
    def getKingMoves(self, r, c, moves):
        allyColor = 'w' if self.whiteToMove else 'b'
        boardRows = len(self.board)
        boardCols = len(self.board[r])
        possibleMoves = [(r+1,c+1), (r+1,c-1),
                         (r-1,c+1), (r-1,c-1),
                         (r,c+1), (r,c-1),
                         (r+1,c), (r-1,c)]
        for possibleMove in possibleMoves:
            rowEnd, colEnd = possibleMove[0], possibleMove[1]
            if rowEnd >= 0 and rowEnd < boardRows:
                if colEnd >= 0 and colEnd < boardCols:
                    if self.board[rowEnd][colEnd][0] != allyColor:
                        moves.append(Move((r,c), (rowEnd,colEnd), self.board))

    def enemyKingUnderAttack(self):
        moves = self.getAllPossibleMoves()
        for move in moves:
            piece = move.pieceCaptured[1]
            if piece == 'K':
                return True
        return False 

    """
    All moves considering checks 
    """
    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        self.isThisCheck()
        for move in moves[::-1]:
            self.makeMove(move, True)
            kingUnderAttack = self.enemyKingUnderAttack()
            if kingUnderAttack: 
                moves.remove(move)
            self.undoMove()
        
        if not(moves):
            if self.inCheck:
                self.checkmate = True
                print("CHECKMATE!!")
                if self.whiteToMove: print('Color Black Wins!')
                else: print('Color White Wins!')
            else: 
                self.stalemate = True
        return moves
    
    def isThisCheck(self):
        self.whiteToMove = not self.whiteToMove
        self.inCheck = self.enemyKingUnderAttack()
        self.whiteToMove = not self.whiteToMove
    
class Move():
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    rowsToRanks = {u:v for v,u in ranksToRows.items()}
    colsToFiles = {u:v for v,u in filesToCols.items()}

    def __init__(self, startSq, endSq, board): 
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol= endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #self.pawnPromotion = False
        #if self.pieceMoved == 'wp' and self.endRow == len(self.board) - 1:
        #    self.pawnPromotion = True
        #if self.pieceMoved == 'bp' and self.endRow == 0:
        #    self.pawnPromotion = True
        self.moveID = self.startCol*1000 + self.startRow*100 + self.endCol*10 + self.endRow

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        else: return False
            
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
    def getChessNotation(self):
        # You can add this to make a real chess notation
        startNotation = self.getRankFile(self.startRow, self.startCol)
        endNotation = self.getRankFile(self.endRow, self.endCol)
        return startNotation + endNotation