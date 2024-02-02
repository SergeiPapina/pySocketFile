import socket
import sys
import os
import tqdm

HOST, PORT = "localhost", 9999

filename = "D://2.avi"


data = " ".join(sys.argv[1:])
if data:
    filename = data

# get the file size
filesize = os.path.getsize(filename)
print(filesize)

SEPARATOR = '#'
BUFFER_SIZE = 4096

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    sock.send(f"t_file{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())
    # sock.sendall(bytes(data + "\n", "utf-8"))

    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            sock.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    sock.close()
