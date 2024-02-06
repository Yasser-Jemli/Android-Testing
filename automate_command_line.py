#!/usr/bin/python3

import subprocess
import pyautogui
import time
import psutil

command_to_run="ls"

def run_terminal_command(command):
    # Open a new terminal
    terminal_process = subprocess.Popen(['gnome-terminal'])

    # Wait for the terminal to open
    time.sleep(2)

    # Type the command
    pyautogui.typewrite(command)

    # Press Enter
    pyautogui.press('enter')
    time.sleep (3)

    pyautogui.typewrite("pwd")

    # Press Enter
    pyautogui.press('enter')
    time.sleep (3)

    pyautogui.typewrite("exit")
    pyautogui.press('enter')

    return terminal_process


if __name__ == "__main__":
    terminal_process = run_terminal_command(command_to_run)


    # Add a delay (you can replace it with your own logic)
    time.sleep(5)



