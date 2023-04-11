#Importations des bibliothèques python
from random import *
import pygame
import math


#Importations des autres fichiers/classes pour le fonctionnement du code 
from includes.caseBarrier import caseBarrier
from includes.casePawn import casePawn

# import serveur
# import client
# import threading

# Coder en Anglais en CamelCase

class game:
    def __init__(self):
        self.__onScreenSurface = None
        self.__sizeBoard = 7  # 5 7 9 11
        self.__grid = []
        self.setFirstGrid()
        self.__numberOfPlayer = 4  # 2 4
        self.__currentPlayer = 1
        self.__pawnCoordinate = {}
        self.setPawnCoordinate()
        self.__gameTurns = 0
        self.__bank = None
        # -----------------------------
        #  Partie réseau
        # self.__reseauPlayer = 0
        # self.__reseauHosteur = False

        # if input("host ?") == "y":
        #     self.__reseauHosteur = True
            
        #     self.__reseauPlayer = 1

        #     chat_server = serveur.serv()
        #     chat_server_thread = threading.Thread(target=chat_server.run)
        #     chat_server_thread.start()
        
        # if input("client ?") == "y":
        #     chat_client = client.player()
        #     chat_server_thread_clien = threading.Thread(target=chat_client.run)
        #     chat_server_thread_clien.start()


        # -----------------------------
        self.bank()
        self.gameBoard()
        # self.console()


    def setFirstGrid(self):
    #-------------------------
        # permet de set la grille au lancement du jeu
        # va placer les pions et ajuster la taille du plateau selon
        # la variable self.__sizeBoard
    #-------------------------
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


    def bank(self):
    #-------------------------
        # permet de set la variable self.__bank qui est
        # un dictionnaire de valeurs clés : couleur du joueur
        # valeur = chiffre int en valeur de barrière dans la banque du joueur
        # la fonction est adapter pour 2 ou 4 joueur grâce a la variable 
        # self.__numberOfPlayer
    #-------------------------
        if self.__numberOfPlayer == 4:
            self.__bank = {"blue": 5, "red": 5, "green": 5, "yellow": 5}
        else:
            self.__bank = {"blue": 10, "red": 10}


    def barrierPlacement(self, x, y):
    #-------------------------
        # permet de placer dans la grille 2 barrières selon les coordonnées
        # X et Y fournies, va les placer à la verticale ou à l'horizontale selon
        # Y (pair ou non)
        # puis va retirer 1 barrière de la banque du joueur en cours
    #-------------------------
        self.__grid[x][y] = caseBarrier(True)
        if y % 2 == 0:
            self.__grid[x][y + 2] = caseBarrier(True)
        else:
            self.__grid[x + 2][y] = caseBarrier(True)
        self.__bank[casePawn(False, self.__currentPlayer).color()] -= 1


    def barrierVerification(self, x, y):
    #-------------------------
        # va verifier si les coordonnées fournis sont acceptables pour
        # poser une barrière, va verifier le contenu en banque
        # puis regarde la direction puis que le placement ne soit pas
        # à la limite du plateau et enfin verifie la 2eme barrière
    #-------------------------
        # verifie si ba barriere est posisionner vertical ou horizontal
        if y % 2 == 0:  # pair donc vertical sinon horizontal
            directions = "horizontal"
        else:
            directions = "vertical"
        if self.__bank[casePawn(False, self.__currentPlayer).color()] > 0:
            if self.__sizeBoard * 2 - 2 in (x, y):  # verifie que le joueur n'est pas cliquer dans les case tout en bas ou tout a droite
                print("false derniere ligne")
                return False
            if self.__grid[y][x].getBarrier() == 0:  # si la position donner est vide alors on passe a la suite
                if directions == "horizontal":
                    return self.__grid[y +2][x].getBarrier() == 0  # verifie 2 case apres si elle est vide (car le coin compt comme une case)
                else:
                    return self.__grid[y][x + 2].getBarrier() == 0  # verifie 2 case en dessous si elle est vide (car le coin compt comme une case)
        else:
            print("false bank")
            return False
        


    def pawnVerification(self, x, y):
    # ----------------------------------
        # pawn vérification
            # va vérifier si les coordonnées fournies sont acceptables pour
            # poser un pion selon les règles du jeu et le joueur en cour
            # crée les variables des coordonnées des position possible ainsi que les barrières possibles
            # vérifie selon la coordonnée qu'aucune barrière n'entrave son chemin
            # va vérifier si le saut de joueur et possible en prenant en compte les barrières
            # va appeler une fonction supplémentaire pour vérifier les diagonales
    # ----------------------------------
        co = [self.__pawnCoordinate[casePawn(False,self.__currentPlayer).color()][0],self.__pawnCoordinate[casePawn(False,self.__currentPlayer).color()][1]]
        possibleCase = ([0,2],[2,0],[0,-2],[-2,0],[-2,2],[2,2],[2,-2],[-2,-2],[0,4],[4,0],[0,-4],[-4,0])
        possibleCaseBarrier = ([0,1],[1,0],[0,-1],[-1,0],[0,3],[3,0],[0,-3],[-3,0])
        case = [co[0]-y,co[1]-x]
        if case in possibleCase:
            index = possibleCase.index(case)
            if self.__grid[y][x].getPawn() == False:
                    if index <= 3: #verrif des 4 case proche N S E W
                        if self.__grid[co[0]-possibleCaseBarrier[index][0]][co[1]-possibleCaseBarrier[index][1]].getBarrier() == False:
                            return True
                        
                    elif index > 7: #verrif du saut de joueur
                        if self.__grid[co[0]-possibleCaseBarrier[index-8][0]][co[1]-possibleCaseBarrier[index-8][1]].getBarrier() == False:
                            if self.__grid[co[0]-possibleCase[index-8][0]][co[1]-possibleCase[index-8][1]].getPawn() == True:
                                if self.__grid[co[0]-possibleCaseBarrier[index-4][0]][co[1]-possibleCaseBarrier[index-4][1]].getBarrier() == False:
                                    return True
                                
                    else:  #verrif diagonal
                        print(index)
                        return self.pawnVerificationDiagonal(index) == True
        return False


    def pawnVerificationDiagonal(self,direction):
    # ----------------------------------
        # aide pour pawnVerification
            # fonction qui permet de vérifier les possibilitées de diagonale
            # selon l'indice donner la direction NE SE SO NO
            # puis va 2 vérifications pour savoirs quel pion est normalement passable
            # va vérifier selon ce dernier si des barrières n'entravent pas le chemin
    # ----------------------------------
        co = [self.__pawnCoordinate[casePawn(False,self.__currentPlayer).color()][0],self.__pawnCoordinate[casePawn(False,self.__currentPlayer).color()][1]]
        nord , sud , est , ouest = False , False , False , False
        if direction == 6:
            check1 = "nord"
            check2 = "est"
        elif direction == 7:
            check1 = "sud"
            check2 = "est"
        elif direction == 4:
            check1 = "sud"
            check2 = "ouest"
        else:
            check1 = "nord"
            check2 = "ouest"
        if check1 == "nord":
            if self.__grid[co[0]-1][co[1]].getBarrier() == False:
                if self.__grid[co[0]-2][co[1]].getPawn() == True:
                    if self.__grid[co[0]-3][co[1]].getBarrier() == True or self.__grid[co[0]-4][co[1]].getPawn() == True:
                        nord = True
        else:
            if self.__grid[co[0]+1][co[1]].getBarrier() == False:
                if self.__grid[co[0]+2][co[1]].getPawn() == True:
                    if self.__grid[co[0]+3][co[1]].getBarrier() == True or self.__grid[co[0]+4][co[1]].getPawn() == True:
                        sud = True
        
        if check2 == "est":
            if self.__grid[co[0]][co[1]+1].getBarrier() == False:
                if self.__grid[co[0]][co[1]+2].getPawn() == True:
                    if self.__grid[co[0]][co[1]+3].getBarrier() == True or self.__grid[co[0]][co[1]+4].getPawn() == True:
                        est = True
        else:
            if self.__grid[co[0]][co[1]-1].getBarrier() == False:
                if self.__grid[co[0]][co[1]-2].getPawn() == True:
                    if self.__grid[co[0]][co[1]-3].getBarrier() == True or self.__grid[co[0]][co[1]-4].getPawn() == True:
                        ouest = True
        if direction == 6:
            if nord == True:
                if self.__grid[co[0]-2][co[1]+1].getBarrier() == False:
                    return True
            if est == True:
                if self.__grid[co[0]-1][co[1]+2].getBarrier() == False:
                    return True
        elif direction == 7:
            if sud == True:
                if self.__grid[co[0]+2][co[1]+1].getBarrier() == False:
                    print("la")
                    return True
            if est == True:
                if self.__grid[co[0]+1][co[1]+2].getBarrier() == False:
                    print("ici")
                    return True
        elif direction == 4:
            if sud == True:
                if self.__grid[co[0]+2][co[1]-1].getBarrier() == False:
                    return True
            if ouest == True:
                if self.__grid[co[0]+1][co[1]-2].getBarrier() == False:
                    return True
        else:
            if nord == True:
                if self.__grid[co[0]-2][co[1]-1].getBarrier() == False:
                    return True
            if ouest == True:
                if self.__grid[co[0]-1][co[1]-2].getBarrier() == False:
                    return True
        return False


    def setPawnCoordinate(self):
    #-------------------------
        # va set la variable self.__pawnCoordinate : un dictionnaire qui a se clé la couleur du joueur
        # et en valeur ses coordonnées sous forme de liste
        # la fonction est adaptée si les joueurs sont 2 ou 4
    #-------------------------
        self.__pawnCoordinate = {"blue": [self.__sizeBoard * 2 - 2, self.__sizeBoard - 1]
            , "red": [0, self.__sizeBoard - 1], }
        self.__grid[self.__sizeBoard * 2 - 2][self.__sizeBoard - 1] = casePawn(True, 1)
        self.__grid[0][self.__sizeBoard - 1] = casePawn(True, 2)
        if self.__numberOfPlayer == 4:
            self.__pawnCoordinate["green"] = [self.__sizeBoard - 1, 0]
            self.__pawnCoordinate["yellow"] = [self.__sizeBoard - 1, self.__sizeBoard * 2 - 2]
            self.__grid[self.__sizeBoard - 1][0] = casePawn(True, 3)
            self.__grid[self.__sizeBoard - 1][self.__sizeBoard * 2 - 2] = casePawn(True, 4)


    def pawnPlacement(self, x, y):
    #-------------------------
        # permet de placer dans la grille 1 pion selon les coordonnées
        # X et Y fournies
        # puis va modifier la variable self.__pawnCoordinate pour l'adapter
    #-------------------------
        self.__grid[x][y] = casePawn(True, self.__currentPlayer)
        self.__grid[self.__pawnCoordinate[casePawn(False, self.__currentPlayer).color()][0]][self.__pawnCoordinate[casePawn(False, self.__currentPlayer).color()][1]] = casePawn(False,0)
        self.__pawnCoordinate[casePawn(False, self.__currentPlayer).color()] = [x, y]


    def gameBoard(self):
    #-------------------------
        # lance la fenêtre principal du programme en pygame
    #-------------------------
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
        
        # Attendre pour fermer la fenêtre
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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
                            caseFinalX = self.caseClicked(caseX,caseY)[0]
                            caseFinalY = self.caseClicked(caseX,caseY)[1]
                            self.gameTurn(caseFinalX , caseFinalY)
                            # self.console()
            if running:
                self.display(x,y)


    def verifyVictory(self):
    # -------------------------
        #Condition de Victoire
    # -------------------------
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


    def caseClicked(self, x, y):
    #-------------------------
        # permet depuis les coordonnées de la souris de savoir quelle case du plateau est cliquée
    #-------------------------
        decimalX = math.floor(x)
        decimalY = math.floor(y)
        caseX = decimalX * 2
        caseY = decimalY * 2
        if (x - decimalX) > 0.6666:
            caseX += 1
        if (y - decimalY) > 0.6666:
            caseY += 1
        
        return (caseX,caseY)



    def gameTurn(self,x,y):
    #-------------------------
        # permet de faire un tour de jeu depuis un clic
        # cette fonction se sert de presque toutes les autres fonctions du programme
    #-------------------------
        if x % 2 == 0:
            if y % 2 == 0:
                if self.pawnVerification(x,y) == True:
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
        self.verifyVictory()


    def changePlayer(self):
    #-------------------------
        # modifie la variable self.__currentPlayer à chaque appel de la fonction
    #-------------------------
        self.__currentPlayer += 1
        if self.__numberOfPlayer == 4:
            if self.__currentPlayer == 5:
                self.__currentPlayer = 1
        else:
            if self.__currentPlayer == 3:
                self.__currentPlayer = 1


    def display(self,x,y):
    #-------------------------
        # cette fonction affiche le plateau selon la grille fournie
    #-------------------------
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
                if i % 2 == 0:  # si la ligne est paire on va placer une case pion puis une case barrier vertical
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


    def console(self):
    # ------------------------------
        #affichage  console
    # ------------------------------
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
                        print("□",end="")
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
                        print("+",end="")
                if j == len(self.__grid)// 2:
                    print("")
        print("________________________________________")

game()