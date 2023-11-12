# Use an official Node.js runtime as a parent image
FROM node:latest

# Set the working directory to /app
WORKDIR /app

# Install Appium and other dependencies
RUN npm install -g appium
RUN npm install -g appium-doctor

# Install Python and pip
# Install required system dependencies
RUN apt-get update && \
    apt-get install -y python3-venv


# Install Robot Framework and AppiumLibrary
RUN pip install -v robotframework
RUN pip install -v robotframework-appiumlibrary


# Expose the Appium server port
EXPOSE 4723

# Set the Appium server URL as an environment variable
ENV APPIUM_SERVER_URL http://localhost:4723/wd/hub

# Run the Robot Framework tests
CMD ["robot", "/app/tests"]

