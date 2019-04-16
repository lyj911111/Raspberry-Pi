import socketserver
import threading

HOST = ''                # allocate IP address of Server automatically
PORT = 9009				 # allocate Port num
lock = threading.Lock()  # syncronized

class UserManager:  # manage users & sending the messages
    # 1. Register User who enter the chatting room
    # 2. Terminate client when users off the room
    # 3. manage user's in and out of the room
    # 4. send the message to all clients who are connected with server

    def __init__(self):
        self.users = {}  # Dictionary for add user's information {user name: (socket, address), ... }

    def addUser(self, username, conn, addr):  # Add the user ID at 'self.users'

        if username in self.users:  # if it already added
            conn.send('it already added ID.\n'.encode())
            return None

        # Register new users
        lock.acquire()  # lock for blocking syncronizing of thread
        self.users[username] = (conn, addr)
        lock.release()  # release the lock after update

        self.sendMessageToAll('[%s] entered the room' % username)
        print('+++ total chatters [%d]' % len(self.users))

        return username

    def removeUser(self, username):  # remove the user from the username list
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        self.sendMessageToAll('[%s] left the room' % username)
        print('--- total chatters [%d]' % len(self.users))

    def messageHandler(self, username, msg):  # process 'msg' which I sent
        if msg[0] != '/':  # if it is not '/' at first character
            self.sendMessageToAll('[%s] %s' % (username, msg))
            return

        if msg.strip() == '/quit':  # if message is 'quit'
            self.removeUser(username)
            return -1

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())


class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    def handle(self):  # print the client address when they are access
        print('[%s] connected' % self.client_address[0])

        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
                print(msg.decode())
                if self.userman.messageHandler(username, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)

        except Exception as e:
            print(e)

        print('[%s] Terminate the access' % self.client_address[0])
        self.userman.removeUser(username)

    def registerUsername(self):
        while True:
            self.request.send('Login ID:'.encode())
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.userman.addUser(username, self.request, self.client_address):
                return username


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
