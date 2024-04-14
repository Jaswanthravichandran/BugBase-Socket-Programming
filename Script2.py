from colorama import Fore, Back, Style
from tqdm import tqdm
import socket
import os
import subprocess
import json
import sys

def receive_file_and_execute(port):
    # Create a directory to store received files if it doesn't exist
    received_files_dir = "Received Files"
    if not os.path.exists(received_files_dir):
        os.makedirs(received_files_dir)
        print(f"{Fore.CYAN}Created directory:{Style.RESET_ALL} {Fore.GREEN}{received_files_dir}{Style.RESET_ALL}")

    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Bind socket to the port
            s.bind(('', port))
            print(f"{Fore.YELLOW}Listening on port {port}{Style.RESET_ALL}")

            # Listen for incoming connections
            s.listen()

            # Accept connection
            conn, addr = s.accept()
            print(f"{Fore.GREEN}Connection established from {addr}{Style.RESET_ALL}")

            # Receive filename and filesize
            data = conn.recv(1024).decode()
            filename, filesize = data.split("::")
            filesize = int(filesize)

            # Initialize tqdm progress bar
            progress = tqdm(total=filesize, unit="B", unit_scale=True, desc=f"Downloading")

            # Receive file content
            received_data = b""
            while len(received_data) < filesize:
                data = conn.recv(1024)
                received_data += data
                progress.update(len(data))

            # Write received data to a file in the received_files_dir
            save_path = os.path.join(received_files_dir, filename)
            with open(save_path, 'wb') as f:
                f.write(received_data)

            progress.close()
            print(f"{Back.GREEN}File {filename} received and saved to {save_path}{Style.RESET_ALL}")

            # Execute command
            output = subprocess.getoutput(f"file {save_path}")

            # Send output back to script1.py
            conn.send(json.dumps({"output": output}).encode())

            print("Output sent back")
        except Exception as e:
            print(f"{Back.RED}[Error] {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Back.BLUE}Usage: python script2.py <port>{Style.RESET_ALL}")
        sys.exit(1)

    port = int(sys.argv[1])

    receive_file_and_execute(port)
