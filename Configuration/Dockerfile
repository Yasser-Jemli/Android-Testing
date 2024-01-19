# Us# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory to /app
WORKDIR /app

# Install required dependencies
RUN apt-get update && \
    apt-get install -y python3-venv python3-pip

# Create and activate a virtual environment
RUN python3 -m venv venv
RUN . venv/bin/activate

# Install Robot Framework and AppiumLibrary inside the virtual environment
RUN pip install -v robotframework
RUN pip install -v robotframework-appiumlibrary

# Expose the Appium server port
EXPOSE 4723

# Set the Appium server URL as an environment variable
ENV APPIUM_SERVER_URL http://localhost:4723/wd/hub

# Create a symbolic link to adb on the host machine
RUN ln -s /usr/local/bin/adb /app/local-adb

# Add the local-adb directory to the PATH
ENV PATH="/usr/bin/:/app/"

# Specify the default command to run when the container starts
CMD ["bash", "-c", "source venv/bin/activate && echo 'Docker container is ready. You can now manually execute your tests.' && exec bash"]
