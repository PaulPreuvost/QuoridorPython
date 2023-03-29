from random import *
import pygame
import math
# import serveur
# import client

# Coder en Anglais en Case

class casePawn:

    """

    cette classe permet de retourner si il y a un pion et 
    la couleur du joueur possaident ce pion

    """

    def __init__(self, pawn = False, player = 0):
        self.__pawn = pawn
        self.__player = player

    def getPawn(self):
        return self.__pawn

    def setPawn(self, x):
        self.__pawn = x

    def getPlayer(self):
        return self.__player

    def setPlayer(self, x):
        self.__player = x

    def color(self):
        if self.__player == 0:
            return "white"
        elif self.__player == 1:
            return "blue"
        elif self.__player == 2:
            return "red"
        elif self.__player == 3:
            return "green"
        elif self.__player == 4:
            return "yellow"


class caseBarrier:

    """

    cette classe permet de retourner s'il y a une barrière

    """
        
    def __init__(self, barrier = False):
        self.__barrier = barrier

    def getBarrier(self):
        return self.__barrier

    def setBarrier(self, x):
        self.__barrier = x


class game:

    def __init__(self):
        self.__onScreenSurface = None
        self.__sizeBoard = 11  # 5 7 9 11
        self.__grid = [] 
        self.__running = None
        self.setFirstGrid()
        self.__numberOfPlayer = 4  # 2 4
        self.__currentPlayer = 1
        self.__pawnCoordinate = {}
        self.setPawnCoordinate()
        self.__gameTurns = 0
        self.__bank = None
        self.bank()
        self.gameBoard()
        #self.console()

#-------------------------
    # permet de set la grille au lancement du jeu
    # va placer les pions et ajuster la taille du plateau selon
    # la variable self.__sizeBoard
#-------------------------

    def setFirstGrid(self):
        for i in range(0, self.__sizeBoard * 2, 2):
            self.__grid.append([])
            self.__grid.append([])
            for j in range(self.__sizeBoard):
                self.__grid[i].append(casePawn())
                self.__grid[i].append(caseBarrier())
                self.__grid[i + 1].append(caseBarrier())
                self.__grid[i + 1].append(caseBarrier(True))
            self.__grid[i].pop()
            self.__grid[i + 1].pop()
        self.__grid.pop()

#-------------------------
    # permet de set la variable self.__bank qui est
    # un dictionnaire de valeurs clés : couleur du joueur
    # valeur = chiffre int en valeur de barrière dans la banque du joueur
    # la fonction est adapter pour 2 ou 4 joueur grâce a la variable 
    # self.__numberOfPlayer
#-------------------------

    def bank(self):
        if self.__numberOfPlayer == 4:
            self.__bank = {"blue": 5, "red": 5, "green": 5, "yellow": 5}
        else:
            self.__bank = {"blue": 10, "red": 10}

#-------------------------
    # permet de placer dans la grille 2 barrières selon les coordonnées
    # X et Y fournies, va les placer à la verticale ou à l'horizontale selon
    # Y (pair ou non)
    # puis va retirer 1 barrière de la banque du joueur en cours
#-------------------------

    def barrierPlacement(self, x, y):
        self.__grid[x][y] = caseBarrier(True)
        if y % 2 == 0:
            self.__grid[x][y + 2] = caseBarrier(True)
        else:
            self.__grid[x + 2][y] = caseBarrier(True)
        self.__bank[casePawn(False, self.__currentPlayer).color()] -= 1

#-------------------------
    # va verifier si les coordonnées fournis sont acceptables pour
    # poser une barrière, va verifier le contenu en banque
    # puis regarde la direction puis que le placement ne soit pas
    # à la limite du plateau et enfin verifie la 2eme barrière
#-------------------------

    def barrierVerification(self, x, y):
        # verifie si la barrière est positionner à la verticale ou à l'horizontale
        if y % 2 == 0:  # pair donc vertical sinon horizontal
            directions = "horizontal"
        else:
            directions = "vertical"

        if self.__bank[casePawn(False, self.__currentPlayer).color()] > 0:
            if self.__sizeBoard * 2 - 2 in (x, y):  # verifie que le joueur n'a pas cliquer dans les cases tout en bas ou tout a droite
                print("false derniere ligne")
                return False
            if self.__grid[y][x].getBarrier() == 0:  # si la position donnée est vide alors on passe a la suite
                if directions == "horizontal":
                    return self.__grid[y +2][x].getBarrier() == 0  # vérifie 2 cases après si elle est vide (car le coin compte comme une case)
                else:
                    return self.__grid[y][x + 2].getBarrier() == 0  # vérifie 2 cases en dessous si elle est vide (car le coin compte comme une case)
        else:
            print("false bank")
            return False
        
#-------------------------
    # va set la variable self.__pawnCoordinate : un dictionnaire qui a en clé la couleur du joueur
    # et en valeur ses coordonée sous forme de liste
    # la fonction est adaptée si les joueurs sont 2 ou 4
