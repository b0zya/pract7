import sys
import pygame
import tkinter as tk
from tkinter import messagebox

from lander import Lander

WIDTH = 800
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (150, 150, 150)

SAFE_LANDING_SPEED = 3   # максимальная скорость для мягкой посадки

PLATFORM_Y = 550          # высота посадочной платформы
PLATFORM_X1 = 300
PLATFORM_X2 = 500

START_X = WIDTH // 2
START_Y = 50


class Game:
    """
    Класс отвечает за окно игры, интерфейс (HUD, кнопка перезапуска),
    посадочную платформу и основной игровой цикл.
    Физику корабля делегирует классу Lander.
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Лунная станция")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

        self.lander = Lander(START_X, START_Y)
        self.game_over = False
        self.restart_button_rect = pygame.Rect(WIDTH - 150, 20, 120, 40)

    def restart_level(self):
        self.lander = Lander(START_X, START_Y)
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button_rect.collidepoint(event.pos):
                    self.restart_level()

    def check_landing(self):
        """
        Задача №4 - проверка условий посадки.
        Возвращает: (touched, success)
        """
        lander = self.lander

        if lander.get_bottom_y() >= PLATFORM_Y and not lander.crashed and not lander.landed:
            on_platform = PLATFORM_X1 <= lander.x <= PLATFORM_X2

            if on_platform and lander.speed_y < SAFE_LANDING_SPEED:
                lander.landed = True
                lander.speed_y = 0
                return True, True
            else:
                lander.crashed = True
                lander.speed_y = 0
                return True, False

        return False, False

    def show_result_message(self, success):
        """Показывает всплывающее окно через tkinter"""
        root = tk.Tk()
        root.withdraw()

        if success:
            messagebox.showinfo("Результат", "Успешная посадка!")
        else:
            messagebox.showinfo("Результат", "Корабль разбился!")

        root.destroy()

    def draw_hud(self):
        """Задача №1 - вывод запаса топлива и скорости падения на экран"""
        fuel_text = self.font.render("Топливо: " + str(self.lander.fuel), True, WHITE)
        speed_text = self.font.render("Скорость: " + str(round(self.lander.speed_y, 2)), True, WHITE)

        self.screen.blit(fuel_text, (20, 20))
        self.screen.blit(speed_text, (20, 50))

    def draw_platform(self):
        """Задача №3 - посадочная платформа (зеленая линия внизу экрана)"""
        pygame.draw.line(self.screen, GREEN, (PLATFORM_X1, PLATFORM_Y), (PLATFORM_X2, PLATFORM_Y), 5)

    def draw_restart_button(self):
        """Задача №1 - кнопка перезапуска уровня"""
        pygame.draw.rect(self.screen, GRAY, self.restart_button_rect)
        text = self.font.render("Перезапуск", True, BLACK)
        self.screen.blit(text, (self.restart_button_rect.x + 5, self.restart_button_rect.y + 10))

    def draw_status_text(self):
        if self.lander.crashed:
            status_text = self.font.render("КОРАБЛЬ РАЗБИЛСЯ", True, RED)
            self.screen.blit(status_text, (WIDTH // 2 - 100, HEIGHT // 2))
        elif self.lander.landed:
            status_text = self.font.render("УСПЕШНАЯ ПОСАДКА", True, GREEN)
            self.screen.blit(status_text, (WIDTH // 2 - 100, HEIGHT // 2))

    def run(self):
        running = True
        while running:
            self.handle_events()

            keys = pygame.key.get_pressed()
            engine_on = keys[pygame.K_UP]

            if not self.game_over:
                self.lander.update(engine_on)

                touched, success = self.check_landing()
                if touched:
                    self.game_over = True
                    self.show_result_message(success)

            self.screen.fill(BLACK)
            self.draw_platform()
            self.lander.draw(self.screen)
            self.draw_hud()
            self.draw_restart_button()
            self.draw_status_text()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
