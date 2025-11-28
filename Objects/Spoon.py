from Objects.Item import Item
import pygame


class Spoon(Item):
    def __init__(self, x, y) :
        super().__init__(x, y, "Assets/Images/spoon.png")
        self.image = pygame.transform.scale(self.image, (170, 170))
        self.rotate()
        self.rect = pygame.Rect(self.x-85, self.y-50, 160, 160)

    def set_location(self, x, y):
        self.x, self.y = x, y
        self.image.get_rect(center=(self.x, self.y))
        self.rect = pygame.Rect(self.x-85, self.y-50, 170, 170)