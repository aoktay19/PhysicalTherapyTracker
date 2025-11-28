from Objects.Item import Item
import pygame


class Sauce(Item):
    def __init__(self, x, y) :
        super().__init__(x, y, "Assets/Images/sauce.png")
        self.image = pygame.transform.scale(self.image, (70, 100))


