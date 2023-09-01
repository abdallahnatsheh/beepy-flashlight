# SQFMI BEEPY FLASHLIGHT

This Python script allows you to control RGB LED using a beepy  button. It provides the following functionality:

- Toggle the LED on and off with a short button press.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3.x installed
- RPi.GPIO library installed

**Note:** You need root (superuser) privileges to access the GPIO pins. You can run the script with `sudo` as shown in the usage instructions.

## Usage

1. Clone this repository to your beepy or download the script (`flashlight.py`) directly.

2. Run the script in the terminal with root privileges using `sudo`:
   `sudo python3 flashlight.py`

	**Note:**  you can add it as alias to run the script with one command in .bashrc  with `alias flash="python3 /path/to/flashlight.py"`
