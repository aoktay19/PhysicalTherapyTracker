from Objects.Item import Item
import pygame


class Lettuce(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "Assets/Images/lettuce.png")
        self.image = pygame.transform.scale(self.image, (75, 75))