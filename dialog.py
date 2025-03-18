import pygame
import sys
from settings import PATH_TO_DIALOG_MENU, PATH_TO_YES_BTN, PATH_TO_YES_BTN_PUSH, FREDOKA, PATH_TO_NO_BTN, \
    PATH_TO_NO_BTN_PUSH
from settings import TILES, WHITE


class LevelCompleteDialog:
    def __init__(self, screen, score):
        self.screen = screen
        self.score = score
        # self.level = level
        # self.total_levels = total_levels

        self.background = pygame.image.load(PATH_TO_DIALOG_MENU)
        self.font = pygame.font.Font(FREDOKA, 13)  # Шрифт для отображения счета

        # Загружаем изображения кнопок
        self.button_yes = pygame.image.load(PATH_TO_YES_BTN)
        self.button_yes_push = pygame.image.load(PATH_TO_YES_BTN_PUSH)
        self.button_no = pygame.image.load(PATH_TO_NO_BTN)
        self.button_no_push = pygame.image.load(PATH_TO_NO_BTN_PUSH)

        # Координаты кнопок
        self.buttons = [
            {"id": "yes",
             "title": "YES",
             "image": self.button_yes,
             "push_image": self.button_yes_push,
             "pos": (TILES * 10, TILES * 20),
             "status": False},
            {"id": "no",
             "title": "NO",  # Исправлено: добавлена запятая
             "image": self.button_no,
             "push_image": self.button_no_push,
             "pos": (TILES * 16, TILES * 20),
             "status": False},
        ]

    def draw(self):
        self.screen.blit(self.background, (TILES * 8, TILES * 8))
        text = self.font.render(f"Score {self.score}", True, WHITE)
        self.screen.blit(text, (TILES * 15, TILES * 16 + 4))
        text = self.font.render("Continue?", True, WHITE)
        self.screen.blit(text, (TILES * 15, TILES * 17))

        # Кнопки
        for button in self.buttons:
            image = button["push_image"] if button["status"] else button["image"]
            self.screen.blit(image, button["pos"])
            score_text = self.font.render(button["title"], True, WHITE)
            self.screen.blit(score_text, (button["pos"][0] + TILES * 2 + 8, button["pos"][1] + TILES))
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in self.buttons:
                    bx, by = button["pos"]
                    bw, bh = button["image"].get_size()
                    if bx <= x <= bx + bw and by <= y <= by + bh:
                        button["status"] = True
                        self.draw()
                        pygame.time.delay(200)
                        return button["id"]
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    button["status"] = False

            return None
