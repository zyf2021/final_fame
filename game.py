import pygame
import pytmx
from datetime import datetime
import pandas as pd
import chardet
from tilemap import GameMap
from settings import BLACK, WIDTH, HEIGHT, BRAUN, WHITE, WIN_SCORE, FREDOKA, PATH_TO_SCORE_TABLE, \
    PATH_TO_DATA_SCORE, TILES, \
    PATH_TO_PLAYER, PATH_TO_MENU_BTN, PATH_TO_MENU_BTN_PUSH, LIST_LEVELS
from player import Player
from game_over import GameOver
from items import Item
from camera import Camera
from spark import Spark
from dialog import LevelCompleteDialog


class Game:
    def __init__(self, level_file, level_id):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Милая ферма")
        self.clock = pygame.time.Clock()

        # Начальный счет
        self.score = 0
        self.font = pygame.font.Font(FREDOKA, 12)  # Шрифт для отображения счета

        # Список уровней
        self.levels = LIST_LEVELS
        self.last_level = str(len(self.levels))
        self.level_id = level_id

        # Координаты кнопок
        self.buttons = [
            {"id": "menu",
             "title": "MENU",
             "font": pygame.font.Font(FREDOKA, 14),
             "font_pos": (TILES * 8 + 4, TILES),
             "image": pygame.image.load(PATH_TO_MENU_BTN),
             "push_image": pygame.image.load(PATH_TO_MENU_BTN_PUSH),
             "pos": (TILES * 6, 0),
             "status": False
             },
        ]

        # Загружаем карту и начальные координаты
        self.game_map, self.pos_enter_x, self.pos_enter_y, self.pos_exit_x, self.pos_exit_y = self.load_map(level_file)

        # Загрузка объектов карты
        self.items = self.game_map.load_items()
        self.enemies = self.game_map.load_enemies()

        # Группа эффектов (искры)
        self.spark_sprite_sheet = pygame.image.load("data/assets/effect2.png").convert_alpha()
        self.effects = pygame.sprite.Group()

        # Создаем камеру
        self.camera = Camera(self.game_map.width, self.game_map.height)

        # Группы спрайтов
        player_sprite_sheet = pygame.image.load(PATH_TO_PLAYER).convert_alpha()
        # Начальные координаты игрока
        self.player = Player(self.pos_enter_x, self.pos_enter_y, player_sprite_sheet, self.game_map, self.enemies)

        # ЗАЧЕМ?
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    # Загрузка карты
    def load_map(self, level_file):
        game_map = GameMap(level_file)
        pos_enter_x, pos_enter_y, pos_exit_x, pos_exit_y = None, None, None, None

        # Находим объект "Enter" для установки позиции игрока
        for obj in game_map.tmx_data.objects:
            if obj.name == "Enter":
                pos_enter_x, pos_enter_y = obj.x, obj.y
        for obj in game_map.tmx_data.objects:
            if obj.name == "Exit":
                pos_exit_x, pos_exit_y = obj.x, obj.y

        return game_map, pos_enter_x, pos_enter_y, pos_exit_x, pos_exit_y

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

    def draw_menu_btn(self):
        for button in self.buttons:
            image = button["push_image"] if button["status"] else button["image"]
            self.screen.blit(image, button["pos"])
            self.screen.blit(button['font'].render(button['title'], True, WHITE), button['font_pos'])

    def check_exit(self):
        """Проверяем, дошел ли игрок до выхода"""
        print("Проверка")
        print(f"Player: ({self.player.abs_x}, {self.player.abs_y}) | Exit: ({self.pos_exit_x}, {self.pos_exit_y})")
        print(self.last_level, self.level_id)
        if abs(self.player.abs_x - self.pos_exit_x) < 10 and abs(self.player.abs_y - self.pos_exit_y) < 10:
            return True
        return False

    def game_over(self):
        """Финальный экран при победе"""
        final_screen = GameOver(self.screen)
        final_screen.score = self.score  # Передаем итоговый счет
        self.add_score(self.score)

        while True:
            final_screen.draw()
            action = final_screen.handle_events()
            if action:  # Если нажали Play
                return 'menu'

    def reset_game(self, map, level_id):
        """Сбрасываем игру после экрана Game Over"""
        self.__init__(map, level_id)
        self.run()

    def continue_game(self):
        """Финальный экран при победе"""
        dialog = LevelCompleteDialog(self.screen, self.score)
        self.add_score(self.score)

        while True:
            dialog.draw()
            action = dialog.handle_events()
            if action:
                return action

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for button in self.buttons:
                        bx, by = button["pos"]
                        bw, bh = button["image"].get_size()
                        if bx <= x <= bx + bw and by <= y <= by + bh:
                            button["status"] = True
                            self.draw_menu_btn()
                            pygame.display.flip()
                            pygame.time.delay(200)
                            return "menu"

                elif event.type == pygame.MOUSEBUTTONUP:
                    for button in self.buttons:
                        button["status"] = False  # Сбрасываем все кнопки в обычное состояние

            # Обновляет состояние игры (игрок, анимации)
            keys = pygame.key.get_pressed()
            self.all_sprites.update(keys)
            self.enemies.update()
            self.items.update(self.camera)  # ВАЖНО! Перед столкновением

            # Проверяем сбор предметов (с искрами)
            collected_items = pygame.sprite.spritecollide(self.player, self.items, True)
            for item in collected_items:
                spark = Spark(item.rect.centerx, item.rect.centery, self.spark_sprite_sheet)
                self.effects.add(spark)
            self.score += len(collected_items)

            # Проверяем уничтожение врагов (с искрами)
            collected_enemies = pygame.sprite.spritecollide(self.player, self.enemies, True)
            for enemy in collected_enemies:
                spark = Spark(enemy.rect.centerx, enemy.rect.centery, self.spark_sprite_sheet)
                self.effects.add(spark)
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

            self.effects.update()

            # Рисуем все
            self.all_sprites.draw(self.screen)
            self.items.draw(self.screen)
            self.enemies.draw(self.screen)
            self.effects.draw(self.screen)

            # Отображаем счет и меню на экране
            self.draw_score()
            self.draw_menu_btn()

            pygame.display.flip()
            self.clock.tick(60)

            if self.check_exit():
                # Еcли это последний уровень, то рисуем экран завершения игры
                if self.last_level == self.level_id:
                    return self.game_over()
                else:
                    # Рисуем диалог
                    res = self.continue_game()
                    if res == "yes":
                        return "next"
                    else:
                        return "menu"

        return "quit"
