from backend import WordleGame

def load_word_list():
    with open("words.txt") as f:
        return [line.strip() for line in f.readlines()]
def main():
    word_list = load_word_list()
    game = WordleGame(word_list)
    print("Welcome to Wordle!")
    while not game.is_game_over():
        guess = input(f"You have {game.attempts} attempts left. Enter your guess: ").strip().upper()
        try:
            feedback = game.make_guess(guess)
            print("Feedback:", feedback)
        except ValueError as e:
            print(e)
    if game.guesses and game.guesses[-1] == game.get_secret_word():
        print("Congratulations! You've guessed the word:", game.get_secret_word())
    else:
        print("Game over! The secret word was:", game.get_secret_word())

if __name__ == "__main__":
    main()