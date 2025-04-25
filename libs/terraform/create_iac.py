def run_terraform(filepath):
    import os
    import subprocess

    terraform_path = filepath
    TIMEOUT = 240 #4 minutes until a timeout error

    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in {terraform_path}: {os.listdir(terraform_path)}")

    tf_commands = [
        ["terraform", "--version"],
        ["terraform", "init"],
        ["terraform", "apply","-auto-approve"]
    ]

    for command in tf_commands:
        try:
            print(f"INFO - Running {command}")
            subprocess.run(command, cwd=terraform_path, check=True, text=True, capture_output=True, timeout=TIMEOUT)
            print(f"INFO - {command} ran successfully!")
        except subprocess.TimeoutExpired:
            print(f"ERROR - Timeout after {TIMEOUT} seconds.")
        except PermissionError:
            print(f"ERROR - Permission denied, please check if the administrador gave you the correct permissions for this operation.")
        except FileNotFoundError:
            print(f"ERROR - Files not found, please check if main.tf and variables.tf are on {terraform_path}.")
        except Exception as e:
            print(f"ERROR - An unexpected error has occured: {e}.")