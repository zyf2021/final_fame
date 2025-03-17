from settings import WIDTH, HEIGHT


class Camera:
    def __init__(self, map_width, map_height):
        self.offset_x = 0
        self.offset_y = 0

    def apply(self, obj):
        """Применяет сдвиг камеры к объекту"""
        obj.rect.x = obj.abs_x - self.offset_x
        obj.rect.y = obj.abs_y - self.offset_y

    def update(self, target):
        """Следит за игроком и ограничивает движение камеры"""
        # self.offset_x = target.abs_x - WIDTH // 2
        # self.offset_y = target.abs_y - HEIGHT // 2
        self.offset_x = (target.abs_x + target.rect.width // 2 - WIDTH // 2)
        self.offset_y = (target.abs_y + target.rect.height // 2 - HEIGHT // 2)

