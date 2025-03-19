# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRAUN = (221, 161, 94)

# Шрифты. Работает только с английским, поэтому все на английском...
FREDOKA = "data/fonts/FredokaOne-Regular.ttf"

# Размеры
WIDTH, HEIGHT = 512, 512
TILES = 16
SCALE_FACTOR = 2

# Скорость игрока (пикселей за кадр)
PLAYER_SPEED = 2
# Скорость анимации игрока (чем меньше число, тем быстрее)
PLAYER_ANIMATION_SPEED = 0.15
ENEMY_SPEED = 1


LIST_LEVELS = [
    {"id": "1", "title": "Level 1", "map": "data/levels/map4.tmx"},
    {"id": "2", "title": "Level 2", "map": "data/levels/map5.tmx"},
    {"id": "3", "title": "Level 3", "map": "data/levels/map6.tmx"},
    {"id": "4", "title": "Level 4", "map": "data/levels/map7.tmx"},
    {"id": "5", "title": "Level 5", "map": "data/levels/map8.tmx"},
]

LEVEL_BUTTONS = {
    "1": {"image": "data/assets/button.png", "push_image": "data/assets/button_push.png"},
    "2": {"image": "data/assets/button.png", "push_image": "data/assets/button_push.png"},
    "3": {"image": "data/assets/button.png", "push_image": "data/assets/button_push.png"},
    "4": {"image": "data/assets/button.png", "push_image": "data/assets/button_push.png"},
    "5": {"image": "data/assets/button.png", "push_image": "data/assets/button_push.png"},
    "6": {"image": "data/assets/button.png", "push_image": "data/assets/button_push.png"},
}

# Пути к изображениям меню
PATH_TO_BACKGROUND_IMAGE = "data/assets/background.png"
PATH_TO_DIALOG_MENU = "data/assets/continious_menu.png"

PATH_TO_START_MENU = "data/assets/start_menu.png"
PATH_TO_FINISH_MENU = "data/assets/final_game.png"
PATH_TO_SCORE_TABLE = "data/assets/score_table.png"

# Пути к изображениям кнопок
PATH_TO_MENU_BTN = "data/assets/btn_menu.png"
PATH_TO_MENU_BTN_PUSH = "data/assets/btn_menu_push.png"

PATH_TO_PLAY_BTN = "data/assets/btn_play.png"
PATH_TO_PLAY_BTN_PUSH = "data/assets/btn_play_push.png"

PATH_TO_YES_BTN = "data/assets/btn_yes.png"
PATH_TO_YES_BTN_PUSH = "data/assets/btn_yes_push.png"

PATH_TO_NO_BTN = "data/assets/btn_no.png"
PATH_TO_NO_BTN_PUSH = "data/assets/btn_no_push.png"

# путь к спрайтам
PATH_TO_PLAYER = "data/assets/player.png"
PATH_TO_ITEM = "data/assets/item.png"
PATH_TO_ENEMY = "data/assets/enemy.png"

# Путь к csv файлу хранилищу баллов
PATH_TO_DATA_SCORE = "data/storage/scores_utf_8_spec.csv"

WIN_SCORE = 200
