import pygame
import time
from Constants import GREEN, WHITE


class Button:
    def __init__(self, width, height, pos, elevation, text=None, image_path=None, label=None, border_radius = 12):
        self.font = pygame.font.Font("Assets/Fonts/ch.ttf", 45)
        self.label_font = pygame.font.Font("Assets/Fonts/intrigora.ttf", 30)
        # Core attributes
        self.text = text
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]
        self.initial_label = label
        self.time = 0
        self.image = None
        self.label = label
        self.label_color = "black"
        self.pos = pos
        self.width = width
        self.height = height
        self.border_radius = border_radius
        self.set_count = None
        self.is_active = True
        self.is_visible = True

        if text:
            self.text_surf = self.font.render(text, True, '#FFFFFF')
            self.text_rect = self.text_surf.get_rect(center=(pos[0], pos[1]))
        elif image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
            self.image = self.apply_border_radius(self.image, self.border_radius)
            self.image_rect = self.image.get_rect(center=(pos[0], pos[1]))

        self.top_rect = pygame.Rect(pos[0] - width / 2, pos[1] - height / 2, width, height)
        self.top_color = '#475F77'
        self.bottom_rect = pygame.Rect(pos[0] - width / 2, pos[1] - height / 2, width, height)
        self.bottom_color = '#354B5E'

    def apply_border_radius(self, image, radius):
        rect = image.get_rect()
        mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, rect.width, rect.height), border_radius=radius)
        mask.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        return mask

    def draw(self, surface):
        if self.is_visible:
            if self.label:
                self.label_surf = self.label_font.render(self.label, True, self.label_color)
                self.label_rect = self.label_surf.get_rect(center=(self.pos[0], self.pos[1] + self.height * 1.1))

            if self.set_count:
                self.set_surf = self.label_font.render(self.set_count, True, self.label_color)
                self.set_rect = self.set_surf.get_rect(center=(self.pos[0], self.pos[1] + self.height * 1.25))

            self.top_rect.y = self.original_y_pos - self.dynamic_elevation
            if self.image:
                self.image_rect.center = self.top_rect.center
            else:
                self.text_rect.center = self.top_rect.center

            self.bottom_rect.midtop = self.top_rect.midtop
            self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

            pygame.draw.rect(surface, self.bottom_color, self.bottom_rect, border_radius=self.border_radius)
            pygame.draw.rect(surface, self.top_color, self.top_rect, border_radius=self.border_radius)

            if self.image:
                surface.blit(self.image, self.image_rect)
            else:
                surface.blit(self.text_surf, self.text_rect)

            if self.label:
                surface.blit(self.label_surf, self.label_rect)
            if self.set_count:
                surface.blit(self.set_surf, self.set_rect)
        else:
            return

    def check_click(self, mouse_pos):
        if self.is_active:
            if self.bottom_rect.collidepoint(mouse_pos):
                if self.time == 0:
                    self.time = time.time()
                self.top_color = '#D74B4B'
                self.label_color = "red"
                if time.time() - self.time >= 1:
                    self.dynamic_elevation = 0
                    self.pressed = True
                    self.time = 0
                    return True
                else:
                    self.dynamic_elevation = self.elevation
                    if self.pressed:
                        print('click')
                        self.pressed = False
            else:
                self.dynamic_elevation = self.elevation
                self.top_color = '#475F77'
                self.label_color = "black"
                self.time = 0
            return False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'
            self.label_color = "black"
            self.time = 0
            return False

    def add_set_count(self, count, maximum):
        self.set_count = f"Daily Goal: {count}/{maximum}"

    def change_text(self, text):
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=(self.pos[0], self.pos[1]))

    def change_image(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = self.apply_border_radius(self.image, self.border_radius)
        self.image_rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))

    def change_pos(self, pos):
        self.pos = pos
        if self.text:
            self.text_surf = self.font.render(self.text, True, '#FFFFFF')
            self.text_rect = self.text_surf.get_rect(center=(pos[0], pos[1]))
        elif self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.image = self.apply_border_radius(self.image, self.border_radius)
            self.image_rect = self.image.get_rect(center=(pos[0], pos[1]))

        self.top_rect = pygame.Rect(pos[0] - self.width / 2, pos[1] - self.height / 2, self.width, self.height)
        self.top_color = '#475F77'
        self.bottom_rect = pygame.Rect(pos[0] - self.width / 2, pos[1] - self.height / 2, self.width, self.height)
        self.bottom_color = '#354B5E'

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

