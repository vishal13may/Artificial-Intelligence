evaluation_values = [[99,-8,8,6,6,8,-8,99],
                     [-8,-24,-4,-3,-3,-4,-24,-8],
                     [8,-4,7,4,4,7,-4,8],
                     [6,-3,4,0,0,4,-3,6],
                     [6,-3,4,0,0,4,-3,6],
                     [8,-4,7,4,4,7,-4,8],
                     [-8,-24,-4,-3,-3,-4,-24,-8],
                     [99,-8,8,6,6,8,-8,99]]

directions =  [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]

dic = {}
dic[0] = 'a'
dic[1] = 'b'
dic[2] = 'c'
dic[3] = 'd'
dic[4] = 'e'
dic[5] = 'f'
dic[6] = 'g'
dic[7] = 'h'


class Othello:
    def __init__(self,start_player, max_depth, board_position):
        self.start_player = start_player
        self.max_depth = max_depth
        self.board_position = board_position

class Node:
    def __init__(self,name,type,alpha,beta,value,children):
        self.name = name
        self.type = type
        self.alpha = alpha
        self.beta = beta
        self.children = children

def find_valid_moves(start_player,board_position):
    validMoves = []
    vMoves = []
    for row in range(0,8):
        for column in range(0,8):
            if board_position[row][column] != '*':
                continue
            result = isValidMove(row,column,start_player,board_position)
            if result:
                move = ''
                move = dic[column] + str(row+1)
                vMoves.append(move)
                validMoves.append([row,column])
    print vMoves
    return validMoves

def isValidMove(row,column,player,board_position):

    for dir in range(0,8):
        x = row
        y = column
        validMove = 0
        while True:
            x += directions[dir][0]
            y += directions[dir][1]
            if x < 0 or x > 7 or y < 0 or y > 7 :
                break
            if board_position[x][y] == '*':
                break
            if board_position[x][y] != player:
                validMove =+ 1
            if board_position[x][y] == player :
                if validMove > 0 :
                    return True
                else :
                    break
    return False

def read_Input_File(filename):
    read_lines = []
    with open(filename,"r") as read_hadnler:
        read_lines =read_hadnler.readlines()
    read_lines = [line.strip() for line in read_lines]
    #print read_lines
    start_player = read_lines[0]
    max_depth = int(read_lines[1])

    initial_board_position = []
    for counter in range(2,len(read_lines)):
        row = []
        for character in read_lines[counter]:
            row.append(character)
        initial_board_position.append(row)

    return start_player,max_depth,initial_board_position

def changeBoard(board,player,move):
    newBoard = []
    for row in board:
        newRow = []
        for column in row:
            newRow.append(column)
        newBoard.append(newRow)
    newBoard[move[0]][move[1]] = player

    for dir in range(0,8):
        x = move[0]
        y = move[1]
        validMove = 0
        temp_positions = []
        while True:
            x += directions[dir][0]
            y += directions[dir][1]
            if x < 0 or x > 7 or y < 0 or y > 7 :
                break
            if newBoard[x][y] == '*':
                break
            if newBoard[x][y] != player:
                temp_positions.append([x,y])
                validMove =+ 1
            if newBoard[x][y] == player :
                if validMove > 0 :
                    for temp_position in temp_positions :
                        newBoard[temp_position[0]][temp_position[1]] = player
                    break
                else :
                    break

    return newBoard

def find_next_moves(max_depth,board_position,validMoves,player):

    previous_player = 'X'
    if player == 'X':
        previous_player = 'O'

    next_player = 'X'
    if player == 'X':
        next_player = 'O'

    if max_depth < 1 :
        # Call evaluation function
        print "Evaluation" + str(validMoves)
        for move in validMoves:
            board = changeBoard(board_position,previous_player,move)
            value = find_move_value(board,start_player)
            print value
        return
    if len(validMoves) == 0:
        #print "pass"
        nextValidMoves = find_valid_moves(player,board_position)
        find_next_moves(max_depth-1,board_position,nextValidMoves,next_player)
    else :
        for move in validMoves :
            #change the board
            newBoard = changeBoard(board_position,previous_player,move)
            nextValidMoves = find_valid_moves(player,newBoard)
            find_next_moves(max_depth-1,newBoard,nextValidMoves,next_player)
    return

def find_move_value(board_position,start_player):
    #print "start-player" + start_player
    start_player_value = 0
    opposite_player_value = 0
    for row in range(0,8):
        for column in range(0,8):
            if board_position[row][column] == start_player:
                start_player_value += evaluation_values[row][column]
            elif board_position[row][column] != start_player and board_position[row][column] != '*':
                opposite_player_value += evaluation_values[row][column]
    return (start_player_value - opposite_player_value)

if __name__ == "__main__":
    start_player,max_depth,initial_board_position = read_Input_File("input.txt")
    othello = Othello(start_player,max_depth,initial_board_position)
    #print initial_board_position
    opposite_player = 'X'
    if start_player == 'X':
        opposite_player = 'O'

    validMoves = find_valid_moves(start_player,initial_board_position)
    #print validMoves
    
    find_next_moves(max_depth - 1,initial_board_position,validMoves,opposite_player)

    '''for move in validMoves :
        #change the board
        newBoard = changeBoard(initial_board_position,start_player,move)
        nextValidMoves = find_valid_moves(opposite_player,newBoard)
        #print nextValidMoves '''

