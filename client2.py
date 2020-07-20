import socket
import numpy as np
import matplotlib.pyplot as plt
import time

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def findLocalMax2d(array,colls,rows):
    colMaxArr = np.amax(array, axis=0)
    resultArr = []
    for i in range(1,colls-1):
        for j in range(1,rows-1):
                if array[i][j-1]<array[i][j]>array[i][j+1]:
                    if array[i-1][j]<array[i][j]>array[i+1][j]:
                        resultArr.append((i,j))
    return resultArr

host = "84.237.21.36"
port = 5152

plt.ion()
plt.figure()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))

    beat = b"nope"

    while beat != b"yep":

        sock.send(b"get")
        bts = recvall(sock, 40002)

        im = np.frombuffer(
            bts[2:], dtype="uint8").reshape(bts[0], bts[1])

        plt.clf()
        plt.imshow(im)

        coordArr = findLocalMax2d(im,bts[0],bts[1])
        if len(coordArr)>1:
            distance = ((coordArr[0][0] - coordArr[1][0])**2 + (coordArr[0][1] - coordArr[1][1])**2)**(1/2)
            res = round(distance,1)
        else:
            res = 0

        #code here

        sock.send(str(res).encode())
        resp = sock.recv(20)
        print(resp)

        sock.send(b"beat")
        beat = sock.recv(10)
        
        plt.pause(0.05)



print("Done!")
