#!/bin/bash


# Wait for Appium to start (modify the sleep time as needed)
sleep 10

# Define the paths to your test suites
TEST_SUITE_1="test_suites/android_tests.robot"
TEST_SUITE_2="test_suites/other_tests.robot"

# Set your variables as command-line arguments
DEVICE_NAME="YourDeviceName"
PLATFORM_NAME="Android"
PLATFORM_VERSION="YourAndroidVersion"
APP_PACKAGE="com.example.yourapp"
APP_ACTIVITY=".MainActivity"

# Run the test suites
robot -d results -v DEVICE_NAME:"$DEVICE_NAME" -v PLATFORM_NAME:"$PLATFORM_NAME" -v PLATFORM_VERSION:"$PLATFORM_VERSION" -v APP_PACKAGE:"$APP_PACKAGE" -v APP_ACTIVITY:"$APP_ACTIVITY" "$TEST_SUITE_1"
robot -d results -v DEVICE_NAME:"$DEVICE_NAME" -v PLATFORM_NAME:"$PLATFORM_NAME" -v PLATFORM_VERSION:"$PLATFORM_VERSION" -v APP_PACKAGE:"$APP_PACKAGE" -v APP_ACTIVITY:"$APP_ACTIVITY" "$TEST_SUITE_2"


