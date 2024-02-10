"""
Tic Tac Toe Player
"""

import math
import unittest
from copy import copy, deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    #print ("PLAYER", board)

    """
    Returns player who has the next turn on a board.
    """
    count_empty = 0
    for i in board:
        for y in i:
            if y == EMPTY:
                count_empty += 1

    # Assumes starting player is always X
    if (count_empty % 2) == 0:
        return O
    else:
        return X
    
    


def actions(board):

    """
    Returns set of all possible actions (i, j) available on the board.
    """
    s = set()
    for x in range(0,3):
        for y in range(0,3):
            if board[x][y] == EMPTY:
                s.add((x,y))

    #print ("ACTIONS", s, board)
    return s




def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = deepcopy(board)

    # Get next player
    p = player(board)

    #print ("RESULT", p, board, action)
    (x,y) = action

    # Should really validate the x and y values here

    new_board[x][y] = p
    
    return new_board


def winner(board):
    #print ("WINNER", board)

    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for x in range(0,3):
        x_count = 0
        o_count = 0
        for y in range(0,3):
            if board[x][y] == X:
                x_count += 1
            elif board[x][y] == O:
                o_count += 1
    
        if o_count == 3:
            return O
        elif x_count == 3:
            return X

    # Check columns
    for y in range(0,3):
        x_count = 0
        o_count = 0
        for x in range(0,3):
            if board[x][y] == X:
                x_count += 1
            elif board[x][y] == O:
                o_count += 1

        if o_count == 3:
            return O
        elif x_count == 3:
            return X

    # Check  diagonals 
    x_count = 0
    o_count = 0
    for y in range(0,3):
        if board[y][y] == X:
            x_count += 1
        elif board[y][y] == O:
            o_count += 1

        if o_count == 3:
            return O
        elif x_count == 3:
            return X

    
    x_count = 0
    o_count = 0
    for y in reversed(range(0,3)):
        if board[2-y][y] == X:
            x_count += 1
        elif board[2-y][y] == O:
            o_count += 1

        if o_count == 3:
            return O
        elif x_count == 3:
            return X
    

    return None

def terminal(board):
    #print ("TERMINAL", board)

    """
    Returns True if game is over, False otherwise.
    """
    count_empty = 0
    for i in board:
        for y in i:
            if y == EMPTY:
                count_empty += 1

    w = winner(board)

    return ((count_empty == 0) or (w != None))


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    a =  winner(board)

    if a == X:
        return 1
    elif a == O:
        return -1
    else:
        return 0
    
def min_value(board):
    if terminal(board):
        return utility(board)
    
    v = 1000
    acts = actions(board)
    for a in acts:
        v = min(v, max_value(result(board, a)))

    return v

def max_value(board):
    if terminal(board):
        return utility(board)
    
    v = -1000

    acts = actions(board)

    for a in acts:
        v = max(v, min_value(result(board, a)))

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    p = player(board)
    acts = actions(board)
    print ('MINIMAX', p, acts, board)

    best_move = None
    set_move = set()
    if p == X:
        print ("BOARD", board, acts, p)
        for a in acts:
            v = min_value(result(board, a))
            print ("RESULTOOO", (p,a,v))
            set_move.add((a,v))
        max = -1000
        best_move = None
        for i in set_move:
            (a,v) = i
            if v >= max:
                max = v
                best_move = a

    elif p == O:
        for a in acts:
            v = max_value(result(board, a))



            set_move.add((a,v))
        min = 1000
        best_move = None
        for i in set_move:
            (a,v) = i
            if v <= min:
                min = v
                best_move = a

    print ("MINIMAX_MOVES", set_move, best_move)

    return best_move
        

