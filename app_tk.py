import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font as tkFont

class App1:
    def __init__(self, master):
        self.master = master
        self.master.title("App 1")

        self.frame = tk.Frame(self.master, padx=20, pady=20)
        self.frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.frame, text="This is App 1")
        self.label.pack(pady=10)

        self.button_close = tk.Button(self.frame, text="Close App 1", command=self.close_app)
        self.button_close.pack(pady=10)

    def close_app(self):
        self.master.destroy()

class App2:
    def __init__(self, root):
        # setting title
        root.title("HMI Auto Manuel Env")
        # setting window size
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # Board Configuration Label
        label_for_board_configuration = tk.Label(root, text="Board Configuration & Wakeup section", font=("Arial", 12, "bold"), bg="#3498db", fg="#ecf0f1")
        label_for_board_configuration.place(x=0, y=0, width=600, height=25)

        # Checkbuttons
        Lawicel_checkbutton = tk.Checkbutton(root, text="Lawicel", font=("Arial", 12), bg="#2980b9", fg="#ecf0f1", selectcolor="#2ecc71")
        Lawicel_checkbutton.place(x=0, y=30, width=100, height=25)

        Korlan_checkbutton = tk.Checkbutton(root, text="Korlan", font=("Arial", 12), bg="#2980b9", fg="#ecf0f1", selectcolor="#2ecc71")
        Korlan_checkbutton.place(x=0, y=60, width=100, height=25)

        # Entry for can0 configuration
        Enty_for_can0_configuration = tk.Entry(root, font=("Arial", 12), fg="#333333", justify="center")
        Enty_for_can0_configuration.place(x=120, y=30, width=120, height=25)
        default_message_0 = "can0 -> ttyUSB"
        Enty_for_can0_configuration.insert(0, default_message_0)
        Enty_for_can0_configuration.config(fg="#555555")  # Change text color to a darker gray
        Enty_for_can0_configuration.bind("<FocusIn>", self.on_entry_click_for_can0_configuration)

        # Entry for can1 configuration
        Enty_for_can1_configuration = tk.Entry(root, font=("Arial", 12), fg="#333333", justify="center")
        Enty_for_can1_configuration.place(x=120, y=60, width=120, height=25)
        default_message_1 = "can1 -> ttyUSB"
        Enty_for_can1_configuration.insert(0, default_message_1)
        Enty_for_can1_configuration.config(fg="#555555")  # Change text color to a darker gray
        Enty_for_can1_configuration.bind("<FocusIn>", self.on_entry_click_for_can1_configuration)

        # Text widget for displaying errors
        error_window = tk.Text(root, height=2, width=30, wrap="word", state=tk.DISABLED, bg="#3498db", fg="#ecf0f1")
        error_window.place(x=360, y=30, width=230, height=100)

        # Buttons
        Board_wakeup_button = tk.Button(root, text="Board wakeup", font=("Arial", 10), bg="#2980b9", fg="#ecf0f1")
        Board_wakeup_button.place(x=250, y=30, width=100, height=25)

        Watch_scrcpy_button = tk.Button(root, text="Watch Scrcpy", font=("Arial", 10), bg="#2980b9", fg="#ecf0f1")
        Watch_scrcpy_button.place(x=250, y=60, width=100, height=25)

        # Board Flashing Label
        Board_flashing_label = tk.Label(root, text="Board Flashing section", font=("Arial", 14, "bold"), bg="#2ecc71", fg="#ecf0f1")
        Board_flashing_label.place(x=0, y=140, width=600, height=25)

        # File Selection Label
        flashing_file_selection_label = tk.Label(root, text="Select Your Flashing Script", font=("Arial", 10), bg="#27ae60", fg="#ecf0f1")
        flashing_file_selection_label.place(x=0, y=180, width=180, height=25)

        # Buttons for file selection
        button_for_file_selection = tk.Button(root, text="Select Your File", font=("Arial", 10), bg="#2980b9", fg="#ecf0f1")
        button_for_file_selection.place(x=200, y=180, width=120, height=25)

        # Buttons for Launching the Flashing Process
        button_for_launching_the_flashing_process = tk.Button(root, text="Start Flashing", font=("Arial", 10), bg="#3498db", fg="#ecf0f1")
        button_for_launching_the_flashing_process.place(x=350, y=180, width=120, height=25)

        # Select Your vehicle_config folder Label
        select_your_vehicle_config_label = tk.Label(root, text="Select Your vehicle_config folder", font=("Arial", 10), bg="#27ae60", fg="#ecf0f1")
        select_your_vehicle_config_label.place(x=0, y=220, width=200, height=25)

        # Buttons for vehicle_config folder selection
        button_for_vehicle_config_folder_selection = tk.Button(root, text="Select Your Folder", font=("Arial", 10), bg="#2980b9", fg="#ecf0f1")
        button_for_vehicle_config_folder_selection.place(x=220, y=220, width=120, height=25)

        # Buttons for starting vehicle_config pushing process
        button_for_starting_vehicle_config_pushing_process = tk.Button(root, text="Start Pushing The Config", font=("Arial", 10), bg="#3498db", fg="#ecf0f1")
        button_for_starting_vehicle_config_pushing_process.place(x=360, y=220, width=160, height=25)

        # Board VSP simulation Label
        signal_simulation_label = tk.Label(root, text="Signal Simulation section", font=("Arial", 14, "bold"), bg="#2ecc71", fg="#ecf0f1")
        signal_simulation_label.place(x=0, y=260, width=600, height=25)

        # Select Your VSP Folder Label
        Select_vsp_folder_label = tk.Label(root, text="Select Your VSP Folder", font=("Arial", 10), bg="#27ae60", fg="#ecf0f1")
        Select_vsp_folder_label.place(x=0, y=300, width=140, height=25)

        # Button for VSP folder selection
        select_your_vsp_folder = tk.Button(root, text="Select VSP folder", font=("Arial", 10), bg="#2980b9", fg="#ecf0f1")
        select_your_vsp_folder.place(x=160, y=300, width=120, height=25)

        # Button for starting VSP manager
        Start_vsp_manager_button = tk.Button(root, text="Start VSP manager", font=("Arial", 10), bg="#3498db", fg="#ecf0f1")
        Start_vsp_manager_button.place(x=300, y=300, width=120, height=25)

        # Button for launching VSPsim
        launching_vsp_sim_button = tk.Button(root, text="Launching VSPsim", font=("Arial", 10), bg="#3498db", fg="#ecf0f1")
        launching_vsp_sim_button.place(x=440, y=300, width=140, height=25)

        # Footer Label section
        GLabel_574 = tk.Label(root, text="All rights reserved 2024", font=("Arial", 12), bg="#3498db", fg="#ecf0f1")
        GLabel_574.place(x=0, y=470, width=600, height=25)


    def GButton_154_command(self):
        print("Board wakeup button clicked")

    def GButton_59_command(self):
        print("Watch Scrcpy button clicked")

    def GButton_103_command(self):
        file_path = filedialog.askopenfilename(title="Select Your Flashing Script", filetypes=[("Text files", "*.txt")])
        if file_path:
            print("Selected File:", file_path)

    def GButton_248_command(self):
        print("Start Flashing button clicked")

    def GButton_306_command(self):
        folder_path = filedialog.askdirectory(title="Select Your vehicle_config folder")
        if folder_path:
            print("Selected Folder:", folder_path)

    def GButton_801_command(self):
        print("Start Pushing The config button clicked")

    def GButton_604_command(self):
        folder_path = filedialog.askdirectory(title="Select Your VSP Folder")
        if folder_path:
            print("Selected VSP Folder:", folder_path)

    def GButton_461_command(self):
        print("Launching VSPsim button clicked")

    
    def on_entry_click_for_can0_configuration(self, event):
        if self.Enty_for_can0_configuration.get() == "can0 -> ttyUSB":
            self.Enty_for_can0_configuration.delete(0, "end")
            self.Enty_for_can0_configuration.config(fg="#000000")  # Change text color to black
            self.error_window.delete(1.0, "end")  # Clear any previous error message

    def on_entry_click_for_can1_configuration(self, event):
        if self.Enty_for_can1_configuration.get() == "can1 -> ttyUSB":
            self.Enty_for_can1_configuration.delete(0, "end")
            self.Enty_for_can1_configuration.config(fg="#000000")  # Change text color to black
            self.error_window.delete(1.0, "end")  # Clear any previous error message



class AppChooser:
    def __init__(self, master):
        self.master = master
        self.master.title("Choose an App")

        self.label = tk.Label(self.master, text="Select an app:")
        self.label.pack(pady=10)

        self.button_app1 = tk.Button(self.master, text="App 1", command=self.run_app1)
        self.button_app1.pack(pady=5)

        self.button_app2 = tk.Button(self.master, text="App 2", command=self.run_app2)
        self.button_app2.pack(pady=5)

    def run_app1(self):
        app1_window = tk.Tk()
        app1 = App1(app1_window)
        app1_window.mainloop()

    def run_app2(self):
        app2_window = tk.Tk()
        app2 = App2(app2_window)
        app2_window.mainloop()

def main():
    root = tk.Tk()
    app_chooser = AppChooser(root)
    root.mainloop()

if __name__ == "__main__":
    main()
