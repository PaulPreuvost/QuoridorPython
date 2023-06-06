import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import subprocess

#Windows :
from Python_Groupe_4_Tours.QuoridorPython.user_interface.colors import get_white, get_black, get_red, get_blue, get_yellow

#macOS :
#from user_interface.colors import get_white, get_black, get_red, get_blue, get_yellow


class Settings:
    def __init__(self):
        self.__onScreenSurface = None
        self.__continuer = True

    def supprimer(self):
        self.__continuer = False

    def display(self):
        global event
        pygame.init()
        windowSize = (1920, 1080)
        pygame.display.set_caption("QUORIDOR")
        self.__onScreenSurface = pygame.display.set_mode(windowSize, pygame.FULLSCREEN | pygame.RESIZABLE)

        # Charger l'image de l'arrière-plan
        background_image = pygame.image.load("../../user_interface/image/launch/background.jpg")
        # Charger l'image Titre
        image_title = pygame.image.load("../../user_interface/image/launch/titre.png")
        image_rect = image_title.get_rect(center=(windowSize[0] // 2, 100))

        font_interface__XL = pygame.font.Font("../../user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf", 70)
        font_interface__L = pygame.font.Font("../../user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf", 45)
        font_interface__M = pygame.font.Font("../../user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf", 20)

        button_width = 400
        button_height = 150
        button_width_dropdown = 200
        button_height_dropdown = 50
        button_width_validate = 100
        button_height_validate = 50

        space = 300  # Espacement entre les boutons
        x_position = ((windowSize[0] - (2 * button_width + 1 * space)) / 2 )
        y_position =1000

        x_position_dropdown = ((windowSize[0] - (4 * button_width_dropdown + 3 * space)) / 2 )
        y_position_dropdown = 500

        x_position_validate = (x_position_dropdown + button_width_dropdown)+10

        button_text_validate = "Enter"  # Texte du bouton Retour

        button_rect_back = pygame.Rect(x_position, y_position, button_width, button_height)  # Rectangle du bouton Retour
        button_rect_play = pygame.Rect(x_position + button_width + space, y_position, button_width, button_height)  # Rectangle du bouton Jouer
        button_rect_rules = pygame.Rect(1600, 40, button_width/1.5, button_height/1.5)  # Rectangle du bouton Règles
        button_rect_network = pygame.Rect(x_position_validate +2.5*(+button_width_dropdown+space),y_position_dropdown-35, button_width/1.5, button_height/1.5)

        button_text_play = "PLAY"  # Texte du bouton Jouer
        button_text_back = "BACK"  # Texte du bouton Retour
        button_text_rules = "RULES"  # Texte du bouton Règles
        button_text_network = "NETWORK"



        btn_number_player = Dropdown(
            self.__onScreenSurface, x_position_dropdown,y_position_dropdown, button_width_dropdown, button_height_dropdown, name='Number of Player',
            choices=[
                '1',
                '2',
                '4',
            ],
            borderRadius=3, colour= get_white(), values=[1, 2, 4],font=font_interface__M, direction='down'
        )

        validate_number_player = Button(
            self.__onScreenSurface, x_position_validate , y_position_dropdown, button_width_validate, button_height_validate, text=button_text_validate,
            margin=15, inactiveColour= get_red(), pressedColour= get_black(),
            radius=5, font=font_interface__M,
            textVAlign='bottom', onClick=lambda: print(btn_number_player.getSelected())
        )

        btn_size_board = Dropdown(
            self.__onScreenSurface, x_position_dropdown+button_width_dropdown+space, y_position_dropdown, button_width_dropdown, button_height_dropdown, name='Board Size',
            choices=[
                '5x5',
                '7x7',
                '9x9',
                '11x11',
            ],
            borderRadius=3, colour= get_white(), values=[5, 7, 9, 11], font=font_interface__M, direction='down'
        )

        validate_size_board = Button(
            self.__onScreenSurface, x_position_validate+button_width_dropdown+space, y_position_dropdown, button_width_validate, button_height_validate, text= button_text_validate,
            margin=15, inactiveColour=get_red(), pressedColour=get_black(),
            radius=5, font=font_interface__M,
            textVAlign='bottom', onClick=lambda: print(btn_size_board.getSelected())
        )


        btn_sound = Dropdown(
            self.__onScreenSurface, x_position_dropdown +2*(+button_width_dropdown+space), y_position_dropdown, button_width_dropdown, button_height_dropdown, name='Sound',
            choices=[
                '100%',
                '75%',
                '50%',
                '25%',
                'Mute',

            ],
            borderRadius=3, colour= get_white(), values=['1', '0.75', '0.50', '0.25', '0'],font=font_interface__M, direction='down'
        )

        validate_sound = Button(
            self.__onScreenSurface, x_position_validate +2*(+button_width_dropdown+space), y_position_dropdown, button_width_validate, button_height_validate, text=button_text_validate,
            margin=15, inactiveColour=get_red(), pressedColour=get_black(),
            radius=5, font=font_interface__M,
            textVAlign='bottom', onClick=lambda: print(btn_sound.getSelected())
        )




        while self.__continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__continuer = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.__continuer = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.__onScreenSurface.fill((0, 0, 0))
                    if button_rect_back.collidepoint(event.pos):  # Évenements bouton Retour
                        if subprocess.Popen.poll(subprocess.Popen("xdotool getactivewindow")) is None:
                            subprocess.Popen(["xdotool", "key", "Alt+F4"])
                        elif button_rect_play.collidepoint(event.pos):  # Évenements bouton Jouer
                            self.__continuer = False
                            #Game().display()  # Lancer le jeu en appelant la méthode run() de la classe Game

            pygame_widgets.update(
                pygame.event.get())
            pygame.display.update()

            self.__onScreenSurface.blit(background_image, (0, 0))  # Afficher l'arrière-plan

            self.__onScreenSurface.blit(image_title, (384.5, 10))  # Afficher le titre

            pygame.draw.rect(self.__onScreenSurface, get_red(), button_rect_back)  # Dessiner le rectangle du bouton Retour
            pygame.draw.rect(self.__onScreenSurface, get_yellow(), button_rect_play)  # Dessiner le rectangle du bouton Jouer
            pygame.draw.rect(self.__onScreenSurface, get_blue(), button_rect_rules)  # Dessiner le rectangle du bouton Règles
            pygame.draw.rect(self.__onScreenSurface, get_blue(), button_rect_network)  # Dessiner le rectangle du bouton Réseaux


# Bouton Retour
            # Créer la surface de texte avec contour noir pour le bouton Retour
            text_surface_back = font_interface__XL.render(button_text_back, True, get_black())
            text_rect_back = text_surface_back.get_rect(center=button_rect_back.center)
            self.__onScreenSurface.blit(text_surface_back, text_rect_back)

            # Créer la surface de texte principale pour le bouton Retour
            main_text_surface_back = font_interface__XL.render(button_text_back, True, get_black())
            main_text_rect_back = main_text_surface_back.get_rect(center=button_rect_back.center)
# Bouton Jouer
            # Créer la surface de texte avec contour noir pour le bouton Jouer
            text_surface_play = font_interface__XL.render(button_text_play, True, get_black())
            text_rect_play = text_surface_play.get_rect(center=button_rect_play.center)
            self.__onScreenSurface.blit(text_surface_play, text_rect_play)

            # Créer la surface de texte principale pour le bouton Jouer
            main_text_surface_play = font_interface__XL.render(button_text_play, True, get_black())
            main_text_rect_play = main_text_surface_play.get_rect(center=button_rect_play.center)

# Bouton Règle
            # Créer la surface de texte avec contour noir pour le bouton Règle
            text_surface_rules = font_interface__XL.render(button_text_rules, True, get_black())
            text_rect_rules = text_surface_rules.get_rect(center=button_rect_rules.center)
            self.__onScreenSurface.blit(text_surface_rules, text_rect_rules)

            # Créer la surface de texte principale pour le bouton Règle
            main_text_surface_rules = font_interface__XL.render(button_text_rules, True, get_black())
            main_text_rect_rules = main_text_surface_rules.get_rect(center=button_rect_rules.center)

# Bouton Réseaux
            # Créer la surface de texte avec contour noir pour le bouton Réseaux
            text_surface_network = font_interface__L.render(button_text_network, True, get_black())
            text_rect_network = text_surface_network.get_rect(center=button_rect_network.center)
            text_rect_network.center = button_rect_network.center
            self.__onScreenSurface.blit(text_surface_network, text_rect_network)

            # Créer la surface de texte principale pour le bouton Réseaux
            main_text_surface_network = font_interface__L.render(button_text_network, True, get_black())
            main_text_rect_network = main_text_surface_network.get_rect(center=button_rect_network.center)
            main_text_rect_network.center = button_rect_network.center

        pygame.quit()


Settings().display()
