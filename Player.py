from datetime import datetime, date
from collections import defaultdict


class Player:
    def __init__(self, player=None):
        if player is None:
            self.name = ""
            self.total_scores = ""
            self.img = ""
            self.is_instructions_completed = [False, False, False]
        else:
            self.name = player.get_name()
            self.total_scores = player.get_total_scores()
            self.img = player.get_img()
            self.is_instructions_completed = player.is_instructions_completed

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_img(self, img):
        self.img = img

    def get_img(self):
        return self.img

    def set_total_scores(self, total_scores):
        self.total_scores = total_scores

    def get_total_scores(self):
        return self.total_scores

    def add_score(self, score):
        scores = self.get_total_scores() + score
        self.set_total_scores(scores)

    def reset_progress(self):
        self.total_scores = ""

    def set_is_instructions_completed(self, index):
        self.is_instructions_completed[index] = True

    def get_is_instructions_completed(self):
        return self.is_instructions_completed

    def group_scores_by_date(self, score_list):
        grouped_scores = defaultdict(lambda: [None, None, None])

        for ex_date, score_data in score_list:
            if score_data[0] is None and score_data[1] is None:
                index = 2
            elif score_data[0] is None and score_data[2] is None:
                index = 1
            else:
                index = 0
            score = score_data[index]
            grouped_scores[ex_date][index] = score

        grouped_scores_list = [[ex_date, scores] for ex_date, scores in grouped_scores.items()]
        grouped_scores_list.sort(key=lambda x: x[0])
        return grouped_scores_list

    def get_scores(self):
        score_count = [0, 0, 0]
        data_string = self.total_scores
        if not data_string.strip():
            return [], [], score_count

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
                    current_day_scores.append([exercise_type, max_score, player_score, angle])

        if current_day_scores:  # Add scores of the last day
            score_by_day.append((current_day, current_day_scores))

        average_scores_by_day = []
        for exercise_date, scores in score_by_day:
            score_dict = []
            for index, score in enumerate(scores):
                if score is not None:
                    # switch case yapilabilir
                    if score[0] == "handsUp":
                        index = 0
                    elif score[0] == "crossBody":
                        index = 1
                    else:
                        index = 2
                    angle = score[3]
                    if (datetime.today() - exercise_date).days == 0:
                        score_count[index] += 1
                    score_dict.append(list())
                    score_dict.append(list())
                    score_dict.append(list())
                    score_dict[index].append(angle)
            for index in range(len(score_dict)):
                if len(score_dict[index]) != 0:
                    score_dict[index] = sum(score_dict[index]) / len(score_dict[index])
                else:
                    score_dict[index] = None
            average_scores_by_day.append((exercise_date, score_dict))
        average_scores_by_day = self.group_scores_by_date(average_scores_by_day)
        return score_by_day, average_scores_by_day, score_count
