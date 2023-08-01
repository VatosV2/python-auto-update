import os
import sys
import requests
import base64

GITHUB_REPO_URL = "https://api.github.com/repos/username/respo-name/contents/"
LOCAL_SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "main_script.py"))
LOCAL_VERSION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "version.txt"))
GITHUB_ACCESS_TOKEN = ""

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def get_client_version():
    with open(LOCAL_VERSION_PATH, "r") as local_version_file:
        return local_version_file.read().strip()

def get_latest_version():
    try:
        headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
        response = requests.get(GITHUB_REPO_URL + "version.txt", headers=headers)
        response.raise_for_status()
        github_version = response.json()["content"]
        latest_version = base64.b64decode(github_version).decode().strip()
        return latest_version
    except Exception as e:
        print(f"Error getting the latest version: {e}")
        return None

def check_for_updates():
    print("Checking for updates...")
    try:
        client_version = get_client_version()
        latest_version = get_latest_version()

        if not latest_version:
            return

        if client_version == latest_version:
            print("Client version is up to date.")
        else:
            while True:
                question = input("Do you want to download the update? (y/n): ")
                if question == 'y':
                    print("Updating the script...")
                    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
                    response = requests.get(GITHUB_REPO_URL + "main_script.py", headers=headers)
                    response.raise_for_status()
                    github_script = response.json()["content"]
                    github_script = base64.b64decode(github_script).decode("utf-8")

                    with open(LOCAL_SCRIPT_PATH, "w", encoding="utf-8") as local_file:
                        local_file.write(github_script)

                    with open(LOCAL_VERSION_PATH, "w", encoding="utf-8") as local_version_file:
                        local_version_file.write(latest_version)
                    print("Update successful.")
                    break
                elif question == 'n':
                    print("Running script without an update...")
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")

    except Exception as e:
        print(f"Error checking for updates: {e}")

def launch_main_script():
    try:
        exec(compile(open(LOCAL_SCRIPT_PATH, "rb").read(), LOCAL_SCRIPT_PATH, 'exec'))
    except Exception as e:
        print(f"Error launching the main script: {e}")

if __name__ == "__main__":
    check_for_updates()
    clear()
    launch_main_script()