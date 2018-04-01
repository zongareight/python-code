import socket
import time


class ClientError(Exception):
    """ERROR"""
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def put(self, metric, value, timestamp=int(time.time())):
        with socket.create_connection(
                (self.host, self.port),
                self.timeout
        ) as sock:
            try:
                sock.sendall(f'put {metric} {value} {timestamp}\n'.encode())
                data = sock.recv(1024).decode()
                if data.split()[0] != 'ok':
                    raise ClientError()
            except socket.timeout:
                print("send data timeout")
            except socket.error as ex:
                print("send data error:", ex)

    def get(self, metric):
        resp = {}
        with socket.create_connection(
                (self.host, self.port),
                self.timeout
        ) as sock:
            try:
                sock.sendall(f'get {metric}\n'.encode())
                data = sock.recv(1024).decode()
                if data.split()[0] != 'ok':
                    raise ClientError()
                for row in data.split('\n')[1:-2]:
                    name, value, tmstmp = row.split()
                    resp[name] = resp.get(name, []) + [(int(tmstmp), float(value))]
                for key in resp:
                    resp.get(key).sort()
                return resp
            except socket.timeout:
                print("send data timeout")
            except socket.error as ex:
                print("send data error:", ex)
