import pygame
import sys
from settings import WIDTH, HEIGHT, TILES, PATH_TO_FINISH_MENU, BLACK, WHITE, FREDOKA, PATH_TO_MENU_BTN, PATH_TO_MENU_BTN_PUSH


class GameOver:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load(PATH_TO_FINISH_MENU)

        self.score = 0
        self.font = pygame.font.Font(FREDOKA, 36)  # Шрифт для отображения счета

        # Загружаем изображения кнопок
        self.button_play = pygame.image.load(PATH_TO_MENU_BTN)
        self.button_play_push = pygame.image.load(PATH_TO_MENU_BTN_PUSH)

        # Координаты кнопок
        self.buttons = [
            {"id": "map1", "image": self.button_play, "push_image": self.button_play_push,
             "pos": (TILES * 13, TILES * 22), "map": "data/levels/map4.tmx", "status": False},
        ]

    def draw(self):
        """Рисуем меню с учетом нажатых кнопок."""
        self.screen.blit(self.background, (0, 0))

        # Заголовок Game Over
        font = pygame.font.Font(FREDOKA, 50)
        text = font.render(" Win Game!", True, WHITE)
        self.screen.blit(text, (TILES * 7, TILES * 2))

        # Отображаем финальный счет
        fontH2 = pygame.font.Font(FREDOKA, 21)
        score_text = fontH2.render(f"Your score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (TILES * 13, TILES * 8))

        # Инструкция для начала новой игры или выхода
        restart_text = fontH2.render("Esc to exit", True, WHITE)
        self.screen.blit(restart_text, (TILES * 15 - 8, TILES * 13))

        # Инструкция для начала новой игры или выхода
        restart_text = fontH2.render("Play to start again", True, WHITE)
        self.screen.blit(restart_text, (TILES * 13 - 13, TILES * 18))

        for button in self.buttons:
            # Если кнопка нажата, рисуем нажатое изображение
            image = button["push_image"] if button["status"] else button["image"]
            self.screen.blit(image, button["pos"])

            font = pygame.font.Font(FREDOKA, 12)
            score_text = font.render(f"MENU", True, WHITE)
            self.screen.blit(score_text, (button["pos"][0] + TILES * 2 + 8, button["pos"][1] + TILES))
        pygame.display.flip()

    def handle_events(self):
        """Обрабатываем события (нажатия кнопок)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_RETURN:
                #     return True  # Начинаем новую игру
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in self.buttons:
                    bx, by = button["pos"]
                    bw, bh = button["image"].get_size()
                    if bx <= x <= bx + bw and by <= y <= by + bh:
                        button["status"] = True  # Отмечаем кнопку как нажатую
                        # Отрисовываем нажатие кнопки
                        self.draw()
                        pygame.time.delay(200)
                        return True  # (button["map"])  # Возвращаем выбранную карту
            elif event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    button["status"] = False  # Сбрасываем все кнопки в обычное состояние

        return None  # Остаемся на экране
