import sys
import os
import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import game
import launch
import serveur

from Python_Groupe_4_Tours.QuoridorPython.require.user_interface.colors import get_black, get_red, \
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
        self.__run = True
        self.__game_state = "Settings"

        # Initialisations de la taille de la fenêtre
        self.__window_size = (1920, 1080)

        # Chargement l'image de l'arrière-plan
        self.__background_image = pygame.image.load(resource_path("user_interface/images/background.jpg"))

        # Chargement des polices de caractères
        self.__font_load = resource_path("user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf")
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


        # Initialisations des paramêtres
        self.__selected_size_board = 11
        self.__selected_number_of_players = 2
        self.__selected_number_of_barrier = 16
        self.__selected_save = 0  # remplacer par true
        self.__selected_sound_volume = 1
        self.__selected_computer = 0
        self.__selected_network = False
        self.__selected_network_choice = False  # Host ou client

    # def get_host_ip_address(self):
    #     # Obtient l'adresse IP de l'hôte
    #     host_name = socket.gethostname()
    #     host_ip = socket.gethostbyname(host_name)
    #     return host_ip

    def supprimer(self):
        self.__run = False

    def display(self):
        pygame.init()
        pygame.display.set_caption("QUORIDOR")
        self.__on_screen_surface = pygame.display.set_mode(self.__window_size, pygame.FULLSCREEN | pygame.RESIZABLE)
        clock = pygame.time.Clock()
        fps = 30  # Nombre de trames par seconde (FPS)
        clock.tick(fps)

        self.__zone_title = pygame.Surface(self.__zone_title_size, pygame.SRCALPHA)
        title_board = self.__font_interface__XXXL.render("Settings", True, get_white())
        title_board_outline = self.__font_interface__XXXL.render("Settings", True, get_black())
        self.__zone_title.blit(title_board_outline, (0 + 2, 0 + 2))
        self.__zone_title.blit(title_board, (0, 0))

        btn_size_board = Dropdown(
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

        validate_size_board = Button(
            self.__on_screen_surface, int(self.__x_position_validate), self.__y_position_dropdown,
            self.__button_width_validate, self.__button_height_validate,
            text=self.__button_text_validate,
            margin=15,
            inactiveColour=get_red(),
            pressedColour=get_black(),
            radius=5,
            font=self.__font_interface__M,
            textVAlign='center',
            onClick=lambda: select_size_board()
        )

        def select_size_board():
            self.__selected_size_board = btn_size_board.getSelected()

        btn_number_player = Dropdown(
            self.__on_screen_surface, int(self.__x_position_dropdown + self.__button_width_dropdown + self.__space),
            self.__y_position_dropdown,
            self.__button_width_dropdown, self.__button_height_dropdown,
            name='Number of Players',
            choices=[
                '1',
                '2',
                '3',
                '4',
            ],
            borderRadius=3,
            colour=get_white(),
            values=[1, 2, 3, 4],
            font=self.__font_interface__M,
            direction='down'
        )

        validate_number_player = Button(
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
            onClick=lambda: select_number_of_player()
        )

        def select_number_of_player():
            self.__selected_number_of_players = btn_number_player.getSelected()

        btn_number_of_barrier = Dropdown(
            self.__on_screen_surface,
            int(self.__x_position_dropdown + 2 * (self.__button_width_dropdown + self.__space)),
            self.__y_position_dropdown,
            self.__button_width_dropdown, self.__button_height_dropdown,
            name='Barrier',
            choices=[
                '4',
                '6',
                '8',
                '16',
            ],
            borderRadius=3,
            colour=get_white(),
            values=[16, 24, 32, 64],  # Divisé par 40
            font=self.__font_interface__M,
            direction='down'
        )

        validate_number_of_barrier = Button(
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
            onClick=lambda: select_number_of_barriere()
        )

        def select_number_of_barriere():
            self.__selected_number_of_barrier = btn_number_of_barrier.getSelected()

        btn_launch_save = Dropdown(
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

        validate_launch_save = Button(
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
            onClick=lambda: select_save()
        )

        def select_save():
            self.__selected_save = btn_launch_save.getSelected()

        btn_sound = Dropdown(
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
            values=['1', '0.75', '0.50', '0.25', '0'],
            font=self.__font_interface__M,
            direction='down'
        )

        validate_sound = Button(
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
            onClick=lambda: select_sound_volume()
        )

        def select_sound_volume():
            self.__selected_sound_volume = btn_sound.getSelected()

        btn_network = Dropdown(
            self.__on_screen_surface,
            int(self.__x_position_dropdown) + 350, self.__y_position_dropdown + 100,
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

        validate_network = Button(
            self.__on_screen_surface, int(self.__x_position_validate) + 350, self.__y_position_dropdown + 100,
            self.__button_width_validate, self.__button_height_validate,
            text=self.__button_text_validate,
            margin=15,
            inactiveColour=get_red(),
            pressedColour=get_black(),
            radius=5,
            font=self.__font_interface__M,
            textVAlign='center',
            onClick=lambda: select_network()
        )

        def select_network():
            self.__selected_network = btn_network.getSelected()

        btn_network_choice = Dropdown(
            self.__on_screen_surface,
            int(self.__x_position_dropdown + self.__button_width_dropdown + self.__space) + 350,
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

        validate_network_choice = Button(
            self.__on_screen_surface,
            int(self.__x_position_validate + self.__button_width_dropdown + self.__space) + 350,
            self.__y_position_dropdown + 100,
            self.__button_width_validate, self.__button_height_validate,
            text=self.__button_text_validate,
            margin=15,
            inactiveColour=get_red(),
            pressedColour=get_black(),
            radius=5,
            font=self.__font_interface__M,
            textVAlign='center',
            onClick=lambda: select_network_choice()
        )

        def select_network_choice():
            self.__selected_network_choice = btn_network_choice.getSelected()
            network_user_choice()
        def network_user_choice():
            if self.__selected_network_choice == 'Host':
                self.__network_host = True
                self.__network_client = False
                return self.__network_host
            elif self.__selected_network_choice == 'Client':
                self.__network_host = False
                self.__network_client = self.__ip_client
                return self.__network_host
            else:
                self.__network_host = False
                self.__network_client = False


        btn_computer = Dropdown(
            self.__on_screen_surface,
            int(self.__x_position_dropdown + 2 * (self.__button_width_dropdown + self.__space)) + 350,
            self.__y_position_dropdown + 100,
            self.__button_width_dropdown, self.__button_height_dropdown,
            name='Computer',
            choices=[
                'Oui',
                'Non',
            ],
            borderRadius=3,
            colour=get_white(),
            values=[1, 0],
            font=self.__font_interface__M,
            direction='down'
        )

        validate_computer = Button(
            self.__on_screen_surface,
            int(self.__x_position_validate + 2 * (self.__button_width_dropdown + self.__space)) + 350,
            self.__y_position_dropdown + 100,
            self.__button_width_validate, self.__button_height_validate,
            text=self.__button_text_validate,
            margin=15,
            inactiveColour=get_red(),
            pressedColour=get_black(),
            radius=5,
            font=self.__font_interface__M,
            textVAlign='center',
            onClick=lambda: select_computer()
        )

        def select_computer():
            self.__selected_computer = btn_computer.getSelected()

        button_rect_play = Button(
            self.__on_screen_surface, int(self.__x_position), self.__y_position + 100,
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

        button_rect_back = Button(
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
            onClick=lambda: (self.back())
        )

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
        self.__zone_host_ip = pygame.Surface(self.__zone_host_ip_size, pygame.SRCALPHA)
        ip_host_label = self.__font_interface__L.render("Host Code : " + serveur.Serveur().get_code(), True, get_white())
        self.__zone_host_ip.blit(ip_host_label, (0, 0))

        self.__zone_client_ip = pygame.Surface(self.__zone_client_ip_size, pygame.SRCALPHA)
        ip_client_label = self.__font_interface__L.render("Client Code : ", True, get_white())
        self.__zone_client_ip.blit(ip_client_label, (0, 0))
        def afficher_zone_texte(x, y, largeur, hauteur, texte):
            zone_texte = pygame.Rect(x, y, largeur, hauteur)
            pygame.draw.rect(self.__on_screen_surface, get_white(), zone_texte)
            pygame.draw.rect(self.__on_screen_surface, get_black(), zone_texte, 2)
            surface_texte_ip = self.__font_interface_XL.render(texte, True, get_black())
            texte_rect = surface_texte_ip.get_rect()
            texte_rect.center = zone_texte.center
            self.__on_screen_surface.blit(surface_texte_ip, texte_rect)

        self.__ip_client = ""

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print(self.__ip_client)
                        # Réinitialiser le texte après avoir traité les données
                        self.__ip_client = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.__ip_client = self.__ip_client[:-1]
                    else:
                        if event.unicode in "0123456789":
                            self.__ip_client += event.unicode



            # Update game state
            if self.__game_state == "Launch":
                button_rect_quit.hide()
                btn_computer.hide()
                btn_launch_save.hide()
                btn_number_of_barrier.hide()
                btn_sound.hide()
                btn_network_choice.hide()
                btn_size_board.hide()
                btn_number_player.hide()
                btn_network.hide()
                validate_computer.hide()
                validate_launch_save.hide()
                validate_number_of_barrier.hide()
                validate_sound.hide()
                validate_network.hide()
                validate_network_choice.hide()
                validate_number_player.hide()
                validate_size_board.hide()
                validate_number_player.hide()
                button_rect_play.hide()
                button_rect_back.hide()
                self.__on_screen_surface.fill(get_blue_cyan())
                launch.Launch().display()

            elif self.__game_state == "Game":
                button_rect_quit.hide()
                btn_computer.hide()
                btn_launch_save.hide()
                btn_number_of_barrier.hide()
                btn_sound.hide()
                btn_network_choice.hide()
                btn_size_board.hide()
                btn_number_player.hide()
                btn_network.hide()
                validate_computer.hide()
                validate_launch_save.hide()
                validate_number_of_barrier.hide()
                validate_sound.hide()
                validate_network.hide()
                validate_network_choice.hide()
                validate_number_player.hide()
                validate_size_board.hide()
                validate_number_player.hide()
                button_rect_play.hide()
                button_rect_back.hide()
                self.__on_screen_surface.fill(get_blue_cyan())
                game.Game(self.__selected_number_of_players,
                          self.__selected_size_board,
                          self.__selected_sound_volume,
                          self.__selected_number_of_barrier,
                          self.__selected_save,
                          self.__selected_computer,
                          self.__selected_network,
                          self.__selected_network_choice,
                          self.__ip_client)

            else:
                # Dessiner les éléments sur l'écran
                self.__on_screen_surface.blit(self.__background_image, (0, 0))  # Afficher l'arrière-plan
                self.__on_screen_surface.blit(self.__zone_title, (735, 20))
                self.__on_screen_surface.blit(self.__zone_host_ip, (735, 700))
                button_rect_play.draw()
                button_rect_back.draw()
                self.__on_screen_surface.blit(self.__zone_client_ip, (450, 510))
                afficher_zone_texte(735, 500, 500, 70, self.__ip_client)

            def validate_input(text):
                # Vérifier si le texte ne contient que des chiffres et des points
                for char in text:
                    if not char.isdigit() and char != '.':
                        return False
                return True

            pygame_widgets.update(pygame.event.get())
            pygame.display.update()

            pygame.display.flip()

            clock.tick(fps)  # Limiter le nombre de trames par seconde

    pygame.quit()

    def quit(self):
        pygame.quit()
    def open_game(self):
        self.__game_state = "Game"

    def back(self):
        self.__game_state = "Launch"


