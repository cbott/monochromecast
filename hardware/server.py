import socket

from tv import TV_Controller

controller = TV_Controller()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 8900))
while True:
    data, addr = sock.recvfrom(128)
    data = data.decode(errors='ignore').strip().lower()
    if data.isdigit():
        controller.set_brightness(int(data))
    elif data == 'e':
        controller.enable_system()
    elif data == 'd':
        controller.disable_system()
    elif data == 'q':
        exit()
