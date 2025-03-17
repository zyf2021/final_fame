import pygame
import pytmx
from items import Item
from enemy import Enemy
from settings import PATH_TO_ITEM

class TileMap:
    """Класс загрузки карты из Tiled (TMX)"""
    def __init__(self, filename):
        self.tmx_data = pytmx.load_pygame(filename)
        self.tilewidth = self.tmx_data.tilewidth
        self.tileheight = self.tmx_data.tileheight
        self.width = self.tmx_data.width * self.tilewidth
        self.height = self.tmx_data.height * self.tileheight

        self.walkable_tiles = self.get_walkable_tiles()  # Список проходимых координат

    def get_walkable_tiles(self):
        """Сканирует слой 'Dirts' и собирает координаты проходимых клеток."""
        walkable = set()
        for layer in self.tmx_data.layers:
            if layer.name == "Dirts":  # Тропинки
                for x, y, gid in layer:
                    if gid:
                        walkable.add((x * self.tilewidth, y * self.tileheight))
        return walkable

    def check_walkable(self, player_rect):
        """Проверяет, что игрок находится на тропинке."""
        tile_x = (player_rect.centerx // self.tilewidth) * self.tilewidth
        tile_y = (player_rect.centery // self.tileheight) * self.tileheight
        return (tile_x, tile_y) in self.walkable_tiles

    def get_items(self):
        """Получает все призы из слоя 'Items' и возвращает Group Items"""
        items = pygame.sprite.Group()
        # items_coord = []
        for obj in self.tmx_data.objects:
            if obj.name == "Items":  # Фильтруем только призы
                item_sprite = Item(obj.x, obj.y, pygame.image.load(PATH_TO_ITEM).convert_alpha())
                items.add(item_sprite)
                # items_coord.append((obj.x, obj.y))
            # print(obj.name)
        return items

    def load_enemies(self):
        """Загружает врагов с карты и добавляет их в группу"""
        enemies = pygame.sprite.Group()
        for obj in self.tmx_data.objects:
            if obj.name == "Enemy":
                enemy = Enemy(obj.x, obj.y)
                enemies.add(enemy)  # Добавляем врага в группу
        return enemies




class TileRenderer:
    """Отрисовывает карту"""
    def __init__(self, tilemap):
        self.tilemap = tilemap

    def draw(self, screen):
        """Отображает карту на экране"""
        for layer in self.tilemap.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tilemap.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (x * self.tilemap.tilewidth, y * self.tilemap.tileheight))



class GameMap:
    """Класс управления картой"""
    def __init__(self, filename):
        self.tilemap = TileMap(filename)
        self.renderer = TileRenderer(self.tilemap)
    def draw(self, screen):
        """Отрисовка карты"""
        self.renderer.draw(screen)
    def check_walkable(self, player_rect):
        """Проверяет, можно ли ходить по текущей клетке"""
        return self.tilemap.check_walkable(player_rect)
