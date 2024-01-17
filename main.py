import subprocess


def main() -> None:
    open_in_new_terminal("python3 chatroom/server.py"),
    open_in_new_terminal("python3 chatroom/client.py"),
    open_in_new_terminal("python3 chatroom/client.py")


def open_in_new_terminal(command: str) -> None:
    subprocess.Popen(f'gnome-terminal -- bash -c "{command}; exec bash"', shell=True).wait()


if __name__ == "__main__":
    main()
