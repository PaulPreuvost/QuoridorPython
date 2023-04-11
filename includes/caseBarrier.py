class caseBarrier:
    #Cette classe permet de retourner s'il y a une barrière
    def __init__(self, barrier = False):
        self.__barrier = barrier

    def getBarrier(self):
        return self.__barrier

    def setBarrier(self, x):
        self.__barrier = x