import socket
import sys
import argparse

# get the parsing port number from the user.
parser = argparse.ArgumentParser()
parser.add_argument("Port", help="Input the port number", type=int)   # input the port
print("Connedted Port number:", args.Port)

args = parser.parse_args()

HOST = ''  			# allocate dynamic Host IP address of PC
PORT = args.Port	# allocate the port number from the user

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
    data = conn.recv(1024)
    if not data:
        break

    conn.sendall(data)
    print(data.decode())

conn.close()
s.close()