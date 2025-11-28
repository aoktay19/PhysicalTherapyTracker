import pygame

from Button import Button


class AvatarScene():
    def __init__(self, window):
        self.font = pygame.font.Font("Assets/Fonts/ch.ttf", 52)
        self.window = window
        self.background_image = pygame.image.load("Assets/Images/avatar_background.png")
        self.mouse_image = pygame.image.load("Assets/Images/mouse.png")
        self.clicked_image = pygame.image.load("Assets/Images/click.png")
        self.window_width, self.window_height = self.window.get_size()
        self.background_image = pygame.transform.scale(self.background_image, (self.window_width, self.window_height))
        self.mouse_image = pygame.transform.scale(self.mouse_image, (30, 30))
        self.clicked_image = pygame.transform.scale(self.clicked_image, (30, 30))
        self.avatar_one = Button(250, 250, (350 , self.window_height / 2 - 50), 5, image_path="Assets/Images/gordon_ramsey.png", label="Golden Remzi")
        self.avatar_two = Button(250, 250, (650, self.window_height / 2 - 50), 5, image_path="Assets/Images/women_chef.png", label="Clare Simit")
        self.avatar_three = Button(250, 250, (950, self.window_height / 2 - 50), 5, image_path="Assets/Images/dobby.jpeg", label="Çağrı Savran")

    def draw(self, pose_landmarks):
        self.pose_landmarks = pose_landmarks
        self.window.blit(self.background_image, (0, 0))
        self.avatar_one.draw(self.window)
        self.avatar_two.draw(self.window)
        self.avatar_three.draw(self.window)

        if 'RIGHT_THUMB_TIP' in pose_landmarks:
            left_index_x, left_index_y = int(pose_landmarks['RIGHT_THUMB_TIP'][0]), int(
                pose_landmarks['RIGHT_THUMB_TIP'][1])
            mouse_pos = (left_index_y, left_index_x)
            mouseRect = self.clicked_image.get_rect(center=mouse_pos)
            if self.avatar_one.check_click(mouse_pos):
                self.window.blit(self.clicked_image, mouseRect)
                return 0, "login_view"
            elif self.avatar_two.check_click(mouse_pos):
                self.window.blit(self.clicked_image, mouseRect)
                return 1, "login_view"
            elif self.avatar_three.check_click(mouse_pos):
                self.window.blit(self.clicked_image, mouseRect)
                return 2, "login_view"
            else:
                mouseRect = self.mouse_image.get_rect(center=mouse_pos)
                self.window.blit(self.mouse_image, mouseRect)
        return -1, "avatar_view"
