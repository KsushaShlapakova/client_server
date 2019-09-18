import socket
from multiprocessing import Process, active_children
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from client import Clients


class Server:
    def __init__(self, m):
        self.m = m
        self.launch()

    def launch(self):
        self.sock = socket.socket()
        self.sock.bind(('127.0.0.1', 10001))
        self.sock.listen(socket.SOMAXCONN)
        while True:
            self.conn, self.addr = self.sock.accept()
            proc = Process(target=self.th)
            proc.start()

    def th(self):
        with ThreadPoolExecutor(max_workers=self.m) as pool:
            q = pool.submit(self.connect, self.conn)

    def connect(self, conn):
        conn.settimeout(5)
        with conn:
            while True:
                try:
                    msg = conn.recv(1024)
                    if msg == b'hours':
                        conn.send(str(datetime.now().hour).encode('utf-8'))
                    elif msg == b'minutes':
                        conn.send(str(datetime.now().minute).encode('utf-8'))
                    elif msg == b'seconds':
                        conn.send(str(datetime.now().second).encode('utf-8'))
                    elif msg == b'stop':
                        conn.close()
                        break
                except socket.timeout:
                    print('\nclose connection by timeout\n')  # cкорее всего не выводится, потому что есть и соединение и данные были отправлены.
                    break


if __name__ == '__main__':
    a = int(input('Количество процессов: '))
    b = int(input('Количество потоков: '))
    c = Clients(a, b)
    c.start()
    s = Server(b)
    for process in active_children():
        process.join()
    c.join()
