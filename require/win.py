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
    # Fonction qui INIT
    def __init__(self, winner: str):
        # Initialisation princiaple 
        pygame.init()
        self.__on_screen_surface = None
        self.__run = True
        self.__winner = winner
        self.__game_state = "Win"

        # Initialisations de la taille de la fenêtre
        self.__window_size = (1920, 1080)

        # Charger l'image de l'arrière-plan
        self.__background_image = pygame.image.load(resource_path("require/user_interface/images/background.jpg"))
        
        # Initialisation des polices d'écritures 
        self.__font_load = resource_path("require/user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf")
        self.__font_interface__XXXL = pygame.font.Font(self.__font_load, 250)
        self.__font_interface_L = pygame.font.Font(self.__font_load, 45)

        # Initialisations des tailles des widgets
        self.__button_width = 250
        self.__button_height = 100

        # Espacement entre les boutons
        self.__space = 300

        # Initialisations des positions de widgets
        self.__x_position = (self.__window_size[0] - (3 * self.__button_width + 2 * self.__space)) / 2
        self.__y_position = 700


    # Fonction qui affiche le gagnant
    def display(self):
        pygame.init()  # Initialisation du module pygame
        pygame.display.set_caption("QUORIDOR")  # Définition du titre de la fenêtre
        self.__on_screen_surface = pygame.display.set_mode(self.__window_size, pygame.FULLSCREEN)  # Création de la surface d'affichage
        self.__clock = pygame.time.Clock()  # Création d'un objet clock pour gérer les fréquences d'images
        self.__fps = 30  # Nombre de trames par seconde (images par seconde)
        self.__clock.tick(self.__fps)  # Limiter le nombre de trames par seconde

        # Création de la surface de texte affichant le gagnant
        self.__texte_surface_win = self.__font_interface__XXXL.render(self.__winner + ' a gagné', True, get_white())
        self.__texte_rect_win = self.__texte_surface_win.get_rect()
        self.__texte_rect_win.center = (self.__window_size[0] // 2, self.__window_size[1] // 3)

        # Création du bouton "Replay" avec ses paramètres
        self.__button_rect_play = Button(
            self.__on_screen_surface, int((self.__x_position + self.__space) + 100), self.__y_position,
            self.__button_width, self.__button_height,
            text='Replay',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_dark_violet(),
            radius=5,
            font=self.__font_interface_L,
            textVAlign='center',
            onClick=lambda: self.replay() # Appel la fonction d'ouverture du jeu (open_game()) quand on clic
        )

        # Création du bouton "Quit" avec ses paramètres
        self.__button_rect_quit = Button(
            self.__on_screen_surface, int((self.__x_position + self.__space) + 400), self.__y_position,
            self.__button_width, self.__button_height,
            text='Quit',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_dark_violet(),
            radius=5,
            font=self.__font_interface_L,
            textVAlign='center',
            onClick=lambda: (self.quit()) # Appel la fonction de fermeture de la fenêtre (quit()) quand on clic
        )

        # Boucle principale du jeu
        while self.__run:
            #Tant que self.__run renvoie True, la fenêtre est active
            for event in pygame.event.get():  # Récupère les événements
                if event.type == pygame.QUIT:  # Si l'événement est de type QUIT, la fenêtre se ferme 
                    pygame.quit() # Arrête la boucle principale et quitte le jeu
                    exit()

            self.__on_screen_surface.blit(self.__background_image, (0, 0))  # Affiche l'arrière-plan sur la surface d'affichage

            # Affichage du texte indiquant le gagnant
            self.__texte_surface_win = self.__font_interface__XXXL.render(self.__winner + ' wins !', True, get_white())
            self.__texte_rect_win = self.__texte_surface_win.get_rect()
            self.__texte_rect_win.center = (self.__window_size[0] // 2, self.__window_size[1] // 3)

            # Mise à jour de l'état du jeu
            if self.__game_state == "Game":  # Test si l'état du jeu est "Game"
                self.__on_screen_surface.fill(get_blue_cyan())  # Remplit la surface d'affichage avec une couleur
                self.hide_widgets()  # Appel la fonction qui cache les widgets
                game.Game(2, 9, 1, 20, 0, False, False, False)  # Appel la fonction de lancement du jeu dans le fichier game.py
            else:  # Test si l'état du jeu n'est pas "Game"
                self.show_widgets()  # Appel la fonction qui affiche les widgets
                self.__on_screen_surface.blit(self.__texte_surface_win, self.__texte_rect_win)  # Affiche le texte du gagnant

            pygame_widgets.update(pygame.event.get())  # Met à jour les widgets en fonction des événements pygame
            pygame.display.update()  # Met à jour l'affichage de la fenêtre
            pygame.display.flip()  # Rafraîchit la fenêtre entière

        pygame.quit()  # Quitte le module pygame

    def quit(self): # Quitte le module pygame
        pygame.quit()
        exit()

    def replay(self): # Fonction pour ouvrir la page de jeu
        self.__game_state = "Game"  # Change l'état du jeux à "Game"

    def hide_widgets(self):
        self.__button_rect_play.hide()  # Cache le bouton "Replay"
        self.__button_rect_quit.hide()  # Cache le bouton "Quit"

    def show_widgets(self):
        self.__button_rect_play.show()  # Affiche le bouton "Replay"
        self.__button_rect_quit.show()  # Affiche le bouton "Quit"
