import pygame
import subprocess


class Setting:
    def __init__(self):
        self.__onScreenSurface = None
        self.__continuer = True

    def display(self):
        pygame.init()
        white = (255, 255, 255)
        black = (0, 0, 0)
        red = (255, 0, 0)
        windowSize = (1920, 1080)
        pygame.display.set_caption("QUORIDOR")
        self.__onScreenSurface = pygame.display.set_mode(windowSize, pygame.FULLSCREEN | pygame.RESIZABLE)

        font = pygame.font.Font(None, 70)

        button_rect = pygame.Rect(200, 1000, 300, 150)  # Rectangle du bouton
        button_text = "Retour"  # Texte du bouton
        text_padding = 2  # Espacement du texte par rapport au rectangle

        while self.__continuer:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__continuer = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.__continuer = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect.collidepoint(event.pos):
                        if subprocess.Popen.poll(subprocess.Popen("xdotool getactivewindow")) is None:
                            subprocess.Popen(["xdotool", "key", "Alt+F4"])
                        else:
                            self.__continuer = False

            self.__onScreenSurface.fill((0, 0, 0))  # Effacer l'écran

            pygame.draw.rect(self.__onScreenSurface, red, button_rect)  # Dessiner le rectangle du bouton

            # Créer la surface de texte avec contour noir
            text_surface = font.render(button_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.__onScreenSurface.blit(text_surface, text_rect)

            # Créer la surface de texte principale
            main_text_surface = font.render(button_text, True, black)
            main_text_rect = main_text_surface.get_rect(center=button_rect.center)

            pygame.display.flip()

        pygame.quit()


Setting().display()
