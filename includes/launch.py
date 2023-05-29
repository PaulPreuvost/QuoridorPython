import pygame
import subprocess

class Launch:
    def __init__(self):
        self.__onScreenSurface = None
        self.__continuer = True

    def display(self):
        white = (255, 255, 255)
        black = (0, 0, 0)
        red = (255, 0, 0)
        yellow = (255, 255, 0)
        pygame.init()
        windowSize = (1920, 1200)
        pygame.display.set_caption("QUORIDOR")
        self.__onScreenSurface = pygame.display.set_mode(windowSize, pygame.FULLSCREEN | pygame.RESIZABLE)

        # Charger l'image de l'arrière-plan
        background_image = pygame.image.load("../user_interface/image/launch/background.jpg")
        # Charger l'image Titre
        image_title = pygame.image.load("../user_interface/image/launch/titre.png")
        image_rect = image_title.get_rect(center=(windowSize[0] // 2, 100))

        font = pygame.font.Font("../user_interface/font/Berlin_Sans_FB_Demi_Bold.ttf", 70)
        button_width = 400
        button_height = 150
        space = 300  # Espacement entre les boutons

        x_position = (windowSize[0] - (3 * button_width + 2 * space)) / 2

        button_rect_back = pygame.Rect(x_position, 1000, button_width, button_height)  # Rectangle du bouton Retour
        button_rect_play = pygame.Rect(x_position + button_width + space, 1000, button_width, button_height)  # Rectangle du bouton Jouer
        button_rect_exit = pygame.Rect(x_position + 2 * (button_width + space), 1000, button_width, button_height)  # Rectangle du bouton Setting

        button_text_back = "Retour"  # Texte du bouton Retour
        button_text_play = "Jouer"  # Texte du bouton Jouer
        button_text_setting = "Paramètres"  # Texte du bouton setting

        while self.__continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__continuer = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.__continuer = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect_back.collidepoint(event.pos):
                        if subprocess.Popen.poll(subprocess.Popen("xdotool getactivewindow")) is None:
                            subprocess.Popen(["xdotool", "key", "Alt+F4"])
                        else:
                            self.__continuer = False
                    elif button_rect_play.collidepoint(event.pos):
                        self.__continuer = False
                        Game().run()  # Lancer le jeu en appelant la méthode run() de la classe Game
                    elif button_rect_exit.collidepoint(event.pos):
                        self.__continuer = False
                        pygame.quit()

            self.__onScreenSurface.blit(background_image, (0, 0))  # Afficher l'arrière-plan

            self.__onScreenSurface.blit(image_title, (384.5, 70))  # Afficher le titre

            pygame.draw.rect(self.__onScreenSurface, red, button_rect_back)  # Dessiner le rectangle du bouton Retour
            pygame.draw.rect(self.__onScreenSurface, yellow, button_rect_play)  # Dessiner le rectangle du bouton Jouer
            pygame.draw.rect(self.__onScreenSurface, white, button_rect_exit)  # Dessiner le rectangle du bouton Setting

            # Créer la surface de texte avec contour noir pour le bouton Retour
            text_surface_back = font.render(button_text_back, True, (0, 0, 0))
            text_rect_back = text_surface_back.get_rect(center=button_rect_back.center)
            self.__onScreenSurface.blit(text_surface_back, text_rect_back)

            # Créer la surface de texte principale pour le bouton Retour
            main_text_surface_back = font.render(button_text_back, True, (255, 255, 255))
            main_text_rect_back = main_text_surface_back.get_rect(center=button_rect_back.center)

            # Créer la surface de texte avec contour noir pour le bouton Jouer
            text_surface_play = font.render(button_text_play, True, (0, 0, 0))
            text_rect_play = text_surface_play.get_rect(center=button_rect_play.center)
            self.__onScreenSurface.blit(text_surface_play, text_rect_play)

            # Créer la surface de texte principale pour le bouton Jouer
            main_text_surface_play = font.render(button_text_play, True, (255, 255, 255))
            main_text_rect_play = main_text_surface_play.get_rect(center=button_rect_play.center)

            # Créer la surface de texte avec contour noir pour le bouton Setting
            text_surface_setting = font.render(button_text_setting, True, (0, 0, 0))
            text_rect_exit = text_surface_setting.get_rect(center=button_rect_exit.center)
            self.__onScreenSurface.blit(text_surface_setting, text_rect_exit)

            # Créer la surface de texte principale pour le bouton Setting
            main_text_surface_setting = font.render(button_text_setting, True, (0, 0, 0))
            main_text_rect_exit = main_text_surface_setting.get_rect(center=button_rect_exit.center)

            pygame.display.flip()

        pygame.quit()

Launch().display()