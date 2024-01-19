*** Settings ***

Library    OperatingSystem
# Library    AppiumLibrary
Library    Process
Library    String
Library    XML
Library    Process
Library    SeleniumLibrary

*** Variables ***

${ADB_COMMAND}    adb devices | grep -v "List of devices attached" | cut -f1 | tr -d '[:space:]'
${XML File Path}    ${CURDIR}/ui_dump.xml
${Search Text}      Township
${Local Dump File}      /home/celadodc-rswl.com/yasser.jamli/Android-Testing/ui_dump.xml
${ADB}    adb

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


Create New Profile Adb
    [Arguments]    ${profile_name}
    [Documentation]    Create New Profile with the given name 
    ${user_id}    Run Process        adb shell pm create-user ${profile_name} | cut -d ' ' -f 5        shell=True
    Log    Creating new Profile with the Name : ${profile_name} and ID : ${user_id.stdout}
    Log To Console     ${\n}Creating new Profile with the Name : ${profile_name} and ID : ${user_id.stdout}
    Run Process    adb shell am switch-user ${user_id.stdout}    shell=True
    Run Keyword And Ignore Error    Tap Element    ${outlinr/rlb_vehicle_updates_later}    access=TEXT    scroll=NO
    Log    Switched to user Profile ${profile_name} with ID : ${user_id.stdout}
    DO WAIT    1000
    Run Keyword And Ignore Error    Check Elements Displayed    ${setupwizard suw_welcome begin}    scroll=NO    Wait=500ms    
    DO WAIT    1000
    


List and Switch User Profile
    [Arguments]    ${selected_name}
    [Documentation]    list Profiles to get the ID of the given name profile and then switch to that profile using extracted ID 
    ${output} =    Run Process    adb shell pm list users | cut -d '{' -f2 | cut -d '}' -f1 | cut -d ':' -f1,2     shell=True
    ${lines} =  Split To Lines  ${output.stdout}
    Log     extracted Profile : ${lines}
    Log To Console    ${\n} extracted Profile : ${lines}
    ${user_ids_and_profiles} =  Create Dictionary
    FOR  ${line}  IN  @{lines}
            ${user_id}  ${profile_name} =  Split String  ${line}  :  
            Set To Dictionary  ${user_ids_and_profiles}  ${user_id}  ${profile_name}
    END
    ${user_info} =  Get Dictionary Items  ${user_ids_and_profiles}
    FOR  ${user_id}  ${profile_name}  IN  @{user_info}
        Run Keyword If  '${profile_name}' == '${selected_name}'
            ...  Run Keyword      Run Process      adb shell am switch-user ${user_id}        shell=True                
    END

List and remmove User Profile
    [Arguments]    ${selected_name}
    [Documentation]    list Profiles to get the ID of the given name profile and then remove that profile using extracted ID 
    ${output} =    Run Process    adb shell pm list users | cut -d '{' -f2 | cut -d '}' -f1 | cut -d ':' -f1,2     shell=True
    ${lines} =  Split To Lines  ${output.stdout}
    Log     extracted Profile : ${lines}
    Log To Console    ${\n} extracted Profile : ${lines}
    ${user_ids_and_profiles} =  Create Dictionary
    FOR  ${line}  IN  @{lines}
            ${user_id}  ${profile_name} =  Split String  ${line}  :  
            Set To Dictionary  ${user_ids_and_profiles}  ${user_id}  ${profile_name}
    END
    ${user_info} =  Get Dictionary Items  ${user_ids_and_profiles}
    FOR  ${user_id}  ${profile_name}  IN  @{user_info}
        Run Keyword If  '${profile_name}' == '${selected_name}'
            ...  Run Keyword      Run Process      adb shell pm remove-user ${user_id}        shell=True                
    END

*** Keywords ***
Check If Text Is Present
    Run ADB Commands
    Parse And Check Text

