from pygwidgets import pygwidgets
from datetime import date

from Exercises.Exercise import Exercise
from ExerciseInstruction.Instruction import Instruction
from ExerciseInstruction.InstructionStep import InstructionStep
from Gesture import Gesture
from Objects.Lettuce import Lettuce
import pygame
import math
from moviepy.editor import VideoFileClip
import SaveLoad
from MovementCorrectnessModel import MovementCorrectnessModel
from Objects.Hand import Hand

class HandsUp(Exercise):
    def __init__(self, window, pose_landmarks):
        super().__init__(window)
        self.saver = SaveLoad.SaveLoad()
        self.score = 0
        self.penalty = 0
        self.window_width, self.window_height = self.window.get_size()
        self.is_position_valid = False
        self.font = pygame.font.Font("Assets/Fonts/intrigora.ttf", 45)
        self.color = '#475F77'
        self.movement_correctness_model = MovementCorrectnessModel()
        self.max_angle = 0
        self.shoulder_coord = (0, 0)
        self.arm_length = 0
        self.initial_body_area = 0
        self.pose_landmarks = pose_landmarks
        self.is_level_started = False
        self.countdown = 3
        self.instruction_steps = Instruction(instruction_steps=[
            InstructionStep(1, 'Please make sure you center your body', False),
            InstructionStep(2, "", False),
            InstructionStep(3, 'Are you ready?', False),
            InstructionStep(4, 'Countdown', False)
            # Add more steps as needed
        ])
        self.collect_sound = pygame.mixer.Sound('Assets/Sounds/collect.mp3')
        self.collect_lettuce_video = VideoFileClip('Assets/Videos/collect_lettuce.mp4').resize(
            (self.window_width, self.window_height)).fadein(1).fadeout(1)
        self.are_you_ready_sound = None
        self.ticking_sound = None
        self.gesture = Gesture()
        self.transparency = 0
        self.transition_counter = 0
        self.transparency_is_decrease = True
        self.is_in_animation = False
        self.go_back_sound_is_played = False
        self.is_finished = False
        self.hand_object = Hand(self.window)

    def set_body_area(self, area):
        self.initial_body_area = area

    def calculate_score(self):
        return self.score - self.penalty

    def calculate_distance(self, point1, point2):
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def start_countdown(self):
        self.start_time = pygame.time.get_ticks()  # Record the current time

    def update_countdown(self, is_in_rest=False):
        current_time = pygame.time.get_ticks()  # Get the current time
        elapsed_time = (current_time - self.start_time) / 1000  # Convert milliseconds to seconds
        if elapsed_time >= 1:  # Check if one second has passed
            self.start_time = current_time
            if is_in_rest:
                self.rest_countdown -= 1
            else:
                self.countdown -= 1

    def init_drawings(self, shoulder_coord, arm_length):
        center_x = shoulder_coord[1]
        center_y = shoulder_coord[0]
        num_points = 6
        for i in range(num_points):
            angle = i * math.pi / num_points  # Calculate angle
            x = center_x + int(arm_length * math.sin(angle))  # Calculate x coordinate
            y = center_y - int(arm_length * math.cos(angle))  # Calculate y coordinate (inverted)
            self.objects.append(Lettuce(x, y))

    def draw(self, pose_landmarks, player):
        left_foot_index = pose_landmarks.get('left_foot_index')
        right_foot_index = pose_landmarks.get('right_foot_index')
        left_shoulder = pose_landmarks.get('left_shoulder')
        if not self.instruction_steps.check_instruction_is_completed():

            if left_foot_index is not None and right_foot_index is not None:
                self.check_is_position_valid(pose_landmarks)
                right_wrist = pose_landmarks.get('right_wrist')
                right_shoulder = pose_landmarks.get('right_shoulder')
                arm_length = self.calculate_distance(right_shoulder, right_wrist)
                if self.is_position_valid:
                    self.arm_length = arm_length
                    self.shoulder_coord = pose_landmarks.get('right_shoulder')

                current_step = self.instruction_steps.find_next_instruction()

                if current_step.index == 1:
                    if not self.go_back_sound_is_played:
                        self.go_back_sound = pygame.mixer.Sound('Assets/Sounds/go_back.wav')
                        self.go_back_sound.play(-1)
                        self.go_back_sound_is_played = True
                    if left_foot_index[0] > self.window_height \
                            or right_foot_index[0] > self.window_height \
                            or (self.window_height - left_shoulder[
                        0]) + arm_length + 50 > self.window_height or not self.is_position_valid:
                        pygwidgets.DisplayText(self.window, (50, 50),
                                               current_step.instructions,
                                               fontSize=60, textColor=(0, 0, 0)).draw()
                        self.transparency = 255 - abs(
                            self.window_height - right_foot_index[0]) / 5
                    else:
                        if not player.get_is_instructions_completed()[0]:
                            self.collect_lettuce_video.preview()
                        current_step.complete_step()
                        self.init_drawings(self.shoulder_coord, self.arm_length)
                        self.go_back_sound.stop()
                        print("level 1 started")

                elif current_step.index == 2:

                    self.gesture.activate_gestures = 0
                    current_step.complete_step()
                    self.are_you_ready_sound = pygame.mixer.Sound('Assets/Sounds/are_you_ready.wav')
                    self.ticking_sound = pygame.mixer.Sound('Assets/Sounds/ticking.wav')
                    self.are_you_ready_sound.play(-1)
                    self.transparency = 50

                elif current_step.index == 3:
                    self.gesture.check_gesture(pose_landmarks)

                    if self.gesture.activate_gestures < 25:
                        self.hand_object.hand_animation()
                        self.font.set_point_size(120)
                        text = self.font.render(current_step.instructions, True, (255, 255, 255))
                        self.window.blit(text, (170, self.window_height / 2 - 75))
                    else:
                        self.hand_object.reset_animation()
                        self.are_you_ready_sound.stop()
                        self.gesture.reset_gesture()
                        current_step.complete_step()
                        self.ticking_sound.play(1)
                        self.start_countdown()
                elif current_step.index == 4:
                    if self.countdown == 0:
                        self.transition_animation()
                        self.ticking_sound.stop()
                        if self.transition_counter == 1:
                            current_step.complete_step()
                            self.transparency = 255
                            self.countdown = 3
                            self.is_in_animation = False
                    else:
                        self.update_countdown()
                        self.transparency = 50
                        pygwidgets.DisplayText(self.window, (self.window_width / 2 - 120, self.window_height / 2 - 150),
                                               str(self.countdown),
                                               fontSize=480, textColor=(255, 255, 255)).draw()

        else:
            self.transparency = 255
            player.set_is_instructions_completed(0)
            self.font.set_point_size(45)

            if 'right_wrist' and 'left_wrist' in pose_landmarks:
                self.check_collision(pose_landmarks)
            if self.rest_countdown == 0:
                self.is_in_rest = False
                self.rest_countdown = 10
            self.update_countdown(self.is_in_rest)
            if self.is_in_rest:
                self.gesture.check_gesture(pose_landmarks)
                if self.gesture.activate_gestures > 15 and self.is_in_rest:
                    self.reset_attributes()
                    player = self.write_data(player)
                    return player, self.is_finished, self.is_in_animation, self.transparency, "exercise_view"
                text_surf = self.font.render(f"Rest: {self.rest_countdown}", True, '#FFFFFF')
                top_rect = pygame.Rect(490 - 100 / 2, 45 - 40 / 2, 100, 40)
                text_rect = text_surf.get_rect(center=top_rect.center)
                self.window.blit(text_surf, text_rect)
                self.hand_object.hand_animation()
            else:
                self.hand_object.reset_animation()
                text_surf = self.font.render(f"Score: {self.score}", True, '#FFFFFF')
                top_rect = pygame.Rect(490 - 100 / 2, 45 - 40 / 2, 100, 40)
                text_rect = text_surf.get_rect(center=top_rect.center)
                self.window.blit(text_surf, text_rect)

            text_surf = self.font.render(f"Set: {self.setCount + 1}", True, '#FFFFFF')
            top_rect = pygame.Rect(730 - 100 / 2, 45 - 40 / 2, 100, 40)
            text_rect = text_surf.get_rect(center=top_rect.center)
            self.window.blit(text_surf, text_rect)

            for i in self.objects:
                if not i.is_collected():
                    self.window.blit(i.get_image(), i.get_location())
        self.is_finished = False
        return player, self.is_finished, self.is_in_animation, self.transparency, "exercise_view"

    def reset_attributes(self):
        self.gesture.reset_gesture()
        self.is_level_started = False
        self.setCount = 0
        self.is_finished = True
        self.is_in_rest = False
        self.instruction_steps.reset_instruction()
        self.countdown = 3
        self.go_back_sound_is_played = False

    def check_collision(self, pose_landmarks):
        hand_coord = pose_landmarks.get('right_wrist')
        right_hip = pose_landmarks.get('right_hip')
        right_elbow = pose_landmarks.get('right_elbow')
        right_shoulder = pose_landmarks.get('right_shoulder')
        self.check_is_position_valid(pose_landmarks)
        if not self.is_in_rest:
            if self.is_position_valid:
                angle = self.movement_correctness_model.calculate_angle(right_hip, right_shoulder, right_elbow)
                if angle > self.max_angle:
                    self.max_angle = angle
                for i in self.objects:
                    rect = i.get_location()
                    if rect.collidepoint(hand_coord[::-1]) and not i.is_collected():
                        self.collect_sound.play()
                        self.score += 1
                        i.collect()
            if self.check_is_set_over(pose_landmarks) and self.is_position_valid:
                self.is_in_rest = True
                self.total_score.append(["handsUp", 6, self.score, int(self.max_angle)])
                self.setCount += 1
                self.clear_level()
                self.init_drawings(self.shoulder_coord, self.arm_length)
                pygame.display.flip()

    def clear_level(self):
        self.objects.clear()
        self.score = 0
        self.max_angle = 0

    def check_is_position_valid(self, pose_landmarks):
        if not self.is_in_animation:
            left_wrist = pose_landmarks.get('left_wrist')
            left_elbow = pose_landmarks.get('left_elbow')
            left_shoulder = pose_landmarks.get('left_shoulder')
            is_left_arm_linear = self.movement_correctness_model.is_linear(left_elbow, left_wrist, left_shoulder)
            if not is_left_arm_linear:
                pygame.draw.line(self.window, (255, 0, 0), left_shoulder[::-1], left_elbow[::-1], 5)
                pygame.draw.line(self.window, (255, 0, 0), left_wrist[::-1], left_elbow[::-1], 5)
            right_wrist = pose_landmarks.get('right_wrist')
            right_elbow = pose_landmarks.get('right_elbow')
            right_shoulder = pose_landmarks.get('right_shoulder')
            is_right_arm_linear = self.movement_correctness_model.is_linear(right_elbow, right_wrist, right_shoulder)
            if not is_right_arm_linear:
                pygame.draw.line(self.window, (255, 0, 0), right_shoulder[::-1], right_elbow[::-1], 5)
                pygame.draw.line(self.window, (255, 0, 0), right_wrist[::-1], right_elbow[::-1], 5)
            left_hip = pose_landmarks.get('left_hip')
            left_knee = pose_landmarks.get('left_knee')
            left_ankle = pose_landmarks.get('left_ankle')
            is_left_leg_linear = self.movement_correctness_model.is_linear(left_knee, left_hip, left_ankle)
            if not is_left_leg_linear:
                pygame.draw.line(self.window, (255, 0, 0), left_hip[::-1], left_knee[::-1], 5)
                pygame.draw.line(self.window, (255, 0, 0), left_knee[::-1], left_ankle[::-1], 5)
            right_hip = pose_landmarks.get('right_hip')
            right_knee = pose_landmarks.get('right_knee')
            right_ankle = pose_landmarks.get('right_ankle')
            is_right_leg_linear = self.movement_correctness_model.is_linear(right_knee, right_hip, right_ankle)
            if not is_right_leg_linear:
                pygame.draw.line(self.window, (255, 0, 0), right_hip[::-1], right_knee[::-1], 5)
                pygame.draw.line(self.window, (255, 0, 0), right_knee[::-1], right_ankle[::-1], 5)
            mid_shoulder = ((left_shoulder[0] + right_shoulder[0]) / 2, (left_shoulder[1] + right_shoulder[1]) / 2)
            mid_hip = ((left_hip[0] + right_hip[0]) / 2, (left_hip[1] + right_hip[1]) / 2)
            spineDiff1 = self.movement_correctness_model.calculate_distance \
                (self.pose_landmarks.get('left_shoulder'), left_shoulder)
            spineDiff2 = self.movement_correctness_model.calculate_distance \
                (self.pose_landmarks.get('left_hip'), left_hip)
            spineDiff3 = self.movement_correctness_model.calculate_distance \
                (self.pose_landmarks.get('right_hip'), right_hip)
            is_spine_linear = max(spineDiff3, spineDiff2, spineDiff1) < 15
            if not is_spine_linear:
                pygame.draw.line(self.window, (255, 0, 0), right_shoulder[::-1], left_shoulder[::-1], 5)
                pygame.draw.line(self.window, (255, 0, 0), right_shoulder[::-1], right_hip[::-1], 5)
                pygame.draw.line(self.window, (255, 0, 0), right_hip[::-1], left_hip[::-1], 5)
                pygame.draw.line(self.window, (255, 0, 0), left_hip[::-1], left_shoulder[::-1], 5)
            is_spine_linear = True
            if is_right_arm_linear and is_left_arm_linear and is_spine_linear and is_left_leg_linear and is_right_leg_linear:
                self.is_position_valid = True
            else:
                self.is_position_valid = False

    def check_is_set_over(self, pose_landmarks):
        right_hip = pose_landmarks.get('right_hip')
        right_elbow = pose_landmarks.get('right_elbow')
        right_shoulder = pose_landmarks.get('right_shoulder')
        angle = self.movement_correctness_model.calculate_angle(right_hip, right_shoulder, right_elbow)
        if (self.max_angle - angle) >= 15 and angle < 25:
            return True
        return False

    def write_data(self, player):
        print("saved")
        score = str(date.today()) + '\n'
        for i in self.total_score:
            string = ""
            for j in i:
                string += str(j) + ","
            score += string[:-1] + '\n'
        player.add_score(score)
        self.saver.add_player(player)
        return player

    def transition_animation(self):
        self.is_in_animation = True
        if self.transparency >= 0 and self.transparency_is_decrease:
            self.transparency -= 75
            if self.transparency <= 0:
                self.transparency_is_decrease = False
        elif (not self.transparency_is_decrease) and self.transparency <= 255:
            self.transparency += 75
            if self.transparency >= 255:
                self.transition_counter = 1
