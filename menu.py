import pygame
import sys
import chardet
import pandas as pd
from settings import TILES, FREDOKA, PATH_TO_START_MENU, WHITE
from settings import PATH_TO_DATA_SCORE, LEVEL_BUTTONS, LIST_LEVELS

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.scores = self.load_scores()
        self.background = pygame.image.load(PATH_TO_START_MENU)
        self.font = pygame.font.Font(FREDOKA, 14)

        self.buttons = []
        for i, level in enumerate(LIST_LEVELS):
            self.buttons.append({
                "id": level["id"],
                "title": level["title"],
                "font_pos": (TILES * 8 + 8, TILES * (6 + i * 2) + 6),
                "image": pygame.image.load(LEVEL_BUTTONS[level["id"]]["image"]),
                "push_image": pygame.image.load(LEVEL_BUTTONS[level["id"]]["push_image"]),
                "pos": (TILES * 6, TILES * (6 + i * 2)),
                "map": level["map"],
                "status": False
            })
        print(self.buttons)

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
            text = self.font.render(button["title"], True, WHITE)
            self.screen.blit(text, button["font_pos"])

        text = self.font.render("SCORES", True, WHITE)
        self.screen.blit(text, (TILES * 24, TILES * 5 - 8))

        y_offset = TILES * 6
        # Отображаем каждый результат из CSV
        self.scores = self.load_scores()
        for date, score in self.scores.sort_values(ascending=False, by= "score")[:7].itertuples(index=False):
            # date = datetime.fromisoformat(date).strftime("%d %B %Y, %H:%M")
            score_text = f"{score}"
            score_surface = self.font.render(score_text, True, WHITE)
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
                        button["status"] = True
                        self.draw()
                        pygame.time.delay(200)
                        return(button["map"], button['id'])

            if event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    button["status"] = False

        return None, None
