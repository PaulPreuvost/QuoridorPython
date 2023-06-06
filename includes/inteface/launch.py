import pygame
import subprocess

from user_interface.colors import get_white, get_black, get_red, get_blue, get_yellow
#from Python_Groupe_4_Tours.QuoridorPython.user_interface.colors import get_white, get_black, get_red, get_blue, get_yellow,\ get_light_grey
class Launch:
    def __init__(self):
        self.__onScreenSurface = None
        self.__continuer = True

    def launch(self):
        pygame.init()
        windowSize = (1920, 1200)
        pygame.display.set_caption("QUORIDOR")
        self.__onScreenSurface = pygame.display.set_mode(windowSize, pygame.FULLSCREEN | pygame.RESIZABLE)

        # Charger l'image de l'arrière-plan
        background_image = pygame.image.load("../../user_interface/image/launch/background.jpg")
        # Charger l'image Titre
        image_title = pygame.image.load("../../user_interface/image/launch/titre.png")
        image_rect = image_title.get_rect(center=(windowSize[0] // 2, 100))

        font_interface__XL = pygame.font.Font("../../user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf", 70)
        button_width = 400
        button_height = 150
        space = 300  # Espacement entre les boutons

        x_position = (windowSize[0] - (3 * button_width + 2 * space)) / 2
        y_position = 1000

        button_rect_back = pygame.Rect(1600, 40, button_width/1.5, button_height/1.5)  # Rectangle du bouton Retour
        button_rect_load = pygame.Rect(x_position, y_position, button_width, button_height) # Rectangle du bouton Chargement
        button_rect_play = pygame.Rect(x_position + button_width + space, y_position, button_width, button_height)  # Rectangle du bouton Jouer
        button_rect_settings = pygame.Rect(x_position + 2 * (button_width + space), y_position, button_width, button_height)  # Rectangle du bouton Paramètres


        button_text_back = "QUIT"  # Texte du bouton Retour
        button_text_load = "LOAD"  # Texte du bouton Chargement
        button_text_play = "PLAY"  # Texte du bouton Jouer
        button_text_setting = "SETTINGS"  # Texte du bouton Paramètres


        while self.__continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__continuer = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.__continuer = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect_back.collidepoint(event.pos): #Évenements bouton Retour
                        if subprocess.Popen.poll(subprocess.Popen("xdotool getactivewindow")) is None:
                            subprocess.Popen(["xdotool", "key", "Alt+F4"])
                        else:
                            self.__continuer = False
                    elif button_rect_play.collidepoint(event.pos): #Évenements bouton Jouer
                        self.__continuer = False
                        #Game().display()  # Lancer le jeu en appelant la méthode run() de la classe Game
                    elif button_rect_settings.collidepoint(event.pos): #Évenements bouton Quitter
                        self.__continuer = False
                        pygame.quit()
                    elif button_rect_load.collidepoint(event.pos): #Évenements bouton Paramètres
                        self.__continuer = False
                        pygame.quit()

            self.__onScreenSurface.blit(background_image, (0, 0))  # Afficher l'arrière-plan

            self.__onScreenSurface.blit(image_title, (384.5, 120))  # Afficher le titre

            pygame.draw.rect(self.__onScreenSurface, get_red(), button_rect_back)  # Dessiner le rectangle du bouton Retour
            pygame.draw.rect(self.__onScreenSurface, get_blue(), button_rect_load)  # Dessiner le rectangle du bouton Chargement
            pygame.draw.rect(self.__onScreenSurface, get_yellow(), button_rect_play)  # Dessiner le rectangle du bouton Jouer
            pygame.draw.rect(self.__onScreenSurface, get_white(), button_rect_settings)  # Dessiner le rectangle du bouton Paramètres

#Bouton Retour
            # Créer la surface de texte avec contour noir pour le bouton Retour
            text_surface_back = font_interface__XL.render(button_text_back, True, get_black())
            text_rect_back = text_surface_back.get_rect(center=button_rect_back.center)
            self.__onScreenSurface.blit(text_surface_back, text_rect_back)

            # Créer la surface de texte principale pour le bouton Retour
            main_text_surface_back = font_interface__XL.render(button_text_back, True, get_black())
            main_text_rect_back = main_text_surface_back.get_rect(center=button_rect_back.center)

# Bouton Chargement
            # Créer la surface de texte avec contour noir pour le bouton Chargement
            text_surface_load = font_interface__XL.render(button_text_load, True, get_black())
            text_rect_load = text_surface_load.get_rect(center=button_rect_load.center)
            self.__onScreenSurface.blit(text_surface_load, text_rect_load)

            # Créer la surface de texte principale pour le bouton Chargement
            main_text_surface_load = font_interface__XL.render(button_text_load, True, get_black())
            main_text_rect_load = main_text_surface_load.get_rect(center=button_rect_load.center)

# Bouton Jouer
            # Créer la surface de texte avec contour noir pour le bouton Jouer
            text_surface_play = font_interface__XL.render(button_text_play, True, get_black())
            text_rect_play = text_surface_play.get_rect(center=button_rect_play.center)
            self.__onScreenSurface.blit(text_surface_play, text_rect_play)

            # Créer la surface de texte principale pour le bouton Jouer
            main_text_surface_play = font_interface__XL.render(button_text_play, True, get_black())
            main_text_rect_play = main_text_surface_play.get_rect(center=button_rect_play.center)

# Bouton Paramètres
            # Créer la surface de texte avec contour noir pour le bouton Paramètres
            text_surface_setting = font_interface__XL.render(button_text_setting, True, get_black())
            text_rect_settings = text_surface_setting.get_rect(center=button_rect_settings.center)
            self.__onScreenSurface.blit(text_surface_setting, text_rect_settings)

            # Créer la surface de texte principale pour le bouton Paramètres
            main_text_surface_setting = font_interface__XL.render(button_text_setting, True, get_black())
            main_text_rect_settings = main_text_surface_setting.get_rect(center=button_rect_settings.center)

            pygame.display.flip()

        pygame.quit()

Launch().launch()