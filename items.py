import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.abs_x = x
        self.abs_y = y

    def update(self, camera):
        """Обновляет экранные координаты в зависимости от камеры."""
        self.rect.x = self.abs_x - camera.offset_x
        self.rect.y = self.abs_y - camera.offset_y