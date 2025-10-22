import pygame
import math
from backend import WordleGame

BG_COLOR = pygame.Color("#FFFFFF")
BLACK = pygame.Color("#000000")
LIGHT_GRAY = pygame.Color("#d3d6da")
GREEN = pygame.Color("#6aaa64")
YELLOW = pygame.Color("#c9b458")
DARK_GRAY = pygame.Color("#787c7e")
BORDER = pygame.Color("#878a8c")
class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color=BLACK, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.hover_color = hover_color
        self.current_color = color
        self.text_color = text_color
        self.action = action
    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    def isPressed(self, x, y):
        return self.rect.collidepoint(x, y)
class WordleFrontend:
    def __init__(self, word_list):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 830))
        pygame.display.set_caption("Wordle")
        self.font = pygame.font.Font('assets/FreeSansBold.ttf', 30)
        self.small_font = pygame.font.Font('assets/FreeSansBold.ttf', 13)
        self.word_list = word_list
        self.reset_game()
    def reset_game(self):
        self.game = WordleGame(self.word_list)
        print('New secret word is:', self.game.get_secret_word())
        self.current_guess = ""
        #Bounce animation
        self.bounce_state = [0] * 5
        self.bounce_time = 200
        self.bounce_max_scale = 1.1
        self.clock = pygame.time.Clock()
        
        #Shake animation
        self.shake_state = 0
        self.shake_time = 400
        self.shake_magnitude = 10
        
        #Flip animation
        self.flip_state = [0] * 5
        self.flip_time = 500
        self.flip_delay = 300
        self.flipping_row_index = -1
        
        self.key_colors = {}
        self.buttons = []
    def draw_board(self):
        dt = self.clock.tick(60)
        for i in range(len(self.bounce_state)):
            if self.bounce_state[i] > 0:
                self.bounce_state[i] -= dt
                if self.bounce_state[i] < 0:
                    self.bounce_state[i] = 0
        if self.shake_state > 0:
            self.shake_state -= dt
            if self.shake_state < 0:
                self.shake_state = 0
        all_flips_done = True
        if self.flipping_row_index != -1:
            feedback = self.game._get_feedback(self.game.guesses[self.flipping_row_index])
            guess = self.game.guesses[self.flipping_row_index]
            for i in range(5):
                if self.flip_state[i] > 0:
                    all_flips_done = False
                    old_time = self.flip_state[i]
                    self.flip_state[i] -= dt
                    
                    # half = self.flip_time / 2
                    
                    # if old_time > (self.flip_time + (i * self.flip_delay) - half) and self.flip_state[i] <= (self.flip_time + (i * self.flip_delay) - half):
                    #     letter = guess[i]
                    #     fb = feedback[i]
                    #     current_key_color = self.key_colors.get(letter, LIGHT_GRAY)
                    #     if fb == 'correct':
                    #         self.key_colors[letter] = GREEN
                    #     elif fb == 'present' and current_key_color != GREEN:
                    #         self.key_colors[letter] = YELLOW
                    #     elif fb == 'absent' and current_key_color not in (GREEN, YELLOW):
                    #         self.key_colors[letter] = DARK_GRAY
                    if self.flip_state[i] < 0:
                        self.flip_state[i] = 0
            if all_flips_done:
                guess = self.game.guesses[self.flipping_row_index]
                feedback = self.game._get_feedback(guess)

                for i in range(5):
                    letter = guess[i]
                    fb = feedback[i]
                    current_key_color = self.key_colors.get(letter, LIGHT_GRAY)
                    
                    if fb == 'correct':
                        self.key_colors[letter] = GREEN
                    elif fb == 'present' and current_key_color != GREEN:
                        self.key_colors[letter] = YELLOW
                    elif fb == 'absent' and current_key_color not in (GREEN, YELLOW):
                        self.key_colors[letter] = DARK_GRAY
                self.flipping_row_index = -1
        keyboard = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        self.buttons = []
        self.screen.fill(BG_COLOR)
        SCREEN_WIDTH = self.screen.get_width()
        KEY_WIDTH = 45
        KEY_HEIGHT = 55
        KEY_GAP = 5
        KEY_PITCH = KEY_WIDTH + KEY_GAP
        
        ENTER_WIDTH = 100
        DEL_WIDTH = 100
        
        rows_widths = []
        
        for i, keys in enumerate(keyboard):
            if i == 0:
                width = (10 * KEY_WIDTH) + (9 * KEY_GAP)
            if i == 1:
                width = (9 * KEY_WIDTH) + (8 * KEY_GAP)
            if i == 2:
                width = DEL_WIDTH + KEY_GAP + (7 * KEY_WIDTH) + (6 * KEY_GAP) + KEY_GAP + ENTER_WIDTH
            rows_widths.append(width)
        
        for row, keys in enumerate(keyboard):
            cur_row_width = rows_widths[row]
            start_x = (SCREEN_WIDTH - cur_row_width) / 2
            y = 625 + (row * 60)
            cur_x = start_x
            if row == 2:
                button = Button(cur_x, y, DEL_WIDTH, KEY_HEIGHT, "Delete", self.font, LIGHT_GRAY, DARK_GRAY)
                self.buttons.append(button)
                cur_x += DEL_WIDTH + KEY_GAP
            for col, key in enumerate(keys):
                x = cur_x + (col * KEY_PITCH)
                key_color = self.key_colors.get(key, LIGHT_GRAY)
                text_color = BLACK if key_color == LIGHT_GRAY else BG_COLOR
                button = Button(x, y, KEY_WIDTH, KEY_HEIGHT, key, self.font, key_color, DARK_GRAY, text_color)
                self.buttons.append(button)
            if row == 2:
                last_letter_x = cur_x + ((len(keys) - 1) * KEY_PITCH)
                last_letter_end_x = last_letter_x + KEY_WIDTH
                enter_x = last_letter_end_x + KEY_GAP
                
                button = Button(enter_x, y, ENTER_WIDTH, KEY_HEIGHT, "Enter", self.font, LIGHT_GRAY, DARK_GRAY)
                self.buttons.append(button)
        for button in self.buttons:
            button.draw(self.screen)
        for row in range(6):
            x_offset = 0
            if row == len(self.game.guesses) and self.shake_state > 0:
                time = (self.shake_time - self.shake_state) / self.shake_time
                x_offset = self.shake_magnitude * math.sin(time * math.pi * 8) * (1.0 - time)
            for col in range(5):
                x = col * 100 + 55 + x_offset
                y = row * 100 + 20
                if row == self.flipping_row_index:
                    time_left = self.flip_state[col]
                    total_time = self.flip_time + (col * self.flip_delay)
                    time_elapsed = total_time - time_left
                    flip_progress = (time_elapsed - (col * self.flip_delay)) / self.flip_time
                    flip_progress = min(1.0, max(0.0, flip_progress))
                    
                    scale_y_box = 1.0
                    if flip_progress > 0:
                        if flip_progress < 0.5:
                            scale_y_box = 1.0 - (flip_progress * 2)
                        else:
                            scale_y_box = (flip_progress - 0.5) * 2
                            
                    cur_h = 90 * scale_y_box
                    cur_y = y + (90 - cur_h) / 2
                    cur_rect = pygame.Rect(x, cur_y, 90, cur_h)
                    
                    letter_to_draw = self.game.guesses[row][col]
                    if flip_progress >= 0.5:
                        guess = self.game.guesses[row]
                        feedback = self.game._get_feedback(guess)
                        color = LIGHT_GRAY
                        if feedback[col] == 'correct':
                            color = GREEN
                        elif feedback[col] == 'present':
                            color = YELLOW
                        elif feedback[col] == 'absent':
                            color = DARK_GRAY
                        pygame.draw.rect(self.screen, color, cur_rect)
                        if cur_h > 5:
                            original_surf = self.font.render(letter_to_draw, True, BG_COLOR)
                            original_size = original_surf.get_size()
                            
                            scaled_h = int(original_size[1] * scale_y_box)
                            if scaled_h < 1:
                                scaled_h = 1
                            scaled_surf = pygame.transform.smoothscale(original_surf, (original_size[0], scaled_h))
                            scaled_rect = scaled_surf.get_rect(center=cur_rect.center)
                            self.screen.blit(scaled_surf, scaled_rect)
                    else:
                        pygame.draw.rect(self.screen, BG_COLOR, cur_rect)
                        pygame.draw.rect(self.screen, BORDER, cur_rect, 2)
                        if cur_h > 5:
                            original_surf = self.font.render(letter_to_draw, True, BLACK)
                            original_size = original_surf.get_size()
                            
                            scaled_h = int(original_size[1] * scale_y_box)
                            if scaled_h < 1:
                                scaled_h = 1
                            scaled_surf = pygame.transform.smoothscale(original_surf, (original_size[0], scaled_h))
                            scaled_rect = scaled_surf.get_rect(center=cur_rect.center)
                            self.screen.blit(scaled_surf, scaled_rect)
                else:
                    base_rect = pygame.Rect(x, y, 90, 90)
                    pygame.draw.rect(self.screen, BG_COLOR, base_rect)
                    
                    cur_x = x
                    cur_y = y
                    cur_w = 90
                    cur_h = 90
                    if row == len(self.game.guesses) and col < len(self.current_guess) and self.bounce_state[col] > 0:
                        time = self.bounce_time - self.bounce_state[col]
                        if time < self.bounce_time / 2:
                            scale = 1 + (self.bounce_max_scale - 1) * (time / (self.bounce_time / 2))
                        else:
                            scale = self.bounce_max_scale - (self.bounce_max_scale - 1) * ((time - self.bounce_time / 2) / (self.bounce_time / 2))
                        cur_w = 90 * scale
                        cur_h = 90 * scale
                        cur_x = x - (cur_w - 90) / 2
                        cur_y = y - (cur_h - 90) / 2
                    rect = pygame.Rect(cur_x, cur_y, cur_w, cur_h)
                    
                    if row == len(self.game.guesses) and col < len(self.current_guess):
                        pygame.draw.rect(self.screen, BORDER, rect, 2)
                    else:
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

                        # for keyboard_row, keys in enumerate(keyboard):
                        #     for keyboard_col, key in enumerate(keys):
                        #         if key == guess[col]:
                        #             keyboard_x = keyboard_col * 50 + 55 + (keyboard_row * 35)
                        #             keyboard_y = 625 + (keyboard_row * 60)
                        #             key_rect = pygame.Rect(keyboard_x, keyboard_y, 45, 55)
                        #             if feedback[col] == 'correct':
                        #                 pygame.draw.rect(self.screen, GREEN, key_rect)
                        #             elif feedback[col] == 'present':
                        #                 if self.screen.get_at(key_rect.topleft) != GREEN:
                        #                     pygame.draw.rect(self.screen, YELLOW, key_rect)
                        #             elif feedback[col] == 'absent':
                        #                 if self.screen.get_at(key_rect.topleft) not in (GREEN, YELLOW):
                        #                     pygame.draw.rect(self.screen, DARK_GRAY, key_rect)
                        #             letter_surf = self.font.render(key, True, BG_COLOR)
                        #             letter_rect = letter_surf.get_rect(center=key_rect.center)
                        #             self.screen.blit(letter_surf, letter_rect)
                    elif row == len(self.game.guesses):
                        if col < len(self.current_guess):
                            pygame.draw.rect(self.screen, BORDER, rect, 2)
                            letter_surf = self.font.render(self.current_guess[col], True, BLACK)
                            letter_rect = letter_surf.get_rect(center=rect.center)
                            self.screen.blit(letter_surf, letter_rect)
        
        pygame.display.flip()
    # (Bạn có thể thêm hàm này vào ngay sau hàm game_over_screen)
    
    def show_message_box(self, message):

        background_copy = self.screen.copy() 
        clock = self.clock

        text_surf = self.small_font.render(message, True, BG_COLOR)
        rect_w = text_surf.get_width() + 20 
        rect_h = 30
        rect_x = (self.screen.get_width() - rect_w) / 2

        start_y = -rect_h
        end_y = 15
        cur_y = start_y
        animation_speed = 120 
        
        aim_loop = True
        while aim_loop:
            dt_sec = clock.tick(60) / 1000.0
            cur_y += animation_speed * dt_sec
            if cur_y >= end_y:
                cur_y = end_y
                aim_loop = False
            
            self.screen.blit(background_copy, (0, 0)) 
            rect = pygame.Rect(rect_x, cur_y, rect_w, rect_h)
            pygame.draw.rect(self.screen, BLACK, rect)
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect) 
            pygame.display.flip()
        pause_time = 1000
        time_elapsed = 0
        pause_loop = True
        while pause_loop:
            dt_ms = clock.tick(60)
            time_elapsed += dt_ms
            if time_elapsed >= pause_time:
                pause_loop = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            
            rect = pygame.Rect(rect_x, end_y, rect_w, rect_h)
            pygame.draw.rect(self.screen, BLACK, rect)
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
            pygame.display.flip()
            
    def input_handle(self, event):
        if self.flipping_row_index != -1:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for button in self.buttons:
                if button.isPressed(x, y):
                    if button.text == "Enter":
                        if len(self.current_guess) == 5:
                            try:
                                self.game.make_guess(self.current_guess)
                                self.flipping_row_index = len(self.game.guesses) - 1
                                for i in range(5):
                                    self.flip_state[i] = self.flip_time + i * self.flip_delay
                                self.current_guess = ""
                                self.bounce_state = [0] * 5
                            except ValueError as e:
                                print(e)
                                self.shake_state = self.shake_time
                        else:
                            self.shake_state = self.shake_time
                    elif button.text == "Delete":
                        if len(self.current_guess) > 0:
                            self.bounce_state[len(self.current_guess) - 1] = 0
                            self.current_guess = self.current_guess[:-1]
                    else:
                        if len(self.current_guess) < 5 and button.text.isalpha():
                            self.current_guess += button.text.upper()
                            self.bounce_state[len(self.current_guess) - 1] = self.bounce_time
                    return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.bounce_state[len(self.current_guess) - 1] = 0
                self.current_guess = self.current_guess[:-1]
            elif event.key == pygame.K_RETURN:
                if len(self.current_guess) == 5:
                    try:
                        self.game.make_guess(self.current_guess)
                        self.flipping_row_index = len(self.game.guesses) - 1
                        for i in range(5):
                            self.flip_state[i] = self.flip_time + i * self.flip_delay
                        self.current_guess = ""
                        self.bounce_state = [0] * 5
                    except ValueError as e:
                        print(e)
                        self.shake_state = self.shake_time
                else:
                    self.shake_state = self.shake_time
            else:
                if len(self.current_guess) < 5 and event.unicode.isalpha():
                    self.current_guess += event.unicode.upper()
                    self.bounce_state[len(self.current_guess) - 1] = self.bounce_time
    def game_over_screen(self):
        background_copy = self.screen.copy()
        clock = self.clock
        
        rect_w = 80
        rect_h = 30
        rect_x = (self.screen.get_width() - rect_w) / 2
        start_y = -rect_h
        end_y = 15
        cur_y = start_y
        animation_speed = 120
        ratings = ["Genius", "Magnificent", "Impressive", "Splendid", "Great", "Phew"]
        if self.game.guesses and self.game.guesses[-1] == self.game.get_secret_word():
            rating = ratings[len(self.game.guesses) - 1]
        else:
            rating = self.game.get_secret_word()
        
        text_surf = self.small_font.render(rating, True, BG_COLOR)
        
        aim_loop = True
        while aim_loop:
            dt_sec = clock.tick(60) / 1000.0
            cur_y += animation_speed * dt_sec
            if cur_y >= end_y:
                cur_y = end_y
                aim_loop = False
            self.screen.blit(background_copy, (0, 0))
            rect = pygame.Rect(rect_x, cur_y, rect_w, rect_h)
            pygame.draw.rect(self.screen, BLACK, rect)
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
            pygame.display.flip()
        pause_time = 1000
        time_elapsed = 0
        pause_loop = True
        while pause_loop:
            dt_ms = clock.tick(60)
            time_elapsed += dt_ms
            if time_elapsed >= pause_time:
                pause_loop = False
            self.screen.blit(background_copy, (0, 0))
            rect = pygame.Rect(rect_x, end_y, rect_w, rect_h)
            pygame.draw.rect(self.screen, BLACK, rect)
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
            pygame.display.flip()
            
        self.screen.blit(background_copy, (0, 0))
        overlay = pygame.Surface(self.screen.get_size())
        overlay.fill(BG_COLOR)
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))
        button_width = 200
        button_height = 60
        button_x = (self.screen.get_width() - button_width) / 2
        button_y = (self.screen.get_height() - button_height) / 2
        replay_button = Button(button_x, button_y, button_width, button_height, "PLAY AGAIN", self.font, DARK_GRAY, LIGHT_GRAY, BG_COLOR)
        quit_button = Button(button_x, button_y + 80, button_width, button_height, "QUIT", self.font, DARK_GRAY, LIGHT_GRAY, BG_COLOR)
        text = "THE ANSWER IS: " + self.game.get_secret_word()
        text_surf = self.font.render(text, True, BLACK)
        text_rect = text_surf.get_rect(center=(self.screen.get_width() / 2, button_y - 100))
        self.screen.blit(text_surf, text_rect)
        pygame.display.flip()
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            if replay_button.rect.collidepoint(mouse_pos):
                replay_button.current_color = replay_button.hover_color
            else:
                replay_button.current_color = DARK_GRAY
            replay_button.draw(self.screen)
            
            mouse_pos = pygame.mouse.get_pos()
            if quit_button.rect.collidepoint(mouse_pos):
                quit_button.current_color = quit_button.hover_color
            else:
                quit_button.current_color = DARK_GRAY
            quit_button.draw(self.screen)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_button.rect.collidepoint(event.pos):
                        return 'replay'
                    elif quit_button.rect.collidepoint(event.pos):
                        return 'quit'
    def run(self):
        play_again = True
        while play_again:
            self.reset_game()
            game_running = True
            while game_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        raise SystemExit
                    else:
                        self.input_handle(event)
                self.draw_board()
                if self.game.is_game_over() and self.flipping_row_index == -1:
                    game_running = False
                pygame.display.flip()
            action = self.game_over_screen()
            if action == 'quit':
                play_again = False
        pygame.quit()
        