*** Settings ***

Library    OperatingSystem
Library    AppiumLibrary
Library    Process
Library    String

*** Variables ***

${ADB_COMMAND}    adb devices | grep -v "List of devices attached" | cut -f1 | tr -d '[:space:]'


*** Keywords ***

Check for Connected ADB Device
    ${output}    Run Process    adb devices    shell=True

    Log    ADB Devices Output: ${output.stdout}

    ${is_device_connected}    Evaluate    "device" in $output.stdout

    Run Keyword If    ${is_device_connected}    Log    ADB Device is Connected
    ...    ELSE    Fail    No ADB Device Connectedvice Connected  adb device     shell=True

Get Android Device Name
    ${output} =    Run    ${ADB_COMMAND}
    Set Suite Variable    ${output}  # Remove leading/trailing whitespace
    [Return]    ${output}

Drop Down the Notification Bar 
    [Arguments]    ${device_name}
    ${notification_bar_state_before}    Run Process    adb -s ${device_name} shell dumpsys statusbar | grep mDisableRecords.size     shell=True
    Log    ${notification_bar_state_before.stdout}
    Run Process        adb -s ${device_name} shell service call statusbar 1    shell=True
    Sleep    1s
    ${notification_bar_state_after}    Run Process     adb -s ${device_name} shell dumpsys statusbar | grep mDisableRecords.size     shell=True
    Log    ${notification_bar_state_after.stdout}
    Should Not Be Equal    ${notification_bar_state_before.stdout}    ${notification_bar_state_after.stdout}    Notification bar not opened

Raise up the Notification Bar
    [Arguments]    ${device_name}
    ${notification_bar_state_before}    Run Process    adb -s ${device_name} shell dumpsys statusbar | grep mDisableRecords.size    shell=True
    Log    ${notification_bar_state_before.stdout}
    Run Process    adb -s ${device_name} shell service call statusbar 2   shell=True
    Sleep  1s
    ${notification_bar_state_after}    Run Process    adb -s ${device_name} shell dumpsys statusbar | grep mDisableRecords.size    shell=True
    Log    ${notification_bar_state_after.stdout}
    Should Not Be Equal    ${notification_bar_state_before.stdout}    ${notification_bar_state_after.stdout}    Notification bar not opened

Get Current User Profile name
    [Arguments]    ${device_name}
    ${current_user_line}    Set Variable    ${EMPTY}

    # Use sed to extract the line containing "running" and cut to get the user ID
    ${current_user_line}    Run Process    adb -s ${device_name} shell pm list users | sed -n '/running/p' | cut -d ':' -f 2 | tr -d ' '    shell=True
    
    Run Keyword If    '${current_user_line}' == ''    Fail    Unable to determine current user
    
    Log    Current User ID: ${current_user_line.stdout}

Get Current User Profile ID
    [Arguments]    ${device_name}
    ${user_list}    Run Process    adb -s ${device_name} shell pm list users    shell=True
    ${user_id}    Set Variable    ${EMPTY}
    
    FOR    ${line}    IN    @{user_list.stdout.splitlines()}
        ${user_id_match}    Get Regexp Matches    ${line}    UserInfo{([0-9]+):
        Run Keyword If    ${user_id_match}    Set Variable    ${user_id}    ${user_id_match[0][1]}
    END
    
    Log    Current User ID: ${user_id}