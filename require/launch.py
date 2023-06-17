import pygame
import pygame_widgets
from pygame_widgets.button import Button
import os
import sys
import game
import settings

from user_interface.colors import get_white, get_dark_violet, get_blue_cyan, \
    get_red, get_yellow

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Launch:
    # Fonction qui INIT
    def __init__(self):
        pygame.init()
        self.__on_screen_surface = None
        self.__run = True
        self.__game_state = "Launch"  # New game state variable

        # Initialisations de la taille de la fenêtre
        self.__window_size = (1920, 1080)

        # Charger l'image de l'arrière-plan
        self.__background_image = pygame.image.load(resource_path("require/user_interface/images/background.jpg"))

        # Charger l'image Titre
        self.__image_title = pygame.image.load(resource_path("require/user_interface/images/title.png"))
        self.__image_rect = self.__image_title.get_rect(center=(self.__window_size[0] // 2, 100))

        # Chargement des polices de caractères
        self.__font_load = resource_path("require/user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf")
        self.__font_interface_XL = pygame.font.Font(self.__font_load, 70)

        # Initialisations des tailles des widgets
        self.__button_width = 400
        self.__button_height = 150

        # Espacement entre les boutons
        self.__space = 300

        # Initialisations des positions des widgets
        self.__x_position = ((self.__window_size[0] - (3 * self.__button_width + 2 * self.__space)) / 2) + 360
        self.__y_position = 800


    def display(self):
        pygame.init()  # Initialisation du module pygame
        pygame.display.set_caption("QUORIDOR")  # Définition du titre de la fenêtre
        self.__on_screen_surface = pygame.display.set_mode(self.__window_size, pygame.FULLSCREEN)  # Création de la surface d'affichage
        self.__clock = pygame.time.Clock()  # Création d'un objet clock pour gérer les fréquences d'images
        self.__fps = 30  # Nombre de trames par seconde (images par seconde)
        self.__clock.tick(self.__fps) # Limiter le nombre de trames par seconde


        # Création du bouton "Quit" avec ses paramètres
        self.__button_rect_quit = Button(
            self.__on_screen_surface, 1600, 40,
            int(self.__button_width / 1.5), int(self.__button_height / 1.5),
            text='Quit',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_red(),
            radius=5,
            font=self.__font_interface_XL,
            textVAlign='center',
            onClick=lambda: (self.quit()) # Appel la fonction de fermeture de la fenêtre (quit()) quand on clic
        )

        # Création du bouton "Play" avec ses paramètres
        self.__button_rect_play = Button(
            self.__on_screen_surface, int(self.__x_position), self.__y_position,
            self.__button_width, self.__button_height,
            text='Play',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_dark_violet(),
            radius=5,
            font=self.__font_interface_XL,
            textVAlign='center',
            onClick=lambda: (self.open_game()) # Appel la fonction d'ouverture du jeu (open_game()) quand on clic
        )

        # Création du bouton "Settings" avec ses paramètres
        self.__button_rect_settings = Button(
            self.__on_screen_surface, int(self.__x_position + self.__button_width + self.__space), self.__y_position,
            self.__button_width, int(self.__button_height),
            text='Settings',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_yellow(),
            radius=5,
            font=self.__font_interface_XL,
            textVAlign='center',
            onClick=lambda: (self.open_settings()) # Appel la fonction d'ouverture des paramêtres (open_settings()) quand on clic
        )

        # Boucle principale du jeu
        while self.__run:
            #Tant que self.__run renvoie True, la fenêtre est active
            for event in pygame.event.get():  # Récupère les événements
                if event.type == pygame.QUIT:  # Si l'événement est de type QUIT, la fenêtre se ferme 
                    pygame.quit() # Arrête la boucle principale et quitte le jeu
                    exit()

            # Mise à jour de l'état du jeu
            if self.__game_state == "Game": # Vérifie si le game_state est égale à "Game"
                # Cache les widgets
                self.__button_rect_quit.hide()
                self.__button_rect_play.hide()
                self.__button_rect_settings.hide()
                self.__on_screen_surface.fill(get_blue_cyan()) # Remplie la zone de l'écran en bleue
                game.Game(2, 9, 1, 20, 0, False, False, False) # Appel la classe Game, avec les valeurs par défaut qui se trouve dans le fichier game.py

            elif self.__game_state == "Settings":  # Vérifie si le game_state est égale à "Settings"
                # Cache les widgets
                self.__button_rect_quit.hide()
                self.__button_rect_play.hide()
                self.__button_rect_settings.hide()
                self.__on_screen_surface.fill(get_blue_cyan()) # Remplie la zone de l'écran en bleue
                settings.Settings().display() # Appel la fonction display de la classe Settings, qui se trouve dans le fichier laucnh.py

            else:
                self.__on_screen_surface.blit(self.__background_image, (0, 0))  # Afficher l'arrière-plan
                self.__on_screen_surface.blit(self.__image_title, (384.5, 120))  # Afficher le titre

            pygame_widgets.update(pygame.event.get())
            pygame.display.flip()


    pygame.quit() # Quitte le module pygame

    def quit(self): # Quitte le module pygame
        pygame.quit()
        exit()

    def open_game(self):
        self.__game_state = "Game" # Change l'état du jeux à "Game"

    def open_settings(self):
        self.__game_state = "Settings" # Change l'état du jeux à "Settings"