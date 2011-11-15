from random import choice, sample
from string import ascii_lowercase as lowercase_letters

def levenshtein(current_word, next_word):
    if len(current_word) < len(next_word):
        return levenshtein(next_word, current_word)
    if not current_word:
        return len(next_word)
 
    previous_row = xrange(len(next_word) + 1)
    
    for i, c1 in enumerate(current_word):
        current_row = [i + 1]
        for j, c2 in enumerate(next_word):
            insertions = previous_row[j + 1] + 1 
            deletions = current_row[j] + 1       
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]

def average(nums):
    return (sum(nums) + 0.0) / len(nums)

class HiddenWord(str):

    def __init__(self, word, hidden_token=None):
        if hidden_token is None:
            hidden_token = '*'
            
        self.hidden_token = hidden_token
        self.letters = word
        self.used_letters = list()
        self.visible = list()

    def change_visiblity(self, letter):
        if letter in self.used_letters:
            return

        self.used_letters.append(letter)
        
        for x, word_letter in enumerate(self.letters):
            if word_letter == letter:
                self.visible.append(x)

    def is_fully_visible(self):
        return len(self.letters) == len(self.visible)

    def reveal(self):
        return self.letters

    def __eq__(self, word):
        return self.letters == word

    def __str__(self):
        return ''.join([self.letters[x] if x in self.visible else self.hidden_token for x in xrange(len(self.letters))])

class HangmanGame(object):

    def __init__(self, word_list):
        self.word = None
        self.been_words = list()

        words = list()
        
        with open(word_list) as f:
            temp_words = f.readlines()
            words = [word.strip() for word in temp_words]
        self.words = words

    def generate_new_word(self):
        if self.word is not None:
            self.been_words.append(self.words.pop(self.words.index(self.word)))

        self.word = self.random_word()

    def random_word(self):
        return HiddenWord(choice(self.words))
    
    def play(self):
        self.generate_new_word()
        while True:
            
            print 'I am thinking of word that looks like {}'.format(self.word)

            while True:
                print 'You have already used {}'.format(self.word.used_letters)
                guess = raw_input('Your guess :').strip().lower()
                if len(guess) != 1:
                    print 'You\'ve guessed the wrong amount of letters!'
                else:
                    break
            self.word.change_visiblity(guess)
            
            if self.word.is_fully_visible():
                print 'You\'ve won! The word was {}'.format(self.word)
                break
    
    def bot_guess(self, letter):
        before_guess = self.word
        if self.word.is_fully_visible():
            return 0
        if before_guess == self.word.change_visiblity(letter):
            return -1
        else:
            return 1
        
        


class HangmanBot(object):

    def __init__(self, word_list):
        self.game = HangmanGame(word_list)
        self.state = dict()
        self.words = self.game.words
        self.ideals = []
        for letter in lowercase_letters:
            self.state[letter] = 0

    def fitting_words(self, wanted):
        return [word for word in self.words if len(wanted) == len(word) ]
        
    def play(self, amount_of_games):
        for x in xrange(amount_of_games):
            #self.setup()
            self.game.generate_new_word()
            while True:
                for letter in sample(lowercase_letters, len(lowercase_letters)):
                    guess_value = self.game.bot_guess(letter)
                    if guess_value == 0:
                        break
                if guess_value == 0:
                    break
                else:
                    self.state[letter] += guess_value

    def learn(self):
        mean = average(self.state.values())
        ideals = []
        for k, v in self.state.iteritems():
            if v >= mean:
                ideals.append(k)
        with open('learning_file.csv','wb') as f:
            f.write(','.join(ideals))

    def set_ideals(self):
        with open('learning_file.csv') as f:
            self.ideals = [x.strip() for x in f.read().split(',')]

    def play_lev_game(self, word=None):
        """Uselessly slow"""
        
        if word is None:
            self.game.generate_new_word()
        else:
            self.game.word = HiddenWord(word)

        words = self.fitting_words(self.game.word)
        moves = 0
        guess_value = -1
        
        while True:
            words = sorted(words, key=lambda x: levenshtein(self.game.word, x))
            for word in words[:]:
                for letter in [letter for letter in word if letter not in self.game.word.used_letters]:
                    moves += 1
                    guess_value = self.game.bot_guess(letter)
                    if guess_value == 0:
                        break
                words.remove(word)
                if guess_value == 0:
                    break
            if guess_value == 0:
                break
            
        return moves
        

    def play_learned_game(self, word=None):
        """Uses less moves than unlearned method on average"""
        
        if not self.ideals:
            self.set_ideals()

        ideals = self.ideals[:]
        
        lower_copy = [letter for letter in lowercase_letters if letter not in ideals]

        if word is None:
            self.game.generate_new_word()
        else:
            self.game.word = HiddenWord(word)
        moves = 0

        while True:
            if ideals == []:
                for letter in lower_copy:
                    moves += 1
                    guess_value = self.game.bot_guess(letter)
                    if guess_value == 0:
                        break
                
            else:
                for letter in ideals[:]:
                    moves += 1
                    guess_value = self.game.bot_guess(letter)
                    ideals.remove(letter)
                    if guess_value == 0:
                        break
            if guess_value == 0:
                break  

        return moves

    def play_unlearned_game(self, word=None):

        if word is None:
            self.game.generate_new_word()
        else:
            self.game.word = HiddenWord(word)
            
        moves = 0
        
        while True:
            for letter in lowercase_letters:
                moves += 1
                guess_value = self.game.bot_guess(letter)
                if guess_value == 0:
                        break
            if guess_value == 0:
                break
            
        return moves
            
            
if __name__ == '__main__':
    bot = HangmanBot('../WordLists/pocket.txt')
    print 'Time to test my learned vs unlearned playing bot:'
    random_word = bot.game.random_word()
    print 'The word was {}'.format(random_word.reveal())
    print 'Learned : {} moves'.format(bot.play_learned_game(random_word))
    print 'Unlearned : {} moves'.format(bot.play_unlearned_game(random_word))
    #print 'Lev : {} moves'.format(bot.play_lev_game(random_word))

    learned_moves = 0
    unlearned_moves = 0
    lev_moves = 0
    n = 5000
    for x in xrange(n):
        random_word = bot.game.random_word()
        learned_moves += bot.play_learned_game(random_word)
        unlearned_moves += bot.play_unlearned_game(random_word)
        #lev_moves += bot.play_lev_game(random_word)

    print 'Moves using learned method : {}'.format(learned_moves)
    print 'Average moves per word with learned : {}'.format(learned_moves/(n +0.0))
    print 'Moves using unlearned method : {}'.format(unlearned_moves)
    print 'Average moves per word with unlearned : {}'.format(unlearned_moves/(n +0.0))
    print 'The difference was {}'.format(unlearned_moves - learned_moves)
    #print 'Moves using lev method : {}'.format(lev_moves)
