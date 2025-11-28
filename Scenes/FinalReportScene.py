from collections import defaultdict
from datetime import datetime, timedelta
import matplotlib
import emoji

from Button import Button
from Objects.Hand import Hand

matplotlib.use("Agg")
import numpy as np
import matplotlib.backends.backend_agg as agg
from Gesture import Gesture
import pylab
import pygame
import Constants
import numpy as np
from scipy.optimize import curve_fit


class Report:
    def __init__(self, window):
        self.window = window
        self.window_width, self.window_height = self.window.get_size()
        self.mouse_image = pygame.image.load("Assets/Images/mouse.png")
        self.mouse_image = pygame.transform.scale(self.mouse_image, (30, 30))
        self.font = pygame.font.Font("Assets/Fonts/intrigora.ttf", 30)
        self.fire_image = pygame.image.load("Assets/Images/fire.png")
        self.fire_image = pygame.transform.scale(self.fire_image, (90, 90))
        self.fire_image_gray = pygame.image.load("Assets/Images/grayFire.png")
        self.fire_image_gray = pygame.transform.scale(self.fire_image_gray, (90, 90))

        self.button_coord = (200, 80)
        self.button_coord2 = (200, 380)
        self.exercise1_button = Button(250, 250, self.button_coord, 5, text=" ")
        self.exercise2_button = Button(250, 250, self.button_coord2, 5, text=" ")
        self.exercise_buttons = [self.exercise1_button,
                                 self.exercise2_button]
        self.button_coords = [self.button_coord, self.button_coord2]
        self.down_arrow_coord = (375, self.window_height // 2 + 25)
        self.down_arrow_button = Button(50, 100, self.down_arrow_coord, 5, image_path="Assets/Images/down.png")
        self.up_arrow_coord = (375, self.window_height // 2 - 125)
        self.up_arrow_button = Button(50, 100, self.up_arrow_coord, 5, image_path="Assets/Images/up.png")
        self.infoButton = Button(300, 50, (self.window_width / 2, 450), 5, text="Mein Menu")
        self.text_path = "records.txt"
        self.score_by_day = list()
        self.average_scores_by_day = list()
        self.score_by_day, self.average_scores_by_day = [], []
        self.predicted_scores_hands_up = []
        self.predicted_scores_cross_body = []
        self.predicted_scores_pendulum = []
        self.gesture = Gesture()
        self.is_visible = 0
        self.bg_color = (240, 240, 240)
        self.table_color = (255, 255, 255)
        self.header_color = (120, 180, 220)
        self.text_color = (50, 50, 50)
        self.prediction_color = (255, 100, 100)
        self.visible_indexes = 0
        self.hand_object = Hand(self.window)

    def grayscale(self, img):
        arr = pygame.surfarray.array3d(img)
        # luminosity filter
        avgs = [[(r * 0.298 + g * 0.587 + b * 0.114) for (r, g, b) in col] for col in arr]
        arr = np.array([[[avg, avg, avg] for avg in col] for col in avgs])
        return pygame.surfarray.make_surface(arr)

    def predict_future_scores(self, max_angle, exercise_type):
        # Get the last known date and score

        if not self.average_scores_by_day or len(self.average_scores_by_day) == 0:
            return []
        if exercise_type == "handsUp":
            index = 0
        elif exercise_type == "crossBody":
            index = 1
        else:
            index = 2

        last_date = None
        last_score = None
        dates = []
        scores = []

        for date, score_dict in self.average_scores_by_day:
            if score_dict[index] is not None:
                dates.append(date)
                scores.append(score_dict[index])
                last_date = date
                last_score = score_dict[index]

        if not last_date or not last_score:
            return []

        date_nums = matplotlib.dates.date2num(dates)
        A = np.vstack([date_nums, np.ones(len(date_nums))]).T
        m, c = np.linalg.lstsq(A, scores, rcond=None)[0]

        predicted_scores = []
        for i in range(1, 8):
            future_date = last_date + timedelta(days=i)
            future_date_num = matplotlib.dates.date2num(future_date)
            predicted_score = m * future_date_num + c
            if predicted_score > max_angle:
                predicted_score = max_angle
            predicted_scores.append((future_date, predicted_score))

        return predicted_scores

    def calculate_consecutive_days(self, exercise_type):
        index = 0 if exercise_type == "handsUp" else 1
        length = len(self.average_scores_by_day)
        if self.average_scores_by_day[-1][1][index] is None:
            return 0
        consecutive_days = 1
        for i in range(length - 1, 0, -1):
            current_date = self.average_scores_by_day[i][0]
            next_date = self.average_scores_by_day[i - 1][0]
            if (current_date - next_date).days == 1 and self.average_scores_by_day[i - 1][1][index] is not None:
                consecutive_days += 1
            else:
                break
        return consecutive_days

    def draw_line_chart(self, average_scores_by_day, exercise_type):
        if exercise_type == "handsUp":
            index = 0
        elif exercise_type == "crossBody":
            index = 1
        else:
            index = 2

        fig = pylab.figure(figsize=[7, 7], dpi=100)
        ax = fig.gca()
        dates = [date for date, scores in average_scores_by_day if scores[index] is not None]
        averages = [scores[index] for date, scores in average_scores_by_day if scores[index] is not None]

        if exercise_type == "handsUp" and self.predicted_scores_hands_up:
            pred_dates = [dates[-1]] + [date for date, _ in self.predicted_scores_hands_up]
            pred_scores = [averages[-1]] + [score for _, score in self.predicted_scores_hands_up]
            ax.plot(pred_dates, pred_scores, 'r--', marker='o', label='Predicted Scores')
        elif exercise_type == "crossBody" and self.predicted_scores_cross_body:
            pred_dates = [dates[-1]] + [date for date, _ in self.predicted_scores_cross_body]
            pred_scores = [averages[-1]] + [score for _, score in self.predicted_scores_cross_body]
            ax.plot(pred_dates, pred_scores, 'r--', marker='o', label='Predicted Scores')
        elif exercise_type == "pendulum" and self.predicted_scores_pendulum:
            pred_dates = [dates[-1]] + [date for date, _ in self.predicted_scores_pendulum]
            pred_scores = [averages[-1]] + [score for _, score in self.predicted_scores_pendulum]
            ax.plot(pred_dates, pred_scores, 'r--', marker='o', label='Predicted Scores')

        ax.plot(dates, averages, marker='o', label='Actual Scores')
        ax.set_xticks(dates)
        ax.set_xticklabels([date.strftime('%d/%m/%Y') for date in dates], rotation=45, ha='right')
        ax.set_title(f"{exercise_type} Average Scores per Day")
        ax.set_ylabel("Average Score")
        ax.legend()

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.window.blit(surf, (500, 0))
        table_rect = pygame.Rect(500, 30, 475, 300)
        header_rect = pygame.Rect(table_rect.left, table_rect.top, table_rect.width, 50)
        pygame.draw.rect(self.window, self.header_color, header_rect)
        pygame.draw.rect(self.window, (150, 200, 220), header_rect, border_radius=10)

        header_text = self.font.render(f"{exercise_type} Performance Report", True, self.text_color)
        self.window.blit(header_text, (table_rect.left + 10, table_rect.top + 10))

        pylab.close(fig)

    def drawExercise(self, exercise_type, button_coord):
        consecutive_days = self.calculate_consecutive_days(exercise_type)
        button_x, y_offset = button_coord
        exercise_text = self.font.render(exercise_type, True, (0, 0, 0))
        self.window.blit(exercise_text, (button_x - 70, y_offset + 10))

        button_x -= 60
        y_offset += 45
        if consecutive_days > 0:
            self.window.blit(self.fire_image, (button_x + 10, y_offset))
        else:
            self.window.blit(self.fire_image_gray, (button_x + 10, y_offset))
        fire_text = self.font.render(str(consecutive_days), True, (0, 0, 0))
        y_offset += 40
        self.window.blit(fire_text, (button_x + 45, y_offset))
        y_offset += 60
        # Extract max score for "test" exercises
        max_test_score = 0
        count = 0
        for _, scores in self.score_by_day:
            for score in scores:
                if score[0] == exercise_type:
                    count += 1
                    if score[3] > max_test_score:
                        max_test_score = score[3]

        # Display max score
        shift = 60 if max_test_score >= 100 else 45
        max_score_text = self.font.render(f"Max Score: {max_test_score}", True, (0, 0, 0))
        self.window.blit(max_score_text, (button_x - shift, y_offset))
        y_offset += 40

        # Display total time spent (hardcoded to 20 min for now)
        shift = 60 if count >= 100 else 45
        total_time_text = self.font.render(f"Set Count: {count}", True, (0, 0, 0))
        self.window.blit(total_time_text, (button_x - shift, y_offset))
        y_offset += 40

    def draw(self, pose_landmarks, player):
        # Clear the window

        self.score_by_day, self.average_scores_by_day, _ = player.get_scores()
        self.gesture.check_gesture(pose_landmarks)
        if self.gesture.activate_gestures > 15:
            self.gesture.reset_gesture()
            return "login_view"
        if not self.score_by_day or not self.average_scores_by_day:
            self.font.set_point_size(70)
            message_text = self.font.render("NO DATA AVAILABLE", True, "black")
            set_rect = message_text.get_rect(center=(self.window_width // 2, self.window_height // 2))
            self.window.fill((255, 255, 255))
            self.window.blit(message_text, set_rect)
            self.font.set_point_size(30)
            self.infoButton.draw(self.window)
            if 'RIGHT_THUMB_TIP' in pose_landmarks:
                right_index_x, right_index_y = int(pose_landmarks['RIGHT_THUMB_TIP'][1]), int(
                    pose_landmarks['RIGHT_THUMB_TIP'][0])
                mouse_pos = (right_index_x, right_index_y)
                mouseRect = self.mouse_image.get_rect(center=mouse_pos)
                self.window.blit(self.mouse_image, mouseRect)
                if self.infoButton.check_click(mouse_pos):
                    return "login_view"
            pygame.display.update()
            return "report_view"

        self.predicted_scores_hands_up = self.predict_future_scores(180, "handsUp")
        self.predicted_scores_cross_body = self.predict_future_scores(15, "crossBody")
        self.predicted_scores_pendulum = self.predict_future_scores(10, "pendulum")
        self.window.fill((255, 255, 255))
        # self.draw_avatar(pose_landmarks)
        # Display report title
        title_text = self.font.render("Exercise Performance Report", True, (0, 0, 0))
        if self.is_visible == 0:
            self.draw_line_chart(self.average_scores_by_day, "handsUp")
        elif self.is_visible == 1:
            self.draw_line_chart(self.average_scores_by_day, "crossBody")
        elif self.is_visible == 2:
            self.draw_line_chart(self.average_scores_by_day, "pendulum")
        if self.visible_indexes == 0:
            self.up_arrow_button.deactivate()
            self.down_arrow_button.activate()
            self.exercise_buttons[0].draw(self.window)
            self.exercise_buttons[1].draw(self.window)
            self.drawExercise("handsUp", self.button_coords[0])
            self.drawExercise("crossBody", self.button_coords[1])
        else:
            self.up_arrow_button.activate()
            self.down_arrow_button.deactivate()
            self.exercise_buttons[0].draw(self.window)
            self.exercise_buttons[1].draw(self.window)
            self.drawExercise("pendulum", self.button_coords[1])
            self.drawExercise("crossBody", self.button_coords[0])
        # self.drawExercise("pendulumStretch")
        self.window.blit(title_text, (20, 20))
        self.up_arrow_button.draw(self.window)
        self.down_arrow_button.draw(self.window)
        if 'LEFT_THUMB_TIP' in pose_landmarks:
            left_index_x, left_index_y = int(pose_landmarks['LEFT_THUMB_TIP'][0]), int(
                pose_landmarks['LEFT_THUMB_TIP'][1])
            mouse_pos = (left_index_y, left_index_x)
            if self.up_arrow_button.check_click(mouse_pos):
                self.visible_indexes = 0
            if self.down_arrow_button.check_click(mouse_pos):
                self.visible_indexes = 1
            mouse_rect = self.mouse_image.get_rect(center=mouse_pos)
            self.window.blit(self.mouse_image, mouse_rect)
            if self.exercise1_button.check_click(mouse_pos):
                self.is_visible = self.visible_indexes
            if self.exercise2_button.check_click(mouse_pos):
                self.is_visible = self.visible_indexes + 1
        self.hand_object.hand_animation()
        pygame.display.update()
        return "report_view"
