import pygame
from settings import PLAYER_SPEED, PLAYER_ANIMATION_SPEED, TILES


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet, gamemap, enemies):
        super().__init__()
        self.sprites = self.load_sprites(sprite_sheet)

        # Начальные параметры
        self.direction = "down"
        self.frame_index = 0
        self.animation_timer = 0
        self.speed = PLAYER_SPEED
        self.score = 0
        self.abs_x = x
        self.abs_y = y

        self.image = self.sprites[self.direction][self.frame_index]
        self.rect = pygame.Rect(x, y, TILES, TILES)

        self.gamemap = gamemap
        self.enemies = enemies

    def load_sprites(self, sprite_sheet):
        """Разрезает спрайт-лист на кадры и создает словарь анимаций."""
        sprite_size = TILES
        sprites = {
            "down": [],
            "up": [],
            "left": [],
            "right": []
        }

        for row, direction in enumerate(sprites.keys()):
            for col in range(4):  # 4 кадра анимации
                frame = sprite_sheet.subsurface(
                    pygame.Rect(col * sprite_size, row * sprite_size, sprite_size, sprite_size)
                )
                sprites[direction].append(frame)

        return sprites

    def update(self, keys):
        """Обновляет движение и анимацию игрока."""
        dx, dy = 0, 0
        # Определяем направление движения
        if keys[pygame.K_w]:
            self.direction = "up"
            dy = -self.speed
        elif keys[pygame.K_s]:
            self.direction = "down"
            dy = self.speed
        elif keys[pygame.K_a]:
            self.direction = "left"
            dx = -self.speed
        elif keys[pygame.K_d]:
            self.direction = "right"
            dx = self.speed

        # Проверяем, можно ли идти
        new_abs_x = self.abs_x + dx
        new_abs_y = self.abs_y + dy
        new_rect = pygame.Rect(new_abs_x, new_abs_y, self.rect.width, self.rect.height)
        if self.gamemap.check_walkable(new_rect):
            self.abs_x = new_abs_x
            self.abs_y = new_abs_y

        # rect ломают столкновения
        # self.rect.x = self.abs_x
        # self.rect.y = self.abs_y

        if dx != 0 or dy != 0:
            self.animate()

    def animate(self):
        """Анимация движения"""
        self.animation_timer += 1
        if self.animation_timer >= PLAYER_ANIMATION_SPEED:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.sprites[self.direction])
            self.image = self.sprites[self.direction][self.frame_index]
