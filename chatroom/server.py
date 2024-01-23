import socket
import asyncio

from logger import Logger


class ChatroomServer:
    __slots__ = ("logger", "host", "port", "clients", "buffer_size")

    def __init__(self, host: str, port: int):
        self.logger = Logger("ChatroomServer").get()
        self.host = host
        self.port = port
        self.clients = []
        self.buffer_size = 1024

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        self.clients.append(writer)
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
        async with (server := await asyncio.start_server(self.handle_client, self.host, self.port)):
            self.logger.info(f"Server started on {self.host}:{self.port}")
            await server.serve_forever()


async def main() -> None:
    server = ChatroomServer(socket.gethostname(), 12345)
    await server.start()


if __name__ == "__main__":
    asyncio.run(main())