#-------------------------

    def setPawnCoordinate(self):
        self.__pawnCoordinate = {"blue": [self.__sizeBoard * 2 - 2, self.__sizeBoard - 1]
            , "red": [0, self.__sizeBoard - 1], }

        self.__grid[self.__sizeBoard * 2 - 2][self.__sizeBoard - 1] = casePawn(True, 1)
        self.__grid[0][self.__sizeBoard - 1] = casePawn(True, 2)

        if self.__numberOfPlayer == 4:
            self.__pawnCoordinate["green"] = [self.__sizeBoard - 1, 0]
            self.__pawnCoordinate["yellow"] = [self.__sizeBoard - 1, self.__sizeBoard * 2 - 2]

            self.__grid[self.__sizeBoard - 1][0] = casePawn(True, 3)
            self.__grid[self.__sizeBoard - 1][self.__sizeBoard * 2 - 2] = casePawn(True, 4)

#-------------------------
    # permet de placer dans la grille 1 pion selon les coordonnées
    # X et Y fournies
    # puis va modifier la variable self.__pawnCoordinate pour l'adapter
#-------------------------

    def pawnPlacement(self, x, y):

        self.__grid[x][y] = casePawn(True, self.__currentPlayer)
        self.__grid[self.__pawnCoordinate[casePawn(False, self.__currentPlayer).color()][0]][
            self.__pawnCoordinate[casePawn(False, self.__currentPlayer).color()][1]] = casePawn(False,self.__currentPlayer)
        self.__pawnCoordinate[casePawn(False, self.__currentPlayer).color()] = [x, y]

#-------------------------
    # lance la fenetre principal du programe en pygame
#-------------------------

    def gameBoard(self):
        
        # Fenêtre du plateau du jeu
        windowSize = (1800, 1000)
        pygame.display.set_caption("QUORIDOR")
        self.__onScreenSurface = (pygame.display.set_mode(windowSize, pygame.RESIZABLE))

        # Surface du plateau
        tableSurfaceSize = ((self.__sizeBoard*75)-25, (self.__sizeBoard*75)-25)
        self.__tableSurface = pygame.Surface(tableSurfaceSize)
        x = (windowSize[0] - tableSurfaceSize[0]) / 2
        y = (windowSize[1] - tableSurfaceSize[1]) / 2
        self.__onScreenSurface.blit(self.__tableSurface, (x, y))

        # Attendez pour fermer la fenêtre
        self.__running = True
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                elif event.type == pygame.VIDEORESIZE:
                    windowSize = event.size
                    self.__onScreenSurface = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
                    x = (windowSize[0] - tableSurfaceSize[0]) / 2
                    y = (windowSize[1] - tableSurfaceSize[1]) / 2
                    self.__onScreenSurface.blit(self.__tableSurface, (x, y))
                    pygame.display.update()
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == True :
                    clicx = pygame.mouse.get_pos()[0]
                    clicy = pygame.mouse.get_pos()[1]
                    size = self.__sizeBoard*75-25
                    
                    if clicx >= x and clicx <= x+size:
                        if clicy >= y and clicy <= y+size:
                            caseX = (clicx - x) / 75
                            caseY = (clicy - y) / 75
                            caseFinalX = self.caseClic(caseX,caseY)[0]
                            caseFinalY = self.caseClic(caseX,caseY)[1]
                            self.gameTurn(caseFinalX , caseFinalY)
                            #self.console()

            if self.__running:
                self.display(x, y)
                # print(pygame.mouse.get_pos())

#-------------------------
    # permet depuis les coordonées de la souris de savoir quelle case du plateau est cliquée
#-------------------------

    def caseClic(self, x, y):
        decimalX = math.floor(x)
        decimalY = math.floor(y)
        caseX = decimalX * 2
        caseY = decimalY * 2
        if (x - decimalX) > 0.6666:
            caseX += 1
        if (y - decimalY) > 0.6666:
            caseY += 1
        
        return (caseX, caseY)

# -------------------------
#Condition de Victoire
# -------------------------
    def verifyVictory(self):
        if self.__pawnCoordinate["red"][0] == self.__sizeBoard * 2 - 2:
            print("Victoire du joueur Rouge !")
            return True
        elif self.__pawnCoordinate["blue"][0] == 0:
            print("Victoire du joueur Bleue !")
            return True
        elif self.__pawnCoordinate["yellow"][1] == 0:
            print("Victoire du joueur Jaune !")
            return True
        elif self.__pawnCoordinate["green"][1] == self.__sizeBoard * 2 - 2:
            print("Victoire du joueur Vert !")
            return True
        else :
            return False

#-------------------------
    # permet de faire un tour de jeu depuis un clic
    # cette fonction se sert de presque toutes les autres fonctions du programme
