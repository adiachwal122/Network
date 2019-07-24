from threading import Thread
import socket
import random
import time

print('wellcome to port scaning!!\n')

host = input('please enter ip to scan :')
type = int(input('1)for scan\n2)for random scan\n3)for smart scan\n'))
counting_open = []
counting_close = []
threads = []

file_name = 'PortScaning.txt'
f = open(file_name, 'w+')
f.write("The scan result on ip ")
f.write(str(host))
f.write(' :\n')
f.close()

def scan(port):
    s = socket.socket()
    result = s.connect_ex((host, port))
    #print('working on port > ' + (str(port)))
    if result == 0:
        counting_open.append(port)
        print((str(port))+' -> open')
        s.close()
    else:
        counting_close.append(port)
        # print((str(port))+' -> close')
        s.close()

if (type == 1):
    from_port = int(input('from port : '))
    to_port = int(input('to port : '))
    file_name = 'PortScaning.txt'
    f = open(file_name, 'a+')
    f.write("Regular scan \n")
    f.write('From port:')
    f.write(str(from_port))
    f.write(' to port:')
    f.write(str(to_port))
    f.write(' :\n')
    f.close()
    for i in range(int(from_port), int(to_port) + 1):
        t = Thread(target=scan, args=(i,))
        threads.append(t)
        t.start()
        #t.join()
    with open("PortScaning.txt", "a+") as myfile:
        for i in range(int(from_port), int(to_port) + 1):
            if i in counting_open:
                myfile.write('port ' + str(i) + ' open\n')
            else:
                myfile.write('port ' + str(i) + ' close\n')
elif (type == 2):
    from_port = int(input('from port : '))
    to_port = int(input('to port : '))
    file_name = 'PortScaning.txt'
    f = open(file_name, 'a+')
    f.write("Random scan \n")
    f.write('From port:')
    f.write(str(from_port))
    f.write(' to port:')
    f.write(str(to_port))
    f.write(' :\n')
    f.close()
    r = list(range(from_port,to_port))
    random.shuffle(r)
    for i in r:
        t = Thread(target=scan, args=(i,))
        threads.append(t)
        t.start()
        #t.join()
    with open("PortScaning.txt", "a+") as myfile:
        for i in counting_open:
            myfile.write('port ' + str(i) + ' open\n')
elif (type == 3):
    ports = [20,21,22,23,25,54,67,68,69,80,110,123,137,138,143,179,389,443,636,989,990]
    s = 'testing common ports: ' + str(ports.pop(0))
    file_name = 'PortScaning.txt'
    f = open(file_name, 'a+')
    f.write("Smart scan \n")
    f.close()
    for p in ports:
        s += ',' + str(p)
    print(s + ':')
    for p in ports:
        t = Thread(target=scan, args=(p,))
        threads.append(t)
        t.start()
        #t.join()

    time.sleep(2)

    with open("PortScaning.txt", "a+") as myfile:
        for i in ports:
            if i in counting_open:
                myfile.write('port ' + str(i) + ' open\n')
            else:
                myfile.write('port ' + str(i) + ' close\n')



[x.join() for x in threads]
print('done')
