import pygame
from pygame_widgets.button import Button
import os
import sys
import subprocess

from Python_Groupe_4_Tours.QuoridorPython.main import Game
#Windows :
from Python_Groupe_4_Tours.QuoridorPython.user_interface.colors import get_white, get_dark_violet, get_blue_cyan, get_red, get_yellow
#macOS :
#from user_interface.colors import get_white, get_black, get_red, get_blue, get_yellow

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Launch:
    def __init__(self):
        self.__onScreenSurface = None
        self.__continuer = True

    def launch(self):
        pygame.init()
        windowSize = (1920, 1080)
        pygame.display.set_caption("QUORIDOR")
        self.__onScreenSurface = pygame.display.set_mode(windowSize, pygame.FULLSCREEN | pygame.RESIZABLE)
        clock = pygame.time.Clock()
        fps = 30  # Nombre de trames par seconde (FPS)
        clock.tick(fps)

        # Charger l'image de l'arrière-plan
        background_image = pygame.image.load(resource_path("../../user_interface/image/launch/background.jpg"))
        # Charger l'image Titre
        image_title = pygame.image.load(resource_path("../../user_interface/image/launch/titre.png"))
        image_rect = image_title.get_rect(center=(windowSize[0] // 2, 100))

        font_load = resource_path("../../user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf")
        font_interface_XL = pygame.font.Font(font_load, 70)
        button_width = 400
        button_height = 150
        space = 300  # Espacement entre les boutons

        x_position = (windowSize[0] - (3 * button_width + 2 * space)) / 2
        y_position = 800

        button_rect_back = Button(
            self.__onScreenSurface, 1600, 40, button_width / 1.5, button_height / 1.5,
            text='Quit',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_red(),
            radius=5,
            font=font_interface_XL,
            textVAlign='center',
            # onClick=lambda: (Game.exit())
        )

        button_rect_load = Button(
            self.__onScreenSurface, x_position, y_position, button_width, button_height,
            text='Load',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_blue_cyan(),
            radius=5,
            font=font_interface_XL,
            textVAlign='center',
            #onClick=
        )

        button_rect_play = Button(
            self.__onScreenSurface, x_position + button_width + space, y_position, button_width, button_height,
            text='Play',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_dark_violet(),
            radius=5,
            font=font_interface_XL,
            textVAlign='center',
            #onClick=
        )

        button_rect_settings = Button(
            self.__onScreenSurface, x_position + 2 * (button_width + space), y_position, button_width, button_height,
            text='Settings',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_yellow(),
            radius=5,
            font=font_interface_XL,
            textVAlign='center',
            #onClick=
        )

        def exit(self):
            self.__continuer = False
            return self.__continuer

        while self.__continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__continuer = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.__continuer = False

            # Dessiner les éléments sur l'écran
            self.__onScreenSurface.blit(background_image, (0, 0))  # Afficher l'arrière-plan
            self.__onScreenSurface.blit(image_title, (384.5, 120))  # Afficher le titre

            events = pygame.event.get()  # Capturer les événements pygame

            # Gérer les événements des boutons
            button_rect_back.listen(events)
            button_rect_load.listen(events)
            button_rect_play.listen(events)
            button_rect_settings.listen(events)

            # Dessiner les boutons
            button_rect_back.draw()
            button_rect_load.draw()
            button_rect_play.draw()
            button_rect_settings.draw()

            pygame.display.update()  # Mettre à jour l'écran

            clock.tick(fps)  # Limiter le nombre de trames par seconde

        pygame.quit()

Launch().launch()