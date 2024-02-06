import subprocess
import os 
import sys 

def starting_a_new_docker_image():
    pid = os.fork()
    if pid == 0 : 
        os.execl("user/bin/gnome-terminal","docker exec -it matrix bash")
    else : 
        # Parent process
        os.waitpid(pid, 0)
        print("Parent process continues...")

starting_a_new_docker_image()
# def run_docker_command(command):
#     try:
#         # Run the command directly in the Docker container, appending '&' to run in the background
#         process = subprocess.Popen(['docker', 'exec', '-i', 'matrix', 'bash', '-c', f'poetry run {command}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

#         # Read and print the PID
#         pid = process.communicate()[0].strip()
#         print(f"PID of the subprocess shell: {pid}")

#         # Read and print the output
#         output, error = process.communicate()
#         print(output)

#         # Check for errors
#         if process.returncode != 0:
#             print(f"Error executing command: {command}")
#             print(f"Error output: {error}")

#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     # commands = [
#     #     'export HAND_DRIVING=LHD',
#     #     'export LANGUAGE=en',
#     #     'robot --test "XXX" -v protocol:CANAKIN -v variant:FullNav -v display_size:9 -v text_direction:ltr -v screenshots:Yes -v target:emulator -v hotspot_name:renault_hotspot -v hotspot_password:renault@1234 hmi_iat/Testcases'
#     # ]

    # for command in commands:
    #     run_docker_command(command)
