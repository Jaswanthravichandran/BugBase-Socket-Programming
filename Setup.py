import platform
import subprocess
import os

def main():
    # Check the operating system
    if platform.system() == "Linux":
        script_path = "/Setup Scripts/setup_linux.sh"
        subprocess.run(["bash", script_path])
    elif platform.system() == "Windows":
        script_directory = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_directory, "Setup-Script", "setup_windows.ps1")
        subprocess.run(["powershell.exe", "-File", script_path], shell=True, check=True)
    else:
        print("Unsupported operating system :(")

if __name__ == "__main__":
    main()
