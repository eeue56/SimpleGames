from random import choice, sample
from string import ascii_lowercase as lowercase_letters
from utils import *
import sys

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

    def characters_left_to_guess(self):
        return self.__str__().count(self.hidden_token)

    def visible_characters(self):
        return [(x, y) for x, y in enumerate(str(self.letters)) if y != self.hidden_token]
    
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
        before_guess = str(self.word)
        self.word.change_visiblity(letter)
        if self.word.is_fully_visible():
            return 0
        if before_guess == str(self.word):
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

    def fitting_words(self, wanted, words=[], been_lengths=[0]):
        """ Returns words of the same length as wanted -
            has basic caching, if the last called wanted word has the same
            as the current wanted, then words is returned without generating
        """
        
        if words is [] or len(wanted) != been_lengths[-1]:
            words = [word for word in self.words if len(wanted) == len(word)]
            been_lengths.append(len(wanted))
        return words
        
    def play_to_learn(self, amount_of_games):
        """ Will play amount_of_games and store information on the letters into
            self.state - this will allow the AI to learn which characters are most
            common
        """
        
        for x in xrange(amount_of_games):
            word = self.game.random_word()
            
            for letter in lowercase_letters:
                self.game.word = HiddenWord(word)
                guess_value = self.game.bot_guess(letter)
                self.state[letter] += guess_value

    def learn(self):
        """ Stores letters from state into a file in order of occurance

        """
        
        ideals = []
        items = sorted(self.state.items(), key=lambda (k, v): (v, k))
        items.reverse()
        for k, v in items:
            ideals.append(k)
        with open('learning_file.csv','wb') as f:
            f.write(','.join(ideals))

    def set_ideals(self):
        """ Opens learning file and sets ideals, if ideals not set, defaults
            to alphabet
        """
        
        try:
            with open('learning_file.csv') as f:
                self.ideals = [x.strip() for x in f.read().split(',')]
        except:
            self.ideals = lowercase_letters

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

    def play_intelligent_lev_game(self, word=None, border=None):
        """ Amazingly fast, averages at 6 moves per word - that's not bad at all!

            Here, I'm using the sorted ideals to check the word until there are border
            letters left to guess (border defaults to len(word)/2, as this was found to be optimum)
            
            Then I'm using the lev algorithm to generate the most likely words
            then using the unprocessed letters from those words to guess

            If no word is passed, one will be generated.
        """
        
        if word is None:
            self.game.generate_new_word()
        else:
            self.game.word = HiddenWord(word)

        if not self.ideals:
            self.set_ideals()

        if border is None:
            border = len(word)/2

        ideals = self.ideals[:]
        moves = 0
        
        while self.game.word.characters_left_to_guess() > border:
            for letter in ideals[:]:
                moves += 1
                guess_value = self.game.bot_guess(letter)
                ideals.remove(letter)
                if guess_value == 1:
                    break
        
        for word in self.advance_fitting_words(self.game.word, border):
            word = [letter for letter in word if letter in ideals]
            for letter in word:
                moves += 1
                guess_value = self.game.bot_guess(letter)
                ideals.remove(letter)
                if guess_value == 0:
                    break
            if guess_value == 0:
                break
            
        return moves
        
    def advance_fitting_words(self, wanted, border=1, words=[]):
        """ This is a bit of cleverness.
            Takes a wanted word, generates a list of words of the same length
            It then searches through those words, if the levenshtein distance
            is less than border, then it checks through that word that the known
            letters of wanted match the letter positions of the given word
            Uses a cache to avoid regenerating stuff
        """
        
        visible_characters = wanted.visible_characters()
        
        if words is []:
            start_out_words = self.fitting_words(wanted)
        else:
            start_out_words = words[:]

        for word in start_out_words:
            if levenshtein(str(wanted), word) <= border:
                valid = True
                for i, letter in visible_characters:
                    if word[i] != letter:
                        valid = False
                        break
                if valid and word not in words:
                    words.append(word)
                elif not valid and word in words:
                    words.remove(word)
        
        return words            

    def play_learned_game(self, word=None):
        """ Plays a game using ideal letters - as generated by the learning algorithm
        """
        
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
            if ideals == [] and lower_copy == []:
                break
            else:
                for letter in ideals[:] + lower_copy[:]:
                    moves += 1
                    guess_value = self.game.bot_guess(letter)
                    if letter in ideals:
                        ideals.remove(letter)
                    else:
                        lower_copy.remove(letter)
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

    def play_random_unlearned_game(self, word=None):
        """Stupidly slow"""
        if word is None:
            self.game.generate_new_word()
        else:
            self.game.word = HiddenWord(word)
            
        moves = 0
        letter_copy = sample(lowercase_letters, len(lowercase_letters))
        while True:
            for letter in letter_copy:
                moves += 1
                guess_value = self.game.bot_guess(letter)
                if guess_value == 0:
                        break
            if guess_value == 0:
                break
            
        return moves
            
            
