import pygame
import pygame_widgets
from pygame_widgets.button import Button
import os
import sys
import game
import settings

from Python_Groupe_4_Tours.QuoridorPython.require.user_interface.colors import get_white, get_dark_violet, get_blue_cyan, \
    get_red, get_yellow

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Launch:
    def __init__(self):
        pygame.init()
        self.__on_screen_surface = None
        self.__run = True
        self.__game_state = "Launch"  # New game state variable

        # Initialisations de la taille de la fenêtre
        self.__window_size = (1920, 1080)

        # Charger l'image de l'arrière-plan
        self.__background_image = pygame.image.load(resource_path("user_interface/images/background.jpg"))

        # Charger l'image Titre
        self.__image_title = pygame.image.load(resource_path("user_interface/images/title.png"))
        self.__image_rect = self.__image_title.get_rect(center=(self.__window_size[0] // 2, 100))

        # Chargement des polices de caractères
        self.__font_load = resource_path("user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf")
        self.__font_interface_XL = pygame.font.Font(self.__font_load, 70)

        # Initialisations des tailles de widget
        self.__button_width = 400
        self.__button_height = 150

        # Espacement entre les boutons
        self.__space = 300

        # Initialisations des positions de widget
        self.__x_position = ((self.__window_size[0] - (3 * self.__button_width + 2 * self.__space)) / 2) + 360
        self.__y_position = 800

    def display(self):
        pygame.display.set_caption("QUORIDOR")
        self.__on_screen_surface = pygame.display.set_mode(self.__window_size, pygame.NOFRAME | pygame.DOUBLEBUF)
        clock = pygame.time.Clock()
        fps = 30  # Nombre de trames par seconde (FPS)
        clock.tick(fps)

        button_rect_quit = Button(
            self.__on_screen_surface, 1600, 40,
            int(self.__button_width / 1.5), int(self.__button_height / 1.5),
            text='Quit',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_red(),
            radius=5,
            font=self.__font_interface_XL,
            textVAlign='center',
            onClick=lambda: (self.quit())
        )

        button_rect_play = Button(
            self.__on_screen_surface, int(self.__x_position), self.__y_position,
            self.__button_width, self.__button_height,
            text='Play',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_dark_violet(),
            radius=5,
            font=self.__font_interface_XL,
            textVAlign='center',
            onClick=lambda: (self.open_game())
        )

        button_rect_settings = Button(
            self.__on_screen_surface, int(self.__x_position + self.__button_width + self.__space), self.__y_position,
            self.__button_width, int(self.__button_height),
            text='Settings',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_yellow(),
            radius=5,
            font=self.__font_interface_XL,
            textVAlign='center',
            onClick=lambda: (self.open_settings())
        )

        while self.__run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.__run = False

            # Update game state
            if self.__game_state == "Game":
                button_rect_quit.hide()
                button_rect_play.hide()
                button_rect_settings.hide()
                self.__on_screen_surface.fill(get_blue_cyan())
                game.Game(2, 11, 1, 24, 0, 0, False, False, False)

            elif self.__game_state == "Settings":
                button_rect_quit.hide()
                button_rect_play.hide()
                button_rect_settings.hide()
                self.__on_screen_surface.fill(get_blue_cyan())
                settings.Settings().display()

            else:
                self.__on_screen_surface.blit(self.__background_image, (0, 0))  # Afficher l'arrière-plan
                self.__on_screen_surface.blit(self.__image_title, (384.5, 120))  # Afficher le titre

            pygame_widgets.update(pygame.event.get())
            pygame.display.flip()

            clock.tick(fps)  # Limiter le nombre de trames par seconde

    pygame.quit()

    def quit(self):
        pygame.quit()

    def open_game(self):
        self.__game_state = "Game"

    def open_settings(self):
        self.__game_state = "Settings"