#!/bin/bash
# This Script is developed By Yasser JEMLI IPN 
# Date : 8 jan 2023
 
# Define log file : will containe all info about board script and executing steps and info of this script
LOG_FILE="log_file_for_board_flashing.txt"


log_info() {
    local timestamp=$(date +"%Y-%m-%d %T")
    echo "[$timestamp] INFO: $1" >> "$LOG_FILE"
}


log_debug() {
    local timestamp=$(date +"%Y-%m-%d %T")
    echo "[$timestamp] DEBUG: $1" >> "$LOG_FILE"
}


log_error() {
    local timestamp=$(date +"%Y-%m-%d %T")
    echo "[$timestamp] ERROR: $1" >> "$LOG_FILE"
}


Flash_the_board() {
    log_info "Rebooting the board to fastboot mode"
    adb reboot bootloader
    sleep 5
    fastboot devices
    sleep 15
    if [ $? -eq 0 ]; then
        log_info "Start the Flashing Process"
        log_info "Executing file: $file"
        "./$file"
        if [ $? eq 0 ]; then 
            log_info "Exit The fastboot Mode Now and back to normal Mode"
            sleep 1
            fastboot reboot
            if [ $? -eq 0 ]; then 
                log_info "Reboot is complete successfully ! :)"
                sleep 5
            else 
                log_error "Facing error while exiting the Fastboot mode"
                zenity --error --text="An error occurred while trying to exit the fastboot mode"
            fi
        else 
            log_error "Error ! : Facing an issue with flashing The board"
            zenity --error --text="An error occurred while flashing The board . Please try again & check Your flashing script."
            exit 1 
        fi
        # Search for a vehicle configs directory in the home directory
        # note this will look of the vehicle Configs folder in the HOME directory only
        log_debug "Note : the vehicle_configs  directory need to be in HOME diretory"
        directory_name="vehicle_configs"
        found_directory=$(sudo find "$HOME" -maxdepth 1 -type d -name "vehicle_configs")

        if [ -n "$found_directory" ]; then
            log_info "Directory '$directory_name' found in $HOME: $found_directory"
            cd $found_directory
            # start Pushing the vehicle Configs ; check adb availble First
            adb devices 
            if [ "$?" -eq 0 ];then
                log_info "adb device is available , start Pushing the Config Now"
                # Logic to push the vehicle Config
                # --------------------------
                # ********************************************
                if [ "$?" -eq 0]; then 
                    log_info " Pushing Config is  success"
                    log_info " the board is ready to use ! Thanks ! "
                    zenity --info --width=450 --height=200 --text="The Board is Ready to be used , Thanks ! "
                    exit 0 
                else
                    log_error "Facing an issue while Pushing the Config"
                    log_error "You can try to push them manually , the board is flashed Correctly !"
                    zenity --error \
                    --width=450 \
                    --height=200 \
                    --text="We are facing an issue while trying to Push the configs , You can try to push them manually , thanks ! "
                fi
            else
                echo "no adb device Found"
                log_debug "No adb device Found"
                # to develope another Logic Here
            fi
        else
            log_error "Directory '$directory_name' not found in $HOME"
            zenity --error --text="The vehicle config Folder is not Found in the home direcoty , please set the vehicle config folder to the home directory or you can Push the config Manually."
        fi
    else 
        log_error "The board is not switching to fastboot Mode"
        zenity --error --text="Board Not switching to fastboot mode , exiting the script with Error"
        exit 1
    fi
}

 

echo " ***********************************************************************************" 
echo " ------------------------    ivi Flashing ----------------------------------------- "
echo " If something Goes wrong the script is designed to handle and give you  a clear Output"
echo " about the error in the console , if you're using the GUI mode then it will print a system popup also "
echo " ************************* Starting now **********************************************" 
echo " For better understanding of this script you can use the help option "
echo "   Run => ./Board_flashing.sh -help"

if [ "$1" == "-help" ]; then 
    echo "This is the help information for your script."
    echo ""
    echo " Usage: ./Board_flashing.sh [option 1] [option2]"
    echo " Note : the two Option are requiered otherwise the script will be not working as expected ! " 
    echo ""
    echo "Option1:"
    echo ""
    echo "  gui     ,   Run the Script with GUI mode will Provide an inforamtion about the Flashing Process with a system popup in case of errors."
    echo ""
    echo "  non-gui ,   This is an implemntation for the CI part : "
    echo "              => this will display a console message instead of popup and no user action will be required or a system popup will be displayed"
    echo ""
    echo "Option2 :"
    echo ""
    echo " This option is for selecting the can type that you will be using"
    echo ""
    echo " lawicel  , it will considere the can used for your setup is Lawicel type "
    echo " korlan   , it will considere the can used for your setup is korlan type "
    echo ""
    echo " More details about how to use your script and its options. "
    echo " you can also check the Readme File in the hmi_iat Project " 
    echo " For any issues or improvement please contact : yasser.jamli@celadodc-rswl.com"
    exit 0 
