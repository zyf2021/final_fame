import pygame
from settings import BLACK, WIDTH, HEIGHT
from game import Game
from menu import MainMenu


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Милая ферма")


    menu = MainMenu(screen)

    selected_map = None

    while selected_map is None:  # Пока не выбрана карта
        menu.draw()
        selected_map = (menu.handle_events())

    print(selected_map)
    game = Game(selected_map)
    game.run()