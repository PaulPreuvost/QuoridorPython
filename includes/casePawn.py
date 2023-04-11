class casePawn:
    #Cette classe permet de retourner s'il y a un pion et la couleur du joueur possède ce pion
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