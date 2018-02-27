class Piece:
    def __init__(self, color):
        self._color = color
    def possible_moves(self, row, col, board):
        pass

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
    def possible_moves(self, row, col, board):
        pass

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
    def possible_moves(self, row, col, board):
        pass

class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
    def possible_moves(self, row, col, board):
        pass

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
    def possible_moves(self, row, col, board):
        pass

class King(Piece):
    def __init__(self, color):
        super().__init__(color)
    def possible_moves(self, row, col, board):
        pass

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
    def possible_moves(self, row, col, board):
        pass

class Board:
    # A board is of size 8
    COL_HEADERS = ['A','B','C','D','E','F','G','H']
    def __init__(self):
        # 2D Piece array
        self._board = [[None] * 8 for _ in range(8)]
        for i in range(8):
            self._board[1][i] = Pawn(True)
            self._board[6][i] = Pawn(False)
        for i in range(1):
            white = i == 0
            row = 0 if white else 7
            self._board[row][0] = Rook(white)
            self._board[row][1] = Bishop(white)
            self._board[row][2] = Knight(white)
            self._board[row][3] = King(white)
            self._board[row][4] = Queen(white)
            self._board[row][5] = Knight(white)
            self._board[row][6] = Bishop(white)
            self._board[row][7] = Rook(white)


    def is_check_for(self, white):
        pass

    def is_checkmate_for(self, white):
        pass

    def can_pick_up(self, pos, turn):
        pass

    def get_moves_for(self, pos):
        pass

    def move(self, fr, to):
        pass

    def print_highlighed_board(self, highlights):
        pass

    def print_board(self):
        self.print_highlighed_board([])

    def __str__(self):
        pass

def print_error(err):
    print(err)
    print("(Press ENTER to continue)")
    input()

def get_valid_input(pred, prompt, err_message):
    valid = False
    while not valid:
        read = input(prompt)
        if pred(read):
            valid = True
        else:
            print_error(err_message)
    return read

def can_parse_position(input):
    if len(input) == 2:
        if any(map(lambda x: x == input[0], Board.COL_HEADERS)):
            if input[1].isdigit():
                return True
    return False

def parse_position(strpos):
    x = Board.COL_HEADERS.index(strpos[0])
    y = int(strpos[1])
    return x,y

def get_valid_position(board, pred, message, err_message):
    picked_valid = False
    while not picked_valid:
        board.print_board()
        strpos = get_valid_input(can_parse_position,
            "Input a position", "Couldn't parse position, use the form 'A3'")
        pos = parse_position(strpos)
        if pred(pos):
            picked_valid = True
        else:
            print_error(err_message)
    return pos

def main():
    board = Board()
    turn = True
    while not board.is_checkmate_for(turn):
        pick_up = get_valid_position(board, lambda p: board.can_pick_up(p, turn), 
            "Select a piece to move", "Can't pick up a piece there")
        valid_moves = board.get_moves_for(pos)
        board.print_highlighed_board(valid_moves)
        move_to = get_valid_position(board, lambda p: p in valid_moves,
            "Select a location to move to", "Can't move there")
        board.move(pick_up, move_to)
        turn = not turn

if __name__ == '__main__':
    main()
