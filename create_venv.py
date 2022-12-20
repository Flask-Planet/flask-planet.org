import pathlib
import subprocess

CURRENT_DIR = pathlib.Path(__file__).parent


def venv():
    if CURRENT_DIR.joinpath("venv").exists():
        print("Virtual environment already exists, delete it to create a new one using this script.")
    else:
        subprocess.call(['python3', '-m', 'venv', 'venv'])
        subprocess.call(['python3', 'venv/bin/pip3', 'install', '-r', 'requirements.txt'])


venv()
