import importlib
import sys
import subprocess


def install_requirements():
    try:
        import pygame
    except ImportError:
        print("Required packages not found. Installing now...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("Installation complete.")
        except subprocess.CalledProcessError:
            print(
                "Failed to install requirements automatically. Please run 'pip install -r requirements.txt' manually.")
            sys.exit(1)


if __name__ == '__main__':
    install_requirements()
    importlib.invalidate_caches()
    from downsized_space.main import main

    main()