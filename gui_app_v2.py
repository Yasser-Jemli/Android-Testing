import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import subprocess
import signal
from tkinter import filedialog , messagebox

root = tk.Tk()
root.title("HMI_IAT : Test Runner")

selected_file_path = ""  # Variable to store the selected docker-compose file path
docker_process = None  # Variable to store the Docker Compose process
selected_config = None # Variable to store the selected Config
select_hand_driving = None # Variable to store the selected Hand_driving
selected_id = None

def handle_interrupt_signal(signum, frame):
    print("Received signal:", signum)
    if signum == signal.SIGINT:  # Handle Ctrl+C (KeyboardInterrupt)
        # Perform necessary actions upon receiving Ctrl+C
        print("Ctrl+C (KeyboardInterrupt) received")
        # Handle cleanup or other actions here
        root.quit()

# Logic to run the command inside the docker 
def execute_command_in_container(container_name, command):
    try:
        # Command to open a terminal in the specified Docker container and execute a command
        subprocess.run(['docker', 'exec', '-it', container_name, 'bash', '-c', command], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command in container: {e}")
    # Replace 'your_container_name' with the actual name of your Docker container
    container_name = 'your_container_name'

    # Replace 'your_command' with the command you want to execute
    command_to_execute = 'ls /'

    execute_command_in_container(container_name, command_to_execute)

def on_select_test_id(event):
    global selected_id
    selected_id = test_id_combo.get()
    print(f"Selected ID: {selected_id}")

def search_ids():
    search_text = search_entry.get()
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
    test_id_combo['values'] = []

    # Add found IDs to the Combobox
    test_id_combo['values'] = tuple(found_ids)

def clear_previous_test_id_search_results():
    test_id_combo['values'] = ()

def on_select_can(value):
    selected_label_can.config(text=f"Selected CAN _Type : {value}")

def on_select_screen_size(value):
    selected_label_screen_size.config(text=f"Selected Screen Size: {value}")

def on_select_hand_driving(value):
    global select_hand_driving
    selected_label_hand_driving.config(text=f"Selected HAND_DRIVING : {value}")
    select_hand_driving = value

def on_select_target(value):
    selected_label_target.config(text=f"Selected Target : {value}")

def on_select_config(event):
    global selected_config
    selected_config = config_combo.get()
    print(f"Selected: {selected_config}")

def update_options_config(event):
    # Get the typed string
    typed = config_combo.get()

    # Remove previous suggestions
    config_combo['values'] = []

    # Filter options based on the typed string
    filtered_options = [option for option in all_options if option.startswith(typed)]

    # Add matching suggestions
    config_combo['values'] = filtered_options

def on_select_push_config(value):
    selected_push_config_state.config(text=f"Select Your push config state here => : {value}")

def run_docker_test():
    global selected_config
    global select_hand_driving
    global selected_id

    try:
        test_process = subprocess.Popen(["docker", "exec", "-it", "matrix", "bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Send commands to the Docker container
        commands = [
            "poetry shell",
            f"export CONFIG={selected_config}",  # Example command to list files
            f"export HAND_DRIVING={select_hand_driving}",
            f"export LANGUAGE=en", # Add your additional command to be executed inside the Docker container
            f"robot --test \"{selected_id}\" -v protocol:VSP -v variant:FullNav -v display_size:12 -v text_direction:ltr -v screenshots:Yes -v target:emulator -v hotspot_name:renault_hotspot -v hotspot_password:renault@1234 hmi_iat/Testcases"  
            ]

        for cmd in commands:
            output, error = test_process.communicate(input=f"{cmd}\n")

            # Print the output and error messages if any
            if output:
                print(f"Output: {output}")
            if error:
                print(f"Error: {error}")

        test_process.stdin.close()  # Close the stdin pipe
        test_process.wait()  # Wait for the process to finish
        
    except Exception as e:
        print(f"Error: {e}")

def run_docker_compose():
    global selected_file_path, docker_process
    if not selected_file_path:
        status_bar.config(bg="red")
        status_label.config(text="No Docker Compose file selected.")
    else:
        try:
            docker_process = subprocess.Popen(["docker-compose", "-f", selected_file_path, "up"])
            status_bar.config(bg="green")
            status_label.config(text="Docker Compose file is running...")
        except Exception as e:
            status_bar.config(bg="red")
            status_label.config(text=f"Error starting Docker Compose file: {e}")

def stop_docker_compose():
    global docker_process, selected_file_path
    if docker_process is None:
        try:
            docker_process.terminate()
            docker_terminate = subprocess.Popen(["docker-compose","-f",selected_file_path,"down"])
            status_bar.config(bg="red")
            status_label.config(text="Docker Compose file stopped.")
        except Exception as e : 
            status_bar.config(bg="red")
            status_label.config(text=f"Error stopping Docker env")

def on_closing():
    global docker_process
    if docker_process and docker_process.poll() is None:
        docker_process.terminate()
    root.destroy()


def Run_test():
    global selected_file_path
    selected_config_var = config_combo.get()
    print(f"Selected value: {selected_config_var}")
    on_select_test_id(Run_test)
    run_docker_test()

    

def select_docker_compose_file():
    global selected_file_path
    file_path = filedialog.askopenfilename(filetypes=[("Docker Compose Files", "docker-compose.yml")])
    if file_path:
        # Do something with the selected file path, like printing it
        confirmation_label.config(text=f"Selected Docker Compose file: {file_path}")
        print("Selected Docker Compose file:", file_path)
        selected_file_path = file_path
    else :
        status_bar.config(bg="red")
        status_label.config(text="No Docker Compose file selected.")

# -----------------  All frames are definied Here  -------------------------------------
# Frame for Test ID search 
frame = tk.Frame(root)
frame.grid(row=0,column=0, sticky="w")

# Frame to select your config docker-compose file 

frame_docker_compose =tk.Frame(root)
frame_docker_compose.grid(row=1,column=1,sticky="w")

# frame for Test Running  
frame_command_generator = tk.Frame(root)
frame_command_generator.grid(row=0,column=1, sticky="w")

# Frame for CAN Configuration
frame_can = tk.Frame(root)
frame_can.grid(row=1,column=0, sticky="w")

# frame For screen Size 
frame_screen_size = tk.Frame(root)
frame_screen_size.grid(row=2,column=0)

# frame for HAND Driving Mode 
frame_hand_driving = tk.Frame(root)
frame_hand_driving.grid(row=3,column=0)

# frame for select Target 
frame_target = tk.Frame(root)
frame_target.grid(row=4,column=0)

# frame for CONFIG selection and wiether you want to push vehicle config or not ! 
frame_config = tk.Frame(root)
frame_config.grid(row=5 , column=0)

# ----------------- Command Generator --------------------------
command_generator_label = tk.Label(frame, text="Click Here to generat the command ")
command_generator_label.grid(row=0, column=0, sticky="w")

command_generator_button = tk.Button(frame_command_generator, text="Run the Test", command=Run_test)
command_generator_button.grid(row=0, column=1, padx=5)

# --------------- Search Freame ----------------------------------------
search_label = tk.Label(frame, text="Enter ID (partial or full):")
search_label.grid(row=0, column=0, sticky="w")

search_entry = tk.Entry(frame, width=30)
search_entry.grid(row=0, column=1, padx=5)

search_button = tk.Button(frame, text="Search", command=search_ids)
search_button.grid(row=0, column=2, padx=5)

test_id_label = tk.Label(frame , text="Your Target Test Case ID ")
test_id_label.grid(row=1,column=0)

test_id_combo = ttk.Combobox(frame, width=30)
test_id_combo.grid(row=1 , column=1)
test_id_combo.bind("<<ComboboxSelected>>", on_select_test_id)

clear_button = tk.Button(frame, text="Clear", command=clear_previous_test_id_search_results)
clear_button.grid(row=0, column=3, pady=5)

#-------------------- Select Your can Type Frame label & ports --------------------------------

selected_label_can = tk.Label(frame_can, text="Selected CAN: ")
selected_label_can.grid(row=0,column=0)

selected_option_can = tk.StringVar(root)
selected_option_can.set("Select an option")

options = ["Korlan", "Lawicel"]

dropdown = tk.OptionMenu(frame_can, selected_option_can, *options, command=on_select_can)
dropdown.grid(row=0, column=1)

Control_CAN0 = tk.Label(frame_can, text="Select The port 'ttyUSB' of Your V-CAN => CAN0 ")
Control_CAN0.grid(row=1,column=0, sticky="w")

can0_entry = tk.Entry(frame_can, width=10)
can0_entry.grid(row=1, column=1, sticky="w")

Control_CAN1 = tk.Label(frame_can, text="Select The port 'ttyUSB' of Your M-CAN => CAN1 ")
Control_CAN1.grid(row=2,column=0, sticky="w")

can1_entry = tk.Entry(frame_can, width=10)
can1_entry.grid(row=2 , column=1 , sticky="w")

# ------------- Screen size selection --------------
selected_label_screen_size = tk.Label(frame_screen_size, text="Selected Screen Size : ")
selected_label_screen_size.grid(row=0,column=0, sticky="w")

selected_option_screen_size = tk.StringVar(root)
selected_option_screen_size.set("Select an option")

options = ["12 inch", "10.4 inch","10.1 inch", "9 inch"]

dropdown = tk.OptionMenu(frame_screen_size, selected_option_screen_size, *options, command=on_select_screen_size)
dropdown.grid(row=0, column=1, sticky="w")

# ---------------------- Hand_Driving option ------------------------- 
selected_label_hand_driving = tk.Label(frame_hand_driving, text="Selected HAND_DRIVING: ")
selected_label_hand_driving.grid(row=0,column=0,sticky="w")

selected_option_hand_driving = tk.StringVar(root)
selected_option_hand_driving.set("Select an option")

options = ["RHD", "LHD"]

dropdown = tk.OptionMenu(frame_hand_driving, selected_option_hand_driving, *options, command=on_select_hand_driving)
dropdown.grid(row=0, column=1)

# ----------------------- Target Option ----------------------------------------
selected_label_target = tk.Label(frame_target, text="Selected Your Target : ")
selected_label_target.grid(row=0,column=0,sticky="w")

selected_option_target = tk.StringVar(root)
selected_option_target.set("Select an option")

options = ["board", "emulator"]

dropdown = tk.OptionMenu(frame_target, selected_option_target, *options, command=on_select_target)
dropdown.grid(row=0, column=1,sticky="w")

# ---------- Config Selected ----------------------------------------------------

#  options
all_options = [
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

select_your_vehicle_config = tk.Label(frame_config, text="Select Your vehicle Config Here => ")
select_your_vehicle_config.grid(row=0,column=0,sticky="w")

# Initialize the Combobox
config_combo = ttk.Combobox(frame_config, values=[], width=40)
config_combo.grid(row=0,column=1)
config_combo.bind("<KeyRelease>", update_options_config)  # Bind the event to handle typing
config_combo.bind("<<ComboboxSelected>>", on_select_config)  # Bind the event for selection

#  Button to wiether you want to push Config Or not ?
selected_push_config_state = tk.Label(frame_config, text="Select If you want to push Vehicle Config or not : ")
selected_push_config_state.grid(row=1,column=0,sticky="w") 

selected_push_config_state = tk.StringVar(root)
selected_push_config_state.set("Select an option")

options = ["Yes : push vehicle config ", "No : don't push vehicle Config "]

dropdown = tk.OptionMenu(frame_config, selected_push_config_state, *options, command=on_select_push_config)
dropdown.grid(row=1, column=1,sticky="w")

# button for select docker-compose file 
select_docker_compose = tk.Button(frame_docker_compose,text="Select Your Docker_compose file",command=select_docker_compose_file)
select_docker_compose.grid(row=0,column=0)

# Confirmation Label for Docker_compose file selection
confirmation_label = tk.Label(frame_docker_compose, text="Selected Docker Compose File => ", fg="green")
confirmation_label.grid(row=1,column=0,sticky="w")

# Status Bar For Docker_Compose Indication 
global status_bar, status_label
status_bar = tk.Label(frame_docker_compose, text="Docker env status ", relief=tk.SUNKEN, anchor=tk.W, bg="red")
status_bar.grid(row=2,column=0)
    
status_label = tk.Label(frame_docker_compose, text="No Docker Compose file selected.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.grid(row=3,column=0)

docker_compose_up =tk.Button(frame_docker_compose,text="docker compose Up !", command=run_docker_compose)
docker_compose_up.grid(row=4,column=0)


docker_compose_down = tk.Button(frame_docker_compose, text="docker compose Down !" , command=stop_docker_compose)
docker_compose_down.grid(row=5,column=0)

root.protocol("WM_DELETE_WINDOW", on_closing)

# Register the signal handler for KeyboardInterrupt (Ctrl+C)
signal.signal(signal.SIGINT, handle_interrupt_signal)

# ---------- Mainloop ----------------------------
root.mainloop()


