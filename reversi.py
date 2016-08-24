# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 15:46:37 2016
返棋，第六版本，初级人工智能
@author: Administrator
"""

# Reversi

import random
import sys

def drawBoard(board):
    # This function prints out the board that it was passed. Returns None.
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(VLINE)
        print(HLINE)


def resetBoard(board):
    # Blanks out the board it is passed, except for the original starting position.
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

    # Starting pieces:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'


def getNewBoard():
    # Creates a brand new, blank board data structure.
    board = []
    for i in range(8):
        board.append([' '] * 8)

    return board


def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # first step in the direction
        y += ydirection # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y): # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' ' # restore the empty space
    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and y <=7


def getBoardWithValidMoves(board, tile):
    # Returns a new board with . marking the valid moves the given player can make.
    dupeBoard = getBoardCopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}


def enterPlayerTile():
    # Lets the player type which tile they want to be.
    # Returns a list with the player's tile as the first item, and the computer's tile as the second.
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

    # the first element in the tuple is the player's tile, the second is the computer's tile.
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def getPlayerMove(board, playerTile):
    # Let the player type in their move.
    # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, or type quit to end the game, or hints to turn off/on hints.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
            print('For example, 81 will be the top-right corner.')

    return [x, y]



def showPoints(playerTile, computerTile):
    # Prints out the current score.
    scores = getScoreOfBoard(mainBoard)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))

    
def isOnSide(x, y):
    return x == 0 or x == 7 or y == 0 or y ==7
    


#统计棋盘空格
def countBlank(board):
    blank=0
    for row in board:
        for i in row:
            if i==' ':
                blank+=1
    return blank
    
#表示下步棋无论怎么走，对方都会占角
def AllDanger(board, computerTile):
    possiblemoves=getValidMoves(board, computerTile)
    len_move=len(possiblemoves)
    len_danger=0
    for i in possiblemoves:
        x=i[0]
        y=i[1]
        if danger(board, computerTile,x,y)==True:
            len_danger+=1
    if len_move==len_danger:
        return True
                
#判断所走棋下步是否有危险
def danger(board, computerTile,x,y):
    dupeBoard = getBoardCopy(board)  #dupeBoard只在函数调用时存在，调用完后消失
    makeMove(dupeBoard, computerTile, x, y)
    blank=countBlank(dupeBoard)
    #转换下棋人
    if computerTile=="X":
        otherTile="O"
    if computerTile=="O":
        otherTile="X" 
    if blank>5:
        move=getComputerMove(dupeBoard, otherTile)
        if isOnCorner(move[0], move[1])==True:
            #print("danger move")
            return True
        else:
            #print("no danger")
            return False
    #清空复制的棋盘
    dupeBoard=getNewBoard()

def bestScoreMove(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)
    # Go through all the possible moves and remember the best scoring move
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:#这是简单覆盖，需要修改，因为有点棋吃子个数一样
            bestMove = [x, y]
            bestScore = score
    return bestMove



def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)

    # randomize the order of the possible moves
    random.shuffle(possibleMoves)

    # always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Go through all the possible moves and remember the best scoring move
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove



def getComputerNoDangerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)
    #print("possibleMoves:",possibleMoves)
    # randomize the order of the possible moves
    random.shuffle(possibleMoves)

    # always go for a corner if available.
    #首要考虑因素是占四个角
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    # Go through all the possible moves and remember the best scoring move
            
    #如果所有情况都会被别人占角，就走吃子多的步骤
    if AllDanger(board, computerTile)==True:
        return bestScoreMove(board, computerTile)
    
    else:
        # Go through all the possible moves and remember the best scoring move
        bestScore = -1
        for x, y in possibleMoves:
            if danger(board, computerTile,x,y)==True:
                continue
        
            dupeBoard1 = getBoardCopy(board)
            makeMove(dupeBoard1, computerTile, x, y)
            score = getScoreOfBoard(dupeBoard1)[computerTile]
            if score > bestScore:#这是简单覆盖，需要修改，因为有点棋吃子个数一样
                bestMove = [x, y]
                bestScore = score
    
    return bestMove


print('Welcome to Reversi!')

while True:
    # Reset the board and game.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')

    while True:
        if turn == 'player':
            # Player's turn.
            if showHints:
                validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                drawBoard(validMovesBoard)
            else:
                drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            move = getPlayerMove(mainBoard, playerTile)
            if move == 'quit':
                print('Thanks for playing!')
                sys.exit() # terminate the program
            elif move == 'hints':
                showHints = not showHints
                continue
            else:
                makeMove(mainBoard, playerTile, move[0], move[1])

            if getValidMoves(mainBoard, computerTile) == []:
                break
            else:
                turn = 'computer'

        else:
            # Computer's turn.
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            input('Press Enter to see the computer\'s move.')
            x, y = getComputerNoDangerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y)

            if getValidMoves(mainBoard, playerTile) == []:
                break
            else:
                turn = 'player'

    # Display the final score.
    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)
    print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
    if scores[playerTile] > scores[computerTile]:
        print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
    else:
        print('The game was a tie!')

    if not playAgain():
        break
