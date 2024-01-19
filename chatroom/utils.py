import platform
import subprocess


def open_in_new_terminal(command: str) -> None:
    if platform.system() == "Windows":
        subprocess.Popen(f"start cmd /k {command}", shell=True).wait()
    else:
        subprocess.Popen(f'gnome-terminal -- bash -c "{command}; exec bash"', shell=True).wait()
