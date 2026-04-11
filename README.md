# Downsized Space
Arcade style space game made with pygame

## Installation
- Find the latest release here: <a href="https://github.com/KissMate04/downsized-space/releases">release</a>
- Windows: download downsized_space_windows.exe and run it
- Linux: download downsized_space_linux and run it

## Running from source
- Download the source code and extract it.
- Open a terminal in the project folder and run: "python launcher.py"
- If you don't have pygame installed this will install it automatically

The game was packaged with pyinstaller using this command: 
"pyinstaller --onefile --noconsole --add-data "downsized_space\audio;downsized_space\audio" --add-data "downsized_space\sprites;downsized_space\sprites" --name "Downsized Space" launcher.py"
Replace '\' with '/' in Linux
  
<img width="480" height="270" alt="showcase" src="https://github.com/user-attachments/assets/a1553692-a6d4-44a5-8f46-6fa29962d330" />
