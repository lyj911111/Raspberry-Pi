import socket

HOST = '192.168.110.186'
PORT = 7777

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:

    # print("wait for typing")
    # msg = input()
    #
    # s.send(msg.encode(encoding='utf_8', errors='strict'))
    # data = s.recv(1024)
    # print('result: ' + str(data))

    print("write now:")
    send_data = input()
    print("Send message:", send_data)

    # encode the data for sending
    s.sendall(send_data.encode())
    if not send_data: break

    receive_data = s.recv(1024)
    print("From server", receive_data.decode())

s.close()
