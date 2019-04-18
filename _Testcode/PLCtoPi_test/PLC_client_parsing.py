import socket
from threading import Thread
import time
import argparse

# get the parsing
parser = argparse.ArgumentParser()
parser.add_argument("ID", help="Type the PLC ID")
args = parser.parse_args()
print("PLC ID is ", args.ID)

HOST = '192.168.110.187'	# IP address that I want to access
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
        sequence = 0
        # msg = input()           # create PLC name by user input data
        msg = args.ID           # create PLC name by Parser
        PLCname = msg
        sock.send(msg.encode()) # 1st msg is information of PLC name

        while True:
            sequence += 1
            # msg = input()
            msg = PLCname + ', Code ,' + str(sequence) + ', signal , def1 , def2 , def3 '     # send the protocol information to server continuously
            time.sleep(1)
            if msg == '/quit':
                sock.send(msg.encode())
                break
            sock.send(msg.encode())


runChat()
