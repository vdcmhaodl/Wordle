import pygame
from backend import WordleGame

BG_COLOR = pygame.Color("#FFFFFF")
BLACK = pygame.Color("#000000")
LIGHT_GRAY = pygame.Color("#d3d6da")
GREEN = pygame.Color("#6aaa64")
YELLOW = pygame.Color("#c9b458")
DARK_GRAY = pygame.Color("#787c7e")
BORDER = pygame.Color("#878a8c")
class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hover_color = hover_color
        self.current_color = color
        self.action = action
    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    def isPressed(self, x, y):
        return self.rect.collidepoint(x, y)
class WordleFrontend:
    def __init__(self, word_list):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 830))
        pygame.display.set_caption("Wordle")
        self.game = WordleGame(word_list)
        self.font = pygame.font.Font('assets/FreeSansBold.ttf', 30)
        self.running = True
        self.current_guess = ""
        
    def draw_board(self):
        keyboard = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        buttons = []
        self.screen.fill(BG_COLOR)
        buttons.append(Button(6.3 * 50 + 55 + (3 * 35), 625 + 2 * 60, 100, 55, "ENTER", self.font, LIGHT_GRAY, DARK_GRAY))
        buttons.append(Button(20, 625 + 2 * 60, 100, 55, "DEL", self.font, LIGHT_GRAY, DARK_GRAY))
        for row, keys in enumerate(keyboard):
            for col, key in enumerate(keys):
                x = col * 50 + 55 + (row * 35)
                y = 625 + (row * 60)
                button = Button(x, y, 45, 55, key, self.font, LIGHT_GRAY, DARK_GRAY)
                buttons.append(button)
        for button in buttons:
            button.draw(self.screen)
    
        for row in range(6):
            for col in range(5):
                x = col * 100 + 55
                y = row * 100 + 20
                rect = pygame.Rect(x, y, 90, 90)
                pygame.draw.rect(self.screen, BG_COLOR, rect)
                pygame.draw.rect(self.screen, LIGHT_GRAY, rect, 2)
                
                if row < len(self.game.guesses):
                    guess = self.game.guesses[row]
                    feedback = self.game._get_feedback(guess)
                    color = LIGHT_GRAY
                    if feedback[col] == 'correct':
                        color = GREEN
                    elif feedback[col] == 'present':
                        color = YELLOW
                    elif feedback[col] == 'absent':
                        color = DARK_GRAY
                    pygame.draw.rect(self.screen, color, rect)
                    letter_surf = self.font.render(guess[col], True, BG_COLOR)
                    letter_rect = letter_surf.get_rect(center=rect.center)
                    self.screen.blit(letter_surf, letter_rect)
                    for keyboard_row, keys in enumerate(keyboard):
                        for keyboard_col, key in enumerate(keys):
                            if key == guess[col]:
                                keyboard_x = keyboard_col * 50 + 55 + (keyboard_row * 35)
                                keyboard_y = 625 + (keyboard_row * 60)
                                key_rect = pygame.Rect(keyboard_x, keyboard_y, 45, 55)
                                if feedback[col] == 'correct':
                                    pygame.draw.rect(self.screen, GREEN, key_rect)
                                elif feedback[col] == 'present':
                                    if self.screen.get_at(key_rect.topleft) != GREEN:
                                        pygame.draw.rect(self.screen, YELLOW, key_rect)
                                elif feedback[col] == 'absent':
                                    if self.screen.get_at(key_rect.topleft) not in (GREEN, YELLOW):
                                        pygame.draw.rect(self.screen, DARK_GRAY, key_rect)
                                letter_surf = self.font.render(key, True, BG_COLOR)
                                letter_rect = letter_surf.get_rect(center=key_rect.center)
                                self.screen.blit(letter_surf, letter_rect)
    
                elif row == len(self.game.guesses):
                    if col < len(self.current_guess):
                        pygame.draw.rect(self.screen, BORDER, rect, 2)
                        letter_surf = self.font.render(self.current_guess[col], True, BLACK)
                        letter_rect = letter_surf.get_rect(center=rect.center)
                        self.screen.blit(letter_surf, letter_rect)
        
        pygame.display.flip()
    def input_handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            keyboard = [
                "QWERTYUIOP",
                "ASDFGHJKL",
                "ZXCVBNM"
            ]
            for row, keys in enumerate(keyboard):
                for col, key in enumerate(keys):
                    bx = col * 50 + 55 + (row * 35)
                    by = 625 + (row * 60)
                    button_rect = pygame.Rect(bx, by, 45, 55)
                    if button_rect.collidepoint(x, y):
                        if len(self.current_guess) < 5:
                            self.current_guess += key
            enter_rect = pygame.Rect(6.3 * 50 + 55 + (3 * 35), 625 + 2 * 60, 100, 55)
            backspace_rect = pygame.Rect(20, 625 + 2 * 60, 100, 55)
            if enter_rect.collidepoint(x, y):
                if len(self.current_guess) == 5:
                    try:
                        self.game.make_guess(self.current_guess)
                        self.current_guess = ""
                    except ValueError as e:
                        print(e)
            if backspace_rect.collidepoint(x, y):
                self.current_guess = self.current_guess[:-1]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.current_guess = self.current_guess[:-1]
            elif event.key == pygame.K_RETURN:
                if len(self.current_guess) == 5:
                    try:
                        self.game.make_guess(self.current_guess)
                        self.current_guess = ""
                    except ValueError as e:
                        print(e)
            else:
                if len(self.current_guess) < 5 and event.unicode.isalpha():
                    self.current_guess += event.unicode.upper()
    def game_over_screen(self):
        self.screen.fill(BG_COLOR)
        ex = "Press any key to exit."
        if self.game.guesses and self.game.guesses[-1] == self.game.get_secret_word():
            text = "Congratulations! You've guessed the word!"
        else:
            text = f"Game over! The secret word was: {self.game.get_secret_word()}"
        text_surf = self.font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=(300, 350))
        self.screen.blit(text_surf, text_rect)
        ex_surf = self.font.render(ex, True, BLACK)
        ex_rect = ex_surf.get_rect(center=(300, 400))
        self.screen.blit(ex_surf, ex_rect)
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.input_handle(event)
            self.draw_board()
            if self.game.is_game_over():
                self.running = False
            pygame.display.flip()
        self.game_over_screen()
        pygame.quit()
        