#!/bin/bash
# This Script is developed By Yasser JEMLI 
# Date : 8 jan 2023 


Flash_the_board() { 
    echo "Reboot into fastboot Mode"
    adb reboot bootloader
    sleep 1
    fastboot devices
    if [ $? -eq 0 ]; then
        echo "Executing file: $file"
        echo "Start the Flashing Process"
        "./$file"
        if [ $? eq 0 ]; then 
            echo "Exit The fastboot Mode Now and back to normal Mode"
            sleep 1
            fastboot reboot
            echo "Reboot is complete successfully ! :)"
        else 
            echo "Error ! : Facing an issue with flashing The board"
            zenity --error --text="An error occurred. Please try again."
            exit 1 
        fi
    
    # Search for a vehicle configs directory in the home directory
    directory_name="specific_directory_name"
    found_directory=$(find "$HOME" -type d -name "$directory_name")

    if [ -n "$found_directory" ]; then
        echo "Directory '$directory_name' found in $HOME: $found_directory"
        cd $found_directory
        # start Pushing the vehicle Configs 

    else
        echo "Directory '$directory_name' not found in $HOME"
        zenity --error --text="The vehicle config Folder is not Found , you can Push the config Manually if you want or try again."
    fi
    fi
}


echo " If something Goes wrong the script is designed to handle and give you  a clear Output"
echo " about the error in the console , if you're using the GUI mode then it will print a system popup also "
echo " For debugging or clarification please contact : yasserjamli37@gmail.com" 
echo " ************************* Starting now **********************************************" 

if [ "$1" == "" ];then
	echo " Invalid Input !!! "
	echo " You can choose between the two option"
	echo " either Run with GUI or NON GUI Mode , to accomplish this =>  "
	echo "     To run with GUI Mode ==> ./Board_flash.sh gui"
    echo "     To run with NON GUI Mode ==> ./Board_flash.sh non-gui"
    zenity --error \
    --width=450 \
    --height=200 \
    --text="No option is selected . expecting one argument 1  getting 0 ==>  Please Check the Console Output to understand this error"
    exit 1 
fi

if [ "$1" == "gui" ]; then
    # GUI mode: Prompt the user for file selection
    file=$(zenity --file-selection --title="Select a file")
    # Check if the user canceled file selection
    if [ $? -eq 1 ]; then
        echo "File selection canceled."
        zenity --error --text="No Fail is selected , we couldn't Procced with Flashing the Board"
        exit 1
    fi
    # Add execution rights to the selected file
    chmod +x "$file"
    # Execute the selected file
    echo "Checking If the Board is in wakeup status"
    adb devices
    if ["!$" == "1"];then 
        # The board is well connected 
        # Flash The board 
        Flash_the_board
    else
        echo "The board is not ON -------- Board in OFF state" 
        echo "Starting another thread to wakeUp the Board using wakeup script"
        # fetching the WakeUp script in the diectory 
        Current_dir=$(pwd)
        ./Current_dir/wake_up_script.sh &
        adb wait-for-device devices
        if [ $? -eq 0 ]; then 
            Flash_the_board
        fi
else
    if [ "$1" == "non-gui" ]; then
        # Non-GUI mode: Perform actions without GUI
        # Example: List files in the current directory
        echo "Non-GUI mode"
                
    fi
fi

