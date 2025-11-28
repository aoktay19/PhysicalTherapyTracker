from datetime import datetime, timedelta
import matplotlib
import emoji

from Button import Button

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
        self.mouse_image = pygame.image.load("Assets/Images/mouse.png")
        self.mouse_image = pygame.transform.scale(self.mouse_image, (30, 30))
        self.font = pygame.font.Font("Assets/Fonts/intrigora.ttf", 30)
        self.fire_image = pygame.image.load("Assets/Images/fire.png")
        self.fire_image = pygame.transform.scale(self.fire_image, (90, 90))
        self.fire_image_gray = pygame.image.load("Assets/Images/grayFire.png")
        self.fire_image_gray = pygame.transform.scale(self.fire_image_gray, (90, 90))
        self.exercise_buttons = []
        self.button_coord = (200, 80)
        self.exercise1_button = Button(250, 250, self.button_coord, 5, text = " ")
        self.text_path = "records.txt"
        self.score_by_day, self.average_scores_by_day = self.read_score_from_txt()
        self.predicted_scores = self.predict_future_scores()
        self.gesture = Gesture()
        self.is_visible = False
        self.bg_color = (240, 240, 240)
        self.table_color = (255, 255, 255)
        self.header_color = (120, 180, 220)
        self.text_color = (50, 50, 50)
        self.prediction_color = (255, 100, 100)

    def grayscale(self, img):
        arr = pygame.surfarray.array3d(img)
        # luminosity filter
        avgs = [[(r * 0.298 + g * 0.587 + b * 0.114) for (r, g, b) in col] for col in arr]
        arr = np.array([[[avg, avg, avg] for avg in col] for col in avgs])
        return pygame.surfarray.make_surface(arr)

    def predict_future_scores(self):
        # Get the last known date and score
        if not self.average_scores_by_day:
            return []

        last_date = self.average_scores_by_day[-1][0]
        last_score = self.average_scores_by_day[-1][1]

        dates = [date for date, _ in self.average_scores_by_day]
        scores = [score for _, score in self.average_scores_by_day]

        # Simple linear regression for prediction
        date_nums = matplotlib.dates.date2num(dates)
        A = np.vstack([date_nums, np.ones(len(date_nums))]).T
        m, c = np.linalg.lstsq(A, scores, rcond=None)[0]

        predicted_scores = []
        for i in range(1, 8):  # Predict for the next 7 days
            future_date = last_date + timedelta(days=i)
            future_date_num = matplotlib.dates.date2num(future_date)
            predicted_score = m * future_date_num + c
            print("m: ", m, " c: ", c)
            if predicted_score > 180:
                predicted_score = 180
            predicted_scores.append((future_date, predicted_score))

        return predicted_scores

    def calculate_consecutive_days(self):
        # Calculate consecutive days of practice
        average_scores_by_day = self.average_scores_by_day
        length = len(average_scores_by_day)
        consecutive_days = 1
        for i in range(length - 1, 0, -1):
            current_date = average_scores_by_day[i][0]
            next_date = average_scores_by_day[i - 1][0]
            if (current_date - next_date).days == 1:
                consecutive_days += 1
            else:
                break
        return consecutive_days
    def get_scores(self, player):
        data_string = player.get_total_scores()
        print(data_string)
        score_by_day = []
        current_day = None
        current_day_scores = []

        for line in data_string.splitlines():
            if line.strip():  # Skip empty lines
                if '-' in line:  # Parse date
                    if current_day_scores:  # Add previous day's scores
                        score_by_day.append((current_day, current_day_scores))
                        current_day_scores = []
                    current_day = datetime.strptime(line.strip(), '%Y-%m-%d')
                else:  # Parse score line
                    parts = line.strip().split(',')
                    exercise_type = parts[0].strip()
                    max_score = int(parts[1].strip())
                    player_score = int(parts[2].strip())
                    angle = int(parts[3].strip())
                    current_day_scores.append((exercise_type, max_score, player_score, angle))

        if current_day_scores:  # Add scores of the last day
            score_by_day.append((current_day, current_day_scores))

        average_scores_by_day = []
        for date, scores in score_by_day:
            test_scores = [score[3] for score in scores if score[0] == "test"]
            if test_scores:
                average_score = sum(test_scores) / len(test_scores)
                average_scores_by_day.append((date, average_score))

        return score_by_day, average_scores_by_day
    def read_score_from_txt(self):

        score_by_day = []
        with open(self.text_path, 'r') as file:
            current_day = None
            current_day_scores = []
            for line in file:
                if line.strip():  # Skip empty lines
                    if '-' in line:  # Parse date
                        if current_day_scores:  # Add previous day's scores
                            score_by_day.append((current_day, current_day_scores))
                            current_day_scores = []
                        current_day = datetime.strptime(line.strip(), '%Y-%m-%d')
                    else:  # Parse score line
                        parts = line.strip().split(',')
                        exercise_type = parts[0].strip()
                        max_score = int(parts[1].strip())
                        player_score = int(parts[2].strip())
                        angle = int(parts[3].strip())
                        current_day_scores.append((exercise_type, max_score, player_score, angle))
            if current_day_scores:  # Add scores of the last day
                score_by_day.append((current_day, current_day_scores))
        average_scores_by_day = []
        for date, scores in score_by_day:
            test_scores = [score[3] for score in scores if score[0] == "test"]
            if test_scores:
                average_score = sum(test_scores) / len(test_scores)
                average_scores_by_day.append((date, average_score))
        return score_by_day, average_scores_by_day

    def draw_line_chart(self, average_scores_by_day):
        fig = pylab.figure(figsize=[7, 7],  # Inches
                           dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        dates = [date for date, _ in average_scores_by_day]
        averages = [score for _, score in average_scores_by_day]

        if self.predicted_scores:
            pred_dates = [dates[-1]] + [date for date, _ in self.predicted_scores]
            pred_scores = [averages[-1]] + [score for _, score in self.predicted_scores]
            ax.plot(pred_dates, pred_scores, 'r--', marker='o', label='Predicted Scores')
        ax.plot(dates, averages, marker='o', label='Actual Scores')
        ax.set_xticks(dates + pred_dates)
        ax.set_xticklabels([date.strftime('%d/%m/%Y') for date in dates + pred_dates], rotation=45, ha='right')
        ax.set_title("Average scores per day")
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
        # shadow_rect = table_rect.inflate(10, 10)  # Inflate the rect to create a shadow effect
        # pygame.draw.rect(self.window, (200, 200, 200), shadow_rect)
        # pygame.draw.rect(self.window, self.table_color, table_rect, border_radius=10)

        # Example of adding gradients to table elements
        header_rect = pygame.Rect(table_rect.left, table_rect.top, table_rect.width, 50)
        pygame.draw.rect(self.window, self.header_color, header_rect)
        pygame.draw.rect(self.window, (150, 200, 220), header_rect, border_radius=10)  # Gradient effect

        # Draw text on the table
        header_text = self.font.render("Exercise Performance Report", True, self.text_color)
        self.window.blit(header_text, (table_rect.left + 10, table_rect.top + 10))

        pylab.close(fig)
    def draw_hands_up_streak(self):
        consecutive_days = self.calculate_consecutive_days()
        button_x, y_offset = self.button_coord
        self.exercise1_button.draw(self.window)
        exercise_text = self.font.render("Hands Up", True, (0, 0, 0))
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
        for _, scores in self.score_by_day:
            for score in scores:
                if score[0] == "test" and score[2] > max_test_score:
                    max_test_score = score[2]

        # Display max score
        max_score_text = self.font.render(f"Max Score: {max_test_score}", True, (0, 0, 0))
        self.window.blit(max_score_text, (button_x - 30, y_offset))
        y_offset += 40

        # Display total time spent (hardcoded to 20 min for now)
        total_time_text = self.font.render("Time: 20 min", True, (0, 0, 0))
        self.window.blit(total_time_text, (button_x - 30, y_offset))
        y_offset += 40

    def draw(self, pose_landmarks, player):
        # Clear the window

        self.score_by_day, self.average_scores_by_day = self.get_scores(player)
        self.window.fill((255, 255, 255))
        # self.draw_avatar(pose_landmarks)
        self.gesture.check_gesture(pose_landmarks)
        # Display report title
        title_text = self.font.render("Exercise Performance Report", True, (0, 0, 0))

        if 'LEFT_THUMB_TIP' in pose_landmarks:
            left_index_x, left_index_y = int(pose_landmarks['LEFT_THUMB_TIP'][0]), int(
                pose_landmarks['LEFT_THUMB_TIP'][1])
            mouse_pos = (left_index_y, left_index_x)
            mouse_rect = self.mouse_image.get_rect(center=mouse_pos)
            self.window.blit(self.mouse_image, mouse_rect)
            if self.exercise1_button.check_click(mouse_pos):
                self.is_visible = True
        if self.is_visible:
            self.draw_line_chart(self.average_scores_by_day)
        self.draw_hands_up_streak()
        self.window.blit(title_text, (20, 20))


        if self.gesture.go_back_gesture > 30:
            self.gesture.reset_gesture()
            return "login_view"

        pygame.display.update()
        return "report_view"
