#pip install pygame-widgets /python -m pip install pygame-widgets
#import pygame_widgets
import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import subprocess
import main


class Settings:
    def __init__(self):
        self.__onScreenSurface = None
        self.__run = True

    def supprimer(self):
        self.__run = False

    def display(self):
        global event
        pygame.init()
        windowSize = (1920, 1080)
        pygame.display.set_caption("QUORIDOR")
        self.__onScreenSurface = pygame.display.set_mode(windowSize, pygame.FULLSCREEN | pygame.RESIZABLE)

        # win = pygame.display.set_mode((400, 280))

        dropdown1 = Dropdown(
            self.__onScreenSurface, 140, 10, 140, 50, name='Nombre de joueur(s)',
            choices=[
                '1',
                '2',
                '4',
            ],
            borderRadius=3, colour=pygame.Color('white'), values=[1, 2, 4], direction='down'
        )

        valide1 = Button(
            self.__onScreenSurface, 300, 10, 100, 50, text='Valider', fontSize=30,
            margin=15, inactiveColour=(255, 0, 0), pressedColour=(255, 255, 255),
            radius=5, font=pygame.font.SysFont('calibri', 16, 'bold'),
            textVAlign='bottom', onClick=lambda: print(dropdown1.getSelected())
        )

        dropdown2 = Dropdown(
            self.__onScreenSurface, 680, 10, 110, 50, name='Taille du plateau',
            choices=[
                '5x5',
                '7x7',
                '9x9',
                '11x11',
            ],
            borderRadius=3, colour=pygame.Color('white'), values=[5, 7, 9, 11], direction='down'
        )

        valide2 = Button(
            self.__onScreenSurface, 800, 10, 100, 50, text='Valider', fontSize=30,
            margin=15, inactiveColour=(255, 0, 0), pressedColour=(255, 255, 255),
            radius=5, font=pygame.font.SysFont('calibri', 16, 'bold'),
            textVAlign='bottom', onClick=lambda: print(dropdown2.getSelected())
        )

        # self.__sizeBoard = dropdown2.getSelected())

        dropdown3 = Dropdown(
            self.__onScreenSurface, 1200, 10, 90, 50, name='Choix de jeu',
            choices=[
                'Local',
                'Réseau',
            ],
            borderRadius=3, colour=pygame.Color('white'), values=['Local', 'Réseau'], direction='down'
        )

        valide3 = Button(
            self.__onScreenSurface, 1300, 10, 100, 50, text='Valider', fontSize=30,
            margin=15, inactiveColour=(255, 0, 0), pressedColour=(255, 255, 255),
            radius=5, font=pygame.font.SysFont('calibri', 16, 'bold'),
            textVAlign='bottom', onClick=lambda: print(dropdown3.getSelected())
        )

        retour = pygame.image.load("image/jeux/retour.png").convert_alpha()
        retour_rect = retour.get_rect()
        retour_rect.y += 750

        jouer = Button(
            self.__onScreenSurface, 750, 500, 200, 100, text='Jouer', fontSize=100,
            margin=25, textColour='white', inactiveColour=(255, 0, 0), pressedColour=(255, 255, 255),
            radius=5, font=pygame.font.SysFont('calibri', 42, 'bold'),
            textVAlign='bottom', onClick=lambda: (self.supprimer(), main.game(dropdown1.getSelected(), dropdown2.getSelected(), dropdown3.getSelected()))
        )

        while self.__run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.__run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.__onScreenSurface.fill((0, 0, 0))
                    if retour_rect.collidepoint(event.pos):
                        self.__run = False

            pygame_widgets.update(pygame.event.get())
            pygame.display.update()

            self.__onScreenSurface.blit(retour, retour_rect)

        pygame.quit()

Settings().display()
