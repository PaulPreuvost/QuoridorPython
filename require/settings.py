import sys
import os
import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import game
import launch
import serveur

from user_interface.colors import get_black, get_red, \
    get_white, get_dark_violet, get_blue_cyan



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Settings:
    def __init__(self):
        pygame.init()
        self.__on_screen_surface = None
        self.__run= True
        self.__game_state = "Settings"

        # Initialisation de la taille de la fenêtre
        self.__window_size = (1920, 1080)

        # Chargement l'image de l'arrière-plan
        self.__background_image = pygame.image.load(resource_path("require/user_interface/images/background.jpg"))

        # Chargement des polices de caractères
        self.__font_load = resource_path("require/user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf")
        self.__font_interface__XXXL = pygame.font.Font(self.__font_load, 130)
        self.__font_interface_XL = pygame.font.Font(self.__font_load, 70)
        self.__font_interface__L = pygame.font.Font(self.__font_load, 45)
        self.__font_interface__M = pygame.font.Font(self.__font_load, 20)

        # Initialisations des tailles de widget
        self.__button_width = 400
        self.__button_height = 150
        self.__button_width_dropdown = 200
        self.__button_height_dropdown = 50
        self.__button_width_validate = 100
        self.__button_height_validate = 50

        # Espacement entre les boutons
        self.__space = 150

        # Initialisations des positions de widget
        self.__x_position = ((self.__window_size[0] - (2 * self.__button_width + 1 * self.__space)) / 2)
        self.__y_position = 800
        self.__x_position_dropdown = 100
        self.__y_position_dropdown = 300
        self.__x_position_validate = (self.__x_position_dropdown + self.__button_width_dropdown) + 10
        self.__button_text_validate = "Enter"  # Texte du bouton Validation
        self.__zone_title_size = (1000, 250)
        self.__zone_host_ip_size = (1000, 250)
        self.__zone_client_ip_size = (1000, 250)


        # Initialisations des paramêtres à choisir par l'utilisateur, 
        # On leurs attribuent les valeurs par défaut 
        self.__selected_size_board = 9 # Taille du plateau
        self.__selected_number_of_players = 2 # Nombre de joueurs
        self.__selected_sound_volume = 1 # Volume de la musique
        self.__selected_number_of_barrier = 20 # Nombre de barrieres
        self.__selected_save = 0 # Sauvegarde
        self.__selected_network = False # Si on joue en réseau
        self.__selected_network_choice = False # Paramêtre du réseau
        self.__network_host = False # Si on est host de la partie
        self.__network_client = False # Si on est client de la partie 
        self.__client_ip_choose = None # Ip choisi par le client pour se connecter au pc du host
        self.__ip_client = "" # Variable temporaire stockant l'ip


    def display(self):
        pygame.init()
        pygame.display.set_caption("QUORIDOR")
        self.__on_screen_surface = pygame.display.set_mode(self.__window_size, pygame.FULLSCREEN)
        self.__clock = pygame.time.Clock()
        self.__fps = 30  # Nombre de trames par seconde (self.__fps)
        self.__clock.tick(self.__fps) # Limiter le nombre de trames par seconde

        # Zone qui permet d'afficher le titre de la fenêtre 
        self.__zone_title = pygame.Surface(self.__zone_title_size, pygame.SRCALPHA)
        title_board = self.__font_interface__XXXL.render("Settings", True, get_white())
        title_board_outline = self.__font_interface__XXXL.render("Settings", True, get_black())
        self.__zone_title.blit(title_board_outline, (0 + 2, 0 + 2))
        self.__zone_title.blit(title_board, (0, 0))

        # Bouton de choix de la taille du plateau 
        self.__btn_size_board = Dropdown(
            self.__on_screen_surface, int(self.__x_position_dropdown), self.__y_position_dropdown,
            self.__button_width_dropdown, self.__button_height_dropdown,
            name='Board Size',
            choices=[
                '5x5',
                '7x7',
                '9x9',
                '11x11',
            ],
            borderRadius=3,
            colour=get_white(),
            values=[5, 7, 9, 11],
            font=self.__font_interface__M,
            direction='down'
        )

        # Bouton de validation de la taille du plateau 
        self.__validate_size_board = Button(
            self.__on_screen_surface, int(self.__x_position_validate), self.__y_position_dropdown,
            self.__button_width_validate, self.__button_height_validate,
            text=self.__button_text_validate,
            margin=15,
            inactiveColour=get_red(),
            pressedColour=get_black(),
            radius=5,
            font=self.__font_interface__M,
            textVAlign='center',
            onClick=lambda: (select_size_board()) # Appel la fonction de validation de la taille du plateau 
        )

        # Fonction de validation de la taille du plateau 
        def select_size_board():
            self.__selected_size_board = self.__btn_size_board.getSelected()

        # Bouton de choix du nombre de joueurs 
        self.__btn_number_player = Dropdown(
            self.__on_screen_surface, int(self.__x_position_dropdown + self.__button_width_dropdown + self.__space),
            self.__y_position_dropdown,
            self.__button_width_dropdown, self.__button_height_dropdown,
            name='Number of Players',
            choices=[
                '1 vs IA',
                '2',
                '3 vs IA',
                '4',
            ],
            borderRadius=3,
            colour=get_white(),
            values=[1, 2, 3, 4],
            font=self.__font_interface__M,
            direction='down'
        )

        # Bouton de validation du nombre de joueurs 
        self.__validate_number_player = Button(
            self.__on_screen_surface, int(self.__x_position_validate + self.__button_width_dropdown + self.__space),
            self.__y_position_dropdown,
            self.__button_width_validate, int(self.__button_height_validate),
            text=self.__button_text_validate,
            margin=15,
            inactiveColour=get_red(),
            pressedColour=get_black(),
            radius=5,
            font=self.__font_interface__M,
            textVAlign='center',
            onClick=lambda: (select_number_of_player())# Appel la fonction de validation du nombre de joueurs
        )

        # Fonction de validation du nombre de joueurs 
        def select_number_of_player():
            self.__selected_number_of_players = self.__btn_number_player.getSelected()

        # Bouton de choix du nombre de barrières
        self.__btn_number_of_barrier = Dropdown(
            self.__on_screen_surface,
            int(self.__x_position_dropdown + 2 * (self.__button_width_dropdown + self.__space)),
            self.__y_position_dropdown,
            self.__button_width_dropdown, self.__button_height_dropdown,
            name='Barrier',
            choices=[
                '4',
                '5',
                '8',
                '16',
            ],
            borderRadius=3,
            colour=get_white(),
            values=[16, 20, 32, 64], # Diviser par le nombre de joueurs pour avoir le nombre de barrières par joueurs
            font=self.__font_interface__M,
            direction='down'
        )

        # Bouton de validation du nombre de barrières 
        self.__validate_number_of_barrier = Button(
            self.__on_screen_surface,
            int(self.__x_position_validate + 2 * (self.__button_width_dropdown + self.__space)),
            self.__y_position_dropdown,
            self.__button_width_validate, int(self.__button_height_validate),
            text=self.__button_text_validate,
            margin=15,
            inactiveColour=get_red(),
            pressedColour=get_black(),
            radius=5,
            font=self.__font_interface__M,
            textVAlign='center',
            onClick=lambda: (select_number_of_barriere()) # Appel la fonction de validation du nombre de barrières
        )

        # Fonction de validation du nombre de barrières 
        def select_number_of_barriere():
            self.__selected_number_of_barrier = self.__btn_number_of_barrier.getSelected()

        # Bouton de choix de sauvegarde
        self.__btn_launch_save = Dropdown(
            self.__on_screen_surface,
            int(self.__x_position_dropdown + 3 * (self.__button_width_dropdown + self.__space)),
            self.__y_position_dropdown,
            self.__button_width_dropdown, self.__button_height_dropdown,
            name='Launch save',
            choices=[
                'Yes',
                'No',
            ],
            borderRadius=3,
            colour=get_white(),
            values=[True, False],
            font=self.__font_interface__M,
            direction='down'
        )

        # Bouton de validation de sauvegarde
        self.__validate_launch_save = Button(
            self.__on_screen_surface,
            int(self.__x_position_validate + 3 * (self.__button_width_dropdown + self.__space)),
            self.__y_position_dropdown,
            self.__button_width_validate, int(self.__button_height_validate),
            text=self.__button_text_validate,
            margin=15,
            inactiveColour=get_red(),
            pressedColour=get_black(),
            radius=5,
            font=self.__font_interface__M,
            textVAlign='center',
            onClick=lambda: (select_save()) # Appel la fonction de validation de sauvegarde 
        )

        # Fonction de validation de sauvegarde
        def select_save():
            self.__selected_save = self.__btn_launch_save.getSelected()

        # Bouton de choix du volume
        self.__btn_sound = Dropdown(
            self.__on_screen_surface,
            int(self.__x_position_dropdown + 4 * (self.__button_width_dropdown + self.__space)),
            self.__y_position_dropdown,
            self.__button_width_dropdown, self.__button_height_dropdown,
            name='Sound',
            choices=[
                '100%',
                '75%',
                '50%',
                '25%',
                'Mute',
            ],
            borderRadius=3,
            colour=get_white(),
            values=[1, 0.75, 0.50, 0.25, 0],
            font=self.__font_interface__M,
            direction='down'
        )

        # Bouton de validation du volume
        self.__validate_sound = Button(
            self.__on_screen_surface,
            int(self.__x_position_validate + 4 * (self.__button_width_dropdown + self.__space)),
            self.__y_position_dropdown,
            self.__button_width_validate, int(self.__button_height_validate),
            text=self.__button_text_validate,
            margin=15,
            inactiveColour=get_red(),
            pressedColour=get_black(),
            radius=5,
            font=self.__font_interface__M,
            textVAlign='center',
            onClick=lambda: (select_sound_volume()) # Appel la fonction de validation du volume 
        )

        # Fonction de validation du volume
        def select_sound_volume():
            self.__selected_sound_volume = self.__btn_sound.getSelected()

        # Bouton de choix du réseaux
        self.__btn_network = Dropdown(
            self.__on_screen_surface,
            int(self.__x_position_dropdown) + 590, self.__y_position_dropdown + 100,
            self.__button_width_dropdown, self.__button_height_dropdown,
            name='Network',
            choices=[
                'Yes',
                'No',
            ],
            borderRadius=3,
            colour=get_white(),
            values=[True, False],
            font=self.__font_interface__M,
            direction='down'
        )

        # Bouton de validation du réseau
        self.__validate_network = Button(
            self.__on_screen_surface, int(self.__x_position_validate) + 590, self.__y_position_dropdown + 100,
            self.__button_width_validate, self.__button_height_validate,
            text=self.__button_text_validate,
            margin=15,
            inactiveColour=get_red(),
            pressedColour=get_black(),
            radius=5,
            font=self.__font_interface__M,
            textVAlign='center',
            onClick=lambda: (select_network()) # Appel la fonction de validation du réseau
        )

        # Fonction de validation du réseau
        def select_network():
            self.__selected_network = self.__btn_network.getSelected()

        # Bouton de choix du réseau (Host/Client)
        self.__btn_network_choice = Dropdown(
            self.__on_screen_surface,
            int(self.__x_position_dropdown + self.__button_width_dropdown + self.__space) + 590,
            self.__y_position_dropdown + 100,
            self.__button_width_dropdown, self.__button_height_dropdown,
            name='Host/Client',
            choices=[
                'Host',
                'Client',
            ],
            borderRadius=3,
            colour=get_white(),
            values=['Host', 'Client'],
            font=self.__font_interface__M,
            direction='down'
        )

        # Bouton de validation du choix du réseau (Host/Client)
        self.__validate_network_choice = Button(
            self.__on_screen_surface,
            int(self.__x_position_validate + self.__button_width_dropdown + self.__space) + 590,
            self.__y_position_dropdown + 100,
            self.__button_width_validate, self.__button_height_validate,
            text=self.__button_text_validate,
            margin=15,
            inactiveColour=get_red(),
            pressedColour=get_black(),
            radius=5,
            font=self.__font_interface__M,
            textVAlign='center',
            onClick=lambda: (select_network_choice()) # Appel la fonction de validation du choix du réseau (Host/Client)
        )

        # Fonction de validation du choix du réseau (Host/Client)
        def select_network_choice():
            self.__selected_network_choice = self.__btn_network_choice.getSelected()
            network_user_choice() # Appel la fonction de paramétrage du réseau

        # Fonction de paramétrage du réseau
        def network_user_choice():
            if self.__selected_network_choice == 'Host': # Vérifie si le réseau est égale à "Host" 
                self.__network_host = True # Renvoie True pour self.__network_host, si self.__selected_network_choice == 'Host'
                self.__network_client = False # Renvoie False pour self.__network_client, si self.__selected_network_choice == 'Host'
                return self.__network_host # Renvoie self.__network_host

            elif self.__selected_network_choice == 'Client': # Vérifie si le réseau est égale à "Client" 
                self.__network_host = False # Renvoie False pour self.__network_host, si self.__selected_network_choice == 'Client'
                self.__network_client = self.__client_ip_choose # Renvoie la variable self.__client_ip_choose pour self.__network_client, 
                #si self.__selected_network_choice == 'Client'
                return self.__network_client # Renvoie self.__network_client

            else: # Autrement
                self.__network_host = False # Renvoie False pour self.__network_host
                self.__network_client = False # Renvoie False pour self.__network_client

        # Bouton de lancement du jeu
        self.__button_rect_play = Button(
            self.__on_screen_surface, int(self.__x_position), self.__y_position + 100,
            self.__button_width, self.__button_height,
            text='Play',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_dark_violet(),
            radius=5,
            font=self.__font_interface_XL,
            textVAlign='center',
            onClick=lambda: (self.open_game()) # Appel la fonction de lancement du jeux avec les valeurs par défaut 
        )

        # Bouton de retour en arrière
        self.__button_rect_back = Button(
            self.__on_screen_surface, int(self.__x_position + self.__button_width + self.__space),
            self.__y_position + 100,
            self.__button_width, self.__button_height,
            text='Back',
            margin=25,
            textColour=get_white(),
            inactiveColour=get_red(),
            radius=5,
            font=self.__font_interface_XL,
            textVAlign='center',
            onClick=lambda: (self.back()) # Appel la fonction pour retourner sur la fenêtre précédente
        )

        # Bouton pour quitter le jeux
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
            onClick=lambda: (self.quit()) # Appel la fonction pour quitter le jeu
        )
        
        # Zone qui affiche l'Host code 
        self.__zone_host_ip = pygame.Surface(self.__zone_host_ip_size, pygame.SRCALPHA)
        ip_host_label = self.__font_interface__L.render("Host Code : " + serveur.Serveur().get_code(), True, get_white())
        self.__zone_host_ip.blit(ip_host_label, (0, 0))

        # Zone du texte qui affiche "Client code :"
        self.__zone_client_ip = pygame.Surface(self.__zone_client_ip_size, pygame.SRCALPHA)
        ip_client_label = self.__font_interface__L.render("Client Code : ", True, get_white())
        self.__zone_client_ip.blit(ip_client_label, (0, 0))

        # Fonction, qui permet d'écrire dans la zone pour le code client
        def texte_zone_view(x, y, largeur, hauteur, texte):
            zone_texte = pygame.Rect(x, y, largeur, hauteur)
            pygame.draw.rect(self.__on_screen_surface, get_white(), zone_texte)
            pygame.draw.rect(self.__on_screen_surface, get_black(), zone_texte, 2)
            surface_texte_ip = self.__font_interface_XL.render(texte, True, get_black())
            texte_rect = surface_texte_ip.get_rect()
            texte_rect.center = zone_texte.center
            self.__on_screen_surface.blit(surface_texte_ip, texte_rect)

        # Boucle principale du jeu
        while self.__run == True:
            # Tant que self.__run renvoie True, la fenêtre est active
            for event in pygame.event.get(): # Récupère les événements
                if event.type == pygame.QUIT: # Si l'événement est de type QUIT, la fenêtre se ferme 
                    pygame.quit() # Arrête la boucle principale et quitte le jeu
                    exit()
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_RETURN:
                        self.__client_ip_choose = self.__ip_client # Si on appuie sur la touche "entrer" du clavier, on valide l'Host Code choisi
                    elif event.key == pygame.K_BACKSPACE:
                        self.__ip_client = self.__ip_client[:-1] # Si on appuie sur la touche "supprimer" du clavier, on supprime le caractère qu'on vien de taper
                    else:
                        if event.unicode in "0123456789": # Vérifie, que ce que l'utilisateur écrit dans la zone de texte est bien un chiffre
                            self.__ip_client += event.unicode


            # Mise à jour de l'état du jeu
            if self.__game_state == "Launch": # Test si l'état du jeu est "Launch"
                # Cache les widgets
                self.__btn_launch_save.hide()
                self.__btn_number_of_barrier.hide()
                self.__btn_sound.hide()
                self.__btn_network_choice.hide()
                self.__btn_size_board.hide()
                self.__btn_number_player.hide()
                self.__btn_network.hide()
                self.__validate_launch_save.hide()
                self.__validate_number_of_barrier.hide()
                self.__validate_sound.hide()
                self.__validate_network.hide()
                self.__validate_network_choice.hide()
                self.__validate_number_player.hide()
                self.__validate_size_board.hide()
                self.__validate_number_player.hide()
                self.__button_rect_play.hide()
                self.__button_rect_back.hide()
                self.__button_rect_quit.hide()
                self.__on_screen_surface.fill(get_blue_cyan()) # Remplie la zone de l'écran en bleue
                launch.Launch().display()  # Appel la fonction display de la classe Settings, qui se trouve dans le fichier laucnh.py

            elif self.__game_state == "Game": # Test si l'état du jeu est "Game"
                # Cache les widgets
                self.__btn_launch_save.hide()
                self.__btn_number_of_barrier.hide()
                self.__btn_sound.hide()
                self.__btn_network_choice.hide()
                self.__btn_size_board.hide()
                self.__btn_number_player.hide()
                self.__btn_network.hide()
                self.__validate_launch_save.hide()
                self.__validate_number_of_barrier.hide()
                self.__validate_sound.hide()
                self.__validate_network.hide()
                self.__validate_network_choice.hide()
                self.__validate_number_player.hide()
                self.__validate_size_board.hide()
                self.__validate_number_player.hide()
                self.__button_rect_play.hide()
                self.__button_rect_back.hide()
                self.__button_rect_quit.hide()
                select_network_choice() # Remplie la zone de l'écran en bleue
                self.__on_screen_surface.fill(get_blue_cyan()) # Appel la fonction game avec les valeurs choisi par l'utilisateur
                game.Game(self.__selected_number_of_players,
                        self.__selected_size_board,
                        self.__selected_sound_volume,
                        self.__selected_number_of_barrier,
                        self.__selected_save,
                        self.__selected_network,
                        self.__network_host,
                        self.__network_client)

            else:
                # Affiche les éléments sur l'écran
                self.__on_screen_surface.blit(self.__background_image, (0, 0)) # Affiche l'arrière-plan
                self.__on_screen_surface.blit(self.__zone_title, (735, 20)) # Affiche la zone de titre
                self.__on_screen_surface.blit(self.__zone_host_ip, (735, 700)) # Affiche la zone pour l'Host Code
                self.__on_screen_surface.blit(self.__zone_client_ip, (450, 510)) # Affiche la zone de texte pour mettre le code client
                self.__button_rect_play.draw()
                self.__button_rect_back.draw()
                self.__button_rect_quit.draw()
                texte_zone_view(735, 500, 500, 70, self.__ip_client) # Appel la fonction pour mettre le code client

            pygame_widgets.update(pygame.event.get())
            pygame.display.update()

            pygame.display.flip()

    pygame.quit()

    def quit(self): # Quitte le module pygame
        pygame.quit()
        exit()

    def open_game(self): # Fonction pour ouvrir la page de jeu
        self.__game_state = "Game" # Change l'état du jeux à "Game"

    def back(self): # Fonction pour revenir sur la page précédente
        self.__game_state = "Launch" # Change l'état du jeux à "Launch"
