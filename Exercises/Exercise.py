from abc import ABC, abstractmethod


class Exercise(ABC):
    def __init__(self, window):
        self.scores = []
        self.window = window
        self.objects = []
        self.setCount = 0
        self.total_score = []
        self.is_completed = False
        self.rest_countdown = 15
        self.is_in_rest = False
        return

    def complete(self):
        self.is_completed = True
    def get_is_completed(self):
        return self.is_completed
    @abstractmethod
    def draw(self, pose_landmarks, player):
        pass

    @abstractmethod
    def calculate_score(self):
        pass
