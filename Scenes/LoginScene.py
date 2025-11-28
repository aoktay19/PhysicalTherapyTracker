# This is Scene A
import pygame

from Button import Button
from moviepy.editor import VideoFileClip


class LoginScene():
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
        self.startButton = Button(300, 50, (self.window_width / 2, 270), 5, text="Start Session")
        self.infoButton = Button(300, 50, (self.window_width / 2, 370), 5, text="Progression")
        self.settingsButton = Button(300, 50, (self.window_width / 2, 470), 5, text="Settings")
        self.quitButton = Button(300, 50, (self.window_width / 2, 570), 5, text="Quit Game")
        self.buttons = [self.startButton, self.infoButton, self.settingsButton, self.quitButton]
        self.hand_animation_video = VideoFileClip('Assets/Videos/hand_animation.mp4').resize(
            (self.window_width, self.window_height))
        self.animation_is_played = False


    def draw(self, pose_landmarks):

        if not self.animation_is_played:
            self.hand_animation_video.preview()
            self.animation_is_played = True

        self.pose_landmarks = pose_landmarks
        self.window.blit(self.background_image, (0, 0))
        for i in self.buttons:
            i.draw(self.window)

        if 'RIGHT_THUMB_TIP' in pose_landmarks:
            left_index_x, left_index_y = int(pose_landmarks['RIGHT_THUMB_TIP'][0]), int(
                pose_landmarks['RIGHT_THUMB_TIP'][1])
            mouse_pos = (left_index_y, left_index_x)
            mouseRect = self.clicked_image.get_rect(center=mouse_pos)
            if self.startButton.check_click(mouse_pos):
                self.window.blit(self.clicked_image, mouseRect)
                return "exercise_view"
            elif self.infoButton.check_click(mouse_pos):
                self.window.blit(self.clicked_image, mouseRect)
                return "report_view"
            elif self.settingsButton.check_click(mouse_pos):
                self.window.blit(self.clicked_image, mouseRect)
                return "settings_view"
            elif self.quitButton.check_click(mouse_pos):
                self.window.blit(self.clicked_image, mouseRect)
                pygame.quit()
                exit()
            else:
                mouseRect = self.mouse_image.get_rect(center=mouse_pos)
                self.window.blit(self.mouse_image, mouseRect)
        return "login_view"
