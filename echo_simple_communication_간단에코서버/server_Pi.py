import socket
import sys

HOST = ''  # allocate dynamically of Host PC
PORT = 7777

# open socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('socket created')

# binding
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed Error code : ' + str(msg[0]) + 'message: ' + msg[1])
    sys.exit()

print('socket bind completed')

# listening
s.listen(10)
print("socket now listening......")

# accept from client socket
conn, addr = s.accept()
print("socket was accepted successfully!")

# keep talking with client
while True:
    print("Connedted with" + addr[0] + ':' + str(addr[1]))

    # Read / send
    data = conn, recv(1024)
    if not data:
        break

    conn.sendall(data)
    print(data.decode())

conn.close()
s.close()