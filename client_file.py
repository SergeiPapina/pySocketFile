import socket
import sys
import os
import tqdm

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    filename = "D://2.avi"

    data = " ".join(sys.argv[1:])
    if data:
        filename = data

    file_size = os.path.getsize(filename)
    print(file_size)

    SEPARATOR = '#'
    BUFFER_SIZE = 4096

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        sock.send(f"t_file{SEPARATOR}{filename}{SEPARATOR}{file_size}".encode())
        # sock.sendall(bytes(data + "\n", "utf-8"))

        progress = tqdm.tqdm(range(file_size), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                sock.sendall(bytes_read)
                progress.update(len(bytes_read))

        sock.close()
