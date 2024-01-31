import subprocess

def run_docker_commands(commands):
    try:
        # Concatenate all commands into a single string separated by semicolons
        all_commands = '; '.join(commands)

        # Run all commands in the same shell
        subprocess.run(['bash', '-c', all_commands], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error executing commands: {e}")
        print(f"Output: {e.output}")

if __name__ == "__main__":
    commands = [
        'pwd',
        'cd',
        'pwd',
        'ls',
        'cd Downloads',
        'ls',
        'pwdg'
    ]

    run_docker_commands(commands)
