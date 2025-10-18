import random

class WordleGame:
    def __init__(self, word_list):
        self.word_list = word_list
        self.secret_word = random.choice(self.word_list).upper()
        self.attempts = 6
        self.guesses = []

    def make_guess(self, guess):
        guess = guess.upper()
        if len(guess) != len(self.secret_word):
            raise ValueError("Guess must be the same length as the secret word.")
        if guess not in self.word_list:
            raise ValueError("Guess must be a valid word from the word list.")
        
        self.guesses.append(guess)
        feedback = self._get_feedback(guess)
        self.attempts -= 1
        return feedback

    def _get_feedback(self, guess):
        feedback = ['absent', 'absent', 'absent', 'absent', 'absent']
        secret = self.secret_word.upper()
        g = guess.upper()
        secret_chars = list(secret)
        for i, ch in enumerate(g):
            if ch == secret_chars[i]:
                feedback[i] = 'correct'
                secret_chars[i] = None
        for i, ch in enumerate(g):
            if feedback[i] == 'correct':
                continue
            if ch in secret_chars:
                feedback[i] = 'present'
                secret_chars[secret_chars.index(ch)] = None
            else:
                feedback[i] = 'absent'

        return feedback

    def is_game_over(self):
        return self.attempts <= 0 or self.guesses and self.guesses[-1] == self.secret_word

    def get_secret_word(self):
        return self.secret_word