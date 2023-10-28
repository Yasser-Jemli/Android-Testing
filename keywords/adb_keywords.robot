*** Settings ***
Library    OperatingSystem
Library    AppiumLibrary
Library    Process
Library    String

*** Variables ***
${ADB_COMMAND}    adb devices | grep -v "List of devices attached" | cut -f 1
${OUTPUT_FILE}    /path/to/output.txt

*** Keywords ***
Get Android Device Name
    ${output} =    Run    ${ADB_COMMAND}
    Set Suite Variable    ${output.strip()}  # Remove leading/trailing whitespace
    [Return]    ${output.strip()}

Drop Down the Notification Bar 
    [Arguments]    ${device_name}
    Log     adb -s ${device_name} shell input swipe 500 0 500 1000 300 
    Run Process    adb -s ${device_name} shell input swipe 500 0 500 1000 300    shell=True