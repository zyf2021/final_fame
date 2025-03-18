import pygame
from settings import BLACK, WIDTH, HEIGHT, LIST_LEVELS
from game import Game
from menu import MainMenu
from game_over import GameOver
from settings import LIST_LEVELS


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Милая ферма")

    selected_map = None
    selected_id = None
    menu = MainMenu(screen)

    while True:  # Запускаем бесконечный цикл, чтобы можно было возвращаться в меню

        while selected_map is None:  # Ждем, пока игрок выберет карту
            menu.draw()
            selected_map, selected_id = menu.handle_events()

        game = Game(selected_map, selected_id)
        result = game.run()  # Запускаем игру и получаем результат

        if result == "menu":  # Если игрок нажал кнопку "Меню"
            selected_map = None # обнуляем текущие карты
            selected_id = None
            continue  # Возвращаемся в главное меню и втыкаемся в цикл

        elif result == "next":
            next_level = str(int(selected_id) + 1)  # Следующий ID
            next_map = next((lvl["map"] for lvl in LIST_LEVELS if lvl["id"] == next_level), None)

            if next_map:
                selected_map, selected_id = next_map, str(next_level)
            # else:
            #     final = GameOver(screen)
            #     final.draw()  # Показываем финальное окно
            #     break

        elif result == "quit":  # Если игрок закрыл игру
            print('попали в выход')
            break  # Выходим из основного цикла

    pygame.quit()