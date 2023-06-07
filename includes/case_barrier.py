class case_barrier:
    #Cette classe permet de retourner s'il y a une barrière
    def __init__(self, barrier=False):
        self.__barrier = barrier

    def get_barrier(self):
        return self.__barrier

    def set_barrier(self, x):
        self.__barrier = x