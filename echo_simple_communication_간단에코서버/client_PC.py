'''
	TCP/IP echo server-client Test
	PC client - Raspberry Pi Sever
	Fixed IP address, Only Parsed the Port num from user
	
	클라이언트 pC - 서버 라즈베리파이 테스트.
	IP주소는 고정, Port번호만 파싱하도록.
'''

import socket
import argparse

# get the parsing from user 유저로 부터 파싱을 받음.
parser = argparse.ArgumentParser()
#parser.add_argument("IP", help="Input the IP address of Server")   # IP는 당분간 고정.
parser.add_argument("Port", help="Input the port number", type=int)   # only input the port 포트번호만 넣도록

args = parser.parse_args()
#print("Connected IP address: ", args.IP)
print("Connedted Port number: ", args.Port) # print information of port number

HOST = '192.168.110.186'
PORT = args.Port			# input the parsed int type data from the user. 파싱받은 int형 값을 대입.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:

    print("write now:")
    send_data = input()
    print("Send message:", send_data)

    # encode the data for sending
    s.sendall(send_data.encode())
    if not send_data:
        break

    receive_data = s.recv(1024)
    print("From server", receive_data.decode()) # print the echoed message from the Server

s.close()