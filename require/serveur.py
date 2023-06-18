import threading
import socket

class Serveur:

    def start(self):
        # Fonction de lancement du serveur elle recupère l'IP wifi de l'utilisateur pour initialiser un serveur qui communique sur le port 5566
        host = self.get_ip()
        port = 5566
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((host, port))
        self.__server.listen()
        self.__clients = []
        self.receive()


    def get_clients(self):
        return self.__clients


    def broadcast(self,message):
        # Fonction qui permet une redistribution broadcast des packets récupérer
        for client in self.__clients:
            client.send(message.encode('utf-8'))


    def handle_client(self,client):
        # Fonction qui permet de recevoir des packets client
        while True:
            try:
                message_bytes = client.recv(1024)
                message = message_bytes.decode('utf-8')
                self.broadcast(message)
            except:
                self.__clients.remove(client)
                client.close()
                break

    def receive(self):
        # Fonction qui permet de recevoire et d'autoriser les connections client ainsi que de les stocker
        while True:
            client, address = self.__server.accept()
            self.__clients.append(client)
            client.send(str(len(self.__clients)).encode('utf-8'))
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


    def get_ip(self):
        # Fonction qui retourne l'IP de l'utilisateur sur le réseau wifi
        ip = socket.gethostbyname_ex(socket.gethostname())[-1]
        return(ip[-1])

    def get_code(self):
        # Fonction qui retourne les 3 derniers chiffres de l'IP wifi de l'utilisateur
        code = self.get_ip()
        code = code.split(".")
        return(code[-1])

if __name__ == "__main__":
    Serveur().start()