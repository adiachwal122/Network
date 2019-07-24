
import ftplib


def ftp_connect():
    while True:
        site_address = input('Please enter FTP address: ')
        user_name = input('Please enter user name: ')
        pass_name = input('Please enter password: ')
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
            except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                error_code = str(e).split(None, 1)
                if error_code[0] == '550':
                    print(error_code[1], 'File may not be exist or you may not have permission to view it.')
        elif commands[0] == 'ls':  # Print directory listing
            print('Directory of', ftp.pwd())
            ftp.dir()
        elif commands[0] == 'exit':  # Exit application
            ftp.quit()
            print('Goodbye!')
            break
        else:
            print('Invalid command, try again (valid options: cd/get/ls/exit).')

print('Welcome to Python FTP')
ftp_connect()
