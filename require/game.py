# Importations des bibliothèques python
import math
import os
import sys
import random
import threading
import pygame
import pygame_widgets
from pygame import mixer
from pygame_widgets.button import Button

from pathlib import Path
from user_interface.colors import get_white, get_black, get_red, get_blue, \
    get_green, get_yellow, get_light_grey, get_blue_wp, get_blue_cyan, get_violet, get_dark_violet, \
    get_green_wp
import client, serveur
from case_barrier import case_barrier
from case_pawn import case_pawn
import settings
import launch
import win

def ressouce_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Game:

    def __init__(self, number_of_player, size_board, volume, number_of_barrier=40, save=0, computer=0,
                 network=False, host=False,
                 clients=False):
        self.__game_state = "Game"
        self.__cpt = 0
        self.__on_screen_surface = None
        self.__size_board = size_board
        self.__grid = []
        self.__running = None
        self.set_first_grid()
        self.__computer = computer
        if self.__computer == 1:
            self.__number_of_player = 2
        else:
            self.__number_of_player = number_of_player
        self.__current_player = 1
        self.__previousActionType = []
        self.__previousPawnCoordinates = []
        self.__previousBarrierCoordinates = []
        self.__pawn_coordinate = {}
        self.set__pawn_coordinate()
        self.__game_turns = 0
        self.__bank = None
        self.__volume = volume
        self.__winner = None

        self.__save = save
        self.__network = False
        self.__network_player = 0
        self.network_host = False
        if network == True:
            self.__network = True
            if host == True:
                self.network_host = True
                print(serveur.Serveur().get_code())
                self.chat_server_thread = threading.Thread(target=serveur.Serveur().start)
                self.chat_server_thread.start()

            if self.network_host:
                ip = serveur.Serveur().get_ip()
                self.player_instance = client.Player()
                self.player_instance.start(ip)
                self.__network_player = self.player_instance.client_receive()

            elif clients != False:
                code = clients
                ip = serveur.Serveur().get_ip()
                ip = ip.split(".")
                ip[-1] = code
                ip = ".".join(ip)
                self.player_instance = client.Player()
                self.player_instance.start(ip)
                self.__network_player = self.player_instance.client_receive()
        self.bank(number_of_barrier)
        if self.__save == 1:
            self.load_save()
        self.game_board()

    def set_first_grid(self):
        # -------------------------
        # permet de set la grille au lancement du jeu
        # va placer les pions et ajuster la taille du plateau selon
        # la variable self.__size_board
        # -------------------------
        for i in range(0, self.__size_board * 2, 2):
            self.__grid.append([])
            self.__grid.append([])
            for j in range(self.__size_board):
                self.__grid[i].append(case_pawn())
                self.__grid[i].append(case_barrier())
                self.__grid[i + 1].append(case_barrier())
                self.__grid[i + 1].append(case_barrier(True))
            self.__grid[i].pop()
            self.__grid[i + 1].pop()
        self.__grid.pop()

    def depth_first_search(self, start_node):
        stack = [(start_node, None)]  # Utilisation d'une pile pour stocker les noeuds à visiter
        visited = set()

        while stack:
            current_node, prev_node = stack.pop()

            # Vérifier si le noeud actuel a déjà été visité
            if current_node in visited:
                continue

            # Marquer le nœud actuel comme visité
            visited.add(current_node)

            # Parcourir les voisins du noeud actuel
            for neighbor in self.get_neighbors(current_node):
                # Vérifier si le voisin n'a pas été visité
                if neighbor not in visited:
                    # Vérifier si le voisin est bloqué par une barrière
                    if self.is_blocked_by_barrier(current_node, neighbor, prev_node):
                        continue

                    # Ajouter le voisin à la pile pour le visiter ultérieurement
                    stack.append((neighbor, current_node))

        # Retourner l'ensemble des noeuds visités
        return visited

    def is_blocked_by_barrier(self, current_node, neighbor, prev_node):
        row_diff = neighbor[0] - current_node[0]
        col_diff = neighbor[1] - current_node[1]
        barrier_node = (current_node[0] + row_diff // 2, current_node[1] + col_diff // 2)

        # Vérifier si le voisin est bloqué par une barrière
        if self.__grid[barrier_node[0]][barrier_node[1]].get_barrier():
            # Vérifier si le voisin est adjacent au noeud précédent (pas de saut de pion)
            if prev_node and neighbor != prev_node:
                return True
            # Vérifier si le voisin est sauté par-dessus une barrière (pas de passage par-dessus)
            if self.__grid[current_node[0]][current_node[1]].get_pawn():
                return True

        return False

    def get_neighbors(self, node):
        row, col = node
        size = len(self.__grid)

        # Coordonnées des voisins (haut, bas, gauche, droite)
        neighbors = [(row - 2, col), (row + 2, col), (row, col - 2), (row, col + 2)]

        # Filtrer les voisins pour s'assurer qu'ils sont dans les limites de la grille
        neighbors = [(r, c) for r, c in neighbors if 0 <= r < size and 0 <= c < size]

        return neighbors

    def bank(self, number_barrier):
        # -------------------------
        # permet de set la variable self.__bank qui est
        # un dictionnaire de valeurs clés : couleur du joueur
        # valeur = chiffre int en valeur de barrière dans la banque du joueur
        # la fonction est adapter pour 2 ou 4 joueur grâce a la variable
        # self.__number_of_player
        # -------------------------
        if self.__number_of_player == 4:
            number_barrier = number_barrier // 4
            self.__bank = {"blue": number_barrier, "red": number_barrier, "green": number_barrier,
                           "yellow": number_barrier}
        else:
            number_barrier = number_barrier // 2
            self.__bank = {"blue": number_barrier, "red": number_barrier}

    def barrier_placement(self, x, y):
        # -------------------------
        # permet de placer dans la grille 2 barrières selon les coordonnées
        # X et Y fournies, va les placer à la verticale ou à l'horizontale selon
        # Y (pair ou non)
        # puis va retirer 1 barrière de la banque du joueur en cours
        # -------------------------
        sound_barrier = (ressouce_path("require/user_interface/son/barrier.mp3"))
        self.__grid[x][y] = case_barrier(True)
        if y % 2 == 0:
            self.__grid[x][y + 2] = case_barrier(True)
        else:
            self.__grid[x + 2][y] = case_barrier(True)
        self.__bank[case_pawn(False, self.__current_player).color()] -= 1
        self.__previousBarrierCoordinates.append([(x, y), (x, y + 2)] if y % 2 == 0 else [(x, y), (x + 2, y)])
        self.__previousActionType.append("barrier")
        sound_thread_barriere = threading.Thread(target=self.play_barrier, args=(sound_barrier,))
        sound_thread_barriere.start()

    def barrier_verification(self, x, y):
        # -------------------------
        # va verifier si les coordonnées fournies sont acceptables pour
        # poser une barrière, va verifier le contenu en banque
        # puis regarde la direction pour que le placement ne soit pas
        # à la limite du plateau et enfin verifie la 2eme barrière
        # -------------------------

        # verifie si ba barriere est posisionner vertical ou horizontal
        if y % 2 == 0:  # pair donc vertical sinon horizontal
            directions = "horizontal"
        else:
            directions = "vertical"

        if self.__bank[case_pawn(False, self.__current_player).color()] > 0:
            if self.__size_board * 2 - 2 in (
                    x, y):  # verifie que le joueur n'est pas cliquer dans les case tout en bas ou tout a droite
                print("false derniere ligne")
                return False
            if self.__grid[y][x].get_barrier() == 0:  # si la position donner est vide alors on passe a la suite
                if directions == "horizontal":
                    return self.__grid[y + 2][
                        x].get_barrier() == 0  # vérifie 2 case apres si elle est vide (car le coin compte comme une
                    # case)
                else:
                    return self.__grid[y][
                        x + 2].get_barrier() == 0  # vérifie 2 case en dessous si elle est vide (car le coin compte
                    # comme une case)
        else:
            print("false bank")
            return False

    def pawn_verification(self, x, y):
        # ----------------------------------
        # pawn vérification
        # va vérifier si les coordonnées fournies sont acceptables pour
        # poser un pion selon les règles du jeu et le joueur en cours
        # crée les variables des coordonnées des positions possibles ainsi que les barrières possibles
        # vérifie selon la coordonnée qu'aucune barrière n'entrave son chemin
        # va vérifier si le saut de joueur et possible en prenant en compte les barrières
        # va appeler une fonction supplémentaire pour vérifier les diagonales
        # ----------------------------------

        co = [self.__pawn_coordinate[case_pawn(False, self.__current_player).color()][0],
              self.__pawn_coordinate[case_pawn(False, self.__current_player).color()][1]]
        possibleCase = (
            [0, 2], [2, 0], [0, -2], [-2, 0], [-2, 2], [2, 2], [2, -2], [-2, -2], [0, 4], [4, 0], [0, -4], [-4, 0])
        possible_case_barrier = ([0, 1], [1, 0], [0, -1], [-1, 0], [0, 3], [3, 0], [0, -3], [-3, 0])
        case = [co[0] - y, co[1] - x]

        if case in possibleCase:
            index = possibleCase.index(case)
            if not self.__grid[y][x].get_pawn():

                if index <= 3:  # vérification des 4 case proche N S E W
                    if not self.__grid[co[0] - possible_case_barrier[index][0]][
                        co[1] - possible_case_barrier[index][1]].get_barrier():
                        return True

                elif index > 7:  # vérification du saut de joueur
                    if not self.__grid[co[0] - possible_case_barrier[index - 8][0]][
                        co[1] - possible_case_barrier[index - 8][1]].get_barrier():
                        if self.__grid[co[0] - possibleCase[index - 8][0]][
                            co[1] - possibleCase[index - 8][1]].get_pawn():
                            if not self.__grid[co[0] - possible_case_barrier[index - 4][0]][
                                co[1] - possible_case_barrier[index - 4][1]].get_barrier():
                                return True

                else:  # vérification diagonales
                    return self.pawn_verification_diagonal(index) == True
        return False

    def pawn_verification_diagonal(self, direction):
        # ----------------------------------
        # aide pour pawnVerification
        # fonction qui permet de vérifier les possibilités de diagonale
        # selon l'indice donner la direction NE SE SO NO
        # puis va 2 vérifications pour savoirs quel pion est normalement passable
        # va vérifier selon ce dernier si des barrières n'entravent pas le chemin
        # ----------------------------------
        co = [self.__pawn_coordinate[case_pawn(False, self.__current_player).color()][0],
              self.__pawn_coordinate[case_pawn(False, self.__current_player).color()][1]]
        nord, sud, est, ouest = False, False, False, False
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
            if not self.__grid[co[0] - 1][co[1]].get_barrier():
                if self.__grid[co[0] - 2][co[1]].get_pawn():
                    if co[0] == 2:
                        pass
                    elif self.__grid[co[0] - 3][co[1]].get_barrier() == True or self.__grid[co[0] - 4][
                        co[1]].get_pawn() == True:
                        nord = True
        else:
            if not self.__grid[co[0] + 1][co[1]].get_barrier():
                if self.__grid[co[0] + 2][co[1]].get_pawn():
                    if co[0] == len(self.__grid) - 3:
                        pass
                    elif self.__grid[co[0] + 3][co[1]].get_barrier() == True or self.__grid[co[0] + 4][
                        co[1]].get_pawn() == True:
                        sud = True

        if check2 == "est":
            if not self.__grid[co[0]][co[1] + 1].get_barrier():
                if self.__grid[co[0]][co[1] + 2].get_pawn():
                    if co[1] == len(self.__grid) - 3:
                        pass
                    elif self.__grid[co[0]][co[1] + 3].get_barrier() == True or self.__grid[co[0]][
                        co[1] + 4].get_pawn() == True:
                        est = True
        else:
            if not self.__grid[co[0]][co[1] - 1].get_barrier():
                if self.__grid[co[0]][co[1] - 2].get_pawn():
                    if co[1] == 2:
                        pass
                    elif self.__grid[co[0]][co[1] - 3].get_barrier() == True or self.__grid[co[0]][
                        co[1] - 4].get_pawn() == True:
                        ouest = True
        if direction == 6:
            if nord:
                if not self.__grid[co[0] - 2][co[1] + 1].get_barrier():
                    return True
            if est:
                if not self.__grid[co[0] - 1][co[1] + 2].get_barrier():
                    return True
        elif direction == 7:
            if sud:
                if not self.__grid[co[0] + 2][co[1] + 1].get_barrier():
                    return True
            if est:
                if not self.__grid[co[0] + 1][co[1] + 2].get_barrier():
                    return True
        elif direction == 4:
            if sud:
                if not self.__grid[co[0] + 2][co[1] - 1].get_barrier():
                    return True
            if ouest:
                if not self.__grid[co[0] + 1][co[1] - 2].get_barrier():
                    return True
        else:
            if nord:
                if not self.__grid[co[0] - 2][co[1] - 1].get_barrier():
                    return True
            if ouest:
                if not self.__grid[co[0] - 1][co[1] - 2].get_barrier():
                    return True
        return False

    def set__pawn_coordinate(self):
        # -------------------------
        # va set la variable self.__pawn_coordinate : un dictionnaire qui en clé la couleur du joueur
        # et en valeur ses coordonnées sous forme de liste
        # la fonction est adaptée si les joueurs sont 2 ou 4
        # -------------------------
        self.__pawn_coordinate = {"blue": [self.__size_board * 2 - 2, self.__size_board - 1]
            , "red": [0, self.__size_board - 1], }

        self.__grid[self.__size_board * 2 - 2][self.__size_board - 1] = case_pawn(True, 1)
        self.__grid[0][self.__size_board - 1] = case_pawn(True, 2)

        if self.__number_of_player == 4:
            self.__pawn_coordinate["green"] = [self.__size_board - 1, 0]
            self.__pawn_coordinate["yellow"] = [self.__size_board - 1, self.__size_board * 2 - 2]

            self.__grid[self.__size_board - 1][0] = case_pawn(True, 3)
            self.__grid[self.__size_board - 1][self.__size_board * 2 - 2] = case_pawn(True, 4)

    def pawn_placement(self, x, y):
        # -------------------------
        # permet de placer dans la grille 1 pion selon les coordonnées
        # X et Y fournies
        # puis va modifier la variable self.__pawn_coordinate pour l'adapter
        # -------------------------
        sound_moove = ressouce_path("require/user_interface/son/pawn.mp3")
        self.__previousPawnCoordinates.append(dict(self.__pawn_coordinate))
        self.__grid[x][y] = case_pawn(True, self.__current_player)
        self.__grid[self.__pawn_coordinate[case_pawn(False, self.__current_player).color()][0]][
            self.__pawn_coordinate[case_pawn(False, self.__current_player).color()][1]] = case_pawn(False, 0)
        self.__pawn_coordinate[case_pawn(False, self.__current_player).color()] = [x, y]
        self.__previousActionType.append("pawn")
        sound_thread_moove = threading.Thread(target=self.play_pop, args=(sound_moove,))
        sound_thread_moove.start()

    def barrier_del(self, x, y):
        self.__grid[x][y] = case_barrier(False)
        if y % 2 == 0:
            self.__grid[x][y + 2] = case_barrier(False)
        else:
            self.__grid[x + 2][y] = case_barrier(False)
        self.__bank[case_pawn(False, self.__current_player).color()] += 1
        self.__previousBarrierCoordinates.pop(-1)

    def get_color_number(self, color):
        # Cette méthode renvoie le numéro correspondant à la couleur du joueur
        if color == "blue":
            return 1
        elif color == "red":
            return 2
        elif color == "green":
            return 3
        elif color == "yellow":
            return 4
        else:
            return 0

    def back(self):
        if len(self.__previousActionType) == 0:
            pass
        else:
            if self.__computer == 0:
                last_action_type = self.__previousActionType.pop()

                if last_action_type == "pawn":
                    previous_pawn_coordinates = self.__previousPawnCoordinates.pop()
                    for color, coordinates in self.__pawn_coordinate.items():
                        if color in previous_pawn_coordinates:
                            x, y = coordinates
                            self.__grid[x][y] = case_pawn(False, 0)  # Remplace la case par une case vide
                            prev_x, prev_y = previous_pawn_coordinates[color]
                            self.__grid[prev_x][prev_y] = case_pawn(True, self.get_color_number(
                                color))  # Restaure la case précédente
                    self.__pawn_coordinate = previous_pawn_coordinates

                elif last_action_type == "barrier":
                    previous_barrier_coordinates = self.__previousBarrierCoordinates.pop()
                    for coordinates in previous_barrier_coordinates:
                        x, y = coordinates
                        self.__grid[x][y] = case_barrier(False)  # Remplace la case par une case vide
                    self.__barrier_coordinate = previous_barrier_coordinates

                if self.__current_player > 1:
                    self.__current_player -= 1
                    if last_action_type == "barrier":
                        self.__bank[case_pawn(False, self.__current_player).color()] += 1
                else:
                    self.__current_player = self.__number_of_player
                    if last_action_type == "barrier":
                        self.__bank[case_pawn(False, self.__current_player).color()] += 1

            if self.__computer == 1:
                for i in range(2):
                    last_action_type = self.__previousActionType.pop()

                    if last_action_type == "pawn":
                        previous_pawn_coordinates = self.__previousPawnCoordinates.pop()
                        for color, coordinates in self.__pawnCoordinate.items():
                            if color in previous_pawn_coordinates:
                                x, y = coordinates
                                self.__grid[x][y] = case_pawn(False, 0)  # Remplace la case par une case vide
                                prev_x, prev_y = previous_pawn_coordinates[color]
                                self.__grid[prev_x][prev_y] = case_pawn(True, self.get_color_number(
                                    color))  # Restaure la case précédente
                        self.__pawnCoordinate = previous_pawn_coordinates

                    elif last_action_type == "barrier":
                        previous_barrier_coordinates = self.__previousBarrierCoordinates.pop()
                        for coordinates in previous_barrier_coordinates:
                            x, y = coordinates
                            self.__grid[x][y] = case_barrier(False)  # Remplace la case par une case vide
                        self.__barrierCoordinate = previous_barrier_coordinates

                    if self.__current_player > 1:
                        self.__current_player -= 1
                        if last_action_type == "barrier":
                            self.__bank[case_pawn(False, self.__current_player).color()] += 1
                    else:
                        self.__current_player = self.__number_of_player
                        if last_action_type == "barrier":
                            self.__bank[case_pawn(False, self.__current_player).color()] += 1

    def game_board(self):
        # -------------------------
        # lance la fenetre principal du programe en pygame
        # -------------------------
        # Fenêtre du plateau du jeu
        pygame.init()
        windowSize = (1920, 1080)
        pygame.display.set_caption("QUORIDOR")
        self.__on_screen_surface = pygame.display.set_mode(windowSize, pygame.FULLSCREEN | pygame.RESIZABLE)
        size = self.__size_board * 75 - 25

        mixer.init()
        sound_background = ressouce_path("require/user_interface/son/bg.mp3")
        sound_thread_background = threading.Thread(target=self.play_sound, args=(sound_background,))
        sound_thread_background .start()

        # Surface du plateau
        tableSurfaceSize = ((self.__size_board * 75) - 25, (self.__size_board * 75) - 25)
        self.__tableSurface = pygame.Surface(tableSurfaceSize)
        x = (windowSize[0] - tableSurfaceSize[0]) / 2
        y = (windowSize[1] - tableSurfaceSize[1]) / 2
        self.__on_screen_surface.blit(self.__tableSurface, (x, y))

        # Attendez pour fermer la fenêtre
        self.__running = True
        while self.__running:
            if int(self.__network_player) == self.__current_player or self.__network == False:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__running = False

                    if event.type == pygame.VIDEORESIZE:
                        windowSize = event.size
                        self.__on_screen_surface = pygame.display.set_mode(windowSize, pygame.RESIZABLE)
                        x = (windowSize[0] - tableSurfaceSize[0]) / 2
                        y = (windowSize[1] - tableSurfaceSize[1]) / 2
                        self.__on_screen_surface.blit(self.__tableSurface, (x, y))
                        pygame.display.update()

                    clicx = pygame.mouse.get_pos()[0]
                    clicy = (pygame.mouse.get_pos()[1]) - 100
                    if x <= clicx <= x + size:
                        if y <= clicy <= y + size:
                            caseX = (clicx - x) / 75
                            caseY = ((clicy - y) / 75)
                            caseFinalX = self.case_clicked(caseX, caseY)[0]
                            caseFinalY = self.case_clicked(caseX, caseY)[1]

                            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] == True:
                                self.game_turn(caseFinalX, caseFinalY)
                                if self.__network:
                                    message = f"{caseFinalX},{caseFinalY}"
                                    print("le message est : ", message)
                                    self.player_instance.client_send(message)
                                    self.display(x, y)

                                # --------parti computer------
                                if self.__computer == 1:
                                    self.case_computer()
            else:
                self.display(x, y)
                message = self.player_instance.client_receive()
                print(message)
                message = message.split(",")
                print(message)
                self.game_turn(int(message[0]), int(message[1]))

            self.display(x, y + 100)
            clock = pygame.time.Clock()
            clock.tick(30)
            self.hide_widgets()

    def case_computer(self):
        while self.__current_player == 2:
            result = 0
            caseX = random.randint(0, self.__size_board * 2 - 2)
            caseY = random.randint(0, self.__size_board * 2 - 2)

            if self.__bank["red"] != 0:
                deplacement = random.randint(0, 1)
            else:
                deplacement = 1

            if deplacement == 1:
                while result == 0 or self.pawn_verification(caseX, caseY) == False:
                    while caseX % 2 != 0:
                        caseX = random.randint(0, self.__size_board * 2 - 2)
                        while caseY % 2 != 0:
                            caseY = random.randint(0, self.__size_board * 2 - 2)
                    if self.pawn_verification(caseX, caseY):
                        result = 1
                    else:
                        caseX = random.randint(0, self.__size_board * 2 - 2)
                        caseY = random.randint(0, self.__size_board * 2 - 2)
            else:
                while result == 0 or self.barrier_verification(caseX, caseY) == False:
                    while caseX % 2 == 0 and caseY % 2 == 0:
                        caseX = random.randint(0, self.__size_board * 2 - 2)
                        caseY = random.randint(0, self.__size_board * 2 - 2)
                    if self.barrier_verification(caseX, caseY):
                        result = 1
                    else:
                        caseX = random.randint(0, self.__size_board * 2 - 2)
                        caseY = random.randint(0, self.__size_board * 2 - 2)
            self.game_turn(caseX, caseY)

    def verify_victory(self):
        # -------------------------
        # Condition de Victoire
        # -------------------------
        if self.__pawn_coordinate["blue"][0] == 0:
            self.__winner = "Blue"
            self.__game_state = "Win"
            return True
        elif self.__pawn_coordinate["red"][0] == self.__size_board * 2 - 2:
            self.__winner = "Red"
            self.__game_state = "Win"
            return True
        if self.__number_of_player == 4:
            if self.__pawn_coordinate["yellow"][1] == 0:
                self.__winner = "Yellow"
                self.__game_state = "Win"
                return True
            elif self.__pawn_coordinate["green"][1] == self.__size_board * 2 - 2:
                self.__winner = "Green"
                self.__game_state = "Win"
                return True
            else:
                return False
        else:
            return False

    def case_clicked(self, x, y):
        # -------------------------
        # permet depuis les coordonées de la souris de savoir quelle case du plateau est cliquée
        # -------------------------
        decimalX = math.floor(x)
        decimalY = math.floor(y)
        caseX = decimalX * 2
        caseY = decimalY * 2
        if (x - decimalX) > 0.6666:
            caseX += 1
        if (y - decimalY) > 0.6666:
            caseY += 1

        return caseX, caseY

    def game_turn(self, x, y):
        # -------------------------
        # permet de faire un tour de jeu depuis un clic
        # cette fonction se sert de presque toutes les autres fonctions du programme
        # -------------------------
        if x % 2 == 0 and y % 2 == 0:
            if self.pawn_verification(x, y):
                self.pawn_placement(y, x)
                self.change_player()
                self.verify_victory()
        else:
            if self.barrier_verification(x, y):
                self.barrier_placement(y, x)
                visited_nodes_blue = list(
                    self.depth_first_search((self.__pawn_coordinate["blue"][0], self.__pawn_coordinate["blue"][1])))
                visited_nodes_red = list(
                    self.depth_first_search((self.__pawn_coordinate["red"][0], self.__pawn_coordinate["red"][1])))
                if self.__number_of_player != 2:
                    visited_nodes_yellow = list(self.depth_first_search(
                        (self.__pawn_coordinate["yellow"][0], self.__pawn_coordinate["yellow"][1])))
                    visited_nodes_green = list(self.depth_first_search(
                        (self.__pawn_coordinate["green"][0], self.__pawn_coordinate["green"][1])))
                    if self.check_path(visited_nodes_blue, visited_nodes_red, visited_nodes_yellow,
                                       visited_nodes_green) == True:
                        self.change_player()
                        self.verify_victory()
                    else:
                        self.barrier_del(y, x)
                else:
                    if self.check_path(visited_nodes_blue, visited_nodes_red) == True:
                        self.change_player()
                        self.verify_victory()
                    else:
                        self.barrier_del(y, x)

    def check_path(self, blue, red, yellow=None, green=None):
        check_blue, check_red, check_yellow, check_green = False, False, False, False
        for i in range(len(blue)):
            if blue[i][0] == 0:
                check_blue = True
            else:
                pass

        for i in range(len(red)):
            if red[i][0] == self.__size_board * 2 - 2:
                check_red = True
            else:
                pass

        if yellow == None and green == None:
            return check_blue == True and check_red == True
        else:
            for i in range(len(yellow)):
                if yellow[i][1] == 0:
                    check_yellow = True
                else:
                    pass

            for i in range(len(green)):
                if green[i][1] == self.__size_board * 2 - 2:
                    check_green = True
                else:
                    pass
            return check_blue == True and check_red == True and check_yellow == True and check_green == True

    def change_player(self):
        # -------------------------
        # modifie la variable self.__current_player à chaque appel de la fonction
        # -------------------------
        self.__current_player += 1
        if self.__number_of_player == 4:
            if self.__current_player == 5:
                self.__current_player = 1
        else:
            if self.__current_player == 3:
                self.__current_player = 1

    def display(self, x, y):
        # -------------------------
        # cette fonction affiche le plateau selon la grille fournie
        # -------------------------

        pygame.init()
        load_font_files = ressouce_path("require/user_interface/fonts/Berlin_Sans_FB_Demi_Bold.ttf")
        font_interface__XXXL = pygame.font.Font(load_font_files, 130)
        font_interface__XL = pygame.font.Font(load_font_files, 70)
        font_interface__L = pygame.font.Font(load_font_files, 45)
        font_interface__M = pygame.font.Font(load_font_files, 20)

        background_image = pygame.image.load(ressouce_path("require/user_interface/images/background.jpg"))

        button_width = 300
        button_height = 100
        button_small_width = 200
        button_small_height = 100
        x_initial = 1500
        y_initial = 300
        x_small_inital = 50
        y_small_initial = 20
        space = 100
        zone_bank_size = (400, 340)
        border_radius = 2

        self.__tableSurface.fill(get_black())

        self.__zone_bank = pygame.Surface(zone_bank_size, pygame.SRCALPHA)
        pygame.draw.rect(self.__zone_bank, get_blue_wp(), pygame.Rect(0, 0, *zone_bank_size))
        pygame.draw.rect(self.__zone_bank, get_black(), pygame.Rect(0, 0, *zone_bank_size), border_radius)

        self.__button_save = Button(
            self.__on_screen_surface, x_initial, y_initial, button_width, button_height, text='Save',
            margin=25,
            textColour=get_black(),
            inactiveColour=get_violet(),
            radius=5,
            font=font_interface__L,
            textVAlign='center',
            onClick=lambda: (self.save())
        )

        self.__button_rect_load = Button(
            self.__on_screen_surface, x_initial, y_initial + (button_height + space), button_width,
            button_height,
            text='Load',
            margin=25,
            textColour=get_black(),
            inactiveColour=get_violet(),
            radius=5,
            font=font_interface__L,
            textVAlign='center',
            onClick=lambda: (self.load_save())
        )

        self.__button_back = Button(
            self.__on_screen_surface, x_initial, y_initial + 2 * (button_height + space), button_width,
            button_height,
            text='Back',
            margin=25,
            textColour=get_black(),
            inactiveColour=get_violet(),
            radius=5,
            font=font_interface__L,
            textVAlign='center',
            onClick=lambda: (self.back())
        )

        self.__button_mute = Button(
            self.__on_screen_surface, x_initial, y_initial + 3 * (button_height + space), button_width,
            button_height,
            text='Mute',
            margin=25,
            textColour=get_black(),
            inactiveColour=get_violet(),
            radius=5,
            font=font_interface__L,
            textVAlign='center',
            onClick=lambda: (self.mute())
        )

        self.__button_back_window = Button(
            self.__on_screen_surface, x_small_inital, y_small_initial, button_small_width,
            button_small_height,
            text='Back',
            margin=25,
            textColour=get_black(),
            inactiveColour=get_red(),
            radius=5,
            font=font_interface__L,
            textVAlign='center',
            onClick=lambda: (self.back_window())
        )

        self.__button_settings = Button(
            self.__on_screen_surface, x_small_inital + 1630, y_small_initial, button_small_width,
            button_small_height,
            text='Settings',
            margin=25,
            textColour=get_black(),
            inactiveColour=get_red(),
            radius=5,
            font=font_interface__L,
            textVAlign='center',
            onClick=lambda: (self.open_settings())
        )

        for i in range(len(self.__grid)):
            for j in range(len(self.__grid) // 2 + 1):

                if i % 2 == 0:  # si la ligne est paire on va placer une case pion puis une case barrier vertical

                    if self.__grid[i][j * 2].get_pawn():
                        if self.__grid[i][j * 2].get_player() == 1:
                            pygame.draw.rect(self.__tableSurface, get_blue(), pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                        elif self.__grid[i][j * 2].get_player() == 2:
                            pygame.draw.rect(self.__tableSurface, get_red(), pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                        elif self.__grid[i][j * 2].get_player() == 3:
                            pygame.draw.rect(self.__tableSurface, get_green(),
                                             pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                        elif self.__grid[i][j * 2].get_player() == 4:
                            pygame.draw.rect(self.__tableSurface, get_yellow(),
                                             pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                    else:
                        if self.pawn_verification(j * 2, i):
                            if self.__current_player == 1:
                                pygame.draw.rect(self.__tableSurface, get_light_grey(),
                                                 pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                            elif self.__current_player == 2:
                                pygame.draw.rect(self.__tableSurface, get_light_grey(),
                                                 pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                            elif self.__current_player == 3:
                                pygame.draw.rect(self.__tableSurface, get_light_grey(),
                                                 pygame.Rect(j * 75, i / 2 * 75, 50, 50))
                            elif self.__current_player == 4:
                                pygame.draw.rect(self.__tableSurface, get_light_grey(),
                                                 pygame.Rect(j * 75, i / 2 * 75, 50, 50))

                        else:
                            pygame.draw.rect(self.__tableSurface, get_green_wp(),
                                             pygame.Rect(j * 75, i / 2 * 75, 50, 50))

                    if j != len(self.__grid) // 2:
                        if self.__grid[i][j * 2 + 1].get_barrier():
                            pygame.draw.rect(self.__tableSurface, get_dark_violet(),
                                             pygame.Rect(j * 75 + 50, i / 2 * 75, 25, 50))
                        else:
                            pygame.draw.rect(self.__tableSurface, get_blue_cyan(),
                                             pygame.Rect(j * 75 + 50, i / 2 * 75, 25, 50))

                else:
                    if self.__grid[i][j * 2].get_barrier():
                        pygame.draw.rect(self.__tableSurface, get_dark_violet(),
                                         pygame.Rect(j * 75, i / 2 * 75 + 12.5, 50, 25))
                    else:
                        pygame.draw.rect(self.__tableSurface, get_blue_cyan(),
                                         pygame.Rect(j * 75, i / 2 * 75 + 12.5, 50, 25))
                    if j != len(self.__grid) // 2:
                        pygame.draw.rect(self.__tableSurface, get_dark_violet(),
                                         pygame.Rect(j * 75 + 50, i / 2 * 75 + 12.5, 25, 25))

        title_text = font_interface__XL.render("Zone Bank", True, get_white())
        title_text_outline = font_interface__XL.render("Zone Bank", True, get_black())
        self.__zone_bank.blit(title_text_outline, (33 + 2, 20 + 2))
        self.__zone_bank.blit(title_text, (33, 20))

        for i in range(1, self.__number_of_player + 1):
            text = str(case_pawn(False, i).color()).capitalize() + " player " + "have " + str(
                self.__bank[case_pawn(False, i).color()]) + " barrier"
            text_surface = font_interface__M.render(text, True, get_white())
            self.__zone_bank.blit(text_surface, (50, 80 + (i * 50)))

        self.__zone_current_player = Button(
            self.__on_screen_surface, 100, 720, button_width + 50, button_height,
            text='Current Player',
            margin=25,
            textColour=get_white(),
            inactiveColour=case_pawn(False, self.__current_player).color(),
            pressedColour=get_white(),
            radius=5,
            font=font_interface__L,
            textVAlign='bottom'
        )

        zone_title_size = (1000, 250)
        self.__zone_title = pygame.Surface(zone_title_size, pygame.SRCALPHA)
        title_board = font_interface__XXXL.render("Game Board", True, get_white())
        title_board_outline = font_interface__XXXL.render("Game Board", True, get_black())
        self.__zone_title.blit(title_board_outline, (0 + 2, 0 + 2))
        self.__zone_title.blit(title_board, (0, 0))

        # Update game state
        if self.__game_state == "Launch":
            self.stop_music()
            self.__on_screen_surface.fill(get_blue_cyan())
            self.hide_widgets()
            launch.Launch().display()

        elif self.__game_state == "Settings":
            self.stop_music()
            self.__on_screen_surface.fill(get_blue_cyan())
            self.hide_widgets()
            settings.Settings().display()

        elif self.__game_state == "Win":
            self.stop_music()
            self.__on_screen_surface.fill(get_blue_cyan())
            self.hide_widgets()
            win.Win(self.__winner).display()

        else:
            self.__on_screen_surface.blit(background_image, (0, 0))
            self.__on_screen_surface.blit(self.__tableSurface, (x, y))
            self.__on_screen_surface.blit(self.__zone_bank, (75, 300))
            self.__on_screen_surface.blit(self.__zone_title, (594, 20))
            self.show_widgets()

        pygame_widgets.update(pygame.event.get())
        pygame.display.update()

        pygame.display.flip()

    def back_window(self):
        self.__game_state = "Launch"

    def open_settings(self):
        self.__game_state = "Settings"

    def hide_widgets(self):
        # Masquez tous les widgets en appelant leur méthode hide()
        self.__button_save.hide()
        self.__button_rect_load.hide()
        self.__button_back.hide()
        self.__button_mute.hide()
        self.__button_back_window.hide()
        self.__button_settings.hide()
        self.__zone_current_player.hide()

    def show_widgets(self):
        # Masquez tous les widgets en appelant leur méthode hide()
        self.__button_save.show()
        self.__button_rect_load.show()
        self.__button_back.show()
        self.__button_mute.show()
        self.__button_back_window.show()
        self.__button_settings.show()
        self.__zone_current_player.show()

    def play_pop(self, filename):
        mixer.init()
        sound = mixer.Sound(filename)
        sound.play()

    def play_barrier(self, filename):
        mixer.init()
        sound = mixer.Sound(filename)
        sound.play()

    def play_sound(self, filename):
        mixer.init()
        mixer.music.load(filename)
        mixer.music.set_volume(self.__volume)
        mixer.music.play(-1)

    def mute(self):
        if self.__cpt == 0:
            pygame.mixer.music.pause()
            self.__cpt += 1
        elif self.__cpt == 1:
            pygame.mixer.music.unpause()
            self.__cpt -= 1

    def stop_music(self):
        pygame.mixer.music.stop()

    def save(self):
        save = Path(__file__).parent / "save.txt"
        conditionFichier = False
        try:
            open(save, 'w')
            conditionFichier = True
        except:
            print("erreur save")
            conditionFichier = False

        if conditionFichier:
            save = open(save, 'w')
            for i in range(len(self.__grid)):
                for j in range(len(self.__grid)):
                    if i % 2 == 0 and j % 2 == 0:
                        save.write(f"{self.__grid[j][i].get_player()}")
                    else:
                        if self.__grid[j][i].get_barrier():
                            save.write("T")
                        else:
                            save.write("F")
            save.write(
                f"\n{self.__number_of_player}\n{self.__current_player}\n{self.__pawn_coordinate}\n{self.__game_turns}\n{self.__bank}\n{self.__computer}\n{self.__size_board}")

            save.close()

    def load_save(self):
        save = Path(__file__).parent / "save.txt"
        conditionFichier = False
        try:
            open(save, 'r')
            conditionFichier = True
        except:
            conditionFichier = False
        if conditionFichier:
            save = open(save, 'r')
            content = save.readlines()
            varGrille = (content[0])
            self.__number_of_player = int(content[1])
            self.__current_player = int(content[2])
            self.__pawn_coordinate = eval((content[3]))
            self.__game_turns = int(content[4])
            self.__bank = eval(content[5])
            self.__computer = int(content[6])
            self.__size_board = int(content[7])
            save.close()
            incremente = 0
            self.__grid = []
            number = "012345"
            for i in range(self.__size_board * 2 - 1):
                self.__grid.append([])
            for i in range(self.__size_board * 2 - 1):
                for j in range(self.__size_board * 2 - 1):
                    if varGrille[incremente] in number:
                        if varGrille[incremente] == "0":
                            self.__grid[j].append(case_pawn(False, 0))
                        else:
                            self.__grid[j].append(case_pawn(True, eval(varGrille[incremente])))
                    else:
                        if varGrille[incremente] == "F":
                            self.__grid[j].append(case_barrier(False))
                        else:
                            self.__grid[j].append(case_barrier(True))
                    incremente += 1

            print(self.__pawn_coordinate, type(self.__pawn_coordinate))
