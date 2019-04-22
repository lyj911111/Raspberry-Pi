import socket
from threading import Thread
import time
import os
# import cv2

HOST = '192.168.110.136'	# IP address that I want to access
PORT = 9009					# Port num

acess_location = '/home/pi/PLClog/sending/'     # Path for accessing the folders.
folderlist = os.listdir(acess_location)         # Save as lists at folder on path

# Return the lines[list] in text file through indexing Folder.
def read_file(index):
    global acess_location, folderlist

    filename = os.listdir(acess_location + folderlist[0])                 # Save the filename from list.
    filetext = acess_location + folderlist[index] + '/' + filename[0]     # .txt file for using read the file
    try:
        f = open(filetext, 'r')                                           # Open as read mode
        lines = f.readlines()                                             # export the lines list
        f.close()
        return lines, filetext
    except: return None, None




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
    global acess_location, folderlist

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        t = Thread(target=rcvMsg, args=(sock,))
        t.daemon = True
        t.start()

        print("PLC name Folder lists: ", folderlist)

        # Read file and Send the message and Remove the copied text file line.
        while True:
            if folderlist != 0:
                for i in range(len(folderlist)):
                    lines, filetext = read_file(i)  # return lines[list], .txt file path
                    for line in lines:

                        # print("Read line :", line)
                        msg = line
                        sock.send(msg.encode())  # Send the message per reading
                        # cv2.waitKey(100)

                        print("file path : ", filetext)
                        print("remove line : ", line)
                        with open(filetext, 'w') as f:      # remove the line after reading
                            if line.strip('\n') != line:
                                f.write(line)

            else:
                print("empty the folders")


runChat()
