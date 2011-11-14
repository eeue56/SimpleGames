from random import sample

class Bagels(object):

    def __init__(self, size=3):
        self.items = list()
        self.size = 3
        self.scores = dict()
    
    def new_game(self):
        self.items = [str(x) for x in sample(xrange(0,10), self.size)]
        self.scores = {'bagels' : 0, 'pico':0, 'fermi':0}

    def how_close(self, guess):

        self.scores = {'bagels' : 0, 'pico':0, 'fermi':0}
        if self.items == guess:
            self.scores['fermi'] = self.size
            return self.scores
        
        if len(guess) != self.size:
            raise ValueError('You can\'t guess more or less things than I contain!')

        
        
        for my_item, guess_item in zip(self.items, guess):
            if my_item == guess_item:
                self.scores['fermi'] += 1
            elif guess_item in self.items:
                self.scores['pico'] += 1

        if all(value == 0 for value in self.scores.values()):
            self.scores['bagels'] = 1
            
        return self.scores
        
            

if __name__ == '__main__':
    while True:
        game = Bagels()
        game.new_game()
        print 'I am thinking of {} numbers...'.format(game.size)
        print 'Enter your guess in order'
        while True:
            guess = raw_input('Enter your next guess: ')
            guess = list(guess)
            try:
                scores = game.how_close(guess)
                if scores['bagels'] == 1:
                    print 'Bagels'
                else:
                    if scores['fermi'] == game.size:
                        print 'You won!'
                        break
                
                    for x in xrange(scores['pico']):
                        print 'pico',
                    for x in xrange(scores['fermi']):
                        print 'fermi',
                    print
            except ValueError:
                print 'Must guess the right amount of numbers!'
        play_again = raw_input('Play again? Y/N : ')
        if play_again.strip().lower() != 'y':
            break
        
    
