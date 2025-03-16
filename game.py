import pygame
from tilemap import GameMap
from settings import BLACK, WIDTH, HEIGHT, PATH_TO_ITEM, WHITE
from player import Player
from items import Item


class Game:
    def __init__(self, level_file):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Милая ферма")
        self.clock = pygame.time.Clock()

        # Начальный счет
        self.score = 0
        self.font = pygame.font.Font(None, 36)  # Шрифт для отображения счета

        # Загружаем карту
        self.game_map = GameMap(level_file)

        # Группы спрайтов
        player_sprite_sheet = pygame.image.load("data/assets/player.png").convert_alpha()
        self.player = Player(16, 208, player_sprite_sheet, self.game_map)  # Начальные координаты

        self.items = self.game_map.tilemap.get_items()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)



    def draw_score(self):
        """Рисует текущий счет на экране"""
        score_text = self.font.render(f"Очки: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

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

            # Проверяем сбор призов
            collected_items = pygame.sprite.spritecollide(self.player, self.items, True) # The dokill argument
            # is a bool. If set to True,
            # all Sprites that collide will be removed from the Group.
            self.score += len(collected_items)  # За каждый собранный приз прибавляем очки

            # Отрисовываем карту и спрайты
            self.screen.fill(BLACK)  # Очищаем экран
            self.game_map.draw(self.screen)  # Рисуем карту
            self.all_sprites.draw(self.screen)  # Рисуем игрока
            self.items.draw(self.screen)  # Отрисовка оставшихся призов
            self.draw_score()  # Отображаем счет на экране

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()