fi

if [ "$1" == "" ]; then
    log_error " Invalid Input !!! "
    log_info "Please see the Help menu " 
    log_debug "Run ==> ./Board_flashing.s -help"
    log_error " Exiting ........ "
    zenity --error \
    --width=450 \
    --height=200 \
    --text="No option is selected . expecting two argument 2  getting 0 ==>  Please Check the Log file to understand this error"
    exit 1 
fi
if [ "$2" == "" ]; then 
    echo " Invalid Input !!! "
    echo " Invalid Input !!! "
    echo "Please see the Help menu " 
    echo "Run ==> ./Board_flashing.s -help"
    echo " Exiting ........ "
    zenity --error \
    --width=450 \
    --height=200 \
    --text="No option is selected for the can type . expecting two argument 2  getting 1 ==>  Please Check the Log file to understand this error" 
    exit 1 
fi 

if [ "$1" == "gui" ]; then
    # GUI mode: Prompt the user for file selection
    file=$(zenity --file-selection --title="Select a file")
    # Check if the user canceled file selection
    if [ $? -eq 1 ]; then
        echo "File selection canceled."
        zenity --error --text="No File is selected , we couldn't Procced with Flashing the Board"
        exit 1
    fi
    # Add execution rights to the selected file
    chmod +x "$file"
    # Execute the selected file
    echo "Checking If the Board is in wakeup status"
    adb devices
    if [ $? -eq 0 ]; then 
        # The board is well connected
        # Flash The board
        Flash_the_board
    else
        echo "The board is not ON -------- Board in OFF state" 
        echo "Starting another thread to wakeUp the Board using wakeup script"
        echo "can_configuration"
        echo "Can-V must be connected to ttyUSB0 , otherwise the script will fail"
        if [ "$2" == "lawicel" ]; then 
            sudo slcand -o -c -f -s6 /dev/ttyUSB0 can0
            # impelementing a logic to check if the can is well connected or not ....
            if [ $? -eq 0 ]; then 
                sudo ifconfig can0 up
                if [ $? -eq 0 ]; then 
                    echo "Can is well configured"
                else 
                    log_error " Error in can configuration"
                    log_debug " you may be forgot your 120ohm resistor or you have a bad connection in your can2usb hardware"
                    log_debug " please check and re-run again"
                    log_error " Exiting ... "
                    zenity --error \
                    --width=450 \
                    --height=200 \
                    --text="Error in setting the Interface to Up state,check the message printed on your console"
                    exit 1
                fi
            else 
                log_error " Error in can configuration ! "
                log_debug " Please Make Sur that the ttyUSB0 is assigned correctly to CAN-V"
                log_debug " if the ttyUSB0 is connected to other can , please considere rebooting your PC " 
                log_debug " and plugg the can-v ==> can0 First to be assigned to ttyUSB" 
                log_debug " and then you could run the script again "
                log_error " Exiting ... " 
                zenity --error \
                --width=450 \
                --height=200 \
                --text="Error in can configuration => Please Check the Log file to understand this error , thanks "
                exit 1 
            fi 
        else
            sudo ip link set can0 up type can bitrate 500000 sample-point 0.875
            # implementing a logic to check if the can is well connected or not ...
            if [ $? -eq 0 ]; then 
                echo " CAN is well configured " 
            else 
                log_error " Error in can configuration ! "
                log_debug " Please Make Sur that the ttyUSB0 is assigned correctly to CAN-V"
                log_debug " if the ttyUSB0 is connected to other can , please considere rebooting your PC " 
                log_debug " and plugg the can-v ==> can0 First to be assigned to ttyUSB" 
                log_info  " and then you could run the script again "
                log_error " Exiting .... "
                zenity --error \
                --width=450 \
                --height=200 \
                --text="Error in can configuration => Please Check the Log file to understand this error , thanks "
                exit 1
            fi
        fi
        # fetching the WakeUp script in the diectory
        Current_dir=$(pwd)/HLK/remote_services/can
        ./$Current_dir/launch_start_sequence.sh &
        adb wait-for-device devices
        if [ $? -eq 0 ]; then 
            log_info " Starting the Flash Process of the board" 
            Flash_the_board
            log_info " Board is flashed Succesfully and vehicle config is pushed successfuly"
            log_info " The board is ready to use " 
            exit 0
        else
            log_error " the Board is not in wake up state even after launching the wake_up script"
            zenity --error --width=450 --height=200 --text=" Board is not waking Up ,Exiting with error => please check the Log file , thanks" 
            exit 1
        fi
    fi
else
    if [ "$1" == "non-gui" ]; then
        # Non-GUI mode: Perform actions without GUI
        # Example: List files in the current directory
        echo "Non-GUI mode"         
    fi
fi


