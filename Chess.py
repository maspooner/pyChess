class Piece:
    def __init__(self, sym, color):
        self._sym = sym
        self._color = color
        
    def matches(self, other_color):
        return self._color == other_color

    def possible_moves(self, pos, board):
        return set(filter(board.valid_pos, self._list_moves(pos, board)))

    def checkable(self):
        return False

    def on_move(self):
        pass

    def print_with_color(self, color):
        return self._sym + color

    def __str__(self):
        return self.print_with_color("+" if self._color else "-")

class EndlessPiece(Piece):
    def __init__(self, sym, color):
        super().__init__(sym, color)

    def _add_moves_direction(self, board, moves, pos, transform):
        test = transform(pos[0], pos[1])
        while board.valid_pos(test) and not board.piece_at(test):
            moves.add(test)
            test = transform(test[0], test[1])
        last = board.piece_at(test)
        if last and not last.matches(self._color):
            moves.add(test)

class Pawn(Piece):
    def __init__(self, color):
        super().__init__("P", color)
        self._has_moved = False

    def _list_moves(self, pos, board):
        x,y = pos
        moves = set()
        direction = 1 if self._color else -1
        onepos = x, y + direction
        twopos = x, y + 2 * direction
        # empty 1 space out
        if not board.piece_at(onepos):
            moves.add(onepos)
            # not moved yet and open two spaces out
            if not self._has_moved and not board.piece_at(twopos):
                moves.add(twopos)
        lc = x + 1, y + direction
        lcp = board.piece_at(lc)
        rc = x - 1, y + direction
        rcp = board.piece_at(rc)
        # capturable
        if lcp and not lcp.matches(self._color):
            moves.add(lc)
        if rcp and not rcp.matches(self._color):
            moves.add(rc)
        return moves

    def on_move(self):
        self._has_moved = True

class Rook(EndlessPiece):
    def __init__(self, color):
        super().__init__("R", color)

    def _list_moves(self, pos, board):
        moves = set()
        self._add_moves_direction(board, moves, pos, lambda x,y: (x - 1, y))
        self._add_moves_direction(board, moves, pos, lambda x,y: (x + 1, y))
        self._add_moves_direction(board, moves, pos, lambda x,y: (x, y - 1))
        self._add_moves_direction(board, moves, pos, lambda x,y: (x, y + 1))
        return moves
    
class Bishop(EndlessPiece):
    def __init__(self, color):
        super().__init__("B", color)
    def _list_moves(self, pos, board):
        moves = set()
        self._add_moves_direction(board, moves, pos, lambda x,y: (x + 1, y - 1))
        self._add_moves_direction(board, moves, pos, lambda x,y: (x - 1, y - 1))
        self._add_moves_direction(board, moves, pos, lambda x,y: (x - 1, y + 1))
        self._add_moves_direction(board, moves, pos, lambda x,y: (x + 1, y + 1))
        return moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__("N", color)

    def _list_moves(self, pos, board):
        x,y = pos
        moves = {(x - 2, y + 1), (x - 2, y - 1),
        (x + 2, y + 1), (x + 2, y - 1),
        (x + 1, y - 2), (x - 1, y - 2),
        (x + 1, y + 2), (x - 1, y + 2)}
        return filter(lambda move: self._can_add(move, board), moves)

    def _can_add(self, new_pos, board):
        p = board.piece_at(new_pos)
        return (not p) or (not p.matches(self._color))

