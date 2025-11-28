import pygame

class Hand():
    def __init__(self, window):
        self.window = window
        self.window_width, self.window_height = self.window.get_size()
        self.open_hand_image = pygame.image.load('Assets/Images/open_hand.png')
        self.fist_hand_image = pygame.image.load('Assets/Images/close_hand.png')
        self.open_hand_image = pygame.transform.scale(self.open_hand_image, (100, 100))
        self.fist_hand_image = pygame.transform.scale(self.fist_hand_image, (100, 100))
        self.hand_frame_count = 0
        self.hand_animation_speed = 20
        self.hand_position = (self.window_width - 200, self.window_height-200)

    def hand_animation(self) :
        # Update frame count
        self.hand_frame_count += 1

        # Determine which image to display based on the frame count
        if (self.hand_frame_count // self.hand_animation_speed) % 2 == 0 :
            current_hand_image = self.open_hand_image
        else :
            current_hand_image = self.fist_hand_image

        # Draw the current hand image on the screen
        self.window.blit(current_hand_image, self.hand_position)

    def reset_animation(self):
        self.hand_frame_count = 0