*** Settings ***
Resource     ../resources/config/android_config.robot
Resource    ../keywords/adb_keywords.robot


*** Test Cases ***
Get Device Name Test

    # #Check for Connected ADB Device
    # #${device_name} =    Get Android Device Name
    # # Drop Down the Notification Bar    ${device_name}
    # # Raise up the Notification Bar     ${device_name}
    # # Get Current User Profile name   ${device_name}    # robotcode: ignore
    # # Get Current User Profile ID    ${device_name}    # robotcode: ignore
    # Check If Text Is Present
    Display Toast with Auto-Close    message= Run is Failed 