class King(Piece):
    def __init__(self, color):
        super().__init__("K", color)

    def _list_moves(self, pos, board):
        x,y = pos
        moves = {(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
        (x, y - 1), (x, y + 1),
        (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)}
        return filter(lambda move: self._can_add(move, board), moves)

    def _can_add(self, new_pos, board):
        p = board.piece_at(new_pos)
        return (not p) or (p and not p.matches(self._color))

    def checkable(self):
        return True

class Queen(EndlessPiece):
    def __init__(self, color):
        super().__init__("Q", color)

    def _list_moves(self, pos, board):
        moves = set()
        self._add_moves_direction(board, moves, pos, lambda x,y: (x + 1, y - 1))
        self._add_moves_direction(board, moves, pos, lambda x,y: (x - 1, y - 1))
        self._add_moves_direction(board, moves, pos, lambda x,y: (x - 1, y + 1))
        self._add_moves_direction(board, moves, pos, lambda x,y: (x + 1, y + 1))
        self._add_moves_direction(board, moves, pos, lambda x,y: (x - 1, y))
        self._add_moves_direction(board, moves, pos, lambda x,y: (x + 1, y))
        self._add_moves_direction(board, moves, pos, lambda x,y: (x, y - 1))
        self._add_moves_direction(board, moves, pos, lambda x,y: (x, y + 1))
        return moves

class Board:
    # A board is of size 8
    COL_HEADERS = ['A','B','C','D','E','F','G','H']
    def __init__(self):
        # 2D Piece array = board[x][y]
        self._board = [[None] * 8 for _ in range(8)]
        for i in range(8):
            self._set_piece(i, 1, Pawn(True))
            self._set_piece(i, 6, Pawn(False))
        for i in range(2):
            color = i == 0
            row = 0 if color else 7
            self._set_piece(0, row, Rook(color))
            self._set_piece(1, row, Knight(color))
            self._set_piece(2, row, Bishop(color))
            self._set_piece(3, row, King(color))
            self._set_piece(4, row, Queen(color))
            self._set_piece(5, row, Bishop(color))
            self._set_piece(6, row, Knight(color))
            self._set_piece(7, row, Rook(color))

    def valid_pos(self, pos):
        return pos[0] >= 0 and pos[0] < 8 and pos[1] >= 0 and pos[1] < 8
    def piece_at(self, pos):
        return self._board[pos[0]][pos[1]] if self.valid_pos(pos) else None

    def is_check_for(self, color):
        king_pos = self._find_king(color)
        pass

    def is_checkmate_for(self, color):
        king_pos = self._find_king(color)
        pass

    def can_pick_up(self, pos, color):
        piece = self.piece_at(pos)
        return piece.matches(color) if piece else False

    def get_moves_for(self, pos):
        return self.piece_at(pos).possible_moves(pos, self)

    def move(self, fr, to):
        p = self.piece_at(fr)
        self._set_piece(to[0], to[1], p)
        self._set_piece(fr[0], fr[1], None)
        p.on_move()

    def print_highlighed_board(self, highlights):
        print("  ", "  ".join(Board.COL_HEADERS))
        for y in range(8):
            print(y + 1, end=": ")
            for x in range(8):
                # inverted
                p = self.piece_at((x, y))
                if (x, y) in highlights:
                    print(p.print_with_color("!") if p else "!!", end=" ")
                else:
                    print(p if p else "  ", end=" ")
            print()

    def print_board(self):
        self.print_highlighed_board([])

    def _set_piece(self, x, y, to):
        self._board[x][y] = to

    def _find_king(self, color):
        for i in range(8):
            for j in range(8):
                p = self.piece_at((i, j))
                if p and p.matches(color) and p.checkable():
                    return i,j
        return None

def print_error(err):
    print(err)
    #print("(Press ENTER to continue)")
    #input()

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
    # one based system
    y = int(strpos[1]) - 1
    print(x,y)
    return x,y

def get_valid_position(board, pred, message, err_message, print_board):
    picked_valid = False
    while not picked_valid:
        print_board()
        strpos = get_valid_input(can_parse_position,
            "Input a position: ", "Couldn't parse position, use the form 'A3'")
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
        valid_moves = set()
        while not valid_moves:
            pick_up = get_valid_position(board, lambda p: board.can_pick_up(p, turn), 
                "Select a piece to move", "Can't pick up a piece there",
                lambda: board.print_board())
            print("!!!Found ", board.piece_at(pick_up))
            valid_moves = board.get_moves_for(pick_up)
            if not valid_moves:
                print_error("Can't move the piece!")
        print("!!!Found valid moves", valid_moves)
        move_to = get_valid_position(board, lambda p: p in valid_moves,
            "Select a location to move to", "Can't move there",
            lambda: board.print_highlighed_board(valid_moves))
        board.move(pick_up, move_to)
        turn = not turn

if __name__ == '__main__':
    main()
'''
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