if __name__ == '__main__':
    import time

    
    bot = HangmanBot('../WordLists/pocket.txt')
    """bot.play_to_learn(7000)
    bot.learn()"""
    print 'Time to test my learned vs unlearned playing bot:'
    #random_word = bot.game.random_word()
    random_word = HiddenWord("postal")
    print 'The word was {}'.format(random_word.reveal())
    print 'Learned : {} moves'.format(bot.play_learned_game(random_word))
    print 'Unlearned : {} moves'.format(bot.play_unlearned_game(random_word))
    print 'Random unlearned : {} moves'.format(bot.play_random_unlearned_game(random_word))
    print 'Lev : {} moves'.format(bot.play_lev_game(random_word))
    print 'InteliLev : {} moves'.format(bot.play_intelligent_lev_game(random_word))

    learned_moves = 0
    learned_time = 0
    unlearned_moves = 0
    unlearned_time = 0
    random_unlearned_moves = 0
    random_unlearned_time = 0
    lev_moves = 0
    lev_time = 0
    intelli_lev_moves = 0
    intelli_lev_time = 0
    
    n = 1000000
    
    for x in xrange(n):
        random_word = bot.game.random_word()

        start_time = time.time()
        learned_moves_this_time = bot.play_learned_game(random_word)
        learned_time += time.time() - start_time

        start_time = time.time()
        unlearned_moves_this_time = bot.play_unlearned_game(random_word)
        unlearned_time += time.time() - start_time

        start_time = time.time()
        intelli_lev_moves_this_time = bot.play_intelligent_lev_game(random_word)
        intelli_lev_time += time.time() - start_time


        learned_moves += learned_moves_this_time

        unlearned_moves += unlearned_moves_this_time

        intelli_lev_moves += intelli_lev_moves_this_time
        
        #random_unlearned_moves += bot.play_random_unlearned_game(random_word)
        #lev_moves += bot.play_lev_game(random_word)

    print
    print 'Moves using learned method : {}'.format(learned_moves)
    print 'Average moves per word with learned : {}'.format(learned_moves/(n +0.0))
    print 'Average time per word : {}'.format(learned_time/n)
    print
    print 'Moves using unlearned method : {}'.format(unlearned_moves)
    print 'Average moves per word with unlearned : {}'.format(unlearned_moves/(n +0.0))
    print 'Average time per word : {}'.format(unlearned_time/n)
    print
    #print 'Moves using random unlearned method : {}'.format(random_unlearned_moves)
    #print 'Average moves per word with random unlearned : {}'.format(random_unlearned_moves/(n +0.0))
    #print
    
    print 'Moves using intelligent lev method : {}'.format(intelli_lev_moves)
    print 'Average moves per word with intelligent lev : {}'.format(intelli_lev_moves/(n +0.0))
    print 'Average time word : {}'.format(intelli_lev_time/n)

