import socket

class Player:
    
    def start(self, ip):
        # Cette fonction prend en paramêtre une IP afin de pouvoir se connecter au serveur sur le port 5566
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((ip, 5566))

    def client_receive(self):
        # Fonction qui permet de décoder et recevoir des paquets / fermer la connexion client
        while True:
            try:
                message_bytes = self.__client.recv(1024)
                message = message_bytes.decode('utf-8')
                return message
            except:
                self.__client.close()
                break

    def client_send(self, message):
        # Permet d'envoyer un message simple au serveur
        self.__client.send(message.encode('utf-8'))


if __name__ == "__main__":
    Player("192.168.43.88")