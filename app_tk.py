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
        label_for_board_configuration = tk.Label(root, text="Board Configuration & Wakeup section", font=("Arial", 12), bg="#2196F3", fg="#FFFFFF")
        label_for_board_configuration.place(x=0, y=0, width=600, height=25)

        # Checkbuttons
        Lawicel_checkbutton = tk.Checkbutton(root, text="Lawicel", font=("Arial", 12), bg="#C8E6C9", fg="#333333")
        Lawicel_checkbutton.place(x=0, y=30, width=100, height=25)

        Korlan_checkbutton = tk.Checkbutton(root, text="Korlan", font=("Arial", 12), bg="#C8E6C9", fg="#333333")
        Korlan_checkbutton.place(x=0, y=60, width=100, height=25)

# ------------------------------------------------------------------------------------------------------------------------
        # Create the Entry widget with font properties
        Enty_for_can0_configuration = tk.Entry(root, font=("Arial", 12), fg="#333333", justify="center")
        Enty_for_can0_configuration.place(x=120, y=30, width=120, height=25)

        # Set default message
        default_message_0 = "can0 -> ttyUSB"
        Enty_for_can0_configuration.insert(0, default_message_0)
        Enty_for_can0_configuration.config(fg="#777777")  # Change text color to gray

        # Bind the click event to the Entry widget
        Enty_for_can0_configuration.bind("<FocusIn>", self.on_entry_click_for_can0_configuration)
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
        # Create the Entry widget with font properties
        Enty_for_can1_configuration = tk.Entry(root, font=("Arial", 12), fg="#333333", justify="center")
        Enty_for_can1_configuration.place(x=120, y=60, width=120, height=25)

        # Set default message
        default_message_1 = "can1 -> ttyUSB"
        Enty_for_can1_configuration.insert(0, default_message_1)
        Enty_for_can1_configuration.config(fg="#777777")  # Change text color to gray

        # Bind the click event to the Entry widget
        Enty_for_can1_configuration.bind("<FocusIn>", self.on_entry_click_for_can1_configuration)
# ------------------------------------------------------------------------------------------------------------------------
        error_window = tk.Text(root, height=2, width=30, wrap="word", state=tk.DISABLED)
        error_window.place(x=360, y=30, width=230 ,height=100)
# ------------------------------------------------------------------------------------------------------------------------
        # Buttons
        Board_wakeup_button = tk.Button(root, text="Board wakeup", font=("Arial", 10), bg="#F0F0F0", fg="#000000")
        Board_wakeup_button.place(x=250, y=30, width=100, height=25)

        Watch_scrcpy_button = tk.Button(root, text="Watch Scrcpy", font=("Arial", 10), bg="#F0F0F0", fg="#000000")
        Watch_scrcpy_button.place(x=250, y=60, width=100, height=25)
# ---------------------------------------------------------------------------------------------------
        # Board Flashing Label
        Board_flashing_label = tk.Label(root, text="Board Flashing section", font=("Arial", 14), bg="#4CAF50", fg="#FFFFFF")
        Board_flashing_label.place(x=0, y=140, width=600, height=25)

        # File Selection Label
        flashing_file_selection_label = tk.Label(root, text="Select Your Flashing Script", font=("Arial", 10), bg="#00BFFF", fg="#333333")
        flashing_file_selection_label.place(x=0, y=180, width=180, height=25)
# ------------------------------------------------------------------------------------------------------------------------
        # Buttons for file selection
        GButton_103 = tk.Button(root, text="Select Your File", font=("Arial", 10), bg="#90F090", fg="#000000")
        GButton_103.place(x=200, y=180, width=120, height=25)

        # Buttons for Launching the Flashing Process
        GButton_248 = tk.Button(root, text="Start Flashing", font=("Arial", 10), bg="#F0F0F0", fg="#000000")
        GButton_248.place(x=350, y=180, width=120, height=25)
# --------------------------------------------------------------------------------------------------------------------
        GLabel_664 = tk.Label(root, text="Select Your vehicle_config folder", font=("Arial", 10), bg="#00CED1", fg="#333333")
        GLabel_664.place(x=0, y=220, width=200, height=25)

        GButton_306 = tk.Button(root, text="Select Your Folder", font=("Arial", 10), bg="#F0F0F0", fg="#000000")
        GButton_306.place(x=220, y=220, width=120, height=25)

        GButton_801 = tk.Button(root, text="Start Pushing The config", font=("Arial", 10), bg="#F0F0F0", fg="#000000")
        GButton_801.place(x=360, y=220, width=160, height=25)

# *****************************************************************************************************************************
        # Board VSP simulation Label
        signal_simulation_label = tk.Label(root, text="Signal Simulation section", font=("Arial", 14), bg="#4CAF50", fg="#FFFFFF")
        signal_simulation_label.place(x=0, y=260, width=600, height=25)

        GLabel_715 = tk.Label(root, text="Select Your VSP Folder", font=("Arial", 12), bg="#00CED1", fg="#333333")
        GLabel_715.place(x=0, y=380, width=140, height=25)

        GButton_604 = tk.Button(root, text="Start VSP manager", font=("Arial", 12), bg="#F0F0F0", fg="#000000",
                                command=self.GButton_604_command)
        GButton_604.place(x=160, y=380, width=120, height=25)

        GButton_461 = tk.Button(root, text="Launching VSPsim", font=("Arial", 12), bg="#F0F0F0", fg="#000000",
                                command=self.GButton_461_command)
        GButton_461.place(x=300, y=380, width=140, height=25)

        # Footer Label
        GLabel_574 = tk.Label(root, text="All rights reserved 2024", font=("Arial", 12), bg="#4CAF50", fg="#FFFFFF")
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

    
    def on_entry_click_for_can0_configuration(self,event):
        if self.Enty_for_can0_configuration.get() == "Default Message":
            self.Enty_for_can0_configuration.delete(0, "end")
            self.Enty_for_can0_configuration.config(fg="#000000")  

    def on_entry_click_for_can1_configuration(self,event):
        if self.Enty_for_can1_configuration.get() == "Default Message":
            self.Enty_for_can1_configuration.delete(0, "end")
            self.Enty_for_can1_configuration.config(fg="#000000")  


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
