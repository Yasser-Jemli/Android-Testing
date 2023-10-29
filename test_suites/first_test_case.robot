*** Settings ***
Resource     ../resources/config/android_config.robot
Resource    ../keywords/adb_keywords.robot

*** Test Cases ***
Get Device Name Test

    Check for Connected ADB Device
    ${device_name} =    Get Android Device Name
    Drop Down the Notification Bar    ${device_name}
