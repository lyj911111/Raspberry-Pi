import socket
from threading import Thread
import time
import argparse

'''
    Defined Protocol : ID,CODE1,CODE2,Sequence,Signal,Def value1,Def value2 ...
    
    Test sample example code
    ->  ID       : PLC1, PLC2, PLC3 ...
        CODE1    : ST01, ST02 ...
        CODE2    : CD01, CD02 ...
        Sequence : 190420_001, 190402_002, 190403_003 ...
        Signal   : RQT, ACK, FIN ...
        Def1     : 0x02,0x11,0x22,0x03
        
    My test sample protocol : PLC1,ST01,CD01,190420_xxx,RQT,0x02,0x11,0x22,0x03
    My test sample protocol : PLC2,ST01,CD01,190420_xxx,RQT,0x02,0x11,0x22,0x03
    My test sample protocol : PLC3,ST01,CD01,190420_xxx,RQT,0x02,0x11,0x22,0x03
    
'''

# get the parsing
parser = argparse.ArgumentParser()
parser.add_argument("ID", help="Type the PLC ID")
args = parser.parse_args()
print("PLC ID is ", args.ID)

HOST = '192.168.110.187'	# IP address that I want to access
PORT = 9009					# Port num

# example protocol for test
CODE1 = 'ST01'
CODE2 = 'CD01'

seq = 0
def sequence():
    global seq
    seq = seq + 1
    if seq > 999:
        seq = 0
    now = time.localtime()
    yr2 = str(now.tm_year)
    sqnce = "%02d%02d%02d_%03d" % (int(yr2[2:]), now.tm_mon, now.tm_mday, seq)
    return sqnce

Signal = 'RQT'
def1 = chr(0x02)
def2 = chr(0x11)
def3 = chr(0x22)
def4 = chr(0x03)


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

        # msg = input()           # create PLC name by user input data
        msg = args.ID           # create PLC name by Parser
        PLCname = msg
        sock.send(msg.encode()) # 1st msg is information of PLC name

        while True:
            sqnce = sequence()
            # msg = input()

            # send the protocol information to server continuously
            msg = PLCname + ',' + CODE1 + ',' + CODE2 + ',' + sqnce + ',' + Signal + ',' + def1 + ',' + def2 + ',' + def3 + ',' + def4
            time.sleep(1)
            if msg == '/quit':
                sock.send(msg.encode())
                break
            sock.send(msg.encode())


runChat()