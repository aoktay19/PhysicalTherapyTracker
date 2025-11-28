import pygame
import random

class SauceParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = random.randint(5, 9)
        self.alpha = 255
        self.color = (255, 0, 0, self.alpha)  # Brown color for sauce
        self.surf = pygame.Surface((self.r * 2, self.r * 2), pygame.SRCALPHA)
        self.surf.fill((0, 0, 0, 0))

    def update(self):
        self.y += random.randint(3, 4)
        self.alpha -= 5
        if self.alpha < 0:
            self.alpha = 0
        self.color = (255, 0, 0, self.alpha)

    def draw(self, screen):
        pygame.draw.circle(self.surf, self.color, (self.r, self.r), self.r)
        screen.blit(self.surf, (self.x - self.r, self.y - self.r))


class SaucePouring:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sauce_particles = []
        self.sauce_particle = SauceParticle(self.x + random.randint(-5, 5), self.y)

    def pour_sauce(self, x, y):
        self.set_location(x,y)
        for _ in range(5):
            self.sauce_particles.append(self.sauce_particle)

    def update_and_draw(self, screen):
        for particle in self.sauce_particles:
            if particle.alpha <= 0:
                self.sauce_particles.remove(particle)
                continue
            particle.update()
            particle.draw(screen)

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.sauce_particle = SauceParticle(self.x + random.randint(-5, 5), self.y)