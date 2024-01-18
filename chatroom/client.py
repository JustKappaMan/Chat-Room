import socket
import threading

from logger import Logger


class ChatClient:
    def __init__(self, host: str, port: int) -> None:
        self.logger = Logger("ChatClient").get()

        self.buffer_size = 1024
        self.keep_running = True

        self.socket = socket.create_connection((host, port))

        self.logger.info(f"Connected to the server running on {host}:{port}")

    def start(self) -> None:
        input_thread = threading.Thread(target=self._receive_messages)
        input_thread.start()

        while self.keep_running:
            try:
                msg = input().strip()
                self._send_message(msg)
            except KeyboardInterrupt:
                self.keep_running = False

        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        input_thread.join()

    def _send_message(self, message: str) -> None:
        self.socket.sendall(message.encode())

    def _receive_messages(self) -> None:
        while self.keep_running:
            try:
                message = self.socket.recv(self.buffer_size)
                print(message.decode())
            except (Exception,) as e:
                self.logger.error(f"Exception while receiving message: {e}", exc_info=True)


if __name__ == "__main__":
    server_port = int(input("Server port: "))
    chat_client = ChatClient(socket.gethostname(), server_port)
    chat_client.start()