class TestMinimaxMethods(unittest.TestCase):

    def test_1(self):
        board = initial_state()

        self.assertTrue(board==
         [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]])

        p = player(board)
        self.assertEqual(p, X)

        a = actions(board)
        self.assertEqual(a, {(0, 1), (1, 2), (2, 1), (0, 0), (1, 1), (2, 0), (0, 2), (2, 2), (1, 0)})

        board = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, X, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

        p = player(board)
        self.assertEqual(p, O)

        board = [[EMPTY, EMPTY, EMPTY],
                 [EMPTY, X,     O],
                 [EMPTY, EMPTY, EMPTY]]
        
        p = player(board)
        self.assertEqual(p, X)


        a = actions(board)
        self.assertEqual(a, {(0, 1), (2, 1), (0, 0), (2, 0), (0, 2), (2, 2), (1, 0)})

        t = terminal(board)
        self.assertEqual(t, False)

        board = [[X, X, X],
                 [O, X, O],
                 [O, O, O]]
        
        t = terminal(board)
        self.assertEqual(t, True)


        # No Win
        w = winner([[X, O, X],
                    [X, O, X],
                    [O, X, O]])
        self.assertTrue(w == None)

        w = winner( [[X, O, O],
                     [O, X, X],
                     [O, X, O]])
        print ('WINNER', w)
        self.assertTrue(w == None)

        

        # X Win
        w = winner( [[X, O, X],
                     [O, X, O],
                     [O, O, X]])
        self.assertTrue(w == X)

        w = winner( [[O, O, X],
                     [O, X, O],
                     [X, O, O]])
        self.assertTrue(w == X)
        w = winner( [[X, X, X],
                     [X, O, O],
                     [O, O, X]])
        self.assertTrue(w == X)
        w = winner( [[X, O, O],
                     [X, X, X],
                     [O, O, X]])
        self.assertTrue(w == X)
        w = winner( [[X, O, X],
                     [O, X, X],
                     [O, O, X]])
        self.assertTrue(w == X)
        w = winner( [[X, O, X],
                     [O, X, O],
                     [X, X, X]])
        self.assertTrue(w == X)
        w = winner( [[X, O, X],
                     [X, X, O],
                     [X, O, X]])
        self.assertTrue(w == X)
        w = winner( [[O, X, X],
                     [O, X, O],
                     [X, X, X]])
        self.assertTrue(w == X)

        # O Win
        w = winner( [[O, O, O],
                     [X, X, O],
                     [O, EMPTY, X]])
        print ('WINNER', w)
        self.assertTrue(w == O)
        w = winner( [[X, X, O],
                     [X, O, O],
                     [O, O, X]])
        print ('WINNER', w)
        self.assertTrue(w == O)
        w = winner( [[O, X, O],
                     [X, X, O],
                     [O, O, O]])
        print ('WINNER', w)
        self.assertTrue(w == O)
        w = winner( [[O, O, X],
                     [X, X, O],
                     [O, O, O]])
        print ('WINNER', w)
        self.assertTrue(w == O)
        w = winner( [[O, O, X],
                     [O, O, O],
                     [X, X, O]])
        print ('WINNER', w)
        self.assertTrue(w == O)
        w = winner( [[O, O, X],
                     [O, X, O],
                     [O, O, X]])
        print ('WINNER', w)
        self.assertTrue(w == O)


        board = result([[EMPTY, EMPTY, EMPTY],
                        [EMPTY, EMPTY, EMPTY],
                        [EMPTY, EMPTY, EMPTY]], (1,1))
        self.assertEqual(board, [[EMPTY, EMPTY, EMPTY],
                                 [EMPTY, X, EMPTY],
                                 [EMPTY, EMPTY, EMPTY]])
        board = result([[EMPTY, EMPTY, EMPTY],
                        [EMPTY, X, EMPTY],
                        [EMPTY, EMPTY, EMPTY]], (0,0))
        self.assertEqual(board, [[O, EMPTY, EMPTY],
                                 [EMPTY, X, EMPTY],
                                 [EMPTY, EMPTY, EMPTY]])
        board = result([[O, EMPTY, EMPTY],
                        [EMPTY, X, EMPTY],
                        [EMPTY, EMPTY, EMPTY]], (0,1))
        self.assertEqual(board, [[O, X, EMPTY],
                                 [EMPTY, X, EMPTY],
                                 [EMPTY, EMPTY, EMPTY]])        

        board = [[O, O, X],
                 [X, X, O],
                 [O, O, O]]
        s = utility(board) 
        self.assertEqual(s, -1)

        board = [[O, EMPTY, X],
                 [X, X, X],
                 [O, X, O]]
        s = utility(board) 
        self.assertEqual(s, 1)    

        board = [[X, O, X],
                 [X, O, X],
                 [O, EMPTY, O]]
        s = utility(board) 
        self.assertEqual(s, 0)

        board = [[O,     EMPTY, EMPTY],
                 [X,     O,     EMPTY],
                 [X,     EMPTY, EMPTY]]
        v = min_value(board)
        print (v)
        v = max_value(board)
        print (v)

        board = [[EMPTY, O, X],
                 [X, EMPTY, X],
                 [O, EMPTY, O]]
        

        v = min_value(board)
        print (v)
        v = max_value(board)
        print (v)

        board = [[EMPTY, O,     X],
                 [X,     O,     X],
                 [X,     EMPTY, O]]
        v = min_value(board)
        print (v)
        v = max_value(board)
        print (v)
   
        board = [[None, None, None], ['X', None, None], [None, None, None]]
        v = min_value(board)
        print (v)
        v = max_value(board)
        print (v)


        board = [['X', None, 'X'], ['X', O, None], [O, None, None]]
        v = min_value(board)
        print (v)
        v = max_value(board)
        print (v)

        v = max_value(result(board, (0,1)))
        print ("RESULT", v)

        m = minimax(board)

if __name__ == '__main__':
    unittest.main()


