#!/usr/bin/env python
import os
import sys
import subprocess

# A laucher egy részében Claude segített


def main():
    # Get the package directory
    package_dir = os.path.dirname(os.path.abspath(__file__))

    # Change to the package directory
    original_dir = os.getcwd()
    os.chdir(package_dir)

    # Run the main script in the package directory
    main_script = os.path.join(package_dir, "main.py")
    result = subprocess.call([sys.executable, main_script] + sys.argv[1:])

    # Change back to the original directory
    os.chdir(original_dir)

    return result


if __name__ == "__main__":
    sys.exit(main())
