from Objects.Item import Item
import pygame


class Pan(Item):
    def __init__(self, x, y) :
        super().__init__(x, y, "Assets/Images/tava.png")
        self.image = pygame.transform.scale(self.image, (250, 250))

    def collect(self):
        return
