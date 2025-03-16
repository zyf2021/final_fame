import pygame
from settings import PLAYER_SPEED, PLAYER_ANIMATION_SPEED, TILES

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet, gamemap):
        super().__init__()
        # Загружаем спрайт-лист и режем его
        self.sprites = self.load_sprites(sprite_sheet)
        # Начальные параметры
        self.direction = "down"  # Стартовое направление
        self.frame_index = 0  # Индекс кадра анимации
        self.animation_timer = 0  # Время смены кадров
        self.speed = PLAYER_SPEED

        self.image = self.sprites[self.direction][self.frame_index]
        self.rect = pygame.Rect(x, y, TILES, TILES)
        self.gamemap = gamemap

    def load_sprites(self, sprite_sheet):
        """Разрезает спрайт-лист на кадры и создает словарь анимаций."""
        sprite_size = TILES  # Размер одного кадра
        sprites = {
            "down": [],  # Вниз (первая строка)
            "up": [],  # Вверх (вторая строка)
            "left": [],  # Влево (третья строка)
            "right": []  # Вправо (четвертая строка)
        }

        for row, direction in enumerate(sprites.keys()):
            for col in range(4):  # Предположим, что у нас 4 кадра анимации
                frame = sprite_sheet.subsurface(
                    pygame.Rect(col * sprite_size, row * sprite_size, sprite_size, sprite_size)
                )
                sprites[direction].append(frame)

        return sprites

    def update(self, keys):
        """Обновляет движение и анимацию игрока."""
        dx, dy = 0, 0

        # Определяем направление движения
        if keys[pygame.K_w]:  # Вверх
            self.direction = "up"
            dy = -self.speed
        elif keys[pygame.K_s]:  # Вниз
            self.direction = "down"
            dy = self.speed
        elif keys[pygame.K_a]:  # Влево
            self.direction = "left"
            dx = -self.speed
        elif keys[pygame.K_d]:  # Вправо
            self.direction = "right"
            dx = self.speed

        new_rect = self.rect.move(dx, dy)
        if self.gamemap.check_walkable(new_rect):
            self.rect = new_rect

        if dx != 0 or dy != 0:
            self.animate()

    def animate(self):
        """Анимация движения"""
        self.animation_timer += 1
        if self.animation_timer >= PLAYER_ANIMATION_SPEED:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.sprites[self.direction])
            self.image = self.sprites[self.direction][self.frame_index]
