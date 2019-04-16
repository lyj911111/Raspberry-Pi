import socketserver
import threading

HOST = ''                # allocate IP address of Server automatically
PORT = 9009				 # allocate Port num
lock = threading.Lock()  # syncronized

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

class UserManager:  # manage users & sending the messages
    # 1. Register User who enter the chatting room
    # 2. Terminate client when users off the room
    # 3. manage user's in and out of the room
    # 4. send the message to all clients who are connected with server

    def __init__(self):
        self.users = {}  # Dictionary for add user's information {user name: (socket, address), ... }

    def addUser(self, PLCname, conn, addr):  # Add the user ID at 'self.users'

        if PLCname in self.users:  # if it already added
            conn.send('it already existed ID.\n'.encode())
            return None

        # Register new PLC
        lock.acquire()  # lock for blocking syncronizing of thread
        self.users[PLCname] = (conn, addr)
        print("Create PLC ID Folder:", PLCname)
        make_folder(PLCname)        # create the folder name of PLC ID
        lock.release()              # release the lock after update

        self.sendMessageToAll('[%s] entered the room' % PLCname)
        print('+++ total chatters [%d]' % len(self.users))

        return PLCname

    def removeUser(self, PLCname):  # remove the user from the PLCname list
        if PLCname not in self.users:
            return

        lock.acquire()
        del self.users[PLCname]
        lock.release()

        self.sendMessageToAll('[%s] left the room' % PLCname)
        print('--- total chatters [%d]' % len(self.users))

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
        print('[%s] connected' % self.client_address[0])

        try:
            PLCname = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
                print(msg.decode())
                if self.userman.messageHandler(PLCname, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)

        except Exception as e:
            print(e)

        print('[%s] Terminate the access' % self.client_address[0])
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
