import pygame


class Item:
    def __init__(self, x, y, path):
        self.image = pygame.image.load(path)
        self.x, self.y = x, y
        self.image.get_rect(center=(self.x, self.y))
        self.rect = pygame.Rect(self.x - 40, self.y - 40, 85, 85)
        self.isCollected = False

    def get_location(self):
        return self.rect

    def get_center_location(self):
        return self.x, self.y

    def is_collected(self):
        return self.isCollected

    def collect(self):
        self.isCollected = True

    def uncollect(self):
        self.isCollected = False

    def rotate(self, angle=180):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def set_location(self, x, y):
        self.x, self.y = x, y
        self.image.get_rect(center=(self.x, self.y))
        self.rect = pygame.Rect(self.x - 40, self.y - 40, 85, 85)

    def get_image(self):
        return self.image
