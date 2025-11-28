import math
import time
import pygame
import pygwidgets

import Constants
from Button import Button
from Exercises.CrossBodyReachExercise import CrossBodyReachExercise
from Exercises.HandsUp import HandsUp
from Exercises.PendulumStretchExercise import PendulumStretchExercise
from Gesture import Gesture
from MovementCorrectnessModel import MovementCorrectnessModel
from Draw import draw_avatar
from Objects.Hand import Hand

class ExerciseScene():
    def __init__(self, window):
        self.window = window
        self.movement_model = MovementCorrectnessModel()
        self.font = pygame.font.Font("Assets/Fonts/intrigora.ttf", 52)
        self.window_width, self.window_height = self.window.get_size()
        self.hands_up_background = pygame.transform.scale(pygame.image.load("Assets/Images/HandsUp.png"),
                                                          (self.window_width, self.window_height))
        self.cross_body_background = pygame.transform.scale(pygame.image.load("Assets/Images/reach_background.png"),
                                                            (self.window_width, self.window_height))
        self.background_image = self.hands_up_background
        self.last_drop_time = time.time()
        self.transparency = 128
        self.is_level_started = False
        self.levels = []
        self.current_level = -1
        self.pose = None
        self.arm_length = 0
        self.is_in_animation = False
        self.button_y = (self.window_height * 0.6) / 2
        self.hands_up_button = Button(200, 200, (350, self.button_y), 5,
                                 image_path="Assets/Images/handsup_pre.png", label=f"Hands Up")
        self.reach_button = Button(200, 200, (650, self.button_y), 5,
                                 image_path="Assets/Images/crossbody_pre.png", label="Cross Body Reach")
        self.pendulum_stretch_button = Button(200, 200, (950, self.button_y), 5,
                                   image_path="Assets/Images/pendulum.png", label="Pendulum Stretch")
        self.infoButton = Button(300, 50, (self.window_width / 2, 550), 5, text="Progression")
        self.buttons = [self.hands_up_button, self.reach_button, self.pendulum_stretch_button]
        self.mouse_image = pygame.image.load("Assets/Images/mouse.png")
        self.clicked_image = pygame.image.load("Assets/Images/click.png")
        self.mouse_image = pygame.transform.scale(self.mouse_image, (30, 30))
        self.clicked_image = pygame.transform.scale(self.clicked_image, (30, 30))
        self.gesture = Gesture()
        self.hand_object = Hand(self.window)
        self.scores = None

    def draw(self, pose_landmarks, player):
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if self.scores is None:
            _, _, self.scores = player.get_scores()
        self.sets = [10, 20, 2]
        self.set_count = 10
        # Draw background
        self.background_image.set_alpha(self.transparency)
        self.window.fill('black')
        self.window.blit(self.background_image, (0, 0))

        if (not self.is_in_animation) and self.is_level_started:
            draw_avatar(self.window, pose_landmarks)
        # if not self.is_in_animation:
        #     self.draw_avatar(pose_landmarks)
        if len(self.levels) == 0:
            self.levels.append(CrossBodyReachExercise(self.window, pose_landmarks))
            self.levels.append(HandsUp(self.window, pose_landmarks))
            self.levels.append(PendulumStretchExercise(self.window, pose_landmarks))

        if self.current_level == -1:
            self.window.fill('#475F77')
            self.hand_object.hand_animation()
            self.font.set_point_size(80)
            message_text = self.font.render("DAILY EXERCISES", True, 'white')
            message_rect = message_text.get_rect(center=(self.window_width/2, 80))
            self.window.blit(message_text, message_rect)
            for i, j in enumerate(self.buttons):
                self.buttons[i].add_set_count(self.scores[i], self.sets[i])
                self.buttons[i].draw(self.window)
            self.infoButton.draw(self.window)
            if 'RIGHT_THUMB_TIP' in pose_landmarks:
                left_index_x, left_index_y = int(pose_landmarks['RIGHT_THUMB_TIP'][0]), int(
                    pose_landmarks['RIGHT_THUMB_TIP'][1])
                self.gesture.check_gesture(pose_landmarks)
                if self.gesture.activate_gestures > 25:
                    self.gesture.reset_gesture()
                    self.scores = None
                    return "login_view"
                mouse_pos = (left_index_y, left_index_x)
                mouseRect = self.clicked_image.get_rect(center=mouse_pos)
                if self.reach_button.check_click(mouse_pos):
                    self.window.blit(self.clicked_image, mouseRect)
                    self.current_level = 0
                    self.background_image = self.cross_body_background
                    self.is_level_started = True
                elif self.hands_up_button.check_click(mouse_pos):
                    self.hand_object.reset_animation()
                    self.window.blit(self.clicked_image, mouseRect)
                    self.current_level = 1
                    self.background_image = self.hands_up_background
                    self.is_level_started = True
                elif self.pendulum_stretch_button.check_click(mouse_pos):
                    self.hand_object.reset_animation()
                    self.window.blit(self.clicked_image, mouseRect)
                    self.current_level = 2
                    self.background_image = self.cross_body_background
                    self.is_level_started = True
                elif self.infoButton.check_click(mouse_pos):
                    self.window.blit(self.clicked_image, mouseRect)
                    return "report_view"
                else:
                    self.window.blit(self.mouse_image, mouseRect)

        if self.current_level in [0, 1, 2]:
            player, is_finished, self.is_in_animation, self.transparency, view_name = self.levels[self.current_level].draw(pose_landmarks, player)
            if is_finished:
                self.is_level_started = False
                self.current_level = -1
                self.gesture.reset_gesture()
            _, _, self.scores = player.get_scores()
            pygame.display.flip()
            return view_name
        return "exercise_view"


    def set_current_level(self, choice):
        self.current_level = choice

    def finish_level(self):
        self.is_level_started = False
