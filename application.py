import subprocess
import pyautogui
import time
import psutil

def run_terminal_command(command):
    # Open a new terminal
    terminal_process = subprocess.Popen(['gnome-terminal'])

    # Wait for the terminal to open
    time.sleep(2)

    # Type the command
    pyautogui.typewrite(command)

    # Press Enter
    pyautogui.press('enter')

    return terminal_process

def close_terminal(command):
    # Find and terminate the terminal process based on the command
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['name'] == 'gnome-terminal' and process.info['cmdline'] is not None and command in process.info['cmdline']:
            process.terminate()

if __name__ == "__main__":
    command_to_run = input("Enter the command to run in the terminal: ")
    terminal_process = run_terminal_command(command_to_run)

    # Add a delay (you can replace it with your own logic)
    time.sleep(5)

    # Close the terminal
    close_terminal(command_to_run)

