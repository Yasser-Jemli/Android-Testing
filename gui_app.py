import os
import re
import tkinter as tk
from tkinter import ttk
import time
import subprocess
import pyautogui
import threading
from tkinter import messagebox

class TestRunnerApp:
    def __init__(self, root):
        # Setting up the main window
        self.root = root
        root.title("HMI_IAT : Test Runner v1.0")
        root.geometry("900x600")
        root.resizable(width=False, height=False)
        
        # Available Vehicle Config
        self.all_options = [
            "DHN_HEV_vc_DT1","DHN_HEV_vc_DT1_LDWS_Present", "DHN_HEV_vc_DT1_Torque_Split_Absent",
            "DHN_HEV_vc_DT1_Trailer_Guideline_Not_Present","DHN_HEV_vc_DT1_Static_Guideline_Not_Present",
            "DHN_HEV_vc_DT1_Dynamic_Guideline_Not_Present","DHN_HEV_vc_DT1_Radio_AM_Present",
            "DHN_HEV_vc_DT2","DHN_HEV_vc_DT2_no_Air_Freshner","DHN_HEV_vc_DT2_Backlight_DimmingStrategy_Present",
            "DHN_HEV_vc_DT2_BSWSonar_Present","DHN_HEV_vc_DT2_Clinometercompass_Absent","DHN_HEV_vc_DT2_CAMAN",
            "DHN_HEV_vc_DT2_Eco_Score_Present","DHN_HEV_vc_DT2_CAREG","DHN_HEV_vc_DT2_No_Parking",
            "DHN_HEV_vc_DT2_CAREG_RHD_Present","DHN_HEV_vc_DT2_PSI_Autoloc_tpms_Present","DHN_HEV_vc_DT2_CASP_Present",
            "DHN_HEV_vc_DT2_Econav_Zevcity_Settings_Present","DHN_HEV_vc_DT2_CAREG_Trilevel_Absent","DHN_HEV_vc_DT2_adas_settings_slauto_present",
            "DHN_HEV_vc_DT2_no_AQS_Clim","DHN_HEV_vc_DT2_Volume_Alarm_Present","DHN_HEV_vc_DT2_front_heated_and_ventilation_seats_available",
            "DHN_HEV_vc_DT4","DHN_HEV_pt_DT4_for_parking","DHN_HEV_vc_DT4_Without_rvc","DHN_HEV_pt_VF1DHN001PVC0000A","BCB_GSR2_vc_XCB_SV1627",
            "BCB_GSR2_vc_XCB_SV1627_Auto_Follow_Me_Present","BCB_GSR2_vc_XCB_SV1627_PSI_Autoloc_tpms_Present","BCB_GSR2_vc_XCB_SV1627_ASR_Present",
            "BCB_GSR2_vc_XCB_SV1627_AmbientLight_present_MexGeneric_not_present","BCB_GSR2_vc_XCB_SV1627_tpms_Present","BCB_GSR2_vc_XCB_SV1627_vsp_choicesounds_11000",
            "BCB_GSR2_vc_XCB_SV1627_vsp_choicesounds_00001","BCB_GSR2_vc_XCB_SV1627_vsp_choicesounds_00111","BCB_GSR2_vc_XCB_SV1627_vsp_choicesounds_00101",
            "BCB_GSR2_vc_XCB_SV1627_vsp_choicesounds_00011","BCB_GSR2_vc_XCB_SV1627_vsp_choicesounds_00010","BCB_GSR2_vc_XCB_SV1627_vsp_choicesounds_01100",
            "BCB_GSR2_vc_XCB_SV1627_vsp_choicesounds_00110","BCB_GSR2_vc_XCB_SV1627_vsp_choicesounds_00100","BCB_GSR2_vc_XCB_SV1627_Sailing_IDLE_Present",
            "BCB_GSR2_vc_XCB_SV1627_Backlight_DimmingStrategy_Present","BCB_GSR2_vc_XCB_SV1639","BCB_GSR2_vc_XCB_SV1639_seats_electromechanical_massage",
            "BCB_GSR2_vc_XCB_SV1639_Backlight_HMD_Present","BCB_GSR2_vc_XCB_SV1639_Snow_AllRoad_Present","BCB_GSR2_vc_XCB_SV1639_CAREG",
            "BCB_GSR2_vc_XCB_SV1639_massage_with_5_intensity_levels","BCB_GSR2_vc_XCB_SV1639_Mex_Engine_Setting_enabled","BCB_GSR2_vc_XCB_SV1639_Mex_Engine_Setting_disabled",
            "BCB_GSR2_vc_XCB_SV1639_Mex_ESE_type_level_Present","BCB_GSR2_vc_XCB_SV1639_Mex_HVAC_Setting_disabled","BCB_GSR2_vc_XCB_SV1639_Consumption_Present_Acceleration_Absent",
            "BCB_GSR2_vc_XCB_SV1639_Without_Drivingmode_Flow_EV","BCB_GSR2_vc_XCB_SV1639_Without_EnergyHistoryconsumption","BCB_GSR2_vc_XCB_SV1639_With_DrivingMode_V2X",
            "BCB_GSR2_vc_XCB_SV1642","HJB_PH2_vc_XJB_SV4011","HJB_PH2_vc_XJB_SV4011_Little_Engine_Petrol","HJB_PH2_vc_XJB_SV4011_Torque_Split_present","HJB_PH2_vc_XJB_SV4011_TPMS_Driving_Eco_Displayed",
            "HJB_PH2_vc_XJB_SV4016","HJB_PH2_vc_XJB_SV4024","HJB_PH2_vc_XJB_SV4024_No_CAM_On_Trunk","HJB_PH2_vc_XJB_SV4024_MVC_Present","HJB_PH2_vc_XJB_SV4046",
            "HJB_PH2_vc_XJB_SV4056","HJB_PH2_vc_XJB_SV4056_RHD_Present_with_HDC","HJB_PH2_vc_XJB_SV4071","HJB_PH2_vc_XJB_SV4071_PSI_Autoloc_tpms_Present",
            "XDD_vc1","XDD_vcVF1XDD000CVC00001"
        ]   
        
        # Variables
        self.selected_id = None
        self.checkbox_board_option_var =     tk.BooleanVar(value=True)
        self.checkbox_emulator_option_var =  tk.BooleanVar(value=False)
        self.checkbox_12_inch_option_var =   tk.BooleanVar(value=True)
        self.checkbox_10_4_inch_option_var = tk.BooleanVar(value=False)
        self.checkbox_10_1_inch_option_var = tk.BooleanVar(value=False)
        self.checkbox_9_inch_option_var =    tk.BooleanVar(value=False)
        self.checkbox_LHD_option_var =       tk.BooleanVar(value=True)
        self.checkbox_RHD_option_var =       tk.BooleanVar(value=False)
        self.checkbox_Korlan_option_var =    tk.BooleanVar(value=False)
        self.checkbox_Lawicel_option_var =   tk.BooleanVar(value=True)
        self.checkbox_CANAKIN_option_var =   tk.BooleanVar(value=True)
        self.checkbox_VSP_option_var =       tk.BooleanVar(value=False)
        self.checkbox_ltr_option_var =       tk.BooleanVar(value=True)
        self.checkbox_rtl_option_var =       tk.BooleanVar(value=False)

        # Variables for Can Configuration can0
        self.default_message_0 = "Put Your Can-V --> can0 ttyUSB* "
        self.entry_can0_var = tk.StringVar()
        self.entry_can0_var.set(self.default_message_0)
        
        # Variables for Can Configuration can1 
        self.default_message_1 = "Put Your Can-M --> can1 ttyUSB* "
        self.entry_can1_var = tk.StringVar()
        self.entry_can1_var.set(self.default_message_1)
        
        # Widgets
        self.create_widgets(root)

    def create_widgets(self, root):
        # Test ID Finder
        test_id_label = tk.Label(root, anchor="center", bg="#2C3E50", font=("Arial", 16, "bold"), fg="#ECF0F1", justify="center", text="Test ID Finder")
        test_id_label.place(x=0, y=0, width=900, height=40)

        # Option Selection
        option_selection = tk.Label(root, anchor="center", bg="#2C3E50", font=("Arial", 16, "bold"), fg="#ECF0F1", justify="center", text="Option Selection Section")
        option_selection.place(x=0, y=90, width=900, height=40)

        # Entry Box for test Searching
        self.entry_box_for_test_searching = tk.Entry(root, borderwidth=2, font=("Arial", 12), fg="#2C3E50", justify="center")
        self.entry_box_for_test_searching.place(x=50, y=50, width=200, height=30)

        self.search_box_for_test_case_ids = ttk.Combobox(root, font=("Arial", 12), justify="center")
        self.search_box_for_test_case_ids.place(x=260, y=50, width=250, height=30)
        self.search_box_for_test_case_ids.bind("<<ComboboxSelected>>", self.select_test_id)

        # Search IDs button
        search_button = tk.Button(root, text="Search for Test", bg="#27AE60", font=("Arial", 12, "bold"), fg="#ECF0F1", relief=tk.FLAT, command=self.search_ids)
        search_button.place(x=580, y=50, width=150, height=30)

        # Select Test ID button
        select_id_button = tk.Button(root, text="Select Test ID", bg="#27AE60", font=("Arial", 12, "bold"), fg="#ECF0F1", relief=tk.FLAT, command=self.select_test_id)
        select_id_button.place(x=750, y=50, width=150, height=30)

        # Check Box for Board Option
        checkbox_board_option = tk.Checkbutton(root, text="Board", variable=self.checkbox_board_option_var, font=("Arial", 12), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_board_option_action)
        checkbox_board_option.place(x=20, y=140, width=100, height=30)

        # Check Box for Emulator Option
        checkbox_emulator_option = tk.Checkbutton(root, text="Emulator", variable=self.checkbox_emulator_option_var, font=("Arial", 12), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_emulator_option_action)
        checkbox_emulator_option.place(x=130, y=140, width=100, height=30)

        # 12 inch option 
        checkbox_12_inch_option = tk.Checkbutton(root, text="12 inch", variable=self.checkbox_12_inch_option_var, font=("Arial", 12), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_12_inch_option_action)
        checkbox_12_inch_option.place(x=250, y=140, width=100, height=30)

        # 10.4 inch option 
        checkbox_10_4_inch_option = tk.Checkbutton(root, text="10.4 inch", variable=self.checkbox_10_4_inch_option_var, font=("Arial", 12), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_10_4_inch_option_action)
        checkbox_10_4_inch_option.place(x=360, y=140, width=100, height=30)

        # 10.1 inch option 
        checkbox_10_1_inch_option = tk.Checkbutton(root, text="10.1 inch", variable=self.checkbox_10_1_inch_option_var, font=("Arial", 12), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_10_1_inch_option_action)
        checkbox_10_1_inch_option.place(x=470, y=140, width=100, height=30)

        # 9 inch option 
        checkbox_9_inch_option = tk.Checkbutton(root, text="9 inch", variable=self.checkbox_9_inch_option_var, font=("Arial", 12), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_9_inch_option_action)
        checkbox_9_inch_option.place(x=580, y=140, width=100, height=30)

        # LHD option 
        checkbox_LHD_option = tk.Checkbutton(root, text="LHD", variable=self.checkbox_LHD_option_var, font=("Arial", 12), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_LHD_option_action)
        checkbox_LHD_option.place(x=20, y=190 , width=100, height=30)

        # RHD Option
        checkbox_RHD_option = tk.Checkbutton(root, text="RHD", variable=self.checkbox_RHD_option_var, font=("Arial", 12), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_RHD_option_action)
        checkbox_RHD_option.place(x=130, y=190 , width=100, height=30)

        # Korlan USB2CAN Option 
        checkbox_Korlan_option = tk.Checkbutton(root, text="Korlan", variable=self.checkbox_Korlan_option_var, font=("Arial", 12), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_Korlan_option_action)
        checkbox_Korlan_option.place(x=250, y=190, width=100, height=30)


        # Lawicel USB2CAN Option 
        checkbox_Lawicel_option = tk.Checkbutton(root, text="Lawicel", variable=self.checkbox_Lawicel_option_var, font=("Arial", 12), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_Lawicel_option_action)
        checkbox_Lawicel_option.place(x=360, y=190 , width=100, height=30)

        # CANAKIN  protocol  Option 
        checkbox_CANAKIN_option = tk.Checkbutton(root, text="CANAKIN", variable=self.checkbox_CANAKIN_option_var, font=("Arial", 11), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_CANAKIN_option_action)
        checkbox_CANAKIN_option.place(x=470, y=190 , width=100, height=30)

        # VSP  protocol  Option 
        checkbox_VSP_option = tk.Checkbutton(root, text="VSP", variable=self.checkbox_VSP_option_var, font=("Arial", 11), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_VSP_option_action)
        checkbox_VSP_option.place(x=580, y=190 , width=100, height=30)

        # ltr Text Direction 
        checkbox_ltr_option = tk.Checkbutton(root, text="text direction : ltr ", variable=self.checkbox_ltr_option_var, font=("Arial", 11), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_ltr_option_action)
        checkbox_ltr_option.place(x=700, y=190 , width=200, height=30)

        # rtl Text Direction 
        checkbox_rtl_option = tk.Checkbutton(root, text="text direction : rtl ", variable=self.checkbox_rtl_option_var, font=("Arial", 11), fg="#2C3E50", bg="#ECF0F1", command=self.checkbox_rtl_option_action)
        checkbox_rtl_option.place(x=700, y=140 , width=200, height=30)
        
        # Can Configuration Section 
        can_configuration_label = tk.Label(root ,anchor="center", bg="#2C3E50", font=("Arial", 16, "bold"), fg="#ECF0F1", justify="center", text="Can & vehicle_config Configuration Section ")
        can_configuration_label.place(x=0, y=240, width=900, height=40)
        
        # Entry Box for can0 configuration (CAN-V)
        self.entry_box_for_can0_configuration = tk.Entry(root, textvariable=self.entry_can0_var , borderwidth=2, font=("Arial", 12), fg="#2C3E50", justify="center")
        self.entry_box_for_can0_configuration.place(x=50, y=290, width=250, height=30)
        self.entry_box_for_can0_configuration.bind("<FocusIn>", self.on_entry_click_can0)
        
        # Entry Box for can1 configuration (CAN-M)
        self.entry_box_for_can1_configuration = tk.Entry(root, textvariable=self.entry_can1_var , borderwidth=2, font=("Arial", 12), fg="#2C3E50", justify="center")
        self.entry_box_for_can1_configuration.place(x=350, y=290, width=250, height=30)
        self.entry_box_for_can1_configuration.bind("<FocusIn>", self.on_entry_click_can1)
        
        # TreeView to check the Output of the command "ls /dev/ttyUSB" and get Updated every 10 seconds
        self.tree = ttk.Treeview(root)
        self.tree.heading('#0', text='Available ttyUSB Ports')
        self.tree.column('#0', stretch=tk.YES)
        self.tree.place(x=620, y=290, width=200, height=80)

        # Run the command initially
        self.update_serial_ports()

        # Set up a thread to update the ports every 10 seconds
        self.schedule_update()
        
        # Run The Test button
        run_test_button = tk.Button(root, text="Run The Test", bg="#E67E22", font=("Arial", 14, "bold"), fg="#ECF0F1", relief=tk.FLAT, command=self.run_test)
        run_test_button.place(x=375, y=490, width=150, height=40)

        # Footer
        footer_label = tk.Label(root, bg="#3498DB", font=("Arial", 12), fg="#ECF0F1", justify="center", text="all rights reserved © 2024")
        footer_label.place(x=0, y=560, width=900, height=40)
        
        # vehcile Config Section ************************************************************
        vehicle_config_options_label = tk.Label(root, bg="#3498DB", font=("Arial", 12), fg="#ECF0F1", justify="center", text="Select Your vehicle Config => ")
        vehicle_config_options_label.place(x=0, y=340, width=240, height=40)
        
        # Initialize the Combobox for the vehicle config
        self.config_combo = ttk.Combobox(root, values=[], width=40)
        self.config_combo.place(x=250, y=340 , width=350 , height=30)
        self.config_combo.bind("<KeyRelease>", self.update_options_config)  # Bind the event to handle typing
        self.config_combo.bind("<<ComboboxSelected>>", self.on_select_config)  # Bind the event for selection

        #  Button to wiether you want to push Config Or not ?
        self.selected_push_config_state = tk.Label(root, text="Select If you want to push Vehicle Config or not : ")
        self.selected_push_config_state.place(x=0,y=390, width=400, height=40) 

        self.selected_push_config_state = tk.StringVar(root)
        self.selected_push_config_state.set("Select push config or not")

        options = ["Yes : push vehicle config ", "No : don't push vehicle Config "]

        self.dropdown = tk.OptionMenu(root, self.selected_push_config_state, *options, command=self.on_select_push_config)
        self.dropdown.place(x=420,y=390 ,width=250,height=40)
        # Initialize a boolean variable
        self.is_push_config_enabled = None

