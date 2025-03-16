import pygame
import sys
from settings import WIDTH, HEIGHT, TILES

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("data/assets/start_menu_background.png")

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
            {"id": "map1", "image": self.button_map1, "push_image": self.button_push_map1,
             "pos": (TILES * 6, TILES * 6), "map": "data/levels/map4.tmx", "status": False},
            {"id": "map2", "image": self.button_map2, "push_image": self.button_push_map2,
             "pos": (TILES * 6, TILES * 8), "map": "data/levels/map2.tmx", "status": False},
            {"id": "map3", "image": self.button_map3, "push_image": self.button_push_map3,
             "pos": (TILES * 6, TILES * 10), "map": "data/levels/map3.tmx", "status": False},
        ]

    def draw(self):
        """Рисуем меню с учетом нажатых кнопок."""
        self.screen.blit(self.background, (0, 0))
        for button in self.buttons:
            # Если кнопка нажата, рисуем нажатое изображение
            image = button["push_image"] if button["status"] else button["image"]
            self.screen.blit(image, button["pos"])
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