'''
class Piece(object):
    def __init__(self, piece, color, row, col):
        self.piece=piece
        self.color=color #blank=-2
        self.row=row
        self.col=col
    def __str__(self):
        return self.get_character()
    def fix_pos(self, row, col):
        self.row=row
        self.col=col
    def get_character(self):
        st=''
        if self.piece==0 and self.color==-2: #color of -2 means blank piece
            return '--'
        elif self.piece==1:
            st='P'
        elif self.piece==2:
            st='R'
        elif self.piece==3:
            st='N'
        elif self.piece==4:
            st='B'
        elif self.piece==5:
            st='Q'
        else:
            st='K'
        if self.color==0:
            return st+"+"
        elif self.color==1:
            return st+"-"
        elif self.color==-1: #used when printing possible moves
            if self.piece==0:
                return 'X-'
            return st+'X'
    def get_pawn_moves(self,board):
        moves=[]
        if self.color==0: direction=1
        else: direction=-1
        #moving forward
        if ((self.row==1 and self.color==0) or self.row==6) and not is_piece(board, self.row+direction, self.col):
            #if first move AND there is no piece in front of it
            moves.append((self.row+2*direction, self.col, False))
        moves.append((self.row+direction, self.col, False))
        #diagonals
        if is_piece(board, self.row+direction, self.col+direction):
            moves.append((self.row+direction, self.col+direction, True))
        if is_piece(board, self.row+direction, self.col-direction):
            moves.append((self.row+direction, self.col-direction, True))
        return moves
    def get_rook_moves(self, board):
        moves=[]
        #rows bellow
        for i in range(self.row,8):
            current_piece=board[i][self.col]
            print("rows",current_piece)
            if current_piece is self:
                continue
            if is_piece(board, i, self.col):
                if not self.is_same_color(current_piece):
                    moves.append((i, self.col, True))
                break
            moves.append((i, self.col, True))
        #rows above
        for i in range(self.row,-1,-1):
            current_piece=board[i][self.col]
            print("rows",current_piece)
            if current_piece is self:
                continue
            if is_piece(board, i, self.col):
                if not self.is_same_color(current_piece):
                    moves.append((i, self.col, True))
                break
            moves.append((i, self.col, True))
        #cols right
        for i in range(self.col,8):
            current_piece=board[self.row][i]
            print("cols",current_piece)
            if current_piece is self:
                continue
            if is_piece(board, self.row, i):
                if not self.is_same_color(current_piece):
                    moves.append((self.row, i, True))
                break
            moves.append((self.row, i, True))
        #cols left
        for i in range(self.col,-1,-1):
            current_piece=board[self.row][i]
            print("cols",current_piece)
            if current_piece is self:
                continue
            if is_piece(board, self.row, i):
                if not self.is_same_color(current_piece):
                    moves.append((self.row, i, True))
                break
            moves.append((self.row, i, True))
        return moves
    def get_bishop_moves(self, board):
        moves=[]
        #loops through directions
        for direction in range(0,4):
            add_row=False
            add_col=False
            direct="" #TODO: remove after debugging
            if direction==0:
                add_row=True
                add_col=True
                direct="SE"
            elif direction==1:
                add_row=True
                add_col=False
                direct="SW"
            elif direction==2:
                add_row=False
                add_col=True
                direct="NE"
            else:
                add_row=False
                add_col=False
                direct="NW"
            for i in range(0,8):
                #c_row = current row
                if add_row:
                    c_row=self.row+i
                else:
                    c_row=self.row-i
                if add_col:
                    c_col=self.col+i
                else:
                    c_col=self.col-i
                if not is_valid_position(c_row, c_col):
                    break
                current_piece=board[c_row][c_col]
                print(direct,current_piece)
                if current_piece is self:
                    continue
                if is_piece(board, c_row, c_col):
                    if not self.is_same_color(current_piece):
                        moves.append((c_row, c_col, True))
                    break
                moves.append((c_row, c_col, True))
        return moves
    def get_knight_moves(self, board):
        moves=[]
        #first space move loop
        for i in range(1,3):
            #direction loop
            for j in range(4):
                c_row=self.row
                c_col=self.col
                if j==0: c_row=self.row+i
                elif j==1: c_row=self.row-i
                elif j==2: c_col=self.col+i
                else: c_col=self.col-i
                for k in range(2):
                    changed_row=False
                    if c_row !=self.row:
                        changed_row=True
                    if i==1: direction=2
                    else: direction=1
                    if k==1: direction = -direction
                    if changed_row:
                        moves.append((c_row, c_col+direction, True))
                    else:
                        moves.append((c_row+direction, c_col, True))
        return moves
    def get_king_moves(self, board):
        king_moves=[]
        for i in range(self.row-1,self.row+2):
            for j in range(self.col-1,self.col+2):
                try:
                    if board[i][j] is self:
                        continue
                    king_moves.append([i,j,True])
                except:
                    continue
        #remove from moves
        for row in board:
            for space in row:        
                if space.color!=self.color and space.color!=-2 and space.piece!=6:
                    #POSSIBLE BUG piece!=6 added because of recursion issue
                    #not same color piece/empty
                    moves=space.get_possible_moves(board)
                    #only keep moves not in both lists
                    to_remove=[]
                    for k_move in king_moves:
                        for move in moves:
                            if k_move[0]==move[0] and k_move[1]==move[1]:
                                to_remove.append(k_move)
                    king_moves[:]=[k_move for k_move in king_moves if not k_move in to_remove]
        return king_moves
    def get_possible_moves(self, board, is_checkmate_check=False):
        #returns a list
        assert self.piece!=0
        #moves: row, col, can_overtake
        moves=[]
        if self.piece==1:
            #pawn
            moves+=self.get_pawn_moves(board)
        elif self.piece==2:
            #rook
            moves+=self.get_rook_moves(board)
        elif self.piece==3:
            #knight
            moves+=self.get_knight_moves(board)
        elif self.piece==4:
            #bishop
            moves+=self.get_bishop_moves(board)
        elif self.piece==5:
            #queen - rook+bishop
            moves+=self.get_rook_moves(board)
            moves+=self.get_bishop_moves(board)
        elif self.piece==6:
            #king
            moves+=self.get_king_moves(board)
        #check for occupied spaces/invalid moves
        moves[:]=[move for move in moves if not (not is_valid_position(move[0], move[1]) or \
                  (is_piece(board, move[0], move[1]) and self.is_same_color(board[move[0]][move[1]]) and not is_checkmate_check) \
                   or (move[2]==False and is_piece(board, move[0], move[1])))]
        print(moves)
        return moves
    def is_same_color(self, piece):
        return self.color==piece.color
#end piece


def print_board(board):
    lst=['A_','B_','C_','D_','E_','F_','G_','H_']
    print('     ', end="")
    for i in lst:
        print(i, end="")
    print()
    print('= = = = = = = = = = = =')
    for i,row in enumerate(board):
        print(str(i+1)+"  ||", end="")
        for space in row:
            print(space, end="")
        print()
    print()

def print_possibles(board, moves):
    changeable_board=copy.deepcopy(board)
    for move in moves:
        changeable_board[move[0]][move[1]].color=-1
    print_board(changeable_board)

def is_piece(board, row, col):
    if not is_valid_position(row, col):
        return False
    return board[row][col].piece!=0
def setup_board(board):
    for i,row in enumerate(board):
        #pawns
        if i==1 or i==6:
            if i==1: color=0
            else: color=1
            for j in range(8):
                row[j]=Piece(1, color, i, j)
        #others
        elif i==0 or i==7:
            if i==0: color=0
            else: color=1
            for j in range(8):
                if j==0 or j==7:
                    row[j]=Piece(2, color,i,j)
                elif j==1 or j==6:
                    row[j]=Piece(3, color,i,j)
                elif j==2 or j==5:
                    row[j]=Piece(4, color,i,j)
                elif j==3:
                    row[j]=Piece(5, color,i,j)
                else:
                    row[j]=Piece(6, color,i,j)
                    
    return board

def move_piece(piece, board):
    moves=piece.get_possible_moves(board)
    #get a valid move
    done=False
    while not done:
        print_possibles(board, moves)
        space=get_user_input('Where will you move?')
        for move in moves:
            if move[0]==space[0] and move[1]==space[1]:
                done=True
        if not done:
            print('Not a valid move. Press Enter.')
            input()
    #move piece
    if is_piece(board,space[0],space[1]):
        #if move captures piece
        board[space[0]][space[1]].piece=0
        board[space[0]][space[1]].color=-2
    #swap
    board[piece.row][piece.col],board[space[0]][space[1]]=board[space[0]][space[1]],board[piece.row][piece.col]
    board[piece.row][piece.col].fix_pos(piece.row, piece.col)
    board[space[0]][space[1]].fix_pos(space[0], space[1])
    
    print(space)
    return board[space[0]][space[1]]
def get_piece_to_play(board, color, is_in_check):
    if is_in_check:
        k_row, k_col=find_king(board, color)
        return board[k_row][k_col]
    else:
        while True:
            print_board(board)
            if color==0: print('It\'s WHITE\'s turn!')
            else: print('It\'s BLACK\'s turn!')
            space=get_user_input('What piece will you move?')
            piece=board[space[0]][space[1]]
            if piece.color==color:
                if len(piece.get_possible_moves(board))>0:
                    break
                else:
                    print('It can\'t move. Press Enter')
                    input()
            else:
                print('Not your piece! Press Enter')
                input()
    return piece
def get_user_input(message):
    while True:
        raw=input(message)
        letters=['A','B','C','D','E','F','G','H']
        space=[]
        try:
            letter=raw[0].upper()
            for let in letters:
                if let==letter:
                    space.append(letters.index(letter))
                    break
            else: raise Exception()
            space.insert(0,int(raw[1])-1)
            break
        except:
            print('Invalid input. Correct Syntax: A4\nPress Enter')
            input()
            continue
    print(space)
    return space
def is_valid_position(row, col):
    if row>=8 or row<0 or col>=8 or col<0:
        return False
    return True
def is_checkmate(board, color):
    k_row, k_col=find_king(board, color)
    king_moves=board[k_row][k_col].get_possible_moves(board, True)
    if len(king_moves)==0: return True
    print('remaining:', king_moves)
    return len(king_moves)==0

def find_king(board, color):
    for row in board:
        for space in row:
            if space.piece==6 and space.color==color:
                return (space.row, space.col)
def is_check(board, last_moved_piece, color_of_king):
    moves=last_moved_piece.get_possible_moves(board)
    temp_list=list(find_king(board, color_of_king))
    temp_list.append(True)
    if tuple(temp_list) in moves:
        #if the king is in the piece's moveset
        print(color_of_king, 'IS IN CHECK')
        return True
    return False
#main
board=[[Piece(0,-2,row,col) for col in range(8)] for row in range(8)]
player1='Player 1' #WHITE
player2='Player 2' #BLACK
WHITE=0
BLACK=1
is_p1_turn=False
is_p1_check=False
is_p2_check=False
winner=-1
if __name__ == '__main__':
    print('*'*50, '\nChess v1.1\nBy Matt Spooner\n'+('*'*50))
    input('Press Enter to Start')
    #board[5][5]=Piece(6,1,5,5)
    #board[7][2]=Piece(4,0,7,2)
    #board[6][6]=Piece(4,0,6,6)
    #board[6][7]=Piece(2,0,6,7)
    #print_possibles(board, board[6][7].get_possible_moves(board))
    setup_board(board)
    while True:
        #TODO: put it all together
        is_p1_turn=not is_p1_turn
        if is_p1_turn:
            moved_piece=move_piece(get_piece_to_play(board, WHITE, is_p1_check), board)
            is_p2_check=is_check(board, moved_piece, BLACK)
        else:
            moved_piece=move_piece(get_piece_to_play(board, BLACK, is_p2_check), board)
            is_p1_check=is_check(board, moved_piece, WHITE)
        if is_checkmate(board, WHITE):
            winner=0
            break
        if is_checkmate(board,BLACK):
            winner=1
            break
    print('GAME END')
    print('WINNER IS:', winner if 'BLACK' else 'WHITE')
    '''