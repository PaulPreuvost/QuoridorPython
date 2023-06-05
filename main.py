#Importations des bibliothèques python
from random import *
import pygame
import math
import threading
from pathlib import Path
import pygame_widgets
from pygame_widgets.button import Button
import random

#Importations des autres fichiers/classes pour le fonctionnement du code
from user_interface.colors import get_white, get_black, get_red, get_blue, get_green, get_grey, get_yellow, get_light_red, get_light_blue, get_light_green, get_light_yellow, get_light_grey
import serveur
import client
from includes.case_barrier import case_barrier
from includes.case_pawn import case_pawn

class game:

    def __init__(self, numberOfPlayer = 2, sizeBoard = 7, mode = "null" , ia = 0 , save = 0):
        self.__onScreenSurface = None
        self.__sizeBoard = sizeBoard
        self.__grid = []
        self.set_first_grid()
        self.__ia = ia
        if self.__ia == 1:
            self.__numberOfPlayer = 2
        else:
            self.__numberOfPlayer = numberOfPlayer
        self.__currentPlayer = 1
        self.__pawnCoordinate = {}
        self.set_pawn_coordinate()
        self.__game_turns = 0
        self.__bank = None
        
        self.__mode = mode
        self.__save = save
        self.__reseau = False
        self.__reseauPlayer = 0 
        self.__reseauHosteur = False
        a="oui"
        self.__reseau = True
        if a == "oui":
            if input("host ?") == "y":
                self.__reseauHosteur = True
                print(serveur.serveur().getCode())
                self.chat_server_thread = threading.Thread(target=serveur.serveur().start)
                self.chat_server_thread.start()

            if self.__reseauHosteur == True:
                ip = serveur.serveur().getIp()
                self.player_instance = client.player()
                self.player_instance.start(ip) 
                self.__reseauPlayer = self.player_instance.client_receive()

            elif input("client ?") == "y":
                code = input("code :")
                ip = serveur.serveur().getIp()
                ip = ip.split(".")
                ip[-1] = code
                ip = ".".join(ip)
                self.player_instance = client.player()
                self.player_instance.start(ip) 
                self.__reseauPlayer = self.player_instance.client_receive()
        self.bank()
        if self.__save == 1:
            self.lireSauvegarde()
        self.game_board()
        # self.console()



    def set_first_grid(self):
    #-------------------------
        # permet de set la grille au lancement du jeu
        # va placer les pions et ajuster la taille du plateau selon
        # la variable self.__sizeBoard
    #-------------------------
        for i in range(0, self.__sizeBoard * 2, 2):
            self.__grid.append([])
            self.__grid.append([])
            for j in range(self.__sizeBoard):
                self.__grid[i].append(case_pawn())
                self.__grid[i].append(case_barrier())
                self.__grid[i + 1].append(case_barrier())
                self.__grid[i + 1].append(case_barrier(True))
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


    def barrier_placement(self, x, y):
    #-------------------------
        # permet de placer dans la grille 2 barrières selon les coordonnées
        # X et Y fournies, va les placer à la verticale ou à l'horizontale selon
        # Y (pair ou non)
        # puis va retirer 1 barrière de la banque du joueur en cours
    #-------------------------

        self.__grid[x][y] = case_barrier(True)
        if y % 2 == 0:
            self.__grid[x][y + 2] = case_barrier(True)
        else:
            self.__grid[x + 2][y] = case_barrier(True)
        self.__bank[case_pawn(False, self.__currentPlayer).color()] -= 1

    def barrier_verification(self, x, y):
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

        if self.__bank[case_pawn(False, self.__currentPlayer).color()] > 0:
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
    

    def pawn_verification(self, x, y):
    # ----------------------------------
        # pawn vérification
            # va vérifier si les coordonnées fournies sont acceptables pour
            # poser un pion selon les règles du jeu et le joueur en cour
            # crée les variables des coordonnées des position possible ainsi que les barrières possibles
            # vérifie selon la coordonnée qu'aucune barrière n'entrave son chemin
            # va vérifier si le saut de joueur et possible en prenant en compte les barrières
            # va appeler une fonction supplémentaire pour vérifier les diagonales
    # ----------------------------------

        co = [self.__pawnCoordinate[case_pawn(False,self.__currentPlayer).color()][0],self.__pawnCoordinate[case_pawn(False,self.__currentPlayer).color()][1]]
        possibleCase = ([0,2],[2,0],[0,-2],[-2,0],[-2,2],[2,2],[2,-2],[-2,-2],[0,4],[4,0],[0,-4],[-4,0])
        possiblecase_barrier = ([0,1],[1,0],[0,-1],[-1,0],[0,3],[3,0],[0,-3],[-3,0])
        case = [co[0]-y,co[1]-x]

        
        if case in possibleCase:
            index = possibleCase.index(case)
            if self.__grid[y][x].getPawn() == False:

                    if index <= 3: #verrif des 4 case proche N S E W
                        if self.__grid[co[0]-possiblecase_barrier[index][0]][co[1]-possiblecase_barrier[index][1]].getBarrier() == False:
                            return True
                        
                    elif index > 7: #verrif du saut de joueur
                        if self.__grid[co[0]-possiblecase_barrier[index-8][0]][co[1]-possiblecase_barrier[index-8][1]].getBarrier() == False:
                            if self.__grid[co[0]-possibleCase[index-8][0]][co[1]-possibleCase[index-8][1]].getPawn() == True:
                                if self.__grid[co[0]-possiblecase_barrier[index-4][0]][co[1]-possiblecase_barrier[index-4][1]].getBarrier() == False:
                                    return True
                                
                    else:  #verrif diagonal
                        return self.pawn_verificationDiagonal(index) == True
        return False
        
    def pawn_verificationDiagonal(self,direction):
    # ----------------------------------
        # aide pour pawnVerification
            # fonction qui permet de vérifier les possibilitées de diagonale
            # selon l'indice donner la direction NE SE SO NO
            # puis va 2 vérifications pour savoirs quel pion est normalement passable
            # va vérifier selon ce dernier si des barrières n'entravent pas le chemin
    # ----------------------------------
        co = [self.__pawnCoordinate[case_pawn(False,self.__currentPlayer).color()][0],self.__pawnCoordinate[case_pawn(False,self.__currentPlayer).color()][1]]
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
                    return True
            if est == True:
                if self.__grid[co[0]+1][co[1]+2].getBarrier() == False:
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




    def set_pawn_coordinate(self):
    #-------------------------
        # va set la variable self.__pawnCoordinate : un dictionnaire qui a se clé la couleur du joueur
        # et en valeur ses coordonnées sous forme de liste
        # la fonction est adaptée si les joueurs sont 2 ou 4
    #-------------------------
        self.__pawnCoordinate = {"blue": [self.__sizeBoard * 2 - 2, self.__sizeBoard - 1]
            , "red": [0, self.__sizeBoard - 1], }

        self.__grid[self.__sizeBoard * 2 - 2][self.__sizeBoard - 1] = case_pawn(True, 1)
        self.__grid[0][self.__sizeBoard - 1] = case_pawn(True, 2)

        if self.__numberOfPlayer == 4:
            self.__pawnCoordinate["green"] = [self.__sizeBoard - 1, 0]
            self.__pawnCoordinate["yellow"] = [self.__sizeBoard - 1, self.__sizeBoard * 2 - 2]

            self.__grid[self.__sizeBoard - 1][0] = case_pawn(True, 3)
            self.__grid[self.__sizeBoard - 1][self.__sizeBoard * 2 - 2] = case_pawn(True, 4)

    def pawn_placement(self, x, y):
    #-------------------------
        # permet de placer dans la grille 1 pion selon les coordonnées
        # X et Y fournies
        # puis va modifier la variable self.__pawnCoordinate pour l'adapter
    #-------------------------
        self.__grid[x][y] = case_pawn(True, self.__currentPlayer)
        self.__grid[self.__pawnCoordinate[case_pawn(False, self.__currentPlayer).color()][0]][self.__pawnCoordinate[case_pawn(False, self.__currentPlayer).color()][1]] = case_pawn(False,0)
        self.__pawnCoordinate[case_pawn(False, self.__currentPlayer).color()] = [x, y]

    def game_board(self):
    #-------------------------
        # lance la fenetre principal du programe en pygame
    #-------------------------
        # Fenêtre du plateau du jeu
        windowSize = (1800, 1000)
        pygame.display.set_caption("QUORIDOR")
        self.__onScreenSurface = (pygame.display.set_mode(windowSize, pygame.RESIZABLE))
        size = self.__sizeBoard*75-25

        # Surface du plateau
        tableSurfaceSize = ((self.__sizeBoard*75)-25, (self.__sizeBoard*75)-25)
        self.__tableSurface = pygame.Surface(tableSurfaceSize)
        x = (windowSize[0] - tableSurfaceSize[0]) / 2
        y = (windowSize[1] - tableSurfaceSize[1]) / 2
        self.__onScreenSurface.blit(self.__tableSurface, (x, y))

        # Attendez pour fermer la fenêtre
        running = True
        while running:
            if int(self.__reseauPlayer) == self.__currentPlayer:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                                running = False

                    if event.type == pygame.VIDEORESIZE:
                                windowSize = event.size
                                self.__onScreenSurface = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
                                x = (windowSize[0] - tableSurfaceSize[0]) / 2
                                y = (windowSize[1] - tableSurfaceSize[1]) / 2
                                self.__onScreenSurface.blit(self.__tableSurface, (x, y))
                                pygame.display.update()


                    clicx = pygame.mouse.get_pos()[0]
                    clicy = pygame.mouse.get_pos()[1]
                    if clicx >= x and clicx <= x+size:
                        if clicy >= y and clicy <= y+size:
                            caseX = (clicx - x) / 75
                            caseY = (clicy - y) / 75
                            caseFinalX = self.case_clicked(caseX,caseY)[0]
                            caseFinalY = self.case_clicked(caseX,caseY)[1]

                            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == True:
                                self.game_turn(caseFinalX , caseFinalY)
                                message = f"{caseFinalX},{caseFinalY}"
                                print("le message est : ",message)
                                self.player_instance.client_send(message)
                                self.display(x,y)

                                #--------parti IA------
                                if self.__ia == 1:
                                    self.case_IA()
            else:
                self.display(x,y)
                message = self.player_instance.client_receive()
                print(message)
                message = message.split(",")
                print(message)
                self.game_turn(int(message[0]),int(message[1]))


                
            if running:
                self.display(x,y)


    def case_IA(self):
        while self.__currentPlayer == 2:
            resulta = 0
            caseX = random.randint(0,self.__sizeBoard*2-2)
            caseY = random.randint(0,self.__sizeBoard*2-2)

            if self.__bank["red"] != 0:
                deplacement = random.randint(0,1)
            else:
                deplacement = 1

            if deplacement == 1:
                while resulta == 0 or self.pawn_verification(caseX,caseY) == False:
                    while caseX % 2 != 0:
                        caseX = random.randint(0,self.__sizeBoard*2-2)
                        while caseY %2 != 0:
                            caseY = random.randint(0,self.__sizeBoard*2-2)
                    if self.pawn_verification(caseX,caseY) == True:
                        resulta = 1
                    else:
                        caseX = random.randint(0,self.__sizeBoard*2-2)
                        caseY = random.randint(0,self.__sizeBoard*2-2)
            else:
                while resulta == 0 or self.barrier_verification(caseX,caseY) == False:
                    while caseX % 2 == 0 and caseY % 2 == 0:
                        caseX = random.randint(0,self.__sizeBoard*2-2)
                        caseY = random.randint(0,self.__sizeBoard*2-2)
                    if self.barrier_verification(caseX,caseY) == True:
                        resulta = 1
                    else:
                        caseX = random.randint(0,self.__sizeBoard*2-2)
                        caseY = random.randint(0,self.__sizeBoard*2-2)
            self.game_turn(caseX,caseY)


    def verify_victory(self):
    # -------------------------
        #Condition de Victoire
    # -------------------------
        if self.__pawnCoordinate["red"][0] == self.__sizeBoard * 2 - 2:
            print("Victoire du joueur Rouge !")
            return True
        elif self.__pawnCoordinate["blue"][0] == 0:
            print("Victoire du joueur Bleue !")
            return True
        
        if self.__numberOfPlayer == 4:
            if self.__pawnCoordinate["yellow"][1] == 0:
                print("Victoire du joueur Jaune !")
                return True
            elif self.__pawnCoordinate["green"][1] == self.__sizeBoard * 2 - 2:
                print("Victoire du joueur Vert !")
                return True
            else :
                return False
        else :
            return False



    def case_clicked(self, x, y):
    #-------------------------
        # permet depuis les coordonées de la souris de savoir quelle case du plateau est cliquée
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
    
    def game_turn(self,x,y):
    #-------------------------
        # permet de faire un tour de jeu depuis un clic
        # cette fonction se sert de presque toutes les autres fonctions du programme
    #-------------------------
        if x % 2 == 0:
            if y % 2 == 0:
                if self.pawn_verification(x,y):
                    self.pawn_placement(y,x)
                    self.change_player()
            else : 
                if self.barrier_verification(x, y) :
                    self.barrier_placement(y, x)
                    self.change_player()
        else : 
            if self.barrier_verification(x, y) == True:
                    self.barrier_placement(y, x)
                    self.change_player()
        self.verify_victory()


    def change_player(self):
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

        font_interface__XL = pygame.font.Font("../../user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf", 70)
        font_interface__L = pygame.font.Font("../../user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf", 45)
        font_interface__M = pygame.font.Font("../../user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf", 20)

        pygame.init()
        self.__onScreenSurface.fill(case_pawn(False,self.__currentPlayer).color())
        self.__onScreenSurface.blit(self.__tableSurface, (x, y))
        self.__tableSurface.fill(get_black())
        save = Button(
            self.__onScreenSurface, 1400, 500, 200, 100, text='Save', fontSize=100,
            margin=25, textColour='white', inactiveColour=(255, 0, 0), pressedColour=get_white(),
            radius=5, font= font_interface__L,
            textVAlign='bottom', onClick=lambda: (self.sauvegarde()))
        send = Button(
            self.__onScreenSurface, 1600, 500, 200, 100, text='Send', fontSize=100,
            margin=25, textColour='white', inactiveColour=(255, 0, 0), pressedColour=get_white(),
            radius=5, font= font_interface__L,
            textVAlign='bottom', onClick=lambda: (self.player_instance.client_send("Yes")))
        for i in range(len(self.__grid)):
            for j in range(len(self.__grid) // 2 + 1):

                if i % 2 == 0:  # si la ligne est paire on va placer une case pion puis une case barrier vertical

                    if self.__grid[i][j * 2].getPawn() == True:
                        if self.__grid[i][j * 2].getPlayer() == 1:
                            pygame.draw.rect(self.__tableSurface, get_blue(), pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                        elif self.__grid[i][j * 2].getPlayer() == 2:
                            pygame.draw.rect(self.__tableSurface, get_red(), pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                        elif self.__grid[i][j * 2].getPlayer() == 3:
                            pygame.draw.rect(self.__tableSurface, get_green(),
                                                pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                        elif self.__grid[i][j * 2].getPlayer() == 4:
                            pygame.draw.rect(self.__tableSurface, get_yellow(),
                                                pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                    else:
                        if self.pawn_verification(j*2,i) == True:
                            if self.__currentPlayer == 1 :
                                pygame.draw.rect(self.__tableSurface, get_light_grey(), pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                            elif self.__currentPlayer == 2 : 
                                pygame.draw.rect(self.__tableSurface, get_light_grey(), pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                            elif self.__currentPlayer == 3 : 
                                pygame.draw.rect(self.__tableSurface, get_light_grey(), pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                            elif self.__currentPlayer == 4 : 
                                pygame.draw.rect(self.__tableSurface, get_light_grey(), pygame.Rect(j * 75, i / 2 * 75, 50, 50))

                        else:
                            pygame.draw.rect(self.__tableSurface, get_white(), pygame.Rect(j * 75, i / 2 * 75, 50, 50))

                    if j != len(self.__grid) // 2:
                        if self.__grid[i][j * 2 + 1].getBarrier() == True:
                            pygame.draw.rect(self.__tableSurface, get_black(),
                                                pygame.Rect(j * 75 + 50, i / 2 * 75, 25, 50))
                        else:
                            pygame.draw.rect(self.__tableSurface, get_grey(),
                                                pygame.Rect(j * 75 + 50, i / 2 * 75, 25, 50))

                else:
                    if self.__grid[i][j * 2].getBarrier() == True:
                        pygame.draw.rect(self.__tableSurface, get_black(),
                                            pygame.Rect(j * 75, i / 2 * 75 + 12.5, 50, 25))
                    else:
                        pygame.draw.rect(self.__tableSurface, get_grey(),
                                            pygame.Rect(j * 75, i / 2 * 75 + 12.5, 50, 25))
                    if j != len(self.__grid) // 2:
                        pygame.draw.rect(self.__tableSurface, get_black(),
                                            pygame.Rect(j * 75 + 50, i / 2 * 75 + 12.5, 25, 25))
    
        font = pygame.font.Font(None, 36)
        for i in range(1,self.__numberOfPlayer+1):
            text = "bank "+ case_pawn(False,i).color() +" "+ str(self.__bank[case_pawn(False, i).color()]) +" !"
            text_surface = font.render(text, True, get_white())
            self.__onScreenSurface.blit(text_surface, (100, 100+(i*50)))
        
        pygame_widgets.update(pygame.event.get())
        pygame.display.update()

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


    def sauvegarde(self):
        save = Path(__file__).parent / "save.txt"
        conditionFichier = False
        try:
            open(save,'w')
            conditionFichier = True
        except:
            print("erreur sauvegarde")
            conditionFichier = False
        
        if conditionFichier == True:
            save=open(save,'w')
            for i in range(len(self.__grid)):
                    for j in range(len(self.__grid)):
                        if i%2 == 0 and j%2 == 0:
                            save.write(f"{self.__grid[j][i].getPlayer()}")
                        else:
                            if self.__grid[j][i].getBarrier() == True:
                                save.write("T")
                            else:
                                save.write("F")
            save.write(f"\n{self.__numberOfPlayer}\n{self.__currentPlayer}\n{self.__pawnCoordinate}\n{self.__game_turns}\n{self.__bank}\n{self.__ia}\n{self.__sizeBoard}")

            save.close()

    def lireSauvegarde(self):
        save = Path(__file__).parent / "save.txt"
        conditionFichier = False
        try:
            open(save,'r')
            conditionFichier = True
        except:
            conditionFichier = False
        if conditionFichier == True:
            save=open(save,'r')
            content = save.readlines()
            varGrille = (content[0])
            self.__numberOfPlayer = int(content[1])
            self.__currentPlayer = int(content[2])
            self.__pawnCoordinate = eval((content[3]))
            self.__game_turns = int(content[4])
            self.__bank = eval(content[5])
            self.__ia = int(content[6])
            self.__sizeBoard = int(content[7])
            save.close()
            incremente = 0
            self.__grid=[]
            number = "012345"
            for i in range(self.__sizeBoard*2-1):
                self.__grid.append([])
            for i in range(self.__sizeBoard*2-1):
                for j in range(self.__sizeBoard*2-1):
                    if varGrille[incremente] in number:
                        if varGrille[incremente] == "0":
                            self.__grid[j].append(case_pawn(False , 0))
                        else :
                            self.__grid[j].append(case_pawn(True , eval(varGrille[incremente])))
                    else:
                        if varGrille[incremente] == "F":
                            self.__grid[j].append(case_barrier(False))
                        else:
                            self.__grid[j].append(case_barrier(True))
                    incremente += 1

            print(self.__pawnCoordinate , type(self.__pawnCoordinate))


    # def pathfinding(self):
    #     a=0
    #     fakeCo = self.__pawnCoordinate
    #     fakeGrid = self.__grid
    #     x,y=0,0
    #     for player in range(self.__numberOfPlayer):
    #         while(self.verify_victory() == False or a < 1000):
    #             a+=1
    #             self.__grid[x][y] = case_pawn(True, player)
game()