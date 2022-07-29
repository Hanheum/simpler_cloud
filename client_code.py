from socket import *
from time import sleep
from os.path import getsize

HOST = input('server ip:')
PORT = int(input('port:'))

cli = socket(AF_INET, SOCK_STREAM)
cli.connect((HOST, PORT))

print('connection established')

while True:
    command = input('command:')
    cli.send(command.encode())
    if command == 'download':
        file_name = input('file name:')
        saving_dir = input('saving dir:')
        file = open(saving_dir, 'wb')
        cli.send(file_name.encode())
        file_size = int(cli.recv(1024).decode())
        sleep(5)
        recved_file = 0
        while recved_file != file_size:
            data = cli.recv(1024)
            recved_file += len(data)
            file.write(data)
        file.close()

    if command == 'upload':
        to_where = input('saving file location:')
        which_file = input('which file:')
        file = open(which_file, 'rb')
        sent_file = 0
        file_size = getsize(which_file)
        cli.send(to_where.encode())
        sleep(0.1)
        cli.send('{}'.format(file_size).encode())
        sleep(5)
        while sent_file != file_size:
            data = file.read(1024)
            sent_file += len(data)
            cli.send(data)
        file.close()

    if command == 'dir':
        first_layer = cli.recv(1024).decode()
        print(first_layer)
        target_dir = input('target dir:')
        cli.send(target_dir.encode())
        second_layer = cli.recv(1024).decode()
        print(second_layer)

    if command == 'quit':
        cli.close()
        break