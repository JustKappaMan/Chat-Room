import socket
import asyncio

from logger import Logger


class ChatroomServer:
    __slots__ = ("logger", "host", "port", "clients", "buffer_size")

    def __init__(self, host: str, port: int):
        self.logger = Logger("ChatroomServer", log_to_console=True).get()
        self.host = host
        self.port = port
        self.clients = set()
        self.buffer_size = 4096

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        self.clients.add(writer)
        self.logger.info(f"New client connected: {writer.get_extra_info('peername')}")

        while True:
            if not (data := await reader.read(self.buffer_size)):
                break

            for client in self.clients:
                if client != writer:
                    client.write(data)
                    await client.drain()

        self.logger.info(f"Client disconnected: {writer.get_extra_info('peername')}")
        self.clients.remove(writer)
        writer.close()

    async def start(self) -> None:
        async with (server := await asyncio.start_server(self._handle_client, self.host, self.port)):
            self.logger.info(f"Server started on {self.host}:{self.port}")
            await server.serve_forever()


async def main() -> None:
    server = ChatroomServer(socket.gethostname(), 12345)
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
