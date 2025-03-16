import pygame
from tilemap import GameMap
from settings import BLACK, WIDTH, HEIGHT
from player import Player


class Game:
    def __init__(self, level_file):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Милая ферма")
        self.clock = pygame.time.Clock()

        # Загружаем карту
        self.game_map = GameMap(level_file)

        # Группы спрайтов
        # Загружаем спрайт игрока
        player_sprite_sheet = pygame.image.load("data/assets/player.png").convert_alpha()
        self.player = Player(16, 208, player_sprite_sheet, self.game_map)  # Начальные координаты


        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)


    def run(self):
        # start_screen(self.screen, self.clock)  # Показ заставки перед игрой
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Обновляет состояние игры (игрок, анимации)
            keys = pygame.key.get_pressed()
            self.all_sprites.update(keys)

            # Отрисовываем карту и спрайты
            self.screen.fill(BLACK)  # Очищаем экран
            self.game_map.draw(self.screen)  # Рисуем карту
            self.all_sprites.draw(self.screen)  # Рисуем игрока

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()





