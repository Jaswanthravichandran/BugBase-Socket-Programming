from colorama import Fore, Back, Style
from tqdm import tqdm
import socket
import os
import sys

def send_file(filename, host, port):
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Connect to the server
            s.connect((host, port))
            print(f"{Fore.YELLOW}Connected to {host}:{port}{Style.RESET_ALL}")

            # Send file name and size
            filesize = os.path.getsize(filename)
            s.send(f"{os.path.basename(filename)}::{filesize}".encode())

            # Initialize tqdm progress bar
            progress = tqdm(total=filesize, unit="B", unit_scale=True, desc=f"Uploading")

            # Send file content
            with open(filename, 'rb') as f:
                data = f.read(1024)
                while data:
                    s.send(data)
                    progress.update(len(data))
                    data = f.read(1024)
                    
            progress.close()
            print(f"{Fore.GREEN}File sent successfully{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Back.RED}[Error] {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"{Back.BLUE}Usage: python script1.py <filename> <host> <port>{Style.RESET_ALL}")
        sys.exit(1)

    filename = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])

    send_file(filename, host, port)
