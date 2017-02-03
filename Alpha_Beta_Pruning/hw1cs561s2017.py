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
    def __init__(self,name,position,type,alpha,beta,value,children):
        self.name = name
        self.position = position
        self.type = type
        self.alpha = alpha
        self.beta = beta
        self.value = value
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

def find_next_moves(max_depth,board_position,player,max_min_counter,root):

    previous_player = 'X'
    if player == 'X':
        previous_player = 'O'

    next_player = 'X'
    if player == 'X':
        next_player = 'O'

    if max_depth < 1 :
        # Call evaluation function
        for child in root.children:
            board = changeBoard(board_position,previous_player,child.position)
            child.value = find_move_value(board,start_player)
            print child.value
        return

    if root.name == "root" and max_min_counter == 2 :
        nextValidMoves = find_valid_moves(player,board_position)
        if len(nextValidMoves) == 0:
            name = "Pass"
            type = 'MAX'
            if max_min_counter % 2 == 0 :
                type = 'MIN'
            value = 99999
            if type == "MAX":
                value = -99999
            children = []
            move = []
            node = Node(name,move,type,-99999,99999,value,children)
            root.children.append(node)
        else:
            for move in nextValidMoves :
                name = dic[move[1]] + str(move[0]+1)
                type = 'MAX'
                if max_min_counter % 2 == 0 :
                    type = 'MIN'
                value = 99999
                if type == "MAX":
                    value = -99999
                children = []
                node = Node(name,move,type,-99999,99999,value,children)
                root.children.append(node)

        find_next_moves(max_depth-1,board_position,next_player,max_min_counter+1,root)

    elif len(root.children) == 1 and root.children[0].name == "Pass":
        #print "pass"
        nextValidMoves = find_valid_moves(player,board_position)
        if len(nextValidMoves) == 0:
            name = "Pass"
            type = 'MAX'
            if max_min_counter % 2 == 0 :
                type = 'MIN'
            value = 99999
            if type == "MAX":
                value = -99999
            children = []
            move = []
            node = Node(name,move,type,-99999,99999,value,children)
            root.children[0].childre.append(node)
        else :
            for move in nextValidMoves :
                name = dic[move[1]] + str(move[0]+1)
                type = 'MAX'
                if max_min_counter % 2 == 0 :
                    type = 'MIN'
                value = 99999
                if type == "MAX":
                    value = -99999
                children = []
                node = Node(name,move,type,-99999,99999,value,children)
                root.children[0].children.append(node)
        find_next_moves(max_depth-1,board_position,next_player,max_min_counter+1,root.children[0])
    else :
        for child in root.children :
            #change the board
            newBoard = changeBoard(board_position,previous_player,child.position)
            nextValidMoves = find_valid_moves(player,newBoard)
            if len(nextValidMoves) == 0:
                name = "Pass"
                type = 'MAX'
                if max_min_counter % 2 == 0 :
                    type = 'MIN'
                value = 99999
                if type == "MAX":
                    value = -99999
                children = []
                move = []
                node = Node(name,move,type,-99999,99999,value,children)
                child.children.append(node)
            else :
                for move in nextValidMoves :
                    name = dic[move[1]] + str(move[0]+1)
                    type = 'MAX'
                    if max_min_counter % 2 == 0 :
                        type = 'MIN'
                    value = 99999
                    if type == "MAX":
                        value = -99999
                    children = []
                    node = Node(name,move,type,-99999,99999,value,children)
                    child.children.append(node)
            find_next_moves(max_depth-1,newBoard,next_player,max_min_counter+1,child)
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

def print_tree(root):

    print "Name =" + root.name + " Value =" + str(root.value) +" Alpha =" + str(root.alpha) + " Beta =" + str(root.beta) + " Position =" + str(root.position) + " Type =" + root.type

    if len(root.children) == 0 :
        return

    for child in root.children :
        print_tree(child)

    return

if __name__ == "__main__":
    start_player,max_depth,initial_board_position = read_Input_File("input.txt")
    othello = Othello(start_player,max_depth,initial_board_position)

    opposite_player = 'X'
    if start_player == 'X':
        opposite_player = 'O'

    #validMoves = find_valid_moves(start_player,initial_board_position)

    children = []
    position = []

    root = Node("root",position,"MAX",-99999,99999,-99999,children)

    find_next_moves(max_depth,initial_board_position,start_player,2,root)

    #print len(root.children)

    print_tree(root)

    '''for move in validMoves :
        #change the board
        newBoard = changeBoard(initial_board_position,start_player,move)
        nextValidMoves = find_valid_moves(opposite_player,newBoard)
        #print nextValidMoves '''

