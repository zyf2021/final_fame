import pygame
import sys
import pandas as pd
import chardet
from pygame.examples.aliens import Score

from settings import WIDTH, HEIGHT, TILES, FREDOKA, PATH_TO_START_MENU, WHITE, PATH_TO_DATA_SCORE
from datetime import datetime

class MainMenu:
    def __init__(self, screen):
        self.screen = screen

        self.scores = self.load_scores()

        self.background = pygame.image.load(PATH_TO_START_MENU)

        # Загружаем изображения кнопок
        self.button_map1 = pygame.image.load("data/assets/button.png")
        self.button_map2 = pygame.image.load("data/assets/button.png")
        self.button_map3 = pygame.image.load("data/assets/button.png")

        self.button_push_map1 = pygame.image.load("data/assets/button_push.png")
        self.button_push_map2 = pygame.image.load("data/assets/button_push.png")
        self.button_push_map3 = pygame.image.load("data/assets/button_push.png")

        # self.button_exit = pygame.image.load("data/assets/button_exit.png")

        # Координаты кнопок
        self.buttons = [
            {"id": "map1",
             "title": "Level 1",
             "image": self.button_map1,
             "push_image": self.button_push_map1,
             "pos": (TILES * 6, TILES * 6),
             "map": "data/levels/map4.tmx",
             "status": False
             },
            {"id": "map2",
             "title": "Level 2",
             "image": self.button_map2,
             "push_image": self.button_push_map2,
             "pos": (TILES * 6, TILES * 8),
             "map": "data/levels/map5.tmx",
             "status": False
             },
            {"id": "map3",
             "title": "Level 3",
             "image": self.button_map3,
             "push_image": self.button_push_map3,
             "pos": (TILES * 6, TILES * 10),
             "map": "data/levels/map3.tmx",
             "status": False
             },
            {"id": "map3",
             "title": "Level 3",
             "image": self.button_map3,
             "push_image": self.button_push_map3,
             "pos": (TILES * 6, TILES * 12),
             "map": "data/levels/map3.tmx",
             "status": False
             },
            {"id": "map3",
             "title": "Level 3",
             "image": self.button_map3,
             "push_image": self.button_push_map3,
             "pos": (TILES * 6, TILES * 14),
             "map": "data/levels/map3.tmx",
             "status": False
             },
        ]

    # Загрузка данных из CSV
    def load_scores(self):
        with open(PATH_TO_DATA_SCORE, 'rb') as f:
            result = chardet.detect(f.read())
        data_score = pd.read_csv(PATH_TO_DATA_SCORE, encoding=result['encoding'])
        return data_score

    def draw(self):
        """Рисуем меню с учетом нажатых кнопок."""
        self.screen.blit(self.background, (0, 0))


        for button in self.buttons:
            # Если кнопка нажата, рисуем нажатое изображение
            image = button["push_image"] if button["status"] else button["image"]
            self.screen.blit(image, button["pos"])

        # Заголовок SCORES
        font = pygame.font.Font(FREDOKA, 14)
        text = font.render("SCORES", True, WHITE)
        self.screen.blit(text, (TILES * 24, TILES * 5 - 8))

        y_offset = TILES * 6
        # Отображаем каждый результат из CSV
        for date, score in self.scores.sort_values(ascending=False, by= "score")[:7].itertuples(index=False):
            date = datetime.fromisoformat(date).strftime("%d %B %Y, %H:%M")

            score_text = f"{score}"
            score_surface = font.render(score_text, True, WHITE)
            self.screen.blit(score_surface, (TILES * 20 + 60, y_offset))
            y_offset += 24


        # Название игры
        font = pygame.font.Font(FREDOKA, 50)
        text = font.render("Cute farm", True, WHITE)
        self.screen.blit(text, (TILES * 9, TILES * 25 - 8))

        pygame.display.flip()


    def handle_events(self):
        """Обрабатываем события (нажатия кнопок)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in self.buttons:
                    bx, by = button["pos"]
                    bw, bh = button["image"].get_size()

                    if bx <= x <= bx + bw and by <= y <= by + bh:
                        button["status"] = True  # Отмечаем кнопку как нажатую
                        # Отрисовываем нажатие кнопки
                        self.draw()
                        pygame.time.delay(200)
                        return(button["map"])  # Возвращаем выбранную карту

            if event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    button["status"] = False # Сбрасываем все кнопки в обычное состояние

        return None
