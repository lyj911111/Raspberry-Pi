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
def read_file(index, numberOfFileindex):
    global acess_location, folderlist

    filename = os.listdir(acess_location + folderlist[index])                 			# Save the filename from list.
    filetext = acess_location + folderlist[index] + '/' + filename[numberOfFileindex]   # "path + .txt" file for using read the file

    try:
        f = open(filetext, 'r')                                               # Open as read mode
        lines = f.readlines()                                                 # export the lines list
        f.close()
        return lines, filetext
    except:
        return None, None

# If text file has only 1 line, Remove the '\n' the end of the line
def lastlineProcess(msg):

    msg = msg.strip()
    return msg


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
            folderlist = os.listdir(acess_location) # Update the path if the folder created
            print("Number of Folder: ", len(folderlist))
            if folderlist != 0:

                # number of folders
                for i in range(len(folderlist)):
                    filename = os.listdir(acess_location + folderlist[i])

                    # number of .txt files
                    for j in range(len(filename)):
                        lines, filetext = read_file(i, j)  # return lines[list], .txt file path

                        if lines != None:
                            for line in lines:
    
                                # if the text file has only 1 line, Remove it, cuz it already sent the message to Server.
                                if len(lines) > 1:
                                    sock.send(line.encode())  # Send the message per reading
                                else:
                                    sock.send(line.encode())        # Send the message per reading when it lower than 1 line
                                    line = lastlineProcess(line)    # Remove only one line
                                    f = open(filetext, 'w')
                                    f.write(line)
                                    f.close()
                                # cv2.waitKey(100)

                                print("file path : ", filetext)
                                print("remove line : ", line)
                                with open(filetext, 'w') as f:      # remove the line after reading
                                    if line.strip('\n') != line:
                                        f.write(line)

            else:
                print("empty the folders")


runChat()