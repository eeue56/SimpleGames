from game_exceptions import PieceAlreadyUsed, GameOver

class Piece(object):

    def __init__(self, start_value):
        self.token = start_value

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.token)

    def __add__(self, string):
        return self.__str__() + string

    def __cmp__(self, item):
        return self.token == item

    def __eq__(self, item):
        return self.token == item

    def __ne__(self, item):
        return not self.__eq__(item)

    def change_token(self, new_value):
        self.token = new_value

        
class GameState(object):

    def __init__(self):
        self.state = 0
        self._state_dict = {0:'In game', 1:'Won, finished', 2:'Draw, finished'}
        
    def __str__(self):
        return str(self._state_dict[self.state])

    def __repr__(self):
        return self.__str__()

    def __eq__(self, item):
        return self.state == item

    def change_state(self, new_state):
        if new_state not in self._state_dict.keys():
            raise ValueError('The given state is out of bounds!')
        self.state = new_state

        
class TicTacToeGame(object):

    def __init__(self, size=3, null_token=None):
        if null_token is None:
            null_token = ' '

        self.state = GameState()
        
        self.null_token = null_token    
        self.pieces = [ [Piece(null_token) for x in xrange(size)] for y in xrange(size)]
        self.size = size
        self.winner = null_token
        self._moves = dict()

    def __str__(self):
        string = []
        
        for row in self.pieces:
            string.append(' | '.join(str(item) for item in row))
            string.append('_' * len(string[0]))
            
        return '\n'.join(string)

    def change_piece(self, new_token, x, y):
        if len(self._moves.keys()) + 1 >= self.size**2:
            raise GameOver('There are no more moves to be made!')
        if not self.is_piece_empty(x, y):
            raise PieceAlreadyUsed('There\'s already a token at [{},{}]'.format(x, y))

        self._moves[len(self._moves.keys())] = (new_token, x, y)
        
        self.pieces[x][y].change_token(new_token)
        
        if self.is_won():
            self.state.change_state(1)
        elif self.is_finished():
            self.state.change_state(2)

    def is_piece_empty(self, x, y):
        return self.pieces[x][y] == self.null_token

    def is_finished(self):
        for row in self.pieces:
            for item in row:
                if item.token == self.null_token:
                    return False
        return True
    
    def is_won(self):
        return self._is_any_row_won() or self._is_any_colom_won() or self._is_any_diagonal_won()

    def winning_move(self):
        return self._moves[max(self._moves.keys())]
    
    def _is_any_row_won(self):
        return any(self._is_series_won(row) for row in self.pieces)

    def _is_any_colom_won(self):
        
        coloms = [ [] for x in self.pieces]
        
        for row_index, row in enumerate(self.pieces):
            for item in row:
                coloms[row_index].append(item)

        for colom in coloms:
            if self._is_series_won(colom):
                return True
        return False

    def _is_any_diagonal_won(self):
        items = [ [], [] ]

        number_of_pieces = len(self.pieces)
        for x in xrange(number_of_pieces):
            items[0].append(self.pieces[x][x])

        for x in xrange(number_of_pieces):
            y = (number_of_pieces - 1) - x
            
            items[1].append(self.pieces[x][y])
        
        return any(self._is_series_won(row) for row in items)
        
    def _is_series_won(self, row):
        if self.null_token in row:
            return False

        first_token = row[0]

        for item in row[1:]:
            if item != first_token:
                return False

        self.winner = first_token
        return True
        
            
if __name__ == '__main__':            
    pass
