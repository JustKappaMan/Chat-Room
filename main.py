from chatroom.utils import open_in_new_terminal


def main() -> None:
    open_in_new_terminal("python3 chatroom/server.py")
    open_in_new_terminal("python3 chatroom/client.py")
    open_in_new_terminal("python3 chatroom/client.py")


if __name__ == "__main__":
    main()
