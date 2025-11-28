import pygame

from Button import Button


class ProfileScene():
    def __init__(self, window, players):
        self.font = pygame.font.Font("Assets/Fonts/ch.ttf", 52)
        self.window = window
        self.background_image = pygame.image.load("Assets/Images/profile_background.png")
        self.mouse_image = pygame.image.load("Assets/Images/mouse.png")
        self.clicked_image = pygame.image.load("Assets/Images/click.png")
        self.cursor_sound = pygame.mixer.Sound('Assets/Sounds/use_right.wav')
        self.window_width, self.window_height = self.window.get_size()
        self.background_image = pygame.transform.scale(self.background_image, (self.window_width, self.window_height))
        self.mouse_image = pygame.transform.scale(self.mouse_image, (30, 30))
        self.clicked_image = pygame.transform.scale(self.clicked_image, (30, 30))
        self.players = players
        self.buttons= []
        self.player_count = len(players)

        self.functionality = 0
        self.cursor_sound.play()
        self.set_buttons(players)
    def set_buttons(self, players):
        self.player = players
        self.profile_one_button = Button(200, 200, (350, (self.window_height / 2) * 1.1), 5, text="+")
        self.profile_two_button = Button(200, 200, (650, (self.window_height / 2) * 1.1), 5, text="+")
        self.profile_three_button = Button(200, 200, (950, (self.window_height / 2) * 1.1), 5, text="+")
        self.buttons = [self.profile_one_button, self.profile_two_button, self.profile_three_button]
        for i in range(min(len(players), 3)):
            x_coord = 350 + i * 300
            self.buttons[i] = Button(200, 200, (x_coord, (self.window_height / 2) * 1.1), 5,
                                     image_path=players[i].get_img(), label=players[i].get_name())

    def draw(self, pose_landmarks, players):

        self.pose_landmarks = pose_landmarks
        self.players = players
        self.window.blit(self.background_image, (0, 0))
        for i in self.buttons:
            i.draw(self.window)
        if 'RIGHT_THUMB_TIP' in pose_landmarks:
            left_index_x, left_index_y = int(pose_landmarks['RIGHT_THUMB_TIP'][0]), int(
                pose_landmarks['RIGHT_THUMB_TIP'][1])
            mouse_pos = (left_index_y, left_index_x)
            mouse_rect = self.mouse_image.get_rect(center=mouse_pos)

            if self.functionality == 0:
                for i, j in enumerate(self.buttons):
                    if j.check_click(mouse_pos):
                        if len(self.players) < i + 1:
                            self.window.blit(self.clicked_image, mouse_rect)
                            return None, "avatar_view"
                        else:
                            self.window.blit(self.clicked_image, mouse_rect)
                            return self.players[i], "login_view"
                self.window.blit(self.mouse_image, mouse_rect)
            elif self.functionality == 1:
                for i, j in enumerate(self.buttons):
                    if j.check_click(mouse_pos) and len(self.players) >= i + 1:
                        self.window.blit(self.clicked_image, mouse_rect)
                        del self.players[i]
                        return i, "profile_view"
                    elif j.check_click(mouse_pos) and len(self.players) < i + 1:
                        self.window.blit(self.clicked_image, mouse_rect)
                        return None, "profile_view"
                self.window.blit(self.mouse_image, mouse_rect)
        return None, "profile_view"

    def set_functionality(self, index):
        self.functionality = index


