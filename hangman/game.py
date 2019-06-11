from .exceptions import *
import random


class GuessAttempt(object):
    def __init__(self, guess,hit=None, miss=None):
        self.guess = guess
        self.hit = hit
        self.miss = miss
        
        if self.hit != None and self.miss != None:
            raise InvalidGuessAttempt()
            
    def is_hit(self):
        if self.hit:
            return True
        return False
    
    def is_miss(self):
        if self.miss:
            return True
        return False
    

class GuessWord(object):
    def __init__(self, answer):
        self.answer = answer
        self.masked = len(self.answer) * '*'
        
        if self.answer == '':
            raise InvalidWordException()
    
    def perform_attempt(self, attempt):
        if len(attempt) > 1:
            raise InvalidGuessedLetterException()

        if attempt.lower() in self.answer.lower():
            attempt = attempt.lower()
            result = []
            
            for index, letter in enumerate(self.answer):
                if letter.lower() == attempt:
                    result.append(index)
                
            for location in result:
                self.masked = self.masked[:location] + attempt + self.masked[location + 1:]
            return (GuessAttempt(attempt, hit=True))
        else:
            return (GuessAttempt(attempt, miss=True))

        
class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self, list_of_words=[], number_of_guesses=5):
        self.words = list_of_words
        if not list_of_words:
            list_of_words = HangmanGame.WORD_LIST
        self.chosen_word = HangmanGame.select_random_word(list_of_words)
        self.word = GuessWord(self.chosen_word)
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.is_finished_flag = None

    def guess(self, guess):
        self.previous_guesses.append(guess.lower())
        guess_try = self.word.perform_attempt(guess)

        if self.is_finished_flag == True:
            raise GameFinishedException

        if guess_try.is_miss() == True:
            self.remaining_misses -= 1
            if self.remaining_misses == 0:
                self.is_finished_flag = True
                raise GameLostException

        if guess_try.is_hit() == True:
            if self.word.answer == self.word.masked:
                self.is_finished_flag = True
                raise GameWonException
        return self.word.perform_attempt(guess)

    @staticmethod
    def select_random_word(list_of_words=[]):
        if list_of_words == []:
            raise InvalidListOfWordsException
        choice = random.choice(list_of_words)
        choice = choice.lower()
        return str(choice)

    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        else:
            return False

    def is_lost(self):
        if self.remaining_misses == 0 and self.word.answer != self.word.masked:
            return True
        else:
            return False

    def is_finished(self):
        if self.is_finished_flag == True:
            return True
        else:
            return False
