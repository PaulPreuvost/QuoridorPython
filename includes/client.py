import socket


class Player:
    def start(self, ip):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((ip, 5566))

        # receive_thread = threading.Thread(target=lambda: self.client_receive())
        # receive_thread.start()

    def client_receive(self):
        while True:
            try:
                message_bytes = self.__client.recv(1024)
                message = message_bytes.decode('utf-8')
                print("ducoup j'ai recut : ", message)
                return message
            except:
                print('Error!')
                self.__client.close()
                break

    def client_send(self, message):
        print("le message est toujours : ", message)
        self.__client.send(message.encode('utf-8'))


if __name__ == "__main__":
    Player("192.168.43.88")