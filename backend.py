import random

class WordleGame:
    def __init__(self, word_list):
        self.word_list = word_list
        self.secret_word = random.choice(self.word_list)
        self.attempts = 6
        self.guesses = []

    def make_guess(self, guess):
        if len(guess) != len(self.secret_word):
            raise ValueError("Guess must be the same length as the secret word.")
        if guess not in self.word_list:
            raise ValueError("Guess must be a valid word from the word list.")
        
        self.guesses.append(guess)
        feedback = self._get_feedback(guess)
        self.attempts -= 1
        return feedback

    def _get_feedback(self, guess):
        feedback = []
        for i in range(len(guess)):
            if guess[i] == self.secret_word[i]:
                feedback.append('correct')
            elif guess[i] in self.secret_word:
                feedback.append('present')
            else:
                feedback.append('absent')
        return feedback

    def is_game_over(self):
        return self.attempts <= 0 or self.guesses and self.guesses[-1] == self.secret_word

    def get_secret_word(self):
        return self.secret_word