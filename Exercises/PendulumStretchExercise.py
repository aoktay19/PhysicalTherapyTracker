from pygwidgets import pygwidgets
from datetime import date
from Exercises.Exercise import Exercise
from ExerciseInstruction.Instruction import Instruction
from ExerciseInstruction.InstructionStep import InstructionStep
from Gesture import Gesture
from Objects.Spoon import Spoon
from Objects.Pan import Pan
import pygame
from moviepy.editor import VideoFileClip
import SaveLoad
from MovementCorrectnessModel import MovementCorrectnessModel
import math
from Objects.Hand import Hand


class PendulumStretchExercise(Exercise):
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
        self.instruction_steps = Instruction(instruction_steps=[
            InstructionStep(1, 'Please make sure you center your body', False),
            InstructionStep(2, "", False),
            InstructionStep(3, 'Are you ready?', False),
            InstructionStep(4, 'Countdown', False)
        ])
        self.reach_instruction_video = VideoFileClip('Assets/Videos/pendulum_instruction.mp4').resize(
            (self.window_width, self.window_height)).fadein(1).fadeout(1)
        self.are_you_ready_sound = None
        self.ticking_sound = None
        self.gesture = Gesture()
        self.transparency = 0
        self.transition_counter = 0
        self.transparency_is_decrease = True
        self.is_in_animation = False
        self.is_finished = False
        self.go_back_sound_is_played = False
        self.exercise_directions = [["Clockwise", False], ["CClockwise", False]]
        self.oscillation_counter = 0
        self.oscillation_start_position = 0.0
        self.previous_angle = None
        self.previous_hand_position = None
        self.is_clockwise = None
        self.circle_radius = None
        self.oscillation_phase = 0
        self.hand_object = Hand(self.window)


    def set_body_area(self, area):
        self.initial_body_area = area

    def calculate_score(self):
        return self.score - self.penalty

    def calculate_distance(self, point1, point2):
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def start_countdown(self):
        self.start_time = pygame.time.get_ticks()  # Record the current time

    def update_countdown(self):
        current_time = pygame.time.get_ticks()  # Get the current time
        elapsed_time = (current_time - self.start_time) / 1000

        if elapsed_time >= 1:  # Check if one second has passed
            self.countdown -= 1
            self.start_time = current_time

    def init_drawings(self, shoulder_coord, arm_length):
        center_x = shoulder_coord[1]
        center_y = shoulder_coord[0]
        y = center_y + int(arm_length)
        self.circle_radius = arm_length
        if len(self.objects) == 0:
            self.objects.append(Spoon(center_x, y))
            self.objects.append(Pan(center_x-50, 500))
        else:
            self.objects[0].set_location(center_x, y)

    def draw(self, pose_landmarks, player):
        left_foot_index = pose_landmarks.get('left_foot_index')
        right_foot_index = pose_landmarks.get('right_foot_index')
        right_ankle = pose_landmarks.get('right_ankle')
        right_hip = pose_landmarks.get('right_hip')
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
                        self.go_back_sound = pygame.mixer.Sound('Assets/Sounds/pendulum_go_back.wav')
                        self.go_back_sound.play(-1)
                        self.go_back_sound_is_played = True
                    if left_foot_index[0] > self.window_height \
                            or right_foot_index[0] > self.window_height \
                            or self.movement_correctness_model.calculate_angle(right_ankle, right_hip, right_shoulder) > 150 or not self.is_position_valid:
                        pygwidgets.DisplayText(self.window, (50, 50),
                                               current_step.instructions,
                                               fontSize=60, textColor=(0, 0, 0)).draw()
                        self.transparency = 255 - abs(
                            self.window_height - right_foot_index[0]) / 5
                    else:
                        if not player.get_is_instructions_completed()[2]:
                            self.reach_instruction_video.preview()
                        current_step.complete_step()
                        self.init_drawings(self.shoulder_coord, self.arm_length)
                        self.go_back_sound.stop()
                        print("level 1 started")

                elif current_step.index == 2:
                    self.gesture.activate_gestures = 0
                    current_step.complete_step()
                    self.are_you_ready_sound = pygame.mixer.Sound('Assets/Sounds/are_you_ready_pendulum.wav')
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
            player.set_is_instructions_completed(2)
            self.font.set_point_size(45)

            if self.detect_oscillation(pose_landmarks) and self.objects[0].is_collected() and self.is_position_valid:
                self.score += 1

            if 'right_wrist' and 'left_wrist' in pose_landmarks:
                if self.check_collision(pose_landmarks):
                    player = self.write_data(player)
                    self.reset_attributes()
                    return player, self.is_finished, self.is_in_animation, self.transparency, "exercise_view"

            text_surf = self.font.render(f"Score: {self.score}", True, '#FFFFFF')
            top_rect = pygame.Rect(490 - 100 / 2, 45 - 40 / 2, 100, 40)
            text_rect = text_surf.get_rect(center=top_rect.center)
            self.window.blit(text_surf, text_rect)

            if not self.exercise_directions[0][1]:
                text_surf = self.font.render(f"{self.exercise_directions[0][0]}", True, '#FFFFFF')
                top_rect = pygame.Rect(730 - 100 / 2, 45 - 40 / 2, 100, 40)
                text_rect = text_surf.get_rect(center=top_rect.center)
                self.window.blit(text_surf, text_rect)
            elif not self.exercise_directions[1][1]:
                text_surf = self.font.render(f"{self.exercise_directions[1][0]}", True, '#FFFFFF')
                top_rect = pygame.Rect(730 - 100 / 2, 45 - 40 / 2, 100, 40)
                text_rect = text_surf.get_rect(center=top_rect.center)
                self.window.blit(text_surf, text_rect)

            self.draw_progress_rect()

            for i in self.objects:
                if i.is_collected():
                    if "right_wrist" in pose_landmarks:
                        right_wrist = pose_landmarks.get("right_wrist")
                        i.set_location(right_wrist[1], right_wrist[0])
                    self.window.blit(i.get_image(), i.get_location())
                else:
                    self.window.blit(i.get_image(), i.get_location())

        self.is_finished = False
        return player, self.is_finished, self.is_in_animation, self.transparency, "exercise_view"

    def reset_attributes(self):
        self.is_level_started = False
        self.is_finished = True
        self.score = 0
        self.exercise_directions[0][1] = False
        self.exercise_directions[1][1] = False
        self.instruction_steps.reset_instruction()
        self.countdown = 3
        self.go_back_sound_is_played = False

    def detect_oscillation(self, pose_landmarks) :
        if "right_wrist" and "right_shoulder" is not None:
            right_wrist = pose_landmarks.get('right_wrist')
            right_shoulder = pose_landmarks.get('right_shoulder')
            if self.oscillation_phase == 0:
                # Start of the oscillation
                self.oscillation_start_position = right_shoulder[1]
                self.oscillation_phase = 1
                return False
            position_diff = right_wrist[1] - self.oscillation_start_position
            if self.oscillation_phase == 1:
                # Moving away from the start
                if position_diff <= -35:
                    self.oscillation_phase = 2
                return False

            elif self.oscillation_phase == 2 :
                # Moving back towards the start
                if position_diff >= 35 :
                    self.oscillation_phase = 1
                    return True
                return False
        return False

    def draw_progress_rect(self):
        rect = pygame.Rect(70, 125, 50, 450)
        pygame.draw.rect(self.window, 'white', rect, border_radius=25)  # Draw the background rect
        fill_height = int(rect.height * (self.score * 100/10)/100)  # Calculate the fill width
        fill_rect = pygame.Rect(rect.x, rect.y + rect.height - fill_height, rect.width, fill_height)
        pygame.draw.rect(self.window, 'red', fill_rect, border_radius=25)

    def check_collision(self, pose_landmarks):
        hand_coord = pose_landmarks.get('right_wrist')
        self.check_is_position_valid(pose_landmarks)
        if self.is_position_valid:
            for i in self.objects:
                rect = i.get_location()
                if rect.collidepoint(hand_coord[::-1]) and not i.is_collected():
                    i.collect()
        if self.check_is_set_over(pose_landmarks) and self.is_position_valid:
            self.complete_direction()
            self.total_score.append(["pendulum", 10, self.score, self.score])
            self.clear_level()
            self.init_drawings(self.shoulder_coord, self.arm_length)

            if self.is_both_directions_complete():
                return True
            pygame.display.flip()
        return False

    def complete_direction(self):
        if not self.exercise_directions[0][1]:
            self.exercise_directions[0][1] = True
        elif not self.exercise_directions[1][1]:
            self.exercise_directions[1][1] = True

    def is_both_directions_complete(self):
        return all(is_complete for _, is_complete in self.exercise_directions)


    def clear_level(self):
        self.objects[0].uncollect()
        self.score = 0

    def check_is_position_valid(self, pose_landmarks):
        if not self.is_in_animation:
            right_wrist = pose_landmarks.get('right_wrist')
            right_elbow = pose_landmarks.get('right_elbow')
            right_shoulder = pose_landmarks.get('right_shoulder')
            is_right_arm_linear = self.movement_correctness_model.is_linear(right_elbow, right_wrist, right_shoulder)
            if not is_right_arm_linear:
                pygame.draw.line(self.window, (255, 0, 0), right_shoulder[::-1], right_elbow[::-1], 5)
                pygame.draw.line(self.window, (255, 0, 0), right_wrist[::-1], right_elbow[::-1], 5)
            right_hip = pose_landmarks.get("right_hip")
            right_ankle = pose_landmarks.get("right_ankle")
            is_lean = self.movement_correctness_model.calculate_angle(right_shoulder, right_hip, right_ankle)
            is_spine_linear = True
            if is_right_arm_linear and is_spine_linear and is_lean < 150:
                self.is_position_valid = True
            else:
                self.is_position_valid = False

    def check_is_set_over(self, pose_landmarks):
        if self.score == 10:
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