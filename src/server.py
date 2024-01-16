import socket
import logging
import threading


class ChatServer:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("ChatServer")

        self.clients = []
        self.clients_lock = threading.Lock()
        self.buffer_size = 1024

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host, self.port = socket.gethostname(), 12345
        self.socket.bind((self.host, self.port))
        self.socket.listen()

        self.logger.info(f"Server started on {self.host}:{self.port}")

    def start(self) -> None:
        while True:
            client, address = self.socket.accept()
            self.logger.info(f"Connection from {address} has been established!")

            with self.clients_lock:
                self.clients.append(client)

            thread = threading.Thread(target=self._handle_client, args=(client,))
            thread.start()

    def _remove_client(self, client: socket.socket) -> None:
        with self.clients_lock:
            client.close()
            self.clients.remove(client)

    def _broadcast(self, message: bytes, sender: socket.socket) -> None:
        for client in self.clients:
            if client != sender:
                try:
                    client.sendall(message)
                except (Exception,) as e:
                    self.logger.error(f"Exception while broadcasting message: {e}")
                    self._remove_client(client)

    def _handle_client(self, client: socket.socket) -> None:
        while True:
            try:
                if not (message := client.recv(self.buffer_size)):
                    break
                self._broadcast(message, client)
            except (Exception,) as e:
                self.logger.error(f"Exception while handling client: {e}")
                self._remove_client(client)


if __name__ == "__main__":
    chat_server = ChatServer()
    chat_server.start()
