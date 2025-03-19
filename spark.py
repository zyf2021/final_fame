import pygame


class Spark(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet, frame_size=(16, 16), frame_count=4, speed=4):
        super().__init__()
        self.frames = self.load_frames(sprite_sheet, frame_size, frame_count)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed  # Чем выше значение, тем медленнее анимация
        self.frame_delay = 0  # Счётчик задержки кадров

    def load_frames(self, sprite_sheet, frame_size, frame_count):
        """Разрезаем спрайт-лист на кадры"""
        frames = []
        for i in range(frame_count):
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_size[0], 0, *frame_size))
            frames.append(frame)
        return frames

    def update(self):
        """Обновляем анимацию с задержкой"""
        self.frame_delay += 1
        if self.frame_delay >= self.speed:  # Если прошло достаточно времени
            self.frame_delay = 0  # Сбрасываем счётчик
            self.current_frame += 1
            if self.current_frame < len(self.frames):
                self.image = self.frames[self.current_frame]
            else:
                self.kill()  # Удаляем объект после завершения анимации
