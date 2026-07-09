import pygame

GRAVITY = 0.05          # ускорение свободного падения за кадр
THRUST_POWER = 0.15     # сила двигателя, замедляющая падение

WHITE = (255, 255, 255)
RED = (200, 0, 0)


class Lander:
    """
    Класс отвечает только за корабль: положение, скорость, топливо и отрисовку.
    Ничего не знает про платформу или интерфейс - только физика падения.
    """

    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.speed_y = 0        # скорость падения (пикселей за кадр)
        self.fuel = 100
        self.width = 20
        self.height = 30
        self.crashed = False
        self.landed = False

    def update(self, engine_on):
        if self.crashed or self.landed:
            return

        # Гравитация всегда тянет корабль вниз
        self.speed_y = self.speed_y + GRAVITY

        # Если нажата стрелка вверх и есть топливо - включаем двигатель
        if engine_on and self.fuel > 0:
            self.speed_y = self.speed_y - THRUST_POWER
            self.fuel = self.fuel - 1
            if self.fuel < 0:
                self.fuel = 0

        self.y = self.y + self.speed_y

    def draw(self, screen):
        # Рисуем корабль в виде треугольника
        top_point = (self.x, self.y)
        left_point = (self.x - self.width // 2, self.y + self.height)
        right_point = (self.x + self.width // 2, self.y + self.height)

        color = RED if self.crashed else WHITE
        pygame.draw.polygon(screen, color, [top_point, left_point, right_point])

    def get_bottom_y(self):
        return self.y + self.height
