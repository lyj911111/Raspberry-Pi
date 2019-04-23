'''
 Upper Server Test.

 This Server is just get the data from Client
 and leave the log

최상위단 서버 테스트

 라즈베라파이 client -> 상위 server

 라즈베리에 기록된 모든 로그를 전송.
 상위서버 폴더에 그 문서를 저장하는 테스트.
'''

import socketserver
import threading
import time
import datetime
import os
import sys
import shutil

HOST = ''                # allocate IP address of Server automatically
PORT = 9009				 # allocate Port num
lock = threading.Lock()  # syncronized

flag = 0
store_location = 'C:/Users/Lee Won Jae/Desktop/client/upper_server_store/'  # 윈도우상 서버 폴더파일 복사 테스트.
# store_location = 'home/pi/PLClog/upper_server_store'  # 리눅스상 서버 폴더파일 복사 테스트

def get_today():
    now = time.localtime()
    local_time = "%04d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    return local_time

def make_folder(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

def check_time_value():
    time = datetime.datetime.now()
    year = time.year
    month = time.month
    day = time.day
    hour = time.hour
    minute = time.minute
    sec = time.second
    return year, month, day, hour, minute, sec

# def read_file(folderpath):
#     global store_location
#     folderpath = store_location + folderpath
#
#     filename = os.listdir(folderpath)
#     # print("### folderpath ???", folderpath)
#     # print("filelist = {}".format(filename))
#     # print(" filename????", filename[0])
#
#     # 읽기 테스트 **
#     # f = open(filename[0], 'r')
#     #f = open('C:/Users/Lee Won Jae/Desktop/client/123_copy/log_20190419.txt', 'r')
#     f = open(folderpath + '/' + filename[0], 'r')
#     line = f.readline()
#     print("내가읽은 라인:", line)
#     f.close()

def leave_log(msg):
    global flag, store_location
    folderpath = store_location

    year, month, day, hour, minute, sec = check_time_value()

    filename = str(year) + str("%02d" % month) + str("%02d" % day)

    # leave the log initial data
    if flag == 0:
        f = open(folderpath + "/log_%s.txt" % filename, 'w', encoding='utf - 8')
        data = " ID  ,  code  ,  sequence  ,  signal  ,  Def values ... Def values  \n"
        f.write(data)
        flag = 1

    # leave the log continuously
    f = open(folderpath + "/log_%s.txt" % filename, 'a')
    msg = filterEndline(msg)    # Edit the message

    f.write(msg)
    f.close()


def filterEndline(msg):

    # 문자열 내에서 세미콜론 ; [0x3B]을 만나면 뒤에 개행 추가시키기
    msg = msg.replace(chr(0x3B), chr(0x3B)+'\n')
    return msg


class UserManager:  # manage PLCs & sending the messages
    # 1. Register PLC client which was accessed with Pi server
    # 2. Terminate PLC client when PLC was disconnected from the Pi server
    # 3. manage PLC connection or disconnection
    # 4. send the message to all PLC clients which are connected with Pi server

    def __init__(self):
        self.users = {}  # Dictionary for adding PLC's information {PLC name: (socket, address), ... }

    def addUser(self, PLCname, conn, addr):  # Add the user ID at 'self.users'

        # if it already have same ID
        if PLCname in self.users:
            conn.send('it already existed ID.\n Please use other ID. \n'.encode())
            server.shutdown()
            server.server_close()   # block the same ID, Disconnect with client
            return None

        # Register new PLC
        lock.acquire()                          # lock for blocking syncronizing of thread
        self.users[PLCname] = (conn, addr)      # add PLC ID
        lock.release()                          # release the lock after update

        self.sendMessageToAll('[%s] PLC is/are connected' % PLCname)
        print('+++ total connected PLC number : [%d]' % len(self.users))

        return PLCname

    def removeUser(self, PLCname):  # remove the PLC ID from the list
        if PLCname not in self.users:
            return

        lock.acquire()
        del self.users[PLCname]     # remove PLC ID
        lock.release()

        self.sendMessageToAll('[%s] PLC is disconnected' % PLCname)
        print('--- total connected PLC number : [%d]' % len(self.users))

    def messageHandler(self, PLCname, msg):  # process 'msg' which I sent
        if msg[0] != '/':  # if it is not '/' at first character
            self.sendMessageToAll('[%s] %s' % (PLCname, msg))
            return

        if msg.strip() == '/quit':  # if message is 'quit'
            self.removeUser(PLCname)
            return -1

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())


class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    def handle(self):  # print the client address when they are access
        PLCname = ''
        print('[%s] connected' % self.client_address[0])

        try:
            PLCname = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
                print(msg.decode())

                leave_log( msg.decode())        # leave the log in the PLC ID name folder   **
                #leave_log('sending/' + PLCname + '_copy', msg.decode()) # **
                #read_file(PLCname + '_copy')               # ** 파일 읽어서 출력하기

                if self.userman.messageHandler(PLCname, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)

        except Exception as e:
            print(e)

        print('[%s] Disconnect the access' % self.client_address[0])
        self.userman.removeUser(PLCname)

    def registerUsername(self):
        while True:
            self.request.send('Login ID:'.encode())
            PLCname = self.request.recv(1024)
            PLCname = PLCname.decode().strip()
            if self.userman.addUser(PLCname, self.request, self.client_address):
                return PLCname


class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def runServer():
    print('+++ Start the chatting server.')
    print('+++ if you want to finish, please press "Ctrl-C" button.')

    try:
        server = ChatingServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('--- Terminate Chatting server.')
        server.shutdown()
        server.server_close()

runServer()
