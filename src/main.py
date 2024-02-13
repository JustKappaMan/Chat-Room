from chatroom.utils import run_in_new_terminal


def main() -> None:
    run_in_new_terminal("python3 chatroom/server.py")
    run_in_new_terminal("python3 chatroom/client.py")
    run_in_new_terminal("python3 chatroom/client.py")


if __name__ == "__main__":
    main()
