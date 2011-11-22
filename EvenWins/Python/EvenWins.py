from random import randint
import sys
    
class Player(object):
    def __init__(self, name):
        self.name = name

    def amount_to_take(self, items):
        print 'There are {} objects left. How many will you take?'.format(items)
        while True:
            try:
                amount = int(raw_input('Please enter the amount to take :> '))
                break
            except ValueError:
                print 'Not a valid int, please try again!'
        return amount

class EvenWinsBot(Player):

    def __init__(self, name, limit, maximum):
        Player.__init__(self, name)
        self.limit = limit
        self.maximum = maximum

    def amount_to_take(self, items):
        #print 'There are {} objects.'.format(items)
        if items > self.maximum:
            amount = randint(self.limit, self.maximum)
        else:
            if items % 2 == 0:
                amount = 1
            else:
                if items == 1:
                    amount = 1
                else:
                    amount = 2
        #print '{} will take {}'.format(self.name, amount)
        return amount

class EvenWinsGame(object):

    def __init__(self, objects, min_to_take=1, max_to_take=4):
        self.objects = objects
        self.min = min_to_take
        self.max = max_to_take
        self._moves = dict()

    def _remove_objects(self, items, number_to_remove, caller):
        if number_to_remove > items:
            raise ValueError('You can\'t take away more objects than what there are!')
        if number_to_remove > self.max or number_to_remove < self.min:
            raise ValueError('Please take only from the given range')

        self._moves[len(self._moves)] = (caller.name, number_to_remove,)
        items -= number_to_remove

        #if items == 0:
        #    print 'Game won!'
        #print 'There are {} pieces left. Next move :>'.format(items)
        return items

    def play(self, players):
        items = self.objects
        while items > 0:
            for player in players:
                #print '{}\'s turn.'.format(player.name)
                while True:
                    try:
                        amount = player.amount_to_take(items)
                        items = self._remove_objects(items, amount, player)
                        break
                    except ValueError as e:
                        print e.message
                if items == 0:
                    winning_player = player
                    break
        #print '{} won!'.format(winning_player.name)
        return winning_player

if __name__ == '__main__':
    player_one = EvenWinsBot('Durp', 1, 4)
    player_two = EvenWinsBot('Borp', 1, 2)
    player_three = EvenWinsBot('Hurp', 1, 4)
    game = EvenWinsGame(27, 1, 4)
    winners = []
    for x in xrange(9999):
        winners.append(game.play([player_one, player_two, player_three]).name)
    for x in sorted(set(winners)):
        print x,
        print winners.count(x)

"""After doing some research into my bot, I have discovered that being first gives a bit a slight lead over others.
The middle player will win more if there is an odd number of players
I will have to apply proper ML to this class later one, though I haven't got there yet"""