#-------------------------
    def gameTurn(self, x, y):
        if x % 2 == 0:
            if y % 2 == 0:
                self.pawnPlacement(y,x)
                self.changePlayer()
            else : 
                if self.barrierVerification(x, y) == True:
                    self.barrierPlacement(y, x)
                    self.changePlayer()
        else : 
            if self.barrierVerification(x, y) == True:
                    self.barrierPlacement(y, x)
                    self.changePlayer()
        if self.verifyVictory() == True :
            self.__running = False
            print("Jeux Terminé")


    #-------------------------
    # modifie la variable self.__currentPlayer à chaque appel de la fonction
#-------------------------

    def changePlayer(self):
        self.__currentPlayer += 1
        if self.__numberOfPlayer == 4:
            if self.__currentPlayer == 5:
                self.__currentPlayer = 1
        else:
            if self.__currentPlayer == 3:
                self.__currentPlayer = 1

#-------------------------
    # cette fonction affiche le plateau selon la grille fournie
#-------------------------

    def display(self, x, y):

        white = (255, 255, 255)
        black = (0, 0, 0)
        red = (255, 0, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)
        yellow = (255, 255, 0)
        grey = (120, 120, 120)
        lightGrey = (190, 190, 190)
        pygame.init()
        self.__onScreenSurface.fill(casePawn(False,self.__currentPlayer).color())
        self.__onScreenSurface.blit(self.__tableSurface, (x, y))
        self.__tableSurface.fill(black)
        for i in range(len(self.__grid)):
            for j in range(len(self.__grid) // 2 + 1):

                if i % 2 == 0:  # si la ligne est paire on va placer une case pion puis une case barrière verticale

                    if self.__grid[i][j * 2].getPawn() == True:
                        if self.__grid[i][j * 2].getPlayer() == 1:
                            pygame.draw.rect(self.__tableSurface, blue, pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                        elif self.__grid[i][j * 2].getPlayer() == 2:
                            pygame.draw.rect(self.__tableSurface, red, pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                        elif self.__grid[i][j * 2].getPlayer() == 3:
                            pygame.draw.rect(self.__tableSurface, green,
                                                pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                        elif self.__grid[i][j * 2].getPlayer() == 4:
                            pygame.draw.rect(self.__tableSurface, yellow,
                                                pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                    else:
                        pygame.draw.rect(self.__tableSurface, white, pygame.Rect(j * 75, i / 2 * 75, 50, 50))

                    if j != len(self.__grid) // 2:
                        if self.__grid[i][j * 2 + 1].getBarrier() == True:
                            pygame.draw.rect(self.__tableSurface, black,
                                                pygame.Rect(j * 75 + 50, i / 2 * 75, 25, 50))
                        else:
                            pygame.draw.rect(self.__tableSurface, grey,
                                                pygame.Rect(j * 75 + 50, i / 2 * 75, 25, 50))

                else:
                    if self.__grid[i][j * 2].getBarrier() == True:
                        pygame.draw.rect(self.__tableSurface, black,
                                            pygame.Rect(j * 75, i / 2 * 75 + 12.5, 50, 25))
                    else:
                        pygame.draw.rect(self.__tableSurface, grey,
                                            pygame.Rect(j * 75, i / 2 * 75 + 12.5, 50, 25))
                    if j != len(self.__grid) // 2:
                        pygame.draw.rect(self.__tableSurface, black,
                                            pygame.Rect(j * 75 + 50, i / 2 * 75 + 12.5, 25, 25))
    
        font = pygame.font.Font(None, 36)
        for i in range(1,self.__numberOfPlayer+1):
            text = "bank "+ casePawn(False,i).color() +" "+ str(self.__bank[casePawn(False, i).color()]) +" !"
            text_surface = font.render(text, True, (255, 255, 255))
            self.__onScreenSurface.blit(text_surface, (100, 100+(i*50)))
        pygame.display.flip()

# ------------------------------
#   affichage  console
# ------------------------------

    def console(self):
        for i in range(len(self.__grid)):
            for j in range(len(self.__grid) // 2 + 1):
                if i % 2 == 0:
                    if self.__grid[i][j * 2].getPawn() == True:
                        if self.__grid[i][j * 2].getPlayer() == 1:
                            print("1",end="")
                        if self.__grid[i][j * 2].getPlayer() == 2:
                            print("2",end="")
                        if self.__grid[i][j * 2].getPlayer() == 3:
                            print("3",end="")
                        if self.__grid[i][j * 2].getPlayer() == 4:
                            print("4",end="")
                    else:
                        print(".",end="")
                    
                    if j != len(self.__grid) // 2:
                        if self.__grid[i][j * 2 + 1].getBarrier() == True:
                            print("|",end="")
                        else:
                            print("*",end="")
                else:
                    if self.__grid[i][j * 2].getBarrier() == True:
                        print("-",end="")
                    else:
                        print("*",end="")
                    if j != len(self.__grid) // 2:
                        print("□",end="")
                if j == len(self.__grid)// 2:
                    print("")
        print("________________________________________")


game()