import threading
import socket

class serveur:

    def start(self):
        host = self.getIp()
        port = 5566
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((host, port))
        self.__server.listen()
        self.__clients = []
        self.receive()


    def getClients(self):
        return self.__clients


    def broadcast(self,message):
        for client in self.__clients:
            print("j'envoie le message : ",message)
            client.send(message.encode('utf-8'))

    # Function to handle clients'connections


    def handle_client(self,client):
        while True:
            try:
                message_bytes = client.recv(1024)
                message = message_bytes.decode('utf-8')
                print("jai recut le message : ",message)
                self.broadcast(message)
            except:
                self.__clients.remove(client)
                client.close()
                break
    # Main function to receive the clients connection


    def receive(self):
        while True:
            print('Server is running and listening ...')
            client, address = self.__server.accept()
            print(f'connection is established with {str(address)}')
            self.__clients.append(client)
            client.send(str(len(self.__clients)).encode('utf-8'))
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


    def getIp(self):
        ip = socket.gethostbyname_ex(socket.gethostname())[-1]
        return(ip[-1])

    def getCode(self):
        code = self.getIp()
        code = code.split(".")
        return(code[-1])

if __name__ == "__main__":
    serveur().start()