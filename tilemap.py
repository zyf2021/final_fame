import pygame
import pytmx
from items import Item
from enemy import Enemy
from settings import PATH_TO_ITEM, PATH_TO_BACKGROUND_IMAGE


class GameMap:
    """Класс управления картой и отрисовка с фоном"""
    def __init__(self, filename):
        # Загружаем данные карты из TMX
        self.tmx_data = pytmx.load_pygame(filename)
        self.tilewidth = self.tmx_data.tilewidth
        self.tileheight = self.tmx_data.tileheight
        self.width = self.tmx_data.width * self.tilewidth
        self.height = self.tmx_data.height * self.tileheight

        # Список проходимых координат
        self.walkable_tiles = self.get_walkable_tiles()

        # Загружаем изображения для фона
        self.background_image = pygame.image.load(PATH_TO_BACKGROUND_IMAGE).convert_alpha()

    def get_walkable_tiles(self):
        """Сканирует слой 'Dirts' и собирает координаты проходимых клеток."""
        walkable = set()
        for layer in self.tmx_data.layers:
            if layer.name == "Dirts":  # Тропинки
                for x, y, gid in layer:
                    if gid:
                        walkable.add((x * self.tilewidth, y * self.tileheight))
        return walkable

    def check_walkable(self, new_rect):
        """Проверяет, можно ли ходить по текущей клетке (по абсолютным координатам)."""
        tile_x = (new_rect.centerx // self.tilewidth) * self.tilewidth
        tile_y = (new_rect.centery // self.tileheight) * self.tileheight

        return (tile_x, tile_y) in self.walkable_tiles

    def load_items(self):
        """Получает все призы из слоя 'Items' и возвращает Group Items"""
        items = pygame.sprite.Group()
        for obj in self.tmx_data.objects:
            if obj.name == "Items":
                items.add(Item(obj.x, obj.y))
        return items

    def load_enemies(self):
        """Загружает врагов с карты и добавляет их в группу"""
        enemies = pygame.sprite.Group()
        for obj in self.tmx_data.objects:
            if obj.name == "Enemy":
                enemies.add(Enemy(obj.x, obj.y))
        return enemies

    def draw_background(self, screen, camera):
        """Отображает статичный фон по центру экрана"""
        if self.background_image:
            screen_width, screen_height = screen.get_size()
            bg_width, bg_height = self.background_image.get_width(), self.background_image.get_height()

            # Вычисляем смещение, чтобы фон был по центру экрана
            offset_x = (screen_width - bg_width) // 2
            offset_y = (screen_height - bg_height) // 2

            # Отображаем фон по центру экрана
            screen.blit(self.background_image, (offset_x, offset_y))

    def draw(self, screen, camera):
        """Отображение карты с фоном и слоями"""
        # Рисуем статичный фон
        self.draw_background(screen, camera)

        # Отображаем все слои карты
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        screen_x = x * self.tilewidth - camera.offset_x
                        screen_y = y * self.tileheight - camera.offset_y
                        screen.blit(tile, (screen_x, screen_y))