Run ADB Commands
    ${result1}=    Run Process    ${ADB}    shell    uiautomator dump /sdcard/ui_dump.xml    shell=True
    Log    ${result1.stdout}
    ${result2}=    Run Process    ${ADB}    pull     /sdcard/ui_dump.xml        shell=True
    Log    ${result2.stdout}
    


Parse And Check Text
    ${tree}=    XML.Parse Xml    ${Local Dump File}
    ${root}=    XML.Get Element    ${tree}
    ${elements}=    XML.Get Elements    ${root}    node
    FOR    ${elem}    IN    @{elements}
        Log    ${elem.tag}  # Log the tag of each element
        ${attributes}=    XML.Get Element Attributes    ${elem}  # Log all attributes of each element
        Log    ${attributes}
        ${text}=    XML.Element To String    ${elem}  # Log the complete XML content of each element
        Log    ${text}
    END
    # IF    ${found}    
    #     Log    Text '${Search Text}' found on the screen.
    # ELSE
    #     Fail   Text '${Search Text}' not found on the screen.
    # END

Dump screen and get the current Time using Adb 
    [Arguements]    ${specifique_ressource_ID}
    [Documentation]    this is a worearound for dumping the current activity and extracted the Text attribute of a specifique Ressouce ID 
    # This command to insure that the adb will run correctly and we will get the UI dump successfully 
    Run Process    adb reconnect      shell=True
    DO WAIT    1000
    ${output}=    Run Process    adb wait-for-device shell uiautomator dump /sdcard/window_dump.xml        shell=True
    Log    ${output.stdout}
    ${output}=    Run Process    adb wait-for-device pull /sdcard/window_dump.xml          shell=True
    Log    ${output.stdout}
    ${output}=    Run Process    python3 Get_element_Text_Attribut-By_ID.py window_dump.xml ${specifique_ressource_ID}        shell=True
    Log    ${output.stdout}
    @{values}=    Split String    ${output.stdout}    
    Log Many    @{values}
    # Cleaning up the Board of the previous UI dump 
    ${output}=      Run Process    adb shell rm -rf /sdcard/window_dump.xml    shell=True
    # Delet the current UI dump XML file from Hmi_iat Directory
    ${output}=      Run Process    rm -rf window_dump.xml              shell=True
    [Return]    ${value_1}     ${value_2} 


Display Toast Popup
    Open Browser    https://www.youtube.com/watch?v=E3iliL2OH2o    Chrome
    Execute JavaScript    alert('This is a toast popup!')
    DO WAIT    7000
    Close Browser

# For Mac OS or windows System Notif Popup
Display System Notification For windows & Mac OS 
    [Arguments]    ${message}
    Run    osascript -e 'display notification "${message}" with title "My Robot Framework Notification"'

# For Linux System Notif Popup 
Run System Notification For LInux 
    [Arguments]    ${message}
    Run    notify-send "My Robot Framework Notification" "${message}"

# For Linux System : Alret Popup 
Display Alert Popup
    [Arguments]    ${message}
    Run    zenity --info --text="${message}" --title="Alert"

Display Toast with Auto-Close
    [Arguments]    ${message}    ${duration}=1    ${Timeout}=5
    ${message}=    Set Variable    "This is a toast message"
    ${title}=    Set Variable    "Toast Popup"
    ${command}=    Set Variable    zenity --info --text=${message} --title=${title}
    Run Process    ${command}       timeout=${Timeout}     shell=True
    Sleep    ${duration}
    Get Zenity PID and Kill Process  # Close the zenity notification window
    # This HLK need to be updated and using the the bash variable $? to see the return of the command
    # This was Fixed By adding the HLK Get Zenity PID and Kill Process

Get Zenity PID and Kill Process
    ${ps_output}=    Run    ps -axl | grep "zenity --info"
    @{ps_lines}=    Split To Lines    ${ps_output}
    FOR    ${line}    IN    @{ps_lines}
        ${columns}=    Split String    ${line}
        ${pid}=    Set Variable    ${columns[2]}
        Run Keyword If    "${pid}" != "PID"    Run Process     kill -9 ${pid}    shell=True
    END