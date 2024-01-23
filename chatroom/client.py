import socket
import threading

from logger import Logger


class ChatroomClient:
    __slots__ = ("logger", "host", "port", "socket", "buffer_size", "keep_running")

    def __init__(self, host: str, port: int):
        self.logger = Logger("ChatroomClient").get()
        self.host = host
        self.port = port
        self.socket = None
        self.buffer_size = 1024
        self.keep_running = True

    def start(self) -> None:
        self.socket = socket.create_connection((self.host, self.port))
        self.logger.info(f"Connected to the server running on {self.host}:{self.port}")

        input_thread = threading.Thread(target=self._receive_data)
        input_thread.start()

        while self.keep_running:
            try:
                msg = input().strip()
                self._send_data(msg)
            except KeyboardInterrupt:
                self.keep_running = False

        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        input_thread.join()

    def _send_data(self, message: str) -> None:
        self.socket.sendall(message.encode())

    def _receive_data(self) -> None:
        while self.keep_running:
            try:
                message = self.socket.recv(self.buffer_size)
                print(message.decode())
            except (Exception,) as e:
                self.logger.error(f"Exception while receiving message: {e}", exc_info=True)


def main() -> None:
    server_port = int(input("Server port: "))
    chat_client = ChatroomClient(socket.gethostname(), server_port)
    chat_client.start()


if __name__ == "__main__":
    main()
