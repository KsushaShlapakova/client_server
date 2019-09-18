import socket
import random
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor


class Clients(Process):
    def __init__(self, n, m):
        super().__init__()
        self.n = n
        self.m = m
        self.d = {}

    def run(self):
        with ThreadPoolExecutor(max_workers=self.m) as pool:
            for i in range(self.n):
                q = pool.submit(self.run_cl, i + 1)

    def run_cl(self, k):
        with socket.create_connection(('127.0.0.1', 10001), 10) as sock:
            sock.settimeout(2)
            try:
                for i in range(3):
                    command = random.choice(['hours', 'minutes', 'seconds', 'stop'])
                    sock.sendall(command.encode('utf-8'))
                    self.q = '\nЗапрос ' + str(k) + ' клиента: ' + str(command) + '\n'
                    print('\n', self.q, '\n')
                    if command == 'stop':
                        break
                    msg = sock.recv(1024)
                    self.s = '\nОтвет сервера на запрос ' + str(k) + ' :' + str(msg.decode('utf-8')) + '\n'
                    print(self.s)
                # time.sleep(5)
            except socket.timeout:
                print('send data timeout')

            except socket.error as err:
                print('client send data error', err)
