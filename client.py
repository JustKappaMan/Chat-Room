import socket
import logging
import threading


class ChatClient:
    def __init__(self, host: str, port: int):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("ChatClient")

        self.buffer_size = 1024

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

        self.logger.info(f"Connected to the server running on {host}:{port}")

    def start(self):
        input_thread = threading.Thread(target=self._receive_messages)
        input_thread.start()

        while True:
            try:
                msg = input().strip()
                self._send_message(msg)
            except KeyboardInterrupt:
                self.socket.close()
                break

    def _send_message(self, message: str) -> None:
        self.socket.sendall(message.encode("utf-8"))

    def _receive_messages(self) -> None:
        while True:
            try:
                message = self.socket.recv(self.buffer_size)
                print(message.decode("utf-8"))
            except (Exception,) as e:
                print(f"Exception while receiving message: {e}")
                break


if __name__ == "__main__":
    chat_client = ChatClient(socket.gethostname(), 12345)
    chat_client.start()
