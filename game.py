import pygame
from datetime import datetime
import pandas as pd
import chardet
from tilemap import GameMap
from settings import BLACK, WIDTH, HEIGHT, BRAUN, PATH_TO_ITEM, WHITE, WIN_SCORE, FREDOKA, PATH_TO_SCORE_TABLE, PATH_TO_DATA_SCORE, TILES, \
    PATH_TO_PLAYER
from player import Player
from game_over import GameOver
from items import Item
from camera import Camera


class Game:
    def __init__(self, level_file):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Милая ферма")
        self.clock = pygame.time.Clock()

        # Начальный счет
        self.score = 0
        self.font = pygame.font.Font(FREDOKA, 12)  # Шрифт для отображения счета

        # Загружаем карту
        self.game_map = GameMap(level_file)
        self.items = self.game_map.load_items()
        self.enemies = self.game_map.load_enemies()

        # Создаем камеру
        self.camera = Camera(self.game_map.width, self.game_map.height)

        # Группы спрайтов
        player_sprite_sheet = pygame.image.load(PATH_TO_PLAYER).convert_alpha()
        self.player = Player(16, 208, player_sprite_sheet, self.game_map, self.enemies)  # Начальные координаты

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def draw_score(self):
        """Рисует текущий счет на экране"""
        self.screen.blit(pygame.image.load(PATH_TO_SCORE_TABLE), (TILES, 0))

        score_text = self.font.render(f"Score", True, WHITE)
        self.screen.blit(score_text, (TILES * 2 + 8, 4))
        score_text = self.font.render(f"{self.score}", True, WHITE)
        self.screen.blit(score_text, (TILES * 3, 28))

    def add_score(self, score):
        with open(PATH_TO_DATA_SCORE, 'rb') as f:
            result = chardet.detect(f.read())
        data_score = pd.read_csv(PATH_TO_DATA_SCORE, encoding=result['encoding'])
        data_score.loc[len(data_score)] = [datetime.now().isoformat(), score]
        data_score.to_csv(PATH_TO_DATA_SCORE, index=False)

    def game_over(self):
        """Финальный экран при победе"""
        final_screen = GameOver(self.screen)
        final_screen.score = self.score  # Передаем итоговый счет
        self.add_score(self.score)

        while True:
            final_screen.draw()
            action = final_screen.handle_events()  # "data/levels/map4.tmx"
            if action:  # Если нажали Enter, запускаем игру заново
                self.reset_game(action)
                return  # Выходим из функции

    def reset_game(self, map):
        """Сбрасываем игру после экрана Game Over"""
        self.__init__(map)  # Перезапускаем игру с той же картой
        self.run()  # Запускаем цикл заново

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
            self.enemies.update()
            self.items.update(self.camera)  # ВАЖНО! Перед столкновением



            # Проверяем сбор призов
            collected_items = pygame.sprite.spritecollide(self.player, self.items, True)
            self.score += len(collected_items)
            collected_enemies = pygame.sprite.spritecollide(self.player, self.enemies, True)
            self.score += len(collected_enemies) * 10

            # Камера следует за игроком
            self.camera.update(self.player)

            # Очищаем экран
            self.screen.fill(BRAUN)
            # Рисуем карту
            self.game_map.draw(self.screen, self.camera)

            # Применяем камеру ко всем спрайтам
            for sprite in self.all_sprites:
                self.camera.apply(sprite)
            for sprite in self.items:
                self.camera.apply(sprite)
            for sprite in self.enemies:
                self.camera.apply(sprite)

            # Рисуем все
            self.all_sprites.draw(self.screen)
            self.items.draw(self.screen)
            self.enemies.draw(self.screen)

            # Отображаем счет на экране
            self.draw_score()

            pygame.display.flip()
            self.clock.tick(60)

            if self.score >= WIN_SCORE:  # Просто для примера, если набрали 100 очков
                running = False
                self.game_over()

        pygame.quit()
