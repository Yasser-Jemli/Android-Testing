import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

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
        root.title("HMI Auto Manual Testing")
        root.geometry("600x500")
        root.resizable(width=False, height=False)

        # Header
        header_frame = ttk.Frame(root, style="Header.TFrame")
        header_frame.grid(row=0, column=0, pady=(0, 20), sticky=(tk.W, tk.E))

        title_label = ttk.Label(header_frame, text="HMI Auto Manual Testing", style="Header.TLabel")
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

        # Board Configuration & Wakeup
        config_frame = ttk.Frame(root, style="Config.TFrame")
        config_frame.grid(row=1, column=0, pady=(0, 20), sticky=(tk.W, tk.E))

        lawicel_checkbox = ttk.Checkbutton(config_frame, text="Lawicel", style="Config.TCheckbutton")
        lawicel_checkbox.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        korlan_checkbox = ttk.Checkbutton(config_frame, text="Korlan", style="Config.TCheckbutton")
        korlan_checkbox.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        can0_entry = ttk.Entry(config_frame, text="can0 => ttyUSB", style="Config.TEntry")
        can0_entry.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)

        can1_entry = ttk.Entry(config_frame, text="can1 => ttyUSB", style="Config.TEntry")
        can1_entry.grid(row=0, column=3, padx=10, pady=10, sticky=tk.W)

        board_wakeup_button = ttk.Button(config_frame, text="Board Wakeup", command=self.board_wakeup, style="Config.TButton")
        board_wakeup_button.grid(row=0, column=4, padx=10, pady=10, sticky=tk.W)

        # Board Flashing
        flash_frame = ttk.Frame(root, style="Flash.TFrame")
        flash_frame.grid(row=2, column=0, pady=(0, 20), sticky=(tk.W, tk.E))

        select_script_label = ttk.Label(flash_frame, text="Select Your Flashing Script", style="Flash.TLabel")
        select_script_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        select_file_button = ttk.Button(flash_frame, text="Select Your File", command=self.select_file, style="Flash.TButton")
        select_file_button.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        start_flashing_button = ttk.Button(flash_frame, text="Start Flashing", command=self.start_flashing, style="Flash.TButton")
        start_flashing_button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)

        # Launching VSP for signal emulation
        vsp_frame = ttk.Frame(root, style="VSP.TFrame")
        vsp_frame.grid(row=3, column=0, pady=(0, 20), sticky=(tk.W, tk.E))

        start_flashing_button = ttk.Button(vsp_frame, text="Start Flashing", command=self.start_flashing, style="VSP.TButton")
        start_flashing_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        select_folder_label = ttk.Label(vsp_frame, text="Select Your vehicle_config folder", style="VSP.TLabel")
        select_folder_label.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        select_folder_button = ttk.Button(vsp_frame, text="Select Your Folder", command=self.select_folder, style="VSP.TButton")
        select_folder_button.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)

        start_pushing_button = ttk.Button(vsp_frame, text="Start Pushing The Config", command=self.start_pushing, style="VSP.TButton")
        start_pushing_button.grid(row=0, column=3, padx=10, pady=10, sticky=tk.W)

        # VSP Configuration
        vsp_config_frame = ttk.Frame(root, style="VSPConfig.TFrame")
        vsp_config_frame.grid(row=4, column=0, pady=(0, 20), sticky=(tk.W, tk.E))

        start_vsp_manager_button = ttk.Button(vsp_config_frame, text="Start VSP Manager", command=self.start_vsp_manager, style="VSPConfig.TButton")
        start_vsp_manager_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        start_vspsim_button = ttk.Button(vsp_config_frame, text="Launching VSPSim", command=self.start_vspsim, style="VSPConfig.TButton")
        start_vspsim_button.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Footer
        footer_frame = ttk.Frame(root, style="Footer.TFrame")
        footer_frame.grid(row=5, column=0, pady=(20, 0), sticky=(tk.W, tk.E))

        footer_label = ttk.Label(footer_frame, text="All rights reserved 2024", style="Footer.TLabel")
        footer_label.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))

    def board_wakeup(self):
        print("Board Wakeup")

    def select_file(self):
        file_path = filedialog.askopenfilename()
        print(f"Selected file: {file_path}")

    def start_flashing(self):
        print("Start Flashing")

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        print(f"Selected folder: {folder_path}")

    def start_pushing(self):
        print("Start Pushing The Config")

    def start_vsp_manager(self):
        print("Start VSP Manager")

    def start_vspsim(self):
        print("Launching VSPSim")

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
