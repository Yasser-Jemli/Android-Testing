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
        root.title("My Tkinter App")
        # setting window size
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # Define a common font
        common_font = tkFont.Font(family='Helvetica', size=10)

        # Header Label
        GLabel_451 = tk.Label(root, text="HMI_Auto_Manual_Testing", font=common_font, bg="#4CAF50", fg="#FFFFFF")
        GLabel_451.place(x=0, y=0, width=600, height=25)

        # Board Configuration Label
        GLabel_829 = tk.Label(root, text="Board Configuration & Wakeup", font=common_font, bg="#2196F3", fg="#FFFFFF")
        GLabel_829.place(x=0, y=20, width=600, height=25)

        # Checkbuttons
        GCheckBox_765 = tk.Checkbutton(root, text="Lawicel", font=common_font, bg="#C8E6C9", fg="#333333",
                                       command=self.GCheckBox_765_command)
        GCheckBox_765.place(x=0, y=60, width=70, height=25)

        GCheckBox_579 = tk.Checkbutton(root, text="Korlan", font=common_font, bg="#C8E6C9", fg="#333333",
                                       command=self.GCheckBox_579_command)
        GCheckBox_579.place(x=80, y=60, width=70, height=25)

        # Entry Widgets
        GLineEdit_732 = tk.Entry(root, font=common_font, fg="#333333", justify="center")
        GLineEdit_732.place(x=170, y=60, width=120, height=25)

        GLineEdit_107 = tk.Entry(root, font=common_font, fg="#333333", justify="center")
        GLineEdit_107.place(x=320, y=60, width=120, height=25)

        # Buttons
        GButton_154 = tk.Button(root, text="Board wakeup", font=common_font, bg="#F0F0F0", fg="#CC0000",
                                command=self.GButton_154_command)
        GButton_154.place(x=470, y=60, width=100, height=25)

        GButton_59 = tk.Button(root, text="Watch Scrcpy", font=common_font, bg="#F0F0F0", fg="#000000",
                               command=self.GButton_59_command)
        GButton_59.place(x=470, y=100, width=100, height=25)

        # Board Flashing Label
        GLabel_976 = tk.Label(root, text="Board Flashing", font=common_font, bg="#4CAF50", fg="#FFFFFF")
        GLabel_976.place(x=0, y=180, width=600, height=25)

        # File Selection Label
        GLabel_469 = tk.Label(root, text="Select Your Flashing Script", font=common_font, bg="#00BFFF", fg="#333333")
        GLabel_469.place(x=0, y=230, width=180, height=25)

        # Buttons for file selection
        GButton_103 = tk.Button(root, text="Select Your File", font=common_font, bg="#90F090", fg="#000000",
                                command=self.GButton_103_command)
        GButton_103.place(x=210, y=230, width=120, height=25)

        # Buttons for flashing and launching VSP
        GButton_248 = tk.Button(root, text="Start Flashing", font=common_font, bg="#F0F0F0", fg="#000000",
                                command=self.GButton_248_command)
        GButton_248.place(x=350, y=230, width=140, height=25)

        GLabel_664 = tk.Label(root, text="Select Your vehicle_config folder", font=common_font, bg="#00CED1", fg="#333333")
        GLabel_664.place(x=0, y=270, width=180, height=25)

        GButton_306 = tk.Button(root, text="Select Your Folder", font=common_font, bg="#F0F0F0", fg="#000000",
                                command=self.GButton_306_command)
        GButton_306.place(x=210, y=270, width=120, height=25)

        GButton_801 = tk.Button(root, text="Start Pushing The config", font=common_font, bg="#F0F0F0", fg="#000000",
                                command=self.GButton_801_command)
        GButton_801.place(x=350, y=270, width=140, height=25)

        GLabel_715 = tk.Label(root, text="Select Your VSP Folder", font=common_font, bg="#00CED1", fg="#333333")
        GLabel_715.place(x=0, y=380, width=140, height=25)

        GButton_604 = tk.Button(root, text="Start VSP manager", font=common_font, bg="#F0F0F0", fg="#000000",
                                command=self.GButton_604_command)
        GButton_604.place(x=160, y=380, width=120, height=25)

        GButton_461 = tk.Button(root, text="Launching VSPsim", font=common_font, bg="#F0F0F0", fg="#000000",
                                command=self.GButton_461_command)
        GButton_461.place(x=300, y=380, width=140, height=25)

        # Footer Label
        GLabel_574 = tk.Label(root, text="All rights reserved 2024", font=common_font, bg="#4CAF50", fg="#FFFFFF")
        GLabel_574.place(x=0, y=470, width=600, height=25)

    def GCheckBox_765_command(self):
        print("Lawicel selected")

    def GCheckBox_579_command(self):
        print("Korlan selected")

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
