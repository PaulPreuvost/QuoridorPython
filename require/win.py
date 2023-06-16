import pygame
import pygame_widgets
from pygame_widgets.button import Button
import os
import sys
import game

from user_interface.colors import get_white, get_blue_cyan, \
    get_dark_violet


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
class Win:
    def __init__(self, winner: str):
        self.__on_screen_surface = None
        self.__run = True
        self.__winner = winner
        self.__game_state = "Win"

    def display(self):
        pygame.init()
        windowSize = (1920, 1080)
        pygame.display.set_caption("QUORIDOR")
        self.__on_screen_surface = pygame.display.set_mode(windowSize, pygame.FULLSCREEN)
        clock = pygame.time.Clock()
        fps = 30  # Nombre de trames par seconde (FPS)
        clock.tick(fps)

        background_image = pygame.image.load(resource_path("require/user_interface/images/background.jpg"))

        font_load = resource_path("require/user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf")
        font_interface__XXXL = pygame.font.Font(font_load, 250)
        font_interface_L = pygame.font.Font(font_load, 45)
        button_width = 250
        button_height = 100
        space = 300  # Espacement entre les boutons

        x_position = (windowSize[0] - (3 * button_width + 2 * space)) / 2
        y_position = 700

        texte_surface = font_interface__XXXL.render(self.__winner + ' a gagné', True, get_white())
        texte_rect = texte_surface.get_rect()
        texte_rect.center = (windowSize[0] // 2, windowSize[1] // 3)

        self.__button_rect_play = Button(
            self.__on_screen_surface, int((x_position + space) + 100), y_position,
            button_width, button_height,
            text='Replay',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_dark_violet(),
            radius=5,
            font=font_interface_L,
            textVAlign='center',
            onClick=lambda: self.replay()
        )

        self.__button_rect_quit = Button(
            self.__on_screen_surface, int((x_position + space) + 400), y_position,
            button_width, button_height,
            text='Quit',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_dark_violet(),
            radius=5,
            font=font_interface_L,
            textVAlign='center',
            onClick=lambda: self.quit()
        )

        while self.__run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.__run = False

            # Dessiner les éléments sur l'écran
            self.__on_screen_surface.blit(background_image, (0, 0))  # Afficher l'arrière-plan

            texte_surface = font_interface__XXXL.render(self.__winner + ' wins !', True, get_white())
            texte_rect = texte_surface.get_rect()
            texte_rect.center = (windowSize[0] // 2, windowSize[1] // 3)

            # Update game state
            if self.__game_state == "Game":
                self.__on_screen_surface.fill(get_blue_cyan())
                self.hide_widgets()
                game.Game(2, 11, 1, 24, 0, False, False, False)

            else:
                self.show_widgets()
                self.__on_screen_surface.blit(texte_surface, texte_rect)

            pygame_widgets.update(pygame.event.get())
            pygame.display.update()

            pygame.display.flip()

    pygame.quit()

    def quit(self):
        pygame.quit()

    def replay(self):
        self.__game_state = "Game"

    def hide_widgets(self):
        self.__button_rect_play.hide()
        self.__button_rect_quit.hide()

    def show_widgets(self):
        self.__button_rect_play.show()
        self.__button_rect_quit.show()
