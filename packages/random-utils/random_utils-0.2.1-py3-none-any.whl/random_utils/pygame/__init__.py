import pygame
from colorsys import rgb_to_hsv, hsv_to_rgb
import numpy as np
import os

class ColorPicker:
    def __init__(self, wheel_pos, wheel_rad, slider_pos, slider_size, slider_horiz, slider_invert, cursor_rad, display_rect_loc, display_rect_size=(150, 150)):
        self.wheel_pos, self.wheel_rad = wheel_pos, wheel_rad
        self.slider_pos, self.slider_size, self.slider_horiz, self.slider_invert = slider_pos, slider_size, slider_horiz, slider_invert
        self.cursor_rad = cursor_rad
        self.display_rect_loc, self.display_rect_size = display_rect_loc, display_rect_size
        self.wheel_cursor, self.slider_cursor = np.array((wheel_rad,)*2), np.array((slider_size[0]//2, 1))
        self.slider_surf = pygame.Surface(slider_size)
        self.wheel_surf = pygame.transform.scale(pygame.image.load(os.path.join(os.path.realpath(os.path.dirname(__file__)), "assets", "color_picker.png")), (wheel_rad * 2,) * 2)
        self.wheel_surf = pygame.Surface((wheel_rad*2,)*2, pygame.SRCALPHA)
        self.wheel_surf.fill((0, 0, 0, 0))
        self.cursor_surf = pygame.Surface((self.cursor_rad*2,)*2, pygame.SRCALPHA)
        self.wheel_darken = pygame.Surface((wheel_rad * 2,) * 2, pygame.SRCALPHA)
        self._create_wheel()
        self._create_slider()
        self.update_wheel()

    def draw(self, window):
        pygame.draw.rect(window, self.get_rgb(), (*self.display_rect_loc, *self.display_rect_size))
        window.blit(self.slider_surf, self.slider_pos)
        self._draw_cursor(window, np.array(self.slider_pos) + np.array(self.slider_cursor))
        window.blit(self.wheel_surf, self.wheel_pos)
        window.blit(self.wheel_darken, self.wheel_pos)
        self._draw_cursor(window, np.array(self.wheel_pos) + np.array(self.wheel_cursor))

    def update(self, window):
        self.draw(window)
        if any(pygame.mouse.get_pressed()):
            x, y = pygame.mouse.get_pos()
            if ((self.wheel_pos[0] + self.wheel_rad - x) ** 2 + (self.wheel_pos[1] + self.wheel_rad - y) ** 2)**0.5 < self.wheel_rad - 2:
                self.wheel_cursor = (x - self.wheel_pos[0], y - self.wheel_pos[1]) if pygame.mouse.get_pressed()[0] else (self.wheel_rad,)*2
                return True
            elif self.slider_pos[0] < x < self.slider_pos[0] + self.slider_size[0] and self.slider_pos[1] < y < self.slider_pos[1] + self.slider_size[1]:
                self.slider_cursor[1] = y - self.slider_pos[1] if pygame.mouse.get_pressed()[0] else 1
                self.update_wheel()
                return True

    def get_rgb(self):
        wrgb = self.wheel_surf.get_at(self.wheel_cursor)
        srgb = self.slider_surf.get_at(self.slider_cursor)
        whsv = rgb_to_hsv(*(np.array(wrgb)/255)[:3])
        shsv = rgb_to_hsv(*(np.array(srgb)/255)[:3])
        hsv = (whsv[0], whsv[1], shsv[2])
        rgb = np.array(hsv_to_rgb(*hsv))*255
        return rgb

    def get_hsv(self):
        rgb = (np.array(self.get_rgb())/255)[:3]
        return np.array(rgb_to_hsv(*rgb))*255

    def update_wheel(self):
        self.wheel_surf.fill((0, 0, 0, 0))
        w, h = self.wheel_surf.get_size()

        for x in w:
            for y in h:
                if (hyp := (x**2 + y**2)**0.5) <= self.wheel_rad:
                    angle = np.arcsin(y/hyp) - np.pi/2
                    hue = angle / (np.pi * 2)
                    sat = hyp / (self.wheel_rad)
                    self.wheel_surf.set_at((x, y), np.array(hsv_to_rgb(hue, sat, 1))*255)

        pygame.draw.circle(self.wheel_darken, (0, 0, 0, np.interp(
            self.get_hsv()[2], (0, 255), (255, 0))), (self.wheel_rad,)*2, self.wheel_rad)

    def _create_wheel(self):
        pygame.draw.circle(self.wheel_surf, (0, 0, 0),
                           (self.wheel_rad+1,)*2, self.wheel_rad, 2)

    def _create_slider(self):
        w, h = self.slider_size
        if self.slider_horiz:
            for x in range(w):
                if self.slider_invert:
                    value = np.interp(x, (0, w), (0, 255))
                else:
                    value = np.interp(x, (0, w), (255, 0))
                pygame.draw.rect(self.slider_surf, (value,)*3, (x, 0, 1, h))

        else:
            for y in range(h):
                if self.slider_invert:
                    value = np.interp(y, (0, h), (0, 255))
                else:
                    value = np.interp(y, (0, h), (255, 0))
                pygame.draw.rect(self.slider_surf, (value,)*3, (0, y, w, 1))
        pygame.draw.rect(self.slider_surf, (0, 0, 0), (0, 0, w, h), 1)

    def _draw_cursor(self, window, pos):
        pygame.draw.circle(window, (255, 255, 255), pos, self.cursor_rad)
        pygame.draw.circle(window, (0, 0, 0), pos, self.cursor_rad, 2)
