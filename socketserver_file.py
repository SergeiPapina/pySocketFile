import socketserver
import os
import tqdm


class TCPHandler(socketserver.BaseRequestHandler):
    filename = None
    file_size = None
    data = None
    data_type = None
    SEPARATOR = '#'
    BUFFER_SIZE = 4096

    def receive_file_name(self) -> bool:
        self.data = self.request.recv(self.BUFFER_SIZE).strip()
        print(f"{self.client_address[0]} sent:")
        # data = self.data.decode('utf-8')
        received = self.data.decode()
        self.data_type, self.filename, self.file_size = received.split(self.SEPARATOR)
        # remove absolute path if there is
        self.filename = os.path.basename(self.filename)
        # convert to integer
        self.file_size = int(self.file_size)
        print(self.filename, self.file_size)
        if self.data_type == 't_file':
            return True
        return False

    def receive_file_data(self):
        progress = tqdm.tqdm(
            range(self.file_size),
            f"Receiving {self.filename}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024
        )
        with open(self.filename, "wb") as f:
            while True:
                self.data = self.request.recv(self.BUFFER_SIZE).strip()
                if not self.data:
                    break
                f.write(self.data)
                # update the progress bar
                progress.update(len(self.data))

    def handle(self):
        if self.receive_file_name():
            self.receive_file_data()
            print("done")
        else:
            print("it isn't a file")


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
        server.serve_forever()
