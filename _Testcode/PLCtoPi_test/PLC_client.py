import socket
from threading import Thread
import time

HOST = '192.168.110.136'	# IP address that I want to access
PORT = 9009					# Port num

def rcvMsg(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            pass


def runChat():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        t = Thread(target=rcvMsg, args=(sock,))
        t.daemon = True
        t.start()

        # for test
        cnt = 0
        msg = input()           # create PLC name by user
        PLCname = msg
        sock.send(msg.encode()) # 1st msg is information of PLC name

        while True:
            cnt += 1
            # msg = input()
            msg = PLCname + ' protocol ' + str(cnt)     # send the protocol information to server continuously
            time.sleep(1)
            if msg == '/quit':
                sock.send(msg.encode())
                break

            sock.send(msg.encode())


runChat()