# ----------------------------------------------------------------------------------------------------
# *************** Method Section ***********************************************************************
    def schedule_update(self):
        self.update_serial_ports()
        self.root.after(10000, self.schedule_update)  # Schedule the next update after 10 seconds

    def update_serial_ports(self):
        try:
            # Run the command and get the output
            output = subprocess.check_output(['ls', '/dev/ttyUSB'], stderr=subprocess.STDOUT).decode('utf-8').strip()

            # Clear existing entries
            for item in self.tree.get_children():
                self.tree.delete(item)

            if output:
                # Insert new entries
                ports = output.split('\n')
                for port in ports:
                    self.tree.insert('', 'end', text=port)
            else:
                self.tree.insert('', 'end', text='No such port available')

        except subprocess.CalledProcessError as e:
            print(f"Error running the command: {e.output.decode('utf-8')}")
        except FileNotFoundError:
            # Handle the case where /dev/ttyUSB is not found
            self.tree.delete(*self.tree.get_children())  # Clear existing entries
            self.tree.insert('', 'end', text='No such port available')

            
    def on_entry_click_can0(self, event):
        if self.entry_can0_var.get() == self.default_message_0:
            self.entry_can0_var.set("")
            
    def on_entry_click_can1(self, event):
        if self.entry_can1_var.get() == self.default_message_1:
            self.entry_can1_var.set("")

    def search_ids(self):
        search_text = self.entry_box_for_test_searching.get()
        found_ids = []
        current_directory = os.getcwd()
        target_directory = os.path.join(current_directory, "Testcases/multimedia-AIVI2")
        for root, dirs, files in os.walk(target_directory):
            for file in files:
                if file.endswith(".robot"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        ids = re.findall(r'\b\d+(?: \d+)+\b', content)  # Extract multiple space-separated digits
                        for id in ids:
                            if search_text in id:
                                found_ids.append(id)

        # Clear previous search results
        self.search_box_for_test_case_ids['values'] = []
        # Add found IDs to the Combobox
        self.search_box_for_test_case_ids['values'] = tuple(found_ids)

    def select_test_id(self, event=None):
        self.selected_id = self.search_box_for_test_case_ids.get()
        print(f"Selected ID: {self.selected_id}")

    def run_test(self):
        # Add your code for running the test here
        print("Running the test...")
        command = f"robot "
        command += f'--test "{self.selected_id}" '
        if self.checkbox_CANAKIN_option_var.get():
            command += f"-v protocol:CANAKIN "
        else:
            command += f"-v protocol:VSP "
        if self.checkbox_Lawicel_option_var.get():
            command +=f"-v USB2CAN:Lawicel "
        elif self.checkbox_Korlan_option_var.get():
            command +=f"-v USB2CAN:Korlan"
        else:
            messagebox.showerror("Error", "No input was Selected for the USB2CAN , please report a bug as the app shall handle such a case .")

        port_can0 = self.entry_can0_var.get()
        port_can1 = self.entry_can1_var.get()
        command += f"-v port_can0:{port_can0} "
        command += f"-v port_can1:{port_can1} "
        command += f"-v variant:FullNav "
        # check the requested display size
        if self.checkbox_12_inch_option_var.get():
            command +=f"-v display_size:12 "
        elif self.checkbox_10_4_inch_option_var.get():
            self.command +=f"-v display_size:10.4 "
        elif checkbox_10_1_inch_option_var.get():
            self.command +=f"-v display_size:10.1 "
        elif self.checkbox_9_inch_option_var.get():
            self.command +=f"-v display_size:9 "
        else:
            messagebox.showerror("Error", "No input was Selected for the display Size , please report a bug as the app shall handle such a case .")
        # check the text direction input 
        if self.checkbox_ltr_option_var.get():
            command +=f"-v text_direction:ltr "
        elif checkbox_rtl_option_var.get():
            command +=f"-v text_direction:rtl "
        else:
            messagebox.showerror("Error", "No input was Selected for the text_direction , please report a bug as the app shall handle such a case.")
        # Add screenshoots arguemnt to Yes 
        command +=f"-v screenshots:Yes "
        if self.checkbox_board_option_var.get():
            command +=f"-v target:board "
        elif self.checkbox_emulator_option_var.get():
            command +=f"-v target:emulator "
        else:
            messagebox.showerror("Error", "No input was Selected for the target option , please report a bug as the app shall handle such a case.")
        command +=f"-v hotspot_name:renault_hotspot -v hotspot_password:renault@1234 hmi_iat/Testcases"
        if self.is_push_config_enabled : 
            print ("pushing the config")
        else:
            command +=f"/multimedia-AIVI2"
        print(command)
        if self.checkbox_LHD_option_var.get():
            command_1 = f"export HAND_DRIVING=LHD"
        elif self.checkbox_RHD_option_var.get():
            command_1 = f"export HAND_DRIVING=RHD"
        else:
            messagebox.showerror("Error", "No input was Selected for the HAND DRIVING, please report a bug as the app shall handle such a case.")
        command_2 = f"export LANGUAGE=en"
        self.selected_config_value = self.config_combo.get()
         
        command_3 = "export CONFIG=" + self.selected_config_value
        # To implement a logic with Xdotool
        subprocess.Popen(['gnome-terminal'])

        # Wait for the terminal to open
        time.sleep(2)

        # Use xdotool to type the command
        subprocess.run(['xdotool', 'type', 'docker exec -it matrix bash'])

        # Simulate pressing Enter
        subprocess.run(['xdotool', 'key', 'Return'])
        time.sleep(2)

        subprocess.run(['xdotool', 'type', 'poetry shell'])

        # Simulate pressing Enter
        subprocess.run(['xdotool', 'key', 'Return'])
        time.sleep(4)
        subprocess.run(['xdotool', 'type', command_1])

        # Simulate pressing Enter
        subprocess.run(['xdotool', 'key', 'Return']) 
        time.sleep(2)
 
        subprocess.run(['xdotool', 'type', command_2])

        # Simulate pressing Enter
        subprocess.run(['xdotool', 'key', 'Return'])
        time.sleep(2)

        subprocess.run(['xdotool', 'type', command_3])

        # Simulate pressing Enter
        subprocess.run(['xdotool', 'key', 'Return'])
        time.sleep(2)

        subprocess.run(['xdotool', 'type', command])

        # Simulate pressing Enter
        subprocess.run(['xdotool', 'key', 'Return'])
            

    def checkbox_board_option_action(self):
        # Handle board option selection
        if self.checkbox_board_option_var.get():
            # Deselect emulator option
            self.checkbox_emulator_option_var.set(False)

    def checkbox_emulator_option_action(self):
        # Handle emulator option selection
        if self.checkbox_emulator_option_var.get():
            # Deselect board option
            self.checkbox_board_option_var.set(False)
            
    def checkbox_12_inch_option_action(self):
        # handle 12 inch selection
        if self.checkbox_12_inch_option_var.get():
            # Deselect all other screen size 
            self.checkbox_10_4_inch_option_var.set(False)
            self.checkbox_10_1_inch_option_var.set(False)
            self.checkbox_9_inch_option_var.set(False)
            
    def checkbox_10_4_inch_option_action(self):
        if self.checkbox_10_4_inch_option_var.get():
            # Deselect all other screen size 
            self.checkbox_12_inch_option_var.set(False)
            self.checkbox_10_1_inch_option_var.set(False)
            self.checkbox_9_inch_option_var.set(False)
            
    def checkbox_10_1_inch_option_action(self):
        if self.checkbox_10_1_inch_option_var.get():
            # Deselect all other screen size 
            self.checkbox_12_inch_option_var.set(False)
            self.checkbox_10_4_inch_option_var.set(False)
            self.checkbox_9_inch_option_var.set(False)
              
    def checkbox_9_inch_option_action(self):
        if self.checkbox_9_inch_option_var.get():
            # Deselect all other screen size
            self.checkbox_12_inch_option_var.set(False)
            self.checkbox_10_4_inch_option_var.set(False)
            self.checkbox_10_1_inch_option_var.set(False)
    
    def checkbox_LHD_option_action(self):
        if self.checkbox_LHD_option_var.get():
            # Deselect all other screen size
            self.checkbox_RHD_option_var.set(False) 
       
    def checkbox_RHD_option_action(self):
        if self.checkbox_RHD_option_var.get():
            # Deselect all other screen size
            self.checkbox_LHD_option_var.set(False)
            
    def checkbox_CANAKIN_option_action(self):
        if self.checkbox_CANAKIN_option_var.get():
            # Deselect VSP option 
            self.checkbox_VSP_option_var.set(False)
            
    def checkbox_VSP_option_action(self):
        if self.checkbox_VSP_option_var.get():
            # Deselect CANAKIN option 
            self.checkbox_CANAKIN_option_var.set(False)
            
    def checkbox_ltr_option_action(self):
        if self.checkbox_ltr_option_var.get():
            # Deselect rtl option
            self.checkbox_rtl_option_var.set(False)
            
    def checkbox_rtl_option_action(self):
        if self.checkbox_rtl_option_var.get():
            # Deselect ltr option
            self.checkbox_ltr_option_var.set(False)
            
    def checkbox_Lawicel_option_action(self):
        if self.checkbox_Lawicel_option_var.get():
            # Deselect Korlan option
            self.checkbox_Korlan_option_var.set(False)
            
    def checkbox_Korlan_option_action(self):
        if self.checkbox_Korlan_option_var.get():
            # Deselect Korlan option
            self.checkbox_Lawicel_option_var.set(False)
    
    # Function FOr vehicle Config 
    def on_select_config(self,event):
        global selected_config
        selected_config = self.config_combo.get()
        print(f"Selected: {selected_config}")

    def update_options_config(self,event):
        # Get the typed string
        typed = self.config_combo.get()

        # Remove previous suggestions
        self.config_combo['values'] = []

        # Filter options based on the typed string
        self.filtered_options = [option for option in self.all_options if option.startswith(typed)]

        # Add matching suggestions
        self.config_combo['values'] = self.filtered_options

    def on_select_push_config(self, value):

        # Update the boolean variable based on user selection
        if "Yes" in value:
            self.is_push_config_enabled = True
        elif "No" in value:
            self.is_push_config_enabled = False

        # For testing purposes, print the updated boolean variable
        print("is_push_config_enabled:", self.is_push_config_enabled)
    
    # *******************************************************      
    def run_terminal_command(self):
        # Open a new terminal
        terminal_process = subprocess.Popen(['gnome-terminal'])

        # Wait for the terminal to open
        time.sleep(2)

        # Open the Matrix Container
        subprocess.run(['xdotool', 'type', 'docker exec -it matrix bash'])
        subprocess.run(['xdotool', 'key', 'Return'])
        
        # Set Poetry shell
        subprocess.run(['xdotool', 'type', 'poetry shell'])
        subprocess.run(['xdotool', 'key', 'Return'])
        time.sleep(2)

        return terminal_process


if __name__ == "__main__":
    root = tk.Tk()
    app = TestRunnerApp(root)
    root.mainloop()

