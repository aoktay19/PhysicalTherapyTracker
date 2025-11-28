# This is Scene A
import pygame

from Button import Button


class SettingsScene():
    def __init__(self, window):
        self.font = pygame.font.Font("Assets/Fonts/ch.ttf", 52)
        self.window = window
        self.button_clicked_time = [None]
        self.background_image = pygame.image.load("Assets/Images/backgroundNew.png")
        self.mouse_image = pygame.image.load("Assets/Images/mouse.png")
        self.clicked_image = pygame.image.load("Assets/Images/click.png")
        self.window_width, self.window_height = self.window.get_size()
        self.background_image = pygame.transform.scale(self.background_image, (self.window_width, self.window_height))
        self.mouse_image = pygame.transform.scale(self.mouse_image, (30, 30))
        self.clicked_image = pygame.transform.scale(self.clicked_image, (30, 30))
        self.buttons = []


    def draw(self, pose_landmarks, player):
        if len(self.buttons) == 0:
            y_offset = self.window_height / 2 - 50
            avatar_one = Button(250, 250, (200, 200), 5,
                                 image_path=player.get_img(), label=player.get_name())
            self.buttons.append(avatar_one)
            changeProfileButton = Button(350, 55, (540, y_offset - 55), 5, text="Change Profile")
            deleteProfileButton = Button(350, 55, (540, y_offset + 145), 5, text="Delete Profile")
            resetButton = Button(350, 55, (900, y_offset + 45), 5, text="Reset Progress")
            goBackButton = Button(350, 55, (900, y_offset + 245), 5, text="Main Menu")
            self.buttons += [changeProfileButton, resetButton, deleteProfileButton, goBackButton]
        else:
            avatar_one = Button(250, 250, (200, 200), 5,
                                image_path=player.get_img(), label=player.get_name())
            self.buttons[0] = avatar_one
        self.pose_landmarks = pose_landmarks
        self.window.blit(self.background_image, (0, 0))
        # for i in range(3):
        #     self.buttons[i].draw(self.window)
        for i in self.buttons:
            i.draw(self.window)

        # self.startButton.draw(self.window)
        # self.infoButton.draw(self.window)
        # self.quitButton.draw(self.window)
        if 'RIGHT_THUMB_TIP' in pose_landmarks:
            left_index_x, left_index_y = int(pose_landmarks['RIGHT_THUMB_TIP'][0]), int(
                pose_landmarks['RIGHT_THUMB_TIP'][1])
            mouse_pos = (left_index_y, left_index_x)
            mouseRect = self.clicked_image.get_rect(center=mouse_pos)
            self.window.blit(self.mouse_image, mouseRect)
            if self.buttons[1].check_click(mouse_pos):
                self.window.blit(self.clicked_image, mouseRect)
                return 0, "profile_view"
            elif self.buttons[2].check_click(mouse_pos):
                self.window.blit(self.clicked_image, mouseRect)
                player.reset_progress()
                return player, "login_view"
            elif self.buttons[3].check_click(mouse_pos):
                self.window.blit(self.clicked_image, mouseRect)
                return 1, "profile_view"
            elif self.buttons[4].check_click(mouse_pos):
                self.window.blit(self.clicked_image, mouseRect)
                return player, "login_view"

        return player, "settings_view"
