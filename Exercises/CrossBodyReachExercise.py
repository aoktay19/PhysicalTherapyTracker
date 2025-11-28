from pygwidgets import pygwidgets
from datetime import date
from Exercises.Exercise import Exercise
from ExerciseInstruction.Instruction import Instruction
from ExerciseInstruction.InstructionStep import InstructionStep
from Gesture import Gesture
from Objects.Sauce import Sauce
from Objects.Pan import Pan
import pygame
import math
from moviepy.editor import VideoFileClip
import SaveLoad
from MovementCorrectnessModel import MovementCorrectnessModel
from SaucePouringEffect import SaucePouring
from Objects.Hand import Hand


class CrossBodyReachExercise(Exercise):
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
        self.shoulder_coord = (0, 0)
        self.arm_length = 0
        self.initial_body_area = 0
        self.pose_landmarks = pose_landmarks
        self.is_level_started = False
        self.countdown = 3
        self.score_countdown = 0
        self.instruction_steps = Instruction(instruction_steps=[
            InstructionStep(1, 'Please make sure you center your body', False),
            InstructionStep(2, "", False),
            InstructionStep(3, 'Are you ready?', False),
            InstructionStep(4, 'Countdown', False)
            # Add more steps as needed
        ])

        self.pour_sound = pygame.mixer.Sound('Assets/Sounds/sauce_pour.wav')
        self.reach_instruction_video = VideoFileClip('Assets/Videos/reach_instruction.mp4').resize(
            (self.window_width, self.window_height)).fadein(1).fadeout(1)
        self.are_you_ready_sound = None
        self.ticking_sound = None
        self.gesture = Gesture()
        self.transparency = 0
        self.transition_counter = 0
        self.transparency_is_decrease = True
        self.is_in_animation = False
        self.sauce_pouring = None
        self.is_finished = False
        self.go_back_sound_is_played = False
        self.hand_object = Hand(self.window)


    def set_body_area(self, area):
        self.initial_body_area = area

    def calculate_score(self):
        return self.score - self.penalty

    def calculate_distance(self, point1, point2):
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def start_countdown(self):
        self.start_time = pygame.time.get_ticks()  # Record the current time

    def update_countdown(self, is_collected=False, is_score=False, is_in_rest=False):
        current_time = pygame.time.get_ticks()  # Get the current time
        elapsed_time = (current_time - self.start_time) / 1000  # Convert milliseconds to seconds
        if elapsed_time >= 1:  # Check if one second has passed
            self.start_time = current_time  # Update start time
            if is_score and is_collected:
                self.score_countdown += 1
            elif is_in_rest and not is_collected:
                self.rest_countdown -= 1
            else:
                self.countdown -= 1

    def init_drawings(self, shoulder_coord, arm_length):
        center_x = shoulder_coord[1]
        center_y = shoulder_coord[0]
        x = center_x - int(arm_length)
        if len(self.objects) == 0:
            self.objects.append(Sauce(x, center_y))
            self.objects.append(Pan(x - 90, 350))
            self.sauce_pouring = SaucePouring(x + (self.objects[0].get_location().width / 2), center_y)
        else:
            self.objects[0].set_location(x, center_y)

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
                        if not player.get_is_instructions_completed()[1]:
                            self.reach_instruction_video.preview()
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
                        self.hand_object.hand_animation()
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

            player.set_is_instructions_completed(1)
            self.font.set_point_size(45)
            self.check_collision(pose_landmarks)

            if self.rest_countdown == 0:
                self.is_in_rest = False
                self.rest_countdown = 15
            self.update_countdown(self.objects[0].is_collected(), True, self.is_in_rest)

            text_surf = self.font.render(f"Set: {self.setCount + 1}", True, '#FFFFFF')
            top_rect = pygame.Rect(730 - 100 / 2, 45 - 40 / 2, 100, 40)
            text_rect = text_surf.get_rect(center=top_rect.center)
            self.window.blit(text_surf, text_rect)

            self.draw_progress_rect()
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
                text_surf = self.font.render(f"Score: {self.score_countdown}", True, '#FFFFFF')
                top_rect = pygame.Rect(490 - 100 / 2, 45 - 40 / 2, 100, 40)
                text_rect = text_surf.get_rect(center=top_rect.center)
                self.window.blit(text_surf, text_rect)

            for i in self.objects:
                if i.is_collected():
                    if "right_wrist" in pose_landmarks:
                        right_wrist = pose_landmarks.get("right_wrist")
                        i.set_location(right_wrist[1], right_wrist[0])
                    self.window.blit(i.get_image(), i.get_location())
                else:
                    self.window.blit(i.get_image(), i.get_location())

            if self.objects[0].is_collected():
                x, y = self.objects[0].get_center_location()
                self.sauce_pouring.pour_sauce(x, y + (self.objects[0].get_location().height / 2))
            self.sauce_pouring.update_and_draw(self.window)

        self.is_finished = False
        return player, self.is_finished, self.is_in_animation, self.transparency, "exercise_view"

    def reset_attributes(self):
        self.gesture.reset_gesture()
        self.is_level_started = False
        self.setCount = 0
        self.is_finished = True
        self.is_in_rest = False
        self.rest_countdown = 15
        self.score_countdown = 0
        self.instruction_steps.reset_instruction()
        self.countdown = 3
        self.go_back_sound_is_played = False

    def draw_progress_rect(self):
        rect = pygame.Rect(70, 125, 50, 450)
        if self.is_in_rest:
            pygame.draw.rect(self.window, 'white', rect, border_radius=25)  # Draw the background rect
            fill_height = int(rect.height * (self.rest_countdown * 100 / 15) / 100)  # Calculate the fill width
            fill_rect = pygame.Rect(rect.x, rect.y+rect.height - fill_height, rect.width, fill_height)
            pygame.draw.rect(self.window, 'red', fill_rect, border_radius=25)
        else:
            pygame.draw.rect(self.window, 'white', rect, border_radius=25)  # Draw the background rect
            fill_height = int(rect.height * (self.score_countdown * 100/15)/100)  # Calculate the fill width
            fill_rect = pygame.Rect(rect.x, rect.y + rect.height - fill_height, rect.width, fill_height)
            pygame.draw.rect(self.window, 'red', fill_rect, border_radius=25)

    def check_collision(self, pose_landmarks):
        hand_coord = pose_landmarks.get('right_wrist')
        self.check_is_position_valid(pose_landmarks)
        left_wrist = pose_landmarks.get('left_wrist')
        right_elbow = pose_landmarks.get('right_elbow')
        distance = self.movement_correctness_model.calculate_distance(left_wrist, right_elbow)
        if self.is_position_valid and not self.is_in_rest and distance < 15:
            for i in self.objects:
                rect = i.get_location()
                if rect.collidepoint(hand_coord[::-1]) and not i.is_collected():
                    i.collect()
                    self.pour_sound.play(-1)
                    self.objects[0].rotate()
                    self.start_countdown()
        if self.check_is_set_over(pose_landmarks) and self.is_position_valid:
            self.total_score.append(["crossBody", 15, self.score_countdown, self.score_countdown])
            self.setCount += 1
            self.is_in_rest = True
            self.clear_level()
            self.init_drawings(self.shoulder_coord, self.arm_length)
            pygame.display.flip()

    def clear_level(self):
        self.objects[0].uncollect()
        self.pour_sound.stop()
        self.sauce_pouring.sauce_particles.clear()
        self.score = 0
        self.score_countdown = 0
        self.objects[0].rotate()

    def check_is_position_valid(self, pose_landmarks):
        if not self.is_in_animation:
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
            is_spine_linear = True
            if is_right_arm_linear and is_spine_linear and is_left_leg_linear and is_right_leg_linear:
                self.is_position_valid = True
            else:
                self.is_position_valid = False

    def check_is_set_over(self, pose_landmarks):
        left_wrist = pose_landmarks.get('left_wrist')
        right_elbow = pose_landmarks.get('right_elbow')
        distance = self.movement_correctness_model.calculate_distance(left_wrist, right_elbow)
        if (distance > 100 and self.objects[0].is_collected()) or self.score_countdown == 15:
            return True
        return False

    def write_data(self, player):
        print("saved")
        # file1 = open("records.txt", "a")
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


