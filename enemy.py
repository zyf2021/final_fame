import pygame
from settings import TILES, PATH_TO_ENEMY

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprite_size = (TILES, TILES)
        self.sprite_sheet = pygame.image.load(PATH_TO_ENEMY).convert_alpha()

        # Загружаем idle-анимацию
        self.sprites_idle = self.load_sprites(self.sprite_sheet)
        self.frame_index = 0
        self.animation_timer = 0
        self.image = self.sprites_idle[self.frame_index]

        self.rect = self.image.get_rect(topleft=(x, y))
        self.abs_x = x
        self.abs_y = y


    def load_sprites(self, sheet):
        """Разрезает спрайт-лист, учитывая 8 кадров в 1 ряду"""
        sprites = []
        for col in range(8):  # 8 кадров в одном ряду
            frame = sheet.subsurface(pygame.Rect(
                col * self.sprite_size[0], 0,  # Используем только 1 ряд (idle)
                self.sprite_size[0], self.sprite_size[1]
            ))
            sprites.append(frame)
        return sprites

    def animate(self):
        """Анимирует врага"""
        self.animation_timer += 1
        if self.animation_timer >= 10:  # Скорость анимации
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.sprites_idle)
            self.image = self.sprites_idle[self.frame_index]

    def update(self):
        """Обновляет анимацию"""
        self.animate()